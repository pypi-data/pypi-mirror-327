"""
  Functions to map postions from PDB files to sequence files.
"""

from dataclasses import dataclass
from typing import Dict, Optional
from Bio.Align import PairwiseAligner
from Bio.PDB.Polypeptide import protein_letters_3to1_extended

from xi_covutils.pdbbank import PDBSource, pdb_structure_from


def build_pdb_sequence(pdb_src:PDBSource, chain:str) -> Dict[int, str]:
  """
  Creates a dictionary that maps the position of a pdb chain to the
  one-letter-code residue.
  Water molecules and residues marked as HETERO are not included.

  Args:
    pdb_src (PDBSource): A string path to a pdb file.
    chain (str): A one-letter string chain code.

  Returns:
    Dict[int, str]: A Dictionary from residue positions in the PDB to one letter
      codes of amino acids.
  """
  model = pdb_structure_from(pdb_src)
  if not model:
    return {}
  model = model[0]
  current_chain = [c for c in model.get_chains() if c.id == chain]
  residues = {
    r.id[1]: (
      protein_letters_3to1_extended.get(r.resname, "X")
    )
    for c in current_chain for r in c.get_residues()
    if r.id[0] == " " and not r.resname == 'HOH'
  }
  return residues

def align_pdb_to_sequence(
    pdb_src:PDBSource,
    chain: str,
    sequence: str
  ) -> dict[int, int]:
  """
  Align a pdb chain to a protein sequence and generates a map from pdb position
  to sequence position.

  Args:
    pdb_src (PDBSource): A PDB source.
    chain (str): A Chain identifier.
    sequence (str): The sequence to map to the PDB reconstructed sequence.

  Returns:
    dict[int, int]: A mapping from pdb position to sequence position.
  """
  residues = build_pdb_sequence(pdb_src, chain)
  if residues:
    aligned_residues = align_dict_to_sequence(residues, sequence)
    return {r:aligned_residues[i+1]
        for i, r in enumerate(sorted(residues.keys()))
        if i+1 in aligned_residues}
  return {}

def build_seq_from_dict(dic: dict[int, str]) -> str:
  """
  Creates a sequence from a dict where keys are positions and values are
  characters.

  Args:
    dic (dict[int, str]): The input data as a dictionary.

  Returns:
    str: The reconstructed sequence.
  """
  return "".join([dic[n] for n in sorted(dic.keys())])

def align_dict_to_sequence(
    dic: dict[int, str],
    sequence: str
  ) -> dict[int, int]:
  """
  Makes an alignment from a dict and another ungapped sequence.

  Args:
    dic (dict[int, str]): The dict should have integers as keys, and strings
      as values
    sequence (str): A string representing a ungapped protein sequence.

  Returns:
    dict[int, int]: A Mapping from the sequence in the dictionary to the
      sequence in the str.
  """
  seq_in_dict = build_seq_from_dict(dic)
  return align_sequence_to_sequence(seq_in_dict, sequence)

@dataclass()
class AlignmentResult:
  """
  AlignmentResult is a simple representation of a pairwise alignment.

  Contains both sequences aligned and a mapping from the aligned positions
  from the first sequence onto the second one.
  """
  mapping: Dict[int, int]
  aln_seq_1: str
  aln_seq_2: str

def align_two_sequences(seq_1:str, seq_2:str) -> AlignmentResult:
  """
  Makes a global alignment of two sequences.

  Args:
    seq_1 (str): First sequence to align.
    seq_2 (str): Second sequence to align.

  Returns:
    AlignmentResult: The result of the alignment, including the aligned
      sequences and the mapping from position of the first sequence to the
      second sequence.
  """
  aligner = PairwiseAligner()
  aligner.mode = "global"
  aligner.open_gap_score = -0.5
  aligner.extend_gap_score = -0.1
  alignment = aligner.align(seq_1.upper(), seq_2.upper())
  seq_1_aln = alignment[0][0, :]
  seq_2_aln = alignment[0][1, :]
  if not isinstance(seq_1_aln, str):
    seq_1_aln = ""
  if not isinstance(seq_2_aln, str):
    seq_2_aln = ""
  mapped = map_align(seq_1_aln, seq_2_aln)
  result = AlignmentResult(
    mapped,
    str(seq_1_aln),
    str(seq_2_aln)
  )
  return result

def align_sequence_to_sequence(
    seq_1:str,
    seq_2:str
  ) -> dict[int, int]:
  """
  Makes an alignment from two sequences.

  Args:
    seq_1 (str): A string representing a ungapped protein sequence.
    seq_2 (str): A string representing a ungapped protein sequence.

  Returns:
    dict[int, int]: A mapping from the first sequence to the sequence.
  """
  aln_result = align_two_sequences(seq_1, seq_2)
  return aln_result.mapping

