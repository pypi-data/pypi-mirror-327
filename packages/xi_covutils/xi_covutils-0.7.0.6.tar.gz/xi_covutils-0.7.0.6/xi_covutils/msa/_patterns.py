"""
Generates Sequence patterns and consensus sequences from MSA data
"""

from typing import Callable, Dict
from xi_covutils.msa._types import MsaTypes
from xi_covutils.msa._pssm import (
  build_dna_pssm,
  build_rna_pssm,
  build_protein_pssm,
  filter_pssm_by_freq,
  Pssm,
  filter_pssm_max_freq,
  DNA_IUPAC_CODES,
  RNA_IUPAC_CODES,
  PROTEIN_DEG_CODES,
)

def _enclose_in_brackets(pattern:str) -> str:
  if len(pattern) == 1:
    return pattern
  return f"[{pattern}]"

def build_dna_pattern(
    msa_data: MsaTypes,
    min_freq: float = 0
  ) -> str:
  """
  Generates the minimum Regex pattern from an MSA, that should match all
  sequences. Sequenes are expected to be ungapped.

  Args:
    msa_data (MsaTypes): The input MSA data.
    min_freq (float, optional): Characters that have a frequency lower or
      equal to this value are discarded. Defaults to 0.

  Returns:
    str: The resulting Pattern.
  """
  return _build_pattern(msa_data, build_dna_pssm, min_freq)

def build_rna_pattern(
    msa_data: MsaTypes,
    min_freq: float = 0
  ) -> str:
  """
  Generates the minimum Regex pattern from an MSA, that should match all
  sequences. Sequenes are expected to be ungapped.

  Args:
    msa_data (MsaTypes): The input MSA data.
    min_freq (float, optional): Characters that have a frequency lower or
      equal to this value are discarded. Defaults to 0.

  Returns:
    str: The resulting Pattern.
  """
  return _build_pattern(msa_data, build_rna_pssm, min_freq)

def build_protein_pattern(
    msa_data: MsaTypes,
    min_freq: float = 0
  ) -> str:
  """
  Generates the minimum Regex pattern from an MSA, that should match all
  sequences. Sequenes are expected to be ungapped.

  Args:
    msa_data (MsaTypes): The input MSA data.
    min_freq (float, optional): Characters that have a frequency lower or
      equal to this value are discarded. Defaults to 0.

  Returns:
    str: The resulting Pattern.
  """
  return _build_pattern(msa_data, build_protein_pssm, min_freq)

def _build_pattern(
    msa_data: MsaTypes,
    build_pssm: Callable[[MsaTypes], Pssm],
    min_freq: float = 0
  ) -> str:
  pssm = build_pssm(msa_data)
  pssm = filter_pssm_by_freq(pssm, min_freq)
  pattern = "".join(
    _enclose_in_brackets(
      "".join(sorted(pos_data.keys()))
    )
    for pos_data in pssm
  )
  return pattern

UNTIE_DNA = {
  "".join(sorted(degen)) : base
  for base, degen in DNA_IUPAC_CODES.items()
}

UNTIE_RNA = {
  "".join(sorted(degen)) : base
  for base, degen in RNA_IUPAC_CODES.items()
}

UNTIE_PROTEINS = {
  "".join(sorted(degen)) : aa
  for aa, degen in PROTEIN_DEG_CODES.items()
}

def build_dna_consensus(
    msa_data: MsaTypes,
  ) -> str:
  """
  Generates a consensus sequence from a DNA MSA.

  Args:
    msa_data (MsaTypes): An input DNA MSA

  Returns:
    str: A consensus sequence.
  """
  return _build_consensus(
    msa_data,
    build_dna_pssm,
    UNTIE_DNA,
    "N"
  )

def build_rna_consensus(
  msa_data: MsaTypes,
) -> str:
  """
  Generates a consensus sequence from a RNA MSA.

  Args:
    msa_data (MsaTypes): An input RNA MSA

  Returns:
    str: A consensus sequence.
  """
  return _build_consensus(
    msa_data,
    build_rna_pssm,
    UNTIE_RNA,
    "N"
  )

def build_protein_consensus(
  msa_data: MsaTypes,
) -> str:
  """
  Generates a consensus sequence from a protein MSA.

  Args:
    msa_data (MsaTypes): An input protein MSA

  Returns:
    str: A consensus sequence.
  """
  return _build_consensus(
    msa_data,
    build_protein_pssm,
    UNTIE_PROTEINS,
    "X"
  )

def _build_consensus(
    msa_data: MsaTypes,
    build_pssm: Callable[[MsaTypes], Pssm],
    untier: Dict[str, str],
    wild_card_char: str
  ) -> str:
  pssm = build_pssm(msa_data)
  pssm = filter_pssm_max_freq(pssm)
  consensus = "".join(
    untier.get(
      "".join(sorted(pos_data.keys())),
      wild_card_char
    )
    for pos_data in pssm
  )
  return consensus
