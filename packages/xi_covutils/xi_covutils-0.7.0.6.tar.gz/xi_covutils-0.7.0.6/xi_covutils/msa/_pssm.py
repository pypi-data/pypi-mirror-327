"""
Create PSSM from an MSA
"""

import re
from collections import defaultdict
from typing import Callable, Dict, Iterable, List
from xi_covutils.msa._msa import as_desc_seq_tuple
from xi_covutils.msa._types import MsaTypes

Pssm = List[Dict[str, float]]
DegCodes = Dict[str, List[str]]

DNA_IUPAC_CODES: DegCodes = {
    "A": ["A"],  # Adenine
    "C": ["C"],  # Cytosine
    "G": ["G"],  # Guanine
    "T": ["T"],  # Thymine
    "R": ["A", "G"],  # A or G (purines)
    "Y": ["C", "T"],  # C or T (pyrimidines)
    "S": ["G", "C"],  # G or C (strong interaction)
    "W": ["A", "T"],  # A or T (weak interaction)
    "K": ["G", "T"],  # G or T (keto groups)
    "M": ["A", "C"],  # A or C (amino groups)
    "B": ["C", "G", "T"],  # C or G or T (not A)
    "D": ["A", "G", "T"],  # A or G or T (not C)
    "H": ["A", "C", "T"],  # A or C or T (not G)
    "V": ["A", "C", "G"],  # A or C or G (not T)
    "N": ["A", "C", "G", "T"],  # any base
}

RNA_IUPAC_CODES: DegCodes = {
    "A": ["A"],  # Adenine
    "C": ["C"],  # Cytosine
    "G": ["G"],  # Guanine
    "U": ["U"],  # Uhymine
    "R": ["A", "G"],  # A or G (purines)
    "Y": ["C", "U"],  # C or U (pyrimidines)
    "S": ["G", "C"],  # G or C (strong interaction)
    "W": ["A", "U"],  # A or U (weak interaction)
    "K": ["G", "U"],  # G or U (keto groups)
    "M": ["A", "C"],  # A or C (amino groups)
    "B": ["C", "G", "U"],  # C or G or U (not A)
    "D": ["A", "G", "U"],  # A or G or U (not C)
    "H": ["A", "C", "U"],  # A or C or U (not G)
    "V": ["A", "C", "G"],  # A or C or G (not U)
    "N": ["A", "C", "G", "U"],  # any base
}

PROTEIN_DEG_CODES: DegCodes = {
  "Q" : ["Q"],
  "W" : ["W"],
  "E" : ["E"],
  "R" : ["R"],
  "T" : ["T"],
  "Y" : ["Y"],
  "I" : ["I"],
  "P" : ["P"],
  "A" : ["A"],
  "S" : ["S"],
  "D" : ["D"],
  "F" : ["F"],
  "G" : ["G"],
  "H" : ["H"],
  "K" : ["K"],
  "L" : ["L"],
  "C" : ["C"],
  "V" : ["V"],
  "N" : ["N"],
  "M" : ["M"],
  "X" : [
    "Q", "W", "E", "R", "T",
    "Y", "I", "P", "A", "S",
    "D", "F", "G", "H", "K",
    "L", "C", "V", "N", "M"
  ],
}

def normalize_rna(sequence: str) -> str:
  """
  Normalize a RNA sequence.
  Al characters are converted to upper case.
  Unrecognized characters are transformed to N.
  T chars are converted to U.
  Gaps are kept.
  """
  sequence = sequence.upper()
  sequence = re.sub("T", "U", sequence)
  non_valid_dna = re.compile("[^-ACGURYSWMBDHVN]")
  sequence = re.sub(non_valid_dna, "N", sequence)
  return sequence

def normalize_dna(sequence: str) -> str:
  """
  Normalize a DNA sequence.
  Al characters are converted to upper case.
  Unrecognized characters are transformed to N.
  U chars are converted to T.
  Gaps are kept.
  """
  sequence = sequence.upper()
  sequence = re.sub("U", "T", sequence)
  non_valid_dna = re.compile("[^-ACGTRYSWMBDHVN]")
  sequence = re.sub(non_valid_dna, "N", sequence)
  return sequence

def normalize_protein(sequence: str) -> str:
  """
  Normalize a protein sequence.
  Al characters are converted to upper case.
  Unrecognized characters are transformed to X.
  Gaps are kept.
  """
  sequence = sequence.upper()
  non_valid_dna = re.compile("[^-QWERTYIPASDFGHKLXCVNM]")
  sequence = re.sub(non_valid_dna, "X", sequence)
  return sequence

