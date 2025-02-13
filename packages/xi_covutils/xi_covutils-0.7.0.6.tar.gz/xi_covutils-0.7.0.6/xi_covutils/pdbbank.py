"""
  Compute some stuff on PDB file
"""
from functools import reduce
from operator import add
from typing import Optional, Union
from warnings import filterwarnings

from Bio.PDB.Atom import Atom
from Bio.PDB.PDBExceptions import PDBConstructionWarning
from Bio.PDB.PDBIO import Select
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Structure import Structure


class DefaultSelect(Select):
  """
  Default Select class. Select everthing from first model.
  """
  def accept_atom(self, atom):
    return True
  def accept_chain(self, chain):
    return True
  def accept_model(self, model):
    return model.get_id() == 0
  def accept_residue(self, residue):
    return True

class CarbonAlphaSelect(DefaultSelect):
  """
  Select Alpha carbon atoms of first model.
  """
  def accept_atom(self, atom):
    return atom.get_name() == 'CA'

def _centroid_atom(atoms):
  filterwarnings('ignore', category=PDBConstructionWarning)
  centroid = reduce(add, (atom.get_coord() for atom in atoms), 0)/len(atoms)
  return Atom('Centroid', centroid, 0, 0, 0, 'Centroid', 1)

def _calc_rg(atoms):
  centroid = _centroid_atom(atoms)
  return reduce(add, ((atom-centroid)**2 for atom in atoms), 0)

def collect_atoms(structure:Structure, select:Select) -> list[Atom]:
  """
  Retrieve all selected atoms from a structure

  Args:
    structure (Structure): A PDB structure.
    select (Select): A selector Select subclass.
  """
  atoms = [
    atom
    for model in structure
    for chain in model
    for residue in chain
    for atom in residue
    if select.accept_model(model)
      and select.accept_chain(chain)
      and select.accept_residue(residue)
      and select.accept_atom(atom)
    ]
  return atoms


def gyration_radius(
    structure:Structure,
    select:Select=CarbonAlphaSelect(),
    by_chain:bool=False
  ):
  """
  Compute radius of gyration of a protein.
  Only takes into account alpha carbon atoms.

  Args:
    structure (Structure): A PDB Structure.
    select (Select): A selector Select subclass.
    by_chain (bool): Calculate for every chain.

  Returns:
    dict[str, dict[str, Any]]
  """
  if by_chain:
    results = {
      'rg': {},
      'compactness' : {}
    }
    for current_chain in structure.get_chains():
      class ChainedSelect(select.__class__):
        """Inner select class for chains"""
        def __init__(self, chain):
          self.c_chain = chain.id
        def accept_chain(self, chain):
          """Overriden accept_chain method."""
          return self.c_chain == chain.id
      chained_select = ChainedSelect(current_chain)
      atoms = collect_atoms(structure, chained_select)
      rad_of_gyr = _calc_rg(atoms)
      results['rg'][current_chain.id] = rad_of_gyr
      results['compactness'][current_chain.id] = rad_of_gyr/len(atoms)
    return results
  atoms = collect_atoms(structure, select)
  rad_of_gyr = _calc_rg(atoms)
  return {
    'rg': {'all': rad_of_gyr},
    'compactness': {'all':rad_of_gyr/len(atoms)}
  }

PDBSource = Union[str, Structure]
def pdb_structure_from(
    pdb_source: PDBSource,
    identifier: str = ""
  ) -> Optional[Structure]:
  """
  Gets a Bio.PDB.Structure.Struture object from different input types.

  Args:
    pdb_source (PDB_SOURCE): A file path to an exisiting pdb file or a PDB
      structure.
    identifier (str, optional): The pdb code of the structure. Defaults to "".

  Returns:
    Structure: A Bio.PDB.Structure.Struture
  """
  if isinstance(pdb_source, str):
    return PDBParser().get_structure(identifier, pdb_source)
  if isinstance(pdb_source, Structure):
    return pdb_source
  return None
