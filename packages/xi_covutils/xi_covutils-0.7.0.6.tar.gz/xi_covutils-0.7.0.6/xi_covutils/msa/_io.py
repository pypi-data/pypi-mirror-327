"""
IO MSA operations
"""

from typing import Union
from Bio import SeqIO

from xi_covutils.msa._types import (
  MsaTypes,
  MsaDescSeqDict,
  MsaDescSeqList,
  MsaSequenceList
)

def read_msa(
    msa_file:str,
    msa_format:str='fasta',
    as_dict:bool=False
  ) -> MsaTypes:
  """
  Reads a complete msa_file.

  Args:
    msa_file (str): The path of the input msa file.
    msa_format (str): The format of the msa file. Can be any of the
      supported by biopython. Defaults to "fasta".
    as_dict (bool): If True returns a dict from id to sequence. Defaults to
      False.

  Returns:
    MsaTypes: Return a list of tuples with with id and sequences or a dict from
      id to sequences.
  """
  with open(msa_file, "r", encoding="utf-8") as handle:
    records = [(r.id, str(r.seq)) for r in SeqIO.parse(handle, msa_format)]
  if as_dict:
    return dict(records)
  return records

def write_msa(
    msa_data: Union[MsaDescSeqDict, MsaDescSeqList],
    msa_file: str
  ):
  """
  Writes a msa to file.

  Only support fasta format at the moment.
  Input data can be:
  - a list of tuples of sequence id and sequence.
  - a dict from sequence id to sequence.

  Args:
    msa_data (Union[MsaDescSeqDict, MsaDescSeqList]): Input sequence data.
    msa_file (str): The output file.

  Throws:
    ValueError: If input data is not recognized.
  """
  if isinstance(msa_data, list):
    seq_iterable = msa_data
  elif isinstance(msa_data, dict):
    seq_iterable = msa_data.items()
  else:
    raise ValueError("msa_data should be a list or dict")
  with open(msa_file, 'w', encoding="utf-8") as handle:
    for seq_id, seq in seq_iterable:
      handle.write(f">{seq_id}\n{seq}\n")

def as_sequence_list(
    input_msa: MsaTypes
  ) -> MsaSequenceList:
  """
  Changes MSA representation to an ordered list of sequences.

  Args:
    input (MsaTypes): The source of the MSA data.

  Returns:
    MsaSequenceList: the MSA data as a list of str.
  """
  if isinstance(input_msa, str):
    msa_data = read_msa(msa_file = input_msa, as_dict=False)
    msa_data = [x[1] for x in msa_data]
    return msa_data
  if isinstance(input_msa, dict):
    return list(input_msa.values())
  if isinstance(input_msa, list):
    msa_data = [
      x if isinstance(x, str) else x[1]
      for x in input_msa
    ]
    return msa_data
  return []

def as_desc_seq_dict(
    input_msa: MsaTypes
  ) -> MsaDescSeqDict:
  """
  Changes MSA representation to an ordered list of sequences.

  Args:
    input MsaTypes: The source of the MSA data.

  Returns:
    MsaDescSeqDict: the MSA data as a dict of descriptions to sequences.
  """
  if isinstance(input_msa, str):
    msa_data = read_msa(msa_file = input_msa, as_dict=True)
    if not isinstance(msa_data, dict):
      return {}
    return msa_data
  if isinstance(input_msa, dict):
    return input_msa
  if isinstance(input_msa, list):
    msa_data = [
      (f"seq_{i+1}", x) if isinstance(x, str) else (x[0], x[1])
      for i, x in enumerate(input_msa)
    ]
    msa_data = dict(msa_data)
    return msa_data
  return {}

def as_desc_seq_tuple(
    input_msa: MsaTypes
  ) -> MsaDescSeqList:
  """
  Changes MSA representation to an ordered list of sequences.

  Args:
    input (MsaTypes): The source of the MSA data.

  Returns:
    MsaDescSeqList: The MSA data as a list of description and sequence tuples.
  """
  if isinstance(input_msa, str):
    msa_data = read_msa(msa_file = input_msa, as_dict=False)
    if not isinstance(msa_data, list):
      return []
    msa_data = [x for x in msa_data if isinstance(x, tuple)]
    return msa_data
  if isinstance(input_msa, dict):
    msa_data = list(input_msa.items())
    return msa_data
  if isinstance(input_msa, list):
    msa_data = [
      (f"seq_{i+1}", x) if isinstance(x, str) else x
      for i, x in enumerate(input_msa)
    ]
    return msa_data
  return []
