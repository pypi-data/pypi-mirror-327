"""
  Functions to work with MSA files
"""
import gzip
from itertools import chain
from builtins import isinstance
from collections import Counter
from functools import reduce
from operator import add
from os.path import join
from random import shuffle
from shutil import rmtree
from tempfile import mkdtemp
from typing import Any, Dict, List, Optional, Tuple, Union
import warnings

import click
import requests
from deprecated import deprecated

from Bio import SeqIO
from Bio.Align import Alignment, PairwiseAligner, PairwiseAlignments
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from xi_covutils.pdbmapper import align_sequence_to_sequence, map_to_ungapped
from xi_covutils.msa._io import read_msa, as_desc_seq_tuple

from xi_covutils.msa._types import (
  MsaTypes,
  MsaDescSeqDict,
  MsaDescSeqList
)

PFAM_URL = 'https://pfam.xfam.org'

@deprecated
def map_reference_to_sequence(
    msa_file:str,
    sequence:str,
    start:int=1,
    end:Optional[int]=None
  ) -> dict[int, int]:
  """
  Align the reference sequence or a substring from it to a another given
  sequence. Substring alignment is useful for paired MSA.

  Reference sequence is assumed to be the first sequence in the alignment.

  Args:
    msa_file (str): Path to a fasta file.
    sequence (int): An ungapped protein sequence to be used as
      destination of mapping.
    start (int): Index of the starting position of the MSA which will be
      mapped. Starting at 1.
    end (Optional[int]): Index of the last position of the MSA which will be
      mapped. Starting at 1.

  Returns:
    dict[int, int]: A dictionary that maps the positions of the given sequence
      to the reference sequence in the MSA.
  """
  ref = str(next(SeqIO.parse(msa_file, "fasta")).seq)
  end = end if end else len(ref)
  ref = ref[start-1: end].replace("-", "")
  return align_sequence_to_sequence(ref, sequence)

def map_ref_to_sequence(
    msa_data:list[tuple[str, str]],
    sequence:str,
    start:int=1,
    end:Optional[int]=None
  ) -> dict[int, int]:
  """
  Align the reference sequence or a substring from it to a another given
  sequence. Substring alignment is useful for paired MSA.

  Reference sequence is assumed to be the first sequence in the alignment.

  Args:
    msa_data (list[tuple[str, str]]): MSA content as a List[Tuple[str, str]].
    sequence (str): An ungapped protein sequence to be used as destination
      of mapping.
    start (int): Index of the starting position of the MSA which will be
      mapped. Starting at 1.
    end (Optional[int]): Index of the last position of the MSA which will be
      mapped. Starting at 1.

  Returns:
    dict[int, int]: A dictionary that maps the positions of the given sequence
      to the reference sequence in the MSA.
  """
  ref = msa_data[0][1]
  end = end if end else len(ref)
  ref = ref[start-1: end].replace("-", "")
  return align_sequence_to_sequence(ref, sequence)

def _count_mismatches(aln_map, seq_src, seq_dst):
  seq_src = seq_src.upper()
  seq_dst = seq_dst.upper()
  matches_iter = (0 if (seq_src[x-1] == seq_dst[y-1]) else 1
          for x, y in aln_map.items())
  return reduce(add, matches_iter)

def _count_gaps(aln_map, seq_src, seq_dst):
  src = (max(aln_map.keys())-min(aln_map.keys())+1)-len(aln_map)
  dst = (max(aln_map.values())-min(aln_map.values())+1)-len(aln_map)
  dangling_at_start = min(chain(aln_map.keys(), aln_map.values()))-1
  dangling_at_end = min(
    len(seq_src)-max(aln_map.keys()),
    len(seq_dst)-max(aln_map.values())
  )
  return dst+src+dangling_at_start*2+dangling_at_end*2

