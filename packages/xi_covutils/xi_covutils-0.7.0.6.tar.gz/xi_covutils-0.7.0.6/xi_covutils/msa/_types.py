"""
Types for MSA inputs
"""
from typing import List, Tuple, Union, Dict

MsaSequenceList = List[str]
MsaDescSeqList = List[Tuple[str,str]]
MsaDescSeqDict = Dict[str,str]
MsaFilename = str
MsaTypes = Union[
  MsaSequenceList,
  MsaDescSeqList,
  MsaDescSeqDict,
  MsaFilename
]
