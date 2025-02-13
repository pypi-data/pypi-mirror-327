"""
  Read results from covariation files
"""
from re import match
from typing import Iterable, Optional

from Bio import SeqIO


def _single_cov_line_reader(accepting_pattern):
  def wrapper(infile):
    with open(infile, 'r', encoding="utf-8") as file_handle:
      for line in file_handle:
        c_match = match(accepting_pattern, line.strip())
        if c_match:
          yield (
            c_match.group("i"),
            c_match.group("j"),
            c_match.group("score")
          )
  return wrapper


def from_gauss_dca(infile:str) -> dict[tuple[int, int], float]:
  """
  Reads a the results of the covariation files from Gauss DCA.

  Args:
    infile (str): A string with the path of the input file.

  Returns:
    dict[tuple[int, int], float]: Returns a dictionary of tuples of indices
      (i,j) where i<=j as keys and score as value. The indices i,j starts at 1.
  """
  gauss_pattern = r"(?P<i>[0-9]+) (?P<j>[0-9]+) (?P<score>[e+-.0-9]+)$"
  gauss_reader = _single_cov_line_reader(gauss_pattern)
  return {
    (int(i), int(j)): float(v)
    for i, j, v in gauss_reader(infile)
  }

def from_mitos_mi(infile:str) -> dict[tuple[int, int], float]:
  """
  Reads a the results of the covariation files from MIToS MI.

  Args:
    infile (str): A string with the path of the input file.

  Returns:
    dict[tuple[int, int], float]: Returns a dictionary of tuples of indices
    (i,j) where i<=j as keys and score as value. The indices i,j starts at 1.
  """
  mitos_mi_pattern = (
    r"(?P<i>[0-9]+),(?P<j>[0-9]+),"
    r"(?P<score>[+-.0-9]+),[e+-.0-9]+$"
  )
  mi_reader = _single_cov_line_reader(mitos_mi_pattern)
  return {
    (int(i), int(j)): float(v)
    for i, j, v in mi_reader(infile)
  }

def from_ccmpred(infile:str) -> dict[tuple[int, int], float]:
  """
  Reads a the results of the covariation files from CCMPRED.

  Args:
    infile (str):A string with the path of the input file.

  Returns:
    dict[tuple[int, int], float]: Returns a dictionary of tuples of indices
      (i,j) where i<=j as keys and score as value. The indices i,j starts at 1.
  """
  with open(infile, 'r', encoding='utf-8') as f_in:
    raw = f_in.readlines()
  scores = {(i+1, j+1):float(v)
        for i, l in enumerate(raw)
        for j, v in enumerate(l.split()) if i <= j}
  return scores

def remap_paired(
    cov_data:dict[tuple[int, int], float],
    msa_file:Optional[str],
    chain_a_len:int,
    chain_a_id:str="1",
    chain_b_id:str="2"
  ) -> dict[tuple[tuple[str, int], tuple[str, int]], float]:
  """
  Remaps the positions of the covariation scores of a paired MSA to each
  individual ungapped chain sequence.

  Args:
    cov_data (dict[tuple[int, int], float]): Input covariation data of a paired
      MSA.
    msa_file (str): A paired input MSA data.
    chain_a_len (int): The number of columns in the MSA that corresponds to the
      first protein of the paired MSA.
    chain_a_id (str): The Chain identifier of the first protein of the paired
      MSA.
    chain_b_id (str): The Chain identifier of the second protein of the paired
      MSA.

  Returns:
    dict[tuple[tuple[str, int], tuple[str, int]], float]: The mapped positons
      of the covariation scores.
  """
  if msa_file:
    records = SeqIO.parse(msa_file, "fasta")
    first_chain_seq = str(next(records).seq)[:chain_a_len]
    first_chain_ungapped_length = len(first_chain_seq.replace("-", ""))
  else:
    first_chain_ungapped_length = chain_a_len
  def _adapt_index(index: int) ->  tuple[str, int]:
    if index <= first_chain_ungapped_length:
      return (chain_a_id, index)
    return (chain_b_id, index-first_chain_ungapped_length)
  return {
    (_adapt_index(i), _adapt_index(j)):v
    for (i, j), v in cov_data.items()
  }

def to_tuple_positions(
    cov_data:dict[tuple[int, int], float],
    chain_id:str
  ) -> dict[tuple[tuple[str, int], tuple[str,int]], float]:
  """
  Converts simple positions to tuples.

  Converts the indexes of covariation results to tupled positions that include
  the protein chain id. Make the results compatible with output of
  remap_paired function

  Args:
    cov_data (dict[tuple[int, int], float]): The results of covariation scores.
      as a dict of indices as keys and scores as values.
    chain_id (str): A chain identifier.

  Returns:
    dict[tuple[tuple[str, int], tuple[str, int]], float]: The covariation data
      with the included chain identifiers.
  """
  return {
    ((chain_id, i), (chain_id, j)): v
    for (i, j), v in cov_data.items()
  }