def map_sequence_to_reference(
    msa_file:str,
    sequence:str,
    msa_format:str='fasta',
    mismatch_tolerance:float=float("inf"),
    gap_tolerance:float=float("inf")
  ) -> dict[int, dict[str, Any]]:
  """
  Creates a mapping from a custom ungapped sequence and the reference (first)
  sequence of and MSA.

  Args:
    msa_file (str): The input MSA file.
    sequence (str): An ungapped protein sequence to be used as the source of the
      mapping.
    msa_format (str): The format of the alignment. Accept any value accepted by
      Biopython.
    mismatch_tolerance (float): A value score to mismatches.
    gap_tolerance (float): A value score for gaps.

  Returns:
    dict[int, dict[str, Any]]: Returns a dict from positions of the custom
      sequence to the positions of the reference sequence. The values of the
      dict are dicts that contains the position number of the target sequence,
      the character of the custom source sequence and the character of the
      target sequences, under the keys: 'position', 'source' and 'target'
      respectively.
  """
  with open(msa_file, "r", encoding="utf-8") as handle:
    reference = next(SeqIO.parse(handle, format=msa_format)).seq
    handle.close()
    ungapped_ref = "".join([s for s in reference if not s == '-'])
    aligned = align_sequence_to_sequence(sequence, ungapped_ref)
    mismatches = _count_mismatches(aligned, sequence, ungapped_ref)
    gaps = _count_gaps(aligned, sequence, ungapped_ref)
    if (
      mismatches <= mismatch_tolerance and
      gaps <= gap_tolerance
    ):
      ungapped_map = {v: k for k, v in map_to_ungapped(reference).items()}
      positions = {a: ungapped_map[aligned[a]] for a in aligned}
      sources = {a: sequence[a-1] for a in aligned}
      targets = {a: reference[positions[a]-1].upper() for a in aligned}
      return {
        a: {
          'position': positions[a],
          'source': sources[a],
          'target': targets[a],
        }
        for a in aligned
      }
  return {}

def _gapstrip_template(sequences:list[str], use_reference:bool) -> list[bool]:
  if use_reference:
    template = [char == "-" for char in sequences[0]]
  else:
    templates = [[char == "-" for char in seq] for seq in sequences]
    template = [True for _ in range(len(templates[0]))]
    for temp in templates:
      template = [x and y for x, y in zip(temp, template)]
  return template

def gapstrip_sequences(
    sequences:list[str],
    use_reference=True
  ) -> list[str]:
  """
  Strips the gaps of list of sequences.

  All sequences are assumed to have the same length

  Args:
    sequences (list[str]): The sequences to gapstrip.
    use_reference (_type_): if True the first sequence is used as reference
      and any position containing a gap in it is removed from all sequences.
      If False, only columns that contains gaps en every sequence are removed.

  Returns:
    list[str]: Returns a list of stripped sequences in the same order as the
      input sequences.
  """
  template = _gapstrip_template(sequences, use_reference)
  return [
    "".join([c for t, c in zip(template, seq) if not t])
    for seq in sequences
  ]


def pop_reference(
    msa_data: Union[MsaDescSeqDict, MsaDescSeqList],
    reference_id: str
  ) -> MsaDescSeqList:
  """
  Puts a reference sequence as the first sequence of a msa.

  Args:
    msa_data (Union[MsaDescSeqDict, MsaDescSeqList]): Input MSA data.
    reference_id (str): The identifier of the reference to pop.

  Returns:
    MsaDescSeqList: Returns a list of tuples of sequence id and sequences.

  Throws:
    ValueError: If MSA data is not recognized or reference identifier not in
      MSA.
  """
  if isinstance(msa_data, list):
    pass
  elif isinstance(msa_data, dict):
    msa_data = list(msa_data.items())
  else:
    raise ValueError("msa_data should be a list or dict")

  results = [(seq_id, seq) for seq_id, seq in msa_data
    if not seq_id == reference_id]
  first = [(seq_id, seq) for seq_id, seq in msa_data
    if seq_id == reference_id]
  if first:
    return first + results
  raise ValueError(f"Sequence: {reference_id} not in msa data")

