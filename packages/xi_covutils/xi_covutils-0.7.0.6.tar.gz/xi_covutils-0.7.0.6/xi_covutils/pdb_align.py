"""
This module has function to align PDB structures.
"""

from copy import deepcopy
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from Bio.PDB.Atom import Atom
from Bio.PDB.Structure import Structure
from Bio.PDB.Superimposer import Superimposer

from xi_covutils.pdbbank import PDBSource, pdb_structure_from
from xi_covutils.pdbmapper import (
  align_sequence_to_sequence,
  build_pdb_sequence
)

@dataclass
class PDBAlignmentResult:
  """
  The result of an alignment of two PDB structures.
  """
  structure: Structure
  """The aligned Biopython Structure."""
  rms: float
  """The rms of the aligned residues."""
  aligned_residues_1: List[int]
  """The list of the aligned residues of the first chain."""
  aligned_residues_2: List[int]
  """The list of the aligned residues of the second chain."""

def align_pdbs(
    pdbsrc1: PDBSource,
    pdbsrc2: PDBSource,
    chain1: str = "A",
    chain2: str = "A"
  ) -> PDBAlignmentResult:
  """
  Align two PDB structures.

  The first structure is considere fixed, and the second is mobile.
  The alignment is made with the Carbon Alpha of alignable residues between
  the two selected chains.

  Args:
    pdbsrc1 (xi_covutils.pdbbank.PDB_SOURCE): Fixed PDB structure.
    pdbsrc2 (xi_covutils.pdbbank.PDB_SOURCE): Mobile PDB structure.
    chain1 (str): Chain ID of the fisrt PDB structure. Defaults to "A".
    chain2 (str): Chain ID of the second PDB structure. Defaults to "A".

  Returns:
    PDBAlignmentResult: A new structure for the second PDBs with the rotation
      and translations applied.
  """
  return align_partial_pdbs(
    pdbsrc1=pdbsrc1,
    pdbsrc2=pdbsrc2,
    region1=None,
    region2=None,
    chain1=chain1,
    chain2=chain2,
  )

# pylint: disable=too-many-arguments, too-many-locals
def align_partial_pdbs(
    pdbsrc1: PDBSource,
    pdbsrc2: PDBSource,
    region1: Optional[List[int]],
    region2: Optional[List[int]],
    chain1: str = "A",
    chain2: str = "A",
  ) -> PDBAlignmentResult:
  """
  Align two PDB structures.

  The first structure is considere fixed, and the second is mobile.
  The alignment is made with the Carbon Alpha of alignable residues between
  the two selected chains and residues.

  Args:
    pdbsrc1 (xi_covutils.pdbbank.PDB_SOURCE): Fixed PDB structure.
    pdbsrc2 (xi_covutils.pdbbank.PDB_SOURCE): Mobile PDB structure.
    region1 (Optional[List[int]]): Residue numbers of the first protein to be
      aligned.
    region2 (Optional[List[int]]): Residue numbers of the second protein to be
      aligned.
    chain1 (str): Chain ID of the fisrt PDB structure. Defaults to "A".
    chain2 (str): Chain ID of the second PDB structure. Defaults to "A".

  Returns:
    PDBAlignmentResult: A new structure for the
      second PDBs with the rotation and translations applied.

  """
  def _select_residue_atoms_ca_in_chain(
      pdb_strucure: Structure,
      residues: List[int],
      chain:str
    ) -> List[Atom]:
    atoms = []
    for res in pdb_strucure[0][chain].get_residues():
      res_n = res.id[1]
      if res_n in residues:
        atoms.append(res["CA"])
    return atoms
  def _get_seq_and_res(
      seq_data: Dict[int, str]
    ) -> Tuple[str, List[int]]:
    res = sorted(seq_data.keys())
    seq = "".join(seq_data[r] for r in res)
    return seq, res
  def _filter_regions(
      aln_res_1: List[int],
      aln_res_2: List[int],
      region1: Optional[List[int]],
      region2: Optional[List[int]],
    ):
    for i, region in enumerate([region1, region2]):
      if region is None:
        continue
      set_r = set(region)
      aln_res = zip(
        *(
          x
          for x in zip(aln_res_1, aln_res_2)
          if x[i] in set_r
        )
      )
      aln_res_1, aln_res_2 = [list(x) for x in aln_res]
    return aln_res_1, aln_res_2
  pdb1 = pdb_structure_from(pdbsrc1)
  if not pdb1:
    raise ValueError("PDB cannot be interpreted")
  pdb2 = pdb_structure_from(pdbsrc2)
  if not pdb2:
    raise ValueError("PDB cannot be interpreted")
  # Build amino acid sequences from pdb as dict
  # from residue number to amino acid.
  seq_1_data = build_pdb_sequence(pdb1, chain1)
  seq_2_data = build_pdb_sequence(pdb2, chain2)
  # Converts sequence data into a string sequence
  # and a list of residues numbers.
  seq1, res1 = _get_seq_and_res(seq_1_data)
  seq2, res2 = _get_seq_and_res(seq_2_data)
  # Align sequences, gets a dict that matches position in seq1 to seq2.
  aln = align_sequence_to_sequence(seq1, seq2)
  # Maps sequence positions to pdb residue numbers.
  aln_res_1 = [res1[i-1] for i in sorted(aln)]
  aln_res_2 = [res2[aln[i]-1] for i in sorted(aln)]
  # Removes residues outside the regions to align
  aln_res_1, aln_res_2 = _filter_regions(
    aln_res_1,
    aln_res_2,
    region1,
    region2
  )
  # There should be at least three residues to align
  if len(aln_res_1) < 3:
    raise ValueError("Alignment requires at least three residues.")
  # Select the atoms corresponding to the selected residues.
  atoms_1 = _select_residue_atoms_ca_in_chain(pdb1, aln_res_1, chain1)
  atoms_2 = _select_residue_atoms_ca_in_chain(pdb2, aln_res_2, chain2)
  # Makes the structural alignment
  sup = Superimposer()
  sup.set_atoms(atoms_1, atoms_2)
  # Makes a new copy of the second structure to avoid
  # affecting the original structure. And applys the
  # geometrical transformations.
  pdb2_copy = deepcopy(pdb2)
  sup.apply(pdb2_copy)
  rms = sup.rms if isinstance(sup.rms, float) else 0
  return PDBAlignmentResult(
    pdb2_copy,
    rms,
    aln_res_1,
    aln_res_2
  )