def map_align(seq1:str, seq2:str) -> dict[int, int]:
  """
  Align two sequences, and generates a dictionaty that maps aligned indices from
  the first sequences onto the second sequence.

  Args:
    seq1 (str): A string representing a potentially gapped protein sequence.
    seq2 (str): A string representing a potentially gapped protein sequence.

  Returns:
    dict[int, int]: A mapping between positions of two gapped sequences.
  """
  dict1 = map_to_ungapped(seq1)
  dict2 = map_to_ungapped(seq2)
  return align_dict_values(dict1, dict2)

def align_dict_values(
    dict1: dict[int, int],
    dict2: dict[int, int]
  ) -> dict[int, int]:
  """
  Creates a new dictionary from two input dictionaries. Values from two
  input dicts are aligned if they correspond to the same key. Input keys are
  assumed to have unique values.

  ```python
  # from alignmet:
  # -ABC-
  # Z-BCD
  data1 = {2:1, 3:2, 4:3}
  data2 = {1:1, 3:2, 4:3, 5:4}
  data3 = align_dict_values(data1, data2)
  assert data3 == {2:2, 3:3}
  ```

  Args:
    dict1 (dict[int, int]): A mapping for the first sequence.
    dict2 (dict[int, int]): A mapping for the second sequence.

  Returns:
    dict[int, int]: A Mapping between two dict values by keys.
  """
  return {
    dict1[k]:dict2[k]
    for k in dict1
    if k in dict2
  }

def map_to_ungapped(seq:str) -> dict[int, int]:
  """
  Creates a dictionary from a gapped sequence. This dictionary maps the position
  (starting in 1) from the gapped position to the ungapped position

  ```python
  seq = "---ABC---"
  mapping = map_to_ungapped(seq)
  assert mapping == {4: 1, 5: 2, 6: 3}
  ```

  Args:
    seq (str): A gapped sequence.

  Returns:
    dict[int, int]: A mapping between positions of the two sequences.
  """
  return {
    i+1: j+1
    for j, i in enumerate([i for i, c in enumerate(seq) if not c == "-"])
  }


class PDBSeqMapper:
  """
  Maps positions between a sequence (from Uniprot foe example) and a
  reconstucted sequence from a pdb file.
  """
  def __init__(self):
    self.pdb_sequence: str = ""
    self.sequence: str = ""
    self.seq_to_res_map: Dict[int, int] = {}
    self.res_to_seq_map: Dict[int, int] = {}
    self.aln_seq_1:str = ""
    self.aln_seq_2:str = ""
  def align_sequence_to_pdb(
      self,
      sequence: str,
      pdbsrc: PDBSource,
      chain: str
    ):
    """
    Aligns a given sequence to the reconstructed sequence from a PDB file.
    It is assumed that both corresponds to the same protein, or are very similar
    at least.

    Args:
      sequence (str): A sequence to align.
      pdbsrc (PDBSource): A PDB structure.
      chain (str): The chain in the PDB file that corresponds to the given
        sequence.
    """
    self.sequence = sequence
    residues = build_pdb_sequence(pdbsrc, chain)
    if not residues:
      return
    self.pdb_sequence = build_seq_from_dict(residues)
    aln_result = align_two_sequences(
      self.pdb_sequence,
      self.sequence
    )
    aligned_residues = aln_result.mapping
    self.aln_seq_1 = aln_result.aln_seq_1
    self.aln_seq_2 = aln_result.aln_seq_2
    self.res_to_seq_map = {
      r:aligned_residues[i+1]
      for i, r in enumerate(sorted(residues.keys()))
      if i+1 in aligned_residues
    }
    self.seq_to_res_map = {v:k for k, v in self.res_to_seq_map.items()}
  def from_seq_to_residue_number(self, pos:int) -> Optional[int]:
    """
    Maps position indices from the sequence to the corresponding residue number.

    Args:
      pos (int): A Index position in the sequence (staarting at 1).

    Returns:
      Optional[int]: The corresponding residue number if it is aligned.
    """
    return self.seq_to_res_map.get(pos)
  def from_residue_number_to_seq(self, pos:int) -> Optional[int]:
    """
    Maps The residue numbers of the PDB file to the corresponding position index
    in the sequence.

    Args:
      pos (int): A residue number as it is annotated in the PDB file.

    Returns:
      Optional[int]: A position index in the sequence if it is mapped.
    """
    return self.res_to_seq_map.get(pos)
  def get_sequence(self) -> str:
    """
    Returns the given sequence to align with the PDB structure.

    Returns:
      str: A sequence.
    """
    return self.sequence
  def get_pdb_sequence(self) -> str:
    """
    Returns the reconstructed sequence from the current chain in the PDB
    structure.

    Returns:
        str: A sequence.
    """
    return self.pdb_sequence
  def get_aln_sequence(self) -> str:
    """
    Returns the given sequence aligned to the PDB structure.

    Returns:
      str: A sequence.
    """
    return self.aln_seq_2
  def get_aln_pdb_sequence(self) -> str:
    """
    Returns the reconstructed sequence from the current chain in the PDB
    structure aligned to the given sequence.

    Returns:
      str: A sequence.
    """
    return self.aln_seq_1