def gapstrip(
    msa_file:str,
    use_reference:bool=True,
    msa_format:str='fasta'
  ) -> List[SeqRecord]:
  """
  Strips the gaps of an MSA.

  Returns a list of SeqRecord objects from biopython.

  Args:
    msa_file (str): The input MSA data.
    use_reference (bool): if True the first sequence is used as reference
      and any position containing a gap in it is removed from all sequences.
      If False, only columns that contains gaps en every sequence are removed.
      Defaults to True.
    msa_format (str): Any format recognized by Bio.SeqIO. Defaults to "fasta".

  Returns:
    List[SeqRecord]: The Gapstripped sequences.
  """
  with open(msa_file, "r", encoding="utf-8") as handle:
    records = [
      (r.id, str(r.seq), r.description)
      for r in SeqIO.parse(handle, msa_format)
    ]
  gs_result = gapstrip_sequences(
    [s for _, s, _ in records],
    use_reference
  )
  seq_ids = (i for i, _, _ in records)
  seq_desc = (i for _, _, i in records)
  return [
    SeqRecord(
      id=i,
      seq=Seq(s),
      description=d
    )
    for i, s, d in zip(seq_ids, gs_result, seq_desc)
  ]

def cut(
  msa_data: MsaDescSeqList,
  start: int,
  end: int
) -> MsaDescSeqList:
  """
  Cut sequences given by the start and end positions.

  Args:
    msa_data (MsaDescSeqList): The input MSA data.
    start (int): The starting index (1-based)
    end (int): The ending index (1-based)

  Returns:
    MsaDescSeqList: The outout cut sequences.
  """
  result = []
  start = start - 1
  for (desc, seq) in msa_data:
    right_gaps = "-" * max(0, end-len(seq))
    new_seq = f"{seq}{right_gaps}"
    new_seq = new_seq[start:end]
    if not new_seq:
      continue
    result.append((desc, new_seq))
  return result

def pad(msa_data: MsaDescSeqList) -> MsaDescSeqList:
  """
  Pads a collection of sequences with gaps, so all of them
  have the same length.

  Args:
    msa_data (MsaDescSeqList): The input MSA data.

  Returns:
    MsaDescSeqList: The padded msa data.
  """
  result = []
  if not msa_data:
    return result
  last_non_gap = max(
    max(i for i, x in enumerate(seq) if x != "-")
    for _, seq in msa_data
  )
  for desc, seq in msa_data:
    if len(seq) < (last_non_gap+1):
      seq = f"{seq}{'-' * (last_non_gap+1-len(seq))}"
    elif len(seq) > (last_non_gap+1):
      seq = seq[:last_non_gap+1]
    result.append(
      (desc, seq)
    )
  return result

def extract_subsequences(
  msa_data: MsaDescSeqList,
  subsequences_indexes: Dict[str, Tuple[int, int]]
) -> MsaDescSeqList:
  """
  Extract subsequences from an MSA,
  using specific subsequence indexes given for each
  sequence. Keeps the original sequence order.

  Args:
    msa_data (MsaDescSeqList): The MSA data.
    subsequences_indexes (Dict[str, Tuple[int, int]]): A dict
      where sequences descriptions are the keys and the value
      is tuple of two integers, that are the start and end positions
      of each subsequence. Fills with gaps when the start or end positions
      goes outof range.

  Returns:
    MsaDescSeqList: A new MSA data as a dict.
  """
  result = []
  for desc, c_seq in msa_data:
    if not desc in subsequences_indexes:
      continue
    start, end = subsequences_indexes[desc]
    if end < start:
      start, end = end, start
    if start == end:
      continue
    left_gaps = "-" * max(0, -start)
    start = max(0, start)
    right_gaps = "-" * max(0, end - len(c_seq))
    result.append(
      (desc, f"{left_gaps}{c_seq[start: end]}{right_gaps}")
    )
  return result

def _download_pfam(pfam_acc, msa_type, tmp_dir):
  full_url = f"{PFAM_URL}/family/{pfam_acc}/alignment/{msa_type}/gzipped"
  request = requests.get(full_url, stream=True, timeout=120)
  gz_temp = join(tmp_dir, 'tmp.gz')
  with open(gz_temp, 'wb') as tmp_fh:
    for chunk in request.iter_content(chunk_size=1024):
      tmp_fh.write(chunk)
  request.close()
  return gz_temp