def remap_tuple_positions(
    cov_data:dict[tuple[tuple[str, int], tuple[str, int]], float],
    mapping:dict[str,dict[int,int]]
  ) -> dict[tuple[tuple[str, int], tuple[str, int]], float]:
  """
  Remaps the positions of cov_data. Cov_data should be represented as a dict
  with keys of the form ((chain_a, index_a), (chain_b, index_b)) and scores as
  values.

  Args:
    cov_data (dict[tuple[tuple[str, int], tuple[str, int]], float]): A dict with
      covariation scores.
    mapping (dict[str, dict[int, int]]): A dict to map the positions, the dict
      should have chain ids as keys, and values should be dicts that maps from
      old positions to new positions.

  Returns:
    dict[tuple[tuple[str, int], tuple[str, int]], float]: The covariation data
      with the mapped positions.
  """
  return {((c1, mapping[c1][p1]), (c2, mapping[c2][p2])):s
      for ((c1, p1), (c2, p2)), s in cov_data.items()
      if p1 in mapping[c1] and p2 in mapping[c2]}

def remove_trivial_tuple(
    cov_data:dict[tuple[tuple[str, int], tuple[str, int]], float],
    min_pos_dif:int=5
  ) -> dict[tuple[tuple[str, int], tuple[str, int]], float]:
  """
  Removes positions from covariation data from residue pairs that are
  a lesser distance than five positions in sequence.

  Covariation data is assumed to be a dict with keys of the form
  ((chain_a, index_a), (chain_b, index_b)) and scores as keys.

  Args:
    cov_data (dict[tuple[tuple[str, int], tuple[str, int]], float]): The input
      covariation data.
    min_pos_dif (int): Minimum distance that two residues should
    have to be included.

  Returns:
    dict[tuple[tuple[str, int], tuple[str, int]], float]: The covariation data
      without the trivials pairs.
  """
  return {((c1, p1), (c2, p2)):score
      for ((c1, p1), (c2, p2)), score in cov_data.items()
      if not ((c1 == c2) and (abs(p2 - p1) < min_pos_dif))}

def intra_covariation(
    cov_data: dict[tuple[tuple[str, int], tuple[str, int]], float]
  ) -> dict[str, dict[tuple[tuple[str, int], tuple[str, int]], float]]:
  """
  Extract intra-chain interactions from paired covariation data.

  Returns a new dict which chain ids are keys and values are subsets
  of cov_data that correspond to intra chain residue pairs.

  Args:
    cov_data (dict[tuple[tuple[str, int], tuple[str, int]], float]): The paired
      covariation data.

  Returns:
    dict[str, dict[tuple[tuple[str, int], tuple[str, int]], float]]: The intra
      chain covariation data for all chains.
  """
  chains = {c for ((c1, _), (c2, _)) in cov_data
        for c in [c1, c2]}
  intra_data = {c:{} for c in chains}
  for ((ch1, po1), (ch2, po2)), score in cov_data.items():
    if ch1 == ch2:
      intra_data[ch1][((ch1, po1), (ch2, po2))] = score
  return intra_data

def merge(
    cov_data_iter: Iterable[
      dict[tuple[tuple[str, int], tuple[str, int]], float]
    ]
  ) -> dict[tuple[tuple[str, int], tuple[str, int]], float]:
  """
  Merge covariation data.

  Args:
    cov_data_iter (Iterable[dict[tuple[tuple[str, int], tuple[str, int]],
      float]]): Is a iterator where each element is covariation
    data.

  Returns:
    dict[tuple[tuple[str, int], tuple[str, int]], float]: Merged covariation
      data.
  """
  return {pair:s for cov in cov_data_iter
      for pair, s in cov.items()}

def inter_covariation(
    cov_data:dict[tuple[tuple[str, int], tuple[str,int]], float]
  ) -> dict[
    tuple[str, str],
    dict[tuple[tuple[str, int], tuple[str,int]],float]
  ]:
  """
  Extract inter-chain interactions from paired covariation data.

  Args:
    cov_data (dict[tuple[tuple[str, int], tuple[str, int]], float]): The
      covariation data from a paired MSA.

  Returns:
    dict[tuple[str, str], dict[tuple[tuple[str, int], tuple[str, int]], float]]:
      Returns a new dict which chain id tuples are keys and values are subsets
      of cov_data that correspond to inter chain residue pairs.
      Chain ids in tuple keys are sorted lexicographically.
  """
  chain_pairs = {
    tuple(sorted([c1, c2])) for ((c1, _), (c2, _)) in cov_data
    if not c1 == c2
  }
  inter_data = {c:{} for c in chain_pairs}
  for ((ch1, po1), (ch2, po2)), score in cov_data.items():
    if not ch1 == ch2:
      key_positions = tuple(
        sorted(
          [(ch1, po1), (ch2, po2)],
          key=lambda x: x[0])
      )
      key_chains = tuple(sorted([ch1, ch2]))
      inter_data[key_chains][key_positions] = score
  return inter_data
