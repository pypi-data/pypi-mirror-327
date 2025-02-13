"""
Compute CIGAR string for sequence alignments.
"""
import itertools
from xi_covutils.msa._msa import get_terminal_gaps

def _aln_to_cigar_aln(target:str, query:str) -> list[str]:
  cigar = []
  ref_len = len(target)
  query_len = len(query)
  if ref_len != query_len:
    raise ValueError("query and target have different lengths")
  query_terminal_gaps = get_terminal_gaps(query)
  target_terminal_gaps = get_terminal_gaps(target)
  iter_data = zip(query, target, query_terminal_gaps, target_terminal_gaps)
  for pos_q, pos_t, ter_q, ter_t in iter_data:
    if ter_q and ter_t:
      raise ValueError("Both sequences have a gap in the same column")
    if ter_q or ter_t:
      cigar.append("S")
      continue
    if pos_q == "-" and pos_t == "-":
      raise ValueError("Both sequences have a gap in the same column")
    if pos_q == "-":
      cigar.append("I")
      continue
    if pos_t == "-":
      cigar.append("D")
      continue
    if pos_q == pos_t:
      cigar.append("M")
      continue
    if pos_q != pos_t:
      cigar.append("X")
      continue
  return cigar

def _compress_cigar_chars(uncompressed_cigar:list[str]) -> str:
  compressed_chars = []
  compressed_counts = []
  for cig_char in uncompressed_cigar:
    last = len(compressed_chars)-1
    if not compressed_chars or compressed_chars[last] != cig_char:
      compressed_chars.append(cig_char)
      compressed_counts.append(1)
      continue
    compressed_counts[last] += 1
  compressed_counts = [str(x) for x in compressed_counts]
  cigar = list(
    itertools.chain.from_iterable(zip(compressed_counts, compressed_chars))
  )
  cigar = "".join(cigar)
  return cigar

def generate_cigar_string(target:str, query:str) -> str:
  """
  Generate a CIGAR string for an alignment of two sequences.
  The generated CIGAR string might not be totally compliant with the standards
  with SOFT and HARD clipping.

  Args:
    target (str): A gapped aligned sequence.
    query (str): A gapped aligned sequence.

  Throws:
    ValueError: If the target and the query have different lengths or both have
      a gap in the same column.

  Returns:
    str: A cigar String.
  """
  cigar = _aln_to_cigar_aln(target, query)
  cigar = _compress_cigar_chars(cigar)
  return cigar