def _extract_pfam(compressed_file, outfile):
  try:
    with gzip.open(compressed_file, 'rb') as gz_fh:
      with open(outfile, 'wb') as file_handle:
        while True:
          chunk = gz_fh.read(1024)
          if not chunk:
            break
          if isinstance(chunk, str):
            chunk = bytes(chunk, 'utf-8')
          file_handle.write(chunk)
    return True
  except EOFError:
    return False

def from_pfam(
    pfam_acc:str,
    outfile:str,
    msa_type:str='full'
  ) -> bool:
  """
  Download an MSA from pfam database.

  Retrieves the requiered MSA for the accession given into a file.

  Args:
    pfam_acc (str): The pFam accession to download.
    outfile (str): The path of the output file.
    msa_type (str): 'full': One of 'seed', 'full', 'rp15', 'rp35', 'rp55',
      'rp75', 'uniprot', 'ncbi' or 'meta'.

  Returns:
    bool: True if the download was successful or False otherwise.
  """
  tmp_dir = mkdtemp()
  gz_temp = _download_pfam(pfam_acc, msa_type, tmp_dir)
  status = _extract_pfam(gz_temp, outfile)
  rmtree(tmp_dir)
  return status

def subset(
    msa_data:MsaDescSeqList,
    columns:list[int]
  ) -> MsaDescSeqList:
  """
  Subset a MSA by columns.

  Creates a new MSA getting some columns of a bigger MSA.

  Args:
    msa_data (MsaDescSeqList): a list of tuples with id and sequence from a MSA.
    columns (list[int]): An object that supports the 'in' operator. Position
      numbers of the source MSA are checked if they are 'in' the columns
      object. If True, the column is kept, if false. Postions are 1-based
      indexes.

  Returns:
    MsaDescSeqList: A new MSA data with the selected columns.
  """
  new_msa = [(
    seq_id,
    "".join([x for i, x in enumerate(seq) if i+1 in columns]))
      for seq_id, seq in msa_data]
  return new_msa

def get_terminal_gaps(sequence:str) -> list[bool]:
  """
  Extract terminal gaps

  Gets a True/False list for a sequence indicating which positions are
  terminal gaps.

  Args:
    sequence (str): A gapped sequence.

  Returns:
    list[bool]: A list where True corresponds to terminal gaps.
  """
  _, terminal_gaps_fw = reduce(
    lambda a, b: (a[0] and b == '-', a[1] + [a[0] and b == '-']),
    sequence,
    (True, [])
  )
  _, terminal_gaps_rv = reduce(
    lambda a, b: (a[0] and b == '-', a[1] + [a[0] and b == '-']),
    reversed(sequence),
    (True, [])
  )
  return [a or b for a, b in zip(terminal_gaps_fw, reversed(terminal_gaps_rv))]

PairwiseAlignmentStats = tuple[int, int, int, int]

def pairwise_aln_stats(aln1:str, aln2:str) -> PairwiseAlignmentStats:
  """
  Count gaps, matches, mismatches and the longest run of matches between two
  aligned sequences.

  Args:
    aln1 (str): A aligned sequence.
    aln2 (str): A aligned sequenec.

  Returns:
    PairwiseAlignmentStats: A tuple with alignment stats.

  Throws:
    ValueError: If sequences has different lengths.
  """
  if not len(aln1) == len(aln2):
    raise ValueError("Aligned sequences have different length")
  aln1 = aln1.upper()
  aln2 = aln2.upper()
  gaps = 0
  matches = 0
  mismatches = 0
  longest_run = 0
  run = 0
  previus_is_match = False
  for char1, char2 in zip(aln1, aln2):
    is_gap = char1 == '-' or char2 == '-'
    is_diff_char = char1 != char2
    is_mismatch = not is_gap and is_diff_char
    is_match = not is_gap and not is_diff_char
    run = ((run if previus_is_match else 0) + 1) if is_match else 0
    previus_is_match = is_match
    gaps += 1 if is_gap else 0
    mismatches += 1 if is_mismatch else 0
    matches += 1 if is_match else 0
    longest_run = longest_run if longest_run >= run else run
  return gaps, matches, mismatches, longest_run