def norm_pssm_to_frq(pssm: Pssm) -> Pssm:
  """
  Normalize the values of the input pssm so every position adds to 1.

  Args:
    pssm (Pssm): The input pssm

  Returns:
    Pssm: The normalized pssm
  """
  result = []
  for pos_data in pssm:
    total_frq = sum(pos_data.values())
    new_pos_data = {
      char: float(frq) / total_frq
      for char, frq in pos_data.items()
    }
    result.append(new_pos_data)
  return result

def build_dna_pssm(
    msa_data: MsaTypes,
    pseudo_freq: float = 0
    ) -> Pssm:
  """
  Creates a new PSSM from DNA alignment.

  Args:
    msa_data (MsaTypes): The input MSA data.

  Returns:
    Pssm: A Position Specific Scoring Matrix.
  """
  return _build_pssm(
    msa_data,
    DNA_IUPAC_CODES,
    normalize_dna,
    pseudo_freq
  )

def build_rna_pssm(
    msa_data: MsaTypes,
    pseudo_freq: float = 0
    ) -> Pssm:
  """
  Creates a new PSSM from DNA alignment.

  Args:
    msa_data (MsaTypes): The input MSA data.

  Returns:
    Pssm: A Position Specific Scoring Matrix.
  """
  return _build_pssm(
    msa_data,
    RNA_IUPAC_CODES,
    normalize_rna,
    pseudo_freq
  )

def build_protein_pssm(
    msa_data: MsaTypes,
    pseudo_freq: float = 0
    ) -> Pssm:
  """
  Creates a new PSSM from DNA alignment.

  Args:
    msa_data (MsaTypes): The input MSA data.

  Returns:
    Pssm: A Position Specific Scoring Matrix.
  """
  return _build_pssm(
    msa_data,
    PROTEIN_DEG_CODES,
    normalize_protein,
    pseudo_freq
  )

def _add_pseudo_freq(
    pssm:Pssm,
    pseudo_frq: float,
    alphabet: Iterable[str]
  ) -> Pssm:
  result = [
    {char: pos_data.get(char, 0)+pseudo_frq for char in alphabet}
    for pos_data in pssm
  ]
  return result

def _dict_to_pssm(pssm_dict: Dict[int, Dict[str, float]]) -> Pssm:
  indexes = sorted(pssm_dict.keys())
  result = [pssm_dict[index] for index in indexes]
  return result

def _build_pssm(
    msa_data: MsaTypes,
    deg_codes: Dict[str, List[str]],
    normalize_seq_function: Callable[[str], str],
    pseudo_freq: float = 0,
) -> Pssm:
  alphabet = set(x for chars in deg_codes.values() for x in chars)
  pssm_dict = _count_pssm(
    msa_data,
    deg_codes,
    normalize_seq_function
  )
  pssm = _dict_to_pssm(pssm_dict)
  pssm = norm_pssm_to_frq(pssm)
  pssm = _add_pseudo_freq(pssm, pseudo_freq, alphabet)
  if pseudo_freq == 0:
    return pssm
  pssm = norm_pssm_to_frq(pssm)
  return pssm

def _count_pssm(
  msa_data: MsaTypes,
  deg_codes: Dict[str, List[str]],
  normalize_seq_function: Callable[[str], str]
) -> Dict[int, Dict[str, float]]:
  msa_list = as_desc_seq_tuple(msa_data)
  result: Dict[int, Dict[str, float]] = defaultdict(lambda: defaultdict(int))
  for _, seq in msa_list:
    seq = normalize_seq_function(seq)
    for i, char in enumerate(seq):
      if char == "-":
        continue
      non_deg_chars = deg_codes[char]
      base_counts = float(1) / len(non_deg_chars)
      for non_deg_char in non_deg_chars:
        result[i][non_deg_char] += base_counts
  return result

def filter_pssm_by_freq(
  pssm:Pssm,
  min_freq: float = 0
) -> Pssm:
  """
  Removes elements from the PSSM if its frequency is not greater than
  a minimum value.

  Args:
    pssm (Pssm): The input PSSM
    min_freq (float): The minimum frequency.

  Returns:
    Pssm: The output pssm.
  """
  return [
    {char: frq for char, frq in pos_data.items() if frq>min_freq}
    for pos_data in pssm
  ]

def filter_pssm_max_freq(
  pssm: Pssm,
) -> Pssm:
  """
  Keeps the elements of maximum frequency in the Pssm

  Args:
    pssm (Pssm): The input Pssm

  Returns:
    Pssm: The result Pssm
  """
  result = []
  for pos_data in pssm:
    max_freq = max(pos_data.values())
    result.append(
      {
        char: frq
        for char, frq in pos_data.items()
        if frq == max_freq
      }
    )
  return result