def strip_terminal_gaps(alns:list[str]) -> list[str]:
  """
  Strips terminal gaps from a collection of sequences.

  Given a list (or other iterable of gapped sequences) returns a new
  list of sequences that correspond to the original ones without the columns
  containing terminal gaps in at least one sequence.

  Terminal gaps are those gaps that starts from the beggining of the sequence
  and continues until a non-gap char, and those gaps the starts from the end
  and continues backward until a non-gap char.

  Args:
    alns (list[str]): A list of sequences.

  Returns:
    list[str]: A list of sequences.
  """
  alns = [aln.upper() for aln in alns]
  terminal_gaps = (get_terminal_gaps(aln) for aln in alns)
  valid = [not any(gaps_in_col) for gaps_in_col in zip(*terminal_gaps)]
  new_alns = ["".join(c for v, c in zip(valid, aln) if v) for aln in alns]
  return new_alns

def default_aligner() -> PairwiseAligner:
  """
  Creates a default aligner with common match, mismatch and gaps scores.

  Returns:
    PairwiseAligner: The newly created default aligner.
  """
  aligner = PairwiseAligner()
  aligner.mode = "global"
  aligner.match_score = 1
  aligner.mismatch_score = -1
  aligner.open_gap_score = -0.5
  aligner.extend_gap_score = -0.2
  return aligner

def pick_reference(
    reference_sequence:str,
    msa_file:str,
    msa_format:str='fasta',
    minimum_longest_run:int=5
  ) -> list[tuple[str, str, str]]:
  """
  Selects a sequence from a MSA to be the reference sequence.

  The sequence selected is the most similar to a given sequence.

  Args:
    reference_sequence (str): a string with the sequence to be used to
      compare to get the reference sequence.
    msa_file (str): the path of the msa file, it can have any format
      interpreted by biopython.
    msa_format (str): the format of the msa_file.
    minimum_longest_run (int): the picked reference sequence should have
    at least this many number of consecutive matches.

  Returns:
    list[tuple[str, str, str]]: The selected reference as a tuple of the
      sequence identifier, the sequemce, and the type of match between the
      sequence and the reference.
  """
  # pylint: disable=too-many-locals
  reference_sequence = reference_sequence.upper()
  msa_data = [(seq_id, seq.replace("-", "").upper())
        for seq_id, seq in read_msa(msa_file, msa_format=msa_format)]
  # Case 1: Identical sequences
  identical = [(seq_id, reference_sequence, str("IDENTICAL_MATCH"))
    for seq_id, seq in msa_data
    if seq == reference_sequence]
  if identical:
    return identical
  # Case 2: Non identical sequences
  max_score = -float("inf")
  max_aln = []
  for seq_id, seq in msa_data:
    try:
      aligner = default_aligner()
      alns = aligner.align(
        seq.upper(),
        reference_sequence.upper(),
      )
    except SystemError:
      warnings.warn(
        f"Sequences couldn't be aligned: {seq} {reference_sequence}",
          UserWarning
        )
      alns = []
    if not isinstance(alns, PairwiseAlignments):
      return []
    if alns:
      alignment:Alignment = alns[0]
      aln1 = alignment[1, :]
      aln2 = alignment[0, :]
      if not isinstance(aln1, str) or not isinstance(aln2, str):
        continue
      score = getattr(alignment, "score")
      if not isinstance(score, float):
        continue
      score = float(score)
      if score >= max_score:
        if score > max_score:
          max_aln, max_score = [], score
        aln1, aln2 = strip_terminal_gaps([aln1, aln2])
        gaps, _, mismatches, run = pairwise_aln_stats(aln1, aln2)
        if run >= minimum_longest_run:
          match_type = (
            "IDENTICAL_SUB_MATCH"
            if gaps == 0 and mismatches == 0
            else "NON_IDENTICAL_MATCH")
          max_aln.append((seq_id, seq, match_type))
  return max_aln

def msa_to_list(msa_data: MsaDescSeqDict) -> list[list[str]]:
  """
  Returns msa data as a list of lists of chars

  Args:
    msa_data (MsaDescSeqDict): The input MSA data.

  Returns:
    list[list[str]]: A list of lists of chars.
  """
  return [list(s) for s in msa_data.values()]

def columns_to_rows(msa_list_data: list[list[str]]) -> list[list[str]]:
  """
  Traspose columns and rows of a MSA.

  Args:
    msa_list_data (list[list[str]]): The input MSA data as list of lists of
      chars.

  Returns:
    list[list[str]]: The transposed MSA data.
  """
  ncols = len(msa_list_data[0])
  trasposed_data = [[] for _ in range(ncols)]
  for row in msa_list_data:
    for i, res in enumerate(row):
      trasposed_data[i].append(res)
  return trasposed_data

def shuffle_without_gaps(char_list: list[str]) -> list[str]:
  """
  Shuffle chars in a list, without moving the gaps out of place

  Args:
    char_list (list[str]): The input gapped sequence as a list of characters.

  Returns:
    list[str]: The shuffle sequence.
  """
  gap_indexes = [i for i, s in enumerate(char_list) if s == "-"]
  chars = [c for c in char_list if c != '-']
  shuffle(chars)
  for g_index in gap_indexes:
    chars.insert(g_index, "-")
  return chars

def shuffle_with_gaps(char_list: list[str]) -> list[str]:
  """
  Shufle characters in alignment, can alter gap positions

  Args:
    char_list (list[str]): Input sequence as a list of characters.

  Returns:
    list[str]: The shuffled sequence.
  """
  shuffle(char_list)
  return char_list


def shuffle_msa(
    msa_data:MsaDescSeqDict,
    by:str=['column', 'row', 'both'][0],
    keep_gaps:bool=True
  ) -> dict[str, list[str]]:
  """
  Shuffle the data of a msa.

  Args:
    msa_data (MsaDescSeqDict): input MSA data.
    by (str): How to shuffle, by 'column', by 'row', or 'both'.
    keep_gaps (bool): Keep gaps positions.

  Returns:
    dict[str, list[str]]: The shuffled MSA.

  Throws:
    ValueError: If by argument is not recognized.
  """
  #pylint: disable=invalid-name
  shuffler = shuffle_without_gaps if keep_gaps else shuffle_with_gaps
  if by == 'column':
    col_data = columns_to_rows(msa_to_list(msa_data))
    col_data = [
      shuffler(col)
      for col in col_data
    ]
    col_data = columns_to_rows(col_data)
    result = dict(zip(msa_data.keys(), col_data))
    return result
  if by == 'row':
    row_data = msa_to_list(msa_data)
    row_data = {
      name: shuffler(row)
      for name, row in zip(msa_data.keys(), row_data)
    }
    return row_data
  if by == 'both':
    row_data = msa_to_list(msa_data)
    row_data = [
      shuffler(row)
      for row in row_data
    ]
    col_data = columns_to_rows(row_data)
    col_data = [
      shuffler(col)
      for col in col_data
    ]
    col_data = columns_to_rows(col_data)
    return dict(zip(msa_data.keys(), col_data))
  raise ValueError("Argument 'by' not recognized")

def gap_content(msa_data: List[Tuple[str, str]]) -> float:
  """
  Return the fraction of the characters that are gaps.

  Args:
    msa_data (List[Tuple[str, str]]): msa_data is list of tuples (id, seq)

  Returns:
    float: The gap content of the MSA.
  """
  counts = ((len(seq), seq.count("-"))
    for _, seq in msa_data)
  total, gaps = map(sum, zip(*counts))
  return float(gaps)/total

def gap_content_by_column(
    msa_data: Union[List[Tuple[str, str]], List[str]]
  ) -> List[float]:
  """
  Return the fraction of the characters that are gaps for each column of the
  alignment.

  Args:
    msa_data (List[Union[Tuple[str, str], str]]): is list of tuples (id, seq) or
      a list of sequences.
  """
  nseqs = len(msa_data)
  counts = []
  mcounts = 0
  msa_data = [
    x[1] if isinstance(x, tuple) else x
    for x in msa_data
  ]
  for sequence in msa_data:
    for i, value in enumerate((1 if c == '-' else 0 for c in sequence)):
      if i < mcounts:
        counts[i] += value
      else:
        counts.append(value)
        mcounts += 1
  counts = [
    float(c)/nseqs
    for c in counts
  ]
  return counts



# pylint: disable=too-many-locals
def compare_two_msa(
      msa_data_1: MsaTypes,
      msa_data_2: MsaTypes
    ) -> Dict[str, Dict[str, Any]]:
  """
  Compares two multiple sequence alignments and gives a reports.

  Args:
    msa_data_1 (MsaTypes): A Multiple Sequence Alignment.
    msa_data_2 (MsaTypes): A Multiple Sequence Alignment.

  Returns:
    Dict[str, str]: The results of the comparison
  """
  msa_1 = as_desc_seq_tuple(msa_data_1)
  msa_2 = as_desc_seq_tuple(msa_data_2)
  result = {}
  msa_result = {}
  msa_result["msa1_n_sequences"] = len(msa_1)
  msa_result["msa2_n_sequences"] = len(msa_2)
  msa_result["has_same_number_of_sequences"] = len(msa_1) == len(msa_2)
  msa_result["identical_msas"] = msa_1 == msa_2
  result["msa"] = msa_result
  desc1 = [d for d, _ in msa_1]
  desc2 = [d for d, _ in msa_2]
  description_results = {}
  description_results["identical"] = (
    dict(Counter(desc1)) == dict(Counter(desc2))
  )
  description_results["has_same_order"] = desc1 == desc2
  result["descriptions"] = description_results
  ungapped_msa_1 = [
    (d, s.replace("-", ""))
    for d, s in msa_1
  ]
  ungapped_msa_2 = [
    (d, s.replace("-", ""))
    for d, s in msa_2
  ]
  ungapped_seqs_1 = [
    s for _, s in ungapped_msa_1
  ]
  ungapped_seqs_2 = [
    s for _, s in ungapped_msa_2
  ]
  ungapped_results = {}
  ungapped_results["identical_seqs"] = (
    dict(Counter(ungapped_seqs_1)) == dict(Counter(ungapped_seqs_2))
  )
  ungapped_results["has_same_order"] = (
    ungapped_seqs_1 == ungapped_seqs_2
  )
  ungapped_results["corresponds_with_desc"] = (
    dict(Counter(ungapped_msa_1)) == dict(Counter(ungapped_msa_2))
  )
  result["ungapped"] = ungapped_results
  gapped_results ={}
  seqs1 = [
    s for _, s in msa_1
  ]
  seqs2 = [
    s for _, s in msa_2
  ]
  gapped_results["identical_seqs"] = (
    dict(Counter(seqs1)) == dict(Counter(seqs2))
  )
  gapped_results["has_same_order"] = (
    seqs1 == seqs2
  )
  gapped_results["corresponds_with_desc"] = (
    dict(Counter(msa_1)) == dict(Counter(msa_2))
  )
  result["gapped"] = gapped_results
  return result

def print_dict(input_msa: Dict[str, Any], depth = 0):
  """
  Prints a dictionary formated to be outputed to the console.

  Args:
      input (Dict[str, Any]): Input MSA.
      depth (int, optional): A depth value that shows how indented is the output
        text. Defaults to 0.
  """
  for key, value in input_msa.items():
    if not isinstance(value, dict):
      print(f"# {' '*(depth)}{key}: {value}")
    if isinstance(value, dict):
      print(f"# {' '*(depth)}{key}:")
      print_dict(value, depth=depth+2)

@click.command()
@click.argument(
  "msa1",
  type=click.Path(exists=True)
)
@click.argument(
  "msa2",
  type=click.Path(exists=True)
)
def compare_msas(msa1:str, msa2:str):
  """
  Compare Two MSAs CLI command.

  Args:
    msa1 (str): A Multiple sequence alignment file.
    msa2 (str): A Multiple sequence alignmetn file.
  """
  click.echo("# Compare Two MSAs")
  result = compare_two_msa(msa1, msa2)
  print_dict(result)
