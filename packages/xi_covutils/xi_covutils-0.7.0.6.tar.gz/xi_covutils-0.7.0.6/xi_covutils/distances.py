"""
  Functions and classes to work with residue distances in proteins structures
"""

import csv
import operator
import re
from functools import reduce
from itertools import combinations, combinations_with_replacement, product
from typing import Callable, Dict, List, Optional, TextIO, Tuple, TypeVar, Union
from Bio.PDB.Atom import Atom

from Bio.PDB.Model import Model
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Residue import Residue
from Bio.PDB.Structure import Structure

from xi_covutils.pdbbank import PDBSource, pdb_structure_from

Chain = str
Position = int
Distance = float
Resname = str
AtomId = str
DistanceElement = Tuple[Chain, Position, Chain, Position, Distance]
DistanceElementLong = Tuple[
  Chain, Position, Resname, AtomId,
  Chain, Position, Resname, AtomId,
  Distance
]
DistanceData = List[DistanceElement]
DistanceDataLong = List[DistanceElementLong]
DistanceDataSH = List[Union[DistanceElement, DistanceElementLong]]

AtomSelector = Callable[[Atom, Atom], bool]

class Distances():
  '''
  Store and access distance data for residues from a protein structure.
  '''
  def __init__(
      self,
      dist_data: DistanceData
    ):
    """
    Creates a new instance from distance data.

    Args:
      dist_data (DistanceData): Distance data should be a list of tuples of five
        elements: (chain1, pos1, chain2, pos2, distance).
    """
    dis:Dict[Tuple[Chain, Position], Dict[Tuple[Chain, Position], float]] = {}
    for ch1, po1, ch2, po2, dist in dist_data:
      if (ch1, po1) not in dis:
        dis[(ch1, po1)] = {}
      dis[(ch1, po1)][(ch2, po2)] = dist
    self._distances = dis

  def raw_distances(self) -> DistanceData:
    """
    Returns:
      DistanceData: Returns the distances data of the object as a list of
        tuples. Each tuples has five elements: (chain1, pos1, chain2, pos2,
        distance).
    """
    return [
      (chain1, pos1, chain2, pos2, dist)
      for (chain1, pos1), c_pos in self._distances.items()
      for (chain2, pos2), dist in c_pos.items()
    ]

  def of( #pylint: disable=invalid-name
      self,
      chain_a:Chain,
      pos_a:Position,
      chain_b:Chain,
      pos_b:Position
    ) -> Optional[Distance]:
    """
    Retrieves distance for a residue pair.

    Args:
      chain_a (str): A string specifying the first residue chain.
      pos_a (int): An integer specifying the first residue position.
      chain_b (str): A string specifying the second residue chain.
      pos_b (int): An integer specifying the second residue position.

    Returns:
      Optional[float]: The distance between two residue positions. If the pair
        is not found, None is returned.
    """
    pair1 = ((chain_a, pos_a))
    pair2 = ((chain_b, pos_b))
    if pair1 == pair2: # Special case for distance with the same residue.
      return 0
    distance = self._distances.get(pair1, {}).get(pair2)
    if not distance:
      distance = self._distances.get(pair2, {}).get(pair1)
    return distance

  def remap_positions(
      self,
      mapping: dict[Chain, dict[Position, Position]]
    ):
    """
    Remap index positions.
    If a positions could not be mapped it is excluded from the results.

    Args:
      mapping (dict[str, dict[int, float]]): a dict that maps old positions to
        new positions.
    """
    T = TypeVar("T")
    def _remap(dic: dict[tuple[str, int], T]) -> dict[tuple[str, int], T]:
      return {
        (chain, mapping[chain][pos]):value
        for (chain, pos), value in dic.items()
        if pos in mapping.get(chain, {})
      }

    self._distances = _remap(
      {
        (c1, p1):_remap(r2)
        for (c1, p1), r2 in self._distances.items()
      }
    )

  def is_contact( #pylint: disable=too-many-arguments
      self,
      chain_a: Chain,
      pos_a: Position,
      chain_b: Chain,
      pos_b: Position,
      distance_cutoff:Distance=6.05
    ) -> bool:
    '''

    Args:
      chain_a (str): A string specifying the first residue chain.
      pos_a (int): An integer specifying the first residue position.
      chain_b (str): A string specifying the second residue chain.
      pos_b (str): An integer specifying the second residue position.
      distance_cutoff (float): a float with the distance cutoff (defaults to
        6.05 angstroms)

    Returns:
      bool: Returns True if a given pair's distance is lower or equal than a
      given distance cutoff.
    '''
    dist = self.of(chain_a, pos_a, chain_b, pos_b)
    if dist is None:
      return False
    return dist <= distance_cutoff

  @staticmethod
  def _sum_true(boolean_list: list[bool]):
    return reduce(lambda a, b: a+(1 if b else 0), boolean_list, 0)

  def mean_intramolecular(self) -> dict[Chain, float]:
    """
    Returns:
      Return the mean number of intramolecular contacts across all residues for
        every chain.
    """
    def _pos_contacts(chain:str, pos1:int, all_positions: list[int]):
      return [
        self.is_contact(chain, pos1, chain, pos2)
        for pos2 in all_positions
        if not pos1 == pos2
      ]
    all_residues = set(self._distances.keys()).union(
      {
        pair2
        for pair1 in self._distances.keys()
        for pair2 in self._distances[pair1].keys()
      }
    )
    all_chains = {chain for chain, _ in all_residues}
    pos_by_chain = {
      chain: [p for c, p in all_residues if c == chain]
      for chain in all_chains
    }
    n_contacts = {
      chain: [
        self._sum_true(_pos_contacts(chain, pos, pos_by_chain[chain]))
        for pos in pos_by_chain[chain]
      ]
      for chain in all_chains
    }
    n_contacts = {
      chain: float(reduce(operator.add, n, 0)) / max(1, len(n))
      for chain, n in n_contacts.items()
    }
    return n_contacts

  @staticmethod
  def from_contact_map(
      contact_map: Dict[Tuple[int, int], bool]
    ) -> 'Distances':
    """
    Create a new Distance object from a contact map.
    Set contact to a distace of 1 and non contacts to 10.
    Sets the chain to be 'A'.
    """
    dist_data = []
    for (pos1, pos2), is_contact in contact_map.items():
      dist_data.append(
        ('A', pos1, 'A', pos2, 1 if is_contact else 10)
      )
    return Distances(dist_data)

def from_mitos(dist_file: str) -> DistanceData:
  """
  Loads data of residue distances from a file generated by MIToS.

  Input data should look like:

  <pre>
  # model_i,chain_i,group_i,pdbe_i,number_i,name_i,model_j,chain_j,group_j,pdbe_j,number_j,name_j,distance
  1,A,ATOM,,55,LEU,1,A,ATOM,,56,LEU,1.3247309160731473
  </pre>

  Args:
    dist_file (str): A string to a text file with the distance data.

  Returns:
    list[tuple[str, int, str, int, float]]: The distances in the file.
  """ # pylint: disable=line-too-long
  d_pattern = re.compile(
    r"(\d+),(.),(.+),.*,(\d+),(.+),(\d+),(.),(.+),.*,(\d+),(.+),(.+)$"
  )
  res = []
  with open(dist_file, "r", encoding="utf8") as handle:
    for line in handle:
      line = line.strip()
      if not line.startswith("#"):
        match = re.match(d_pattern, line)
        if not match:
          continue
        try:
          res.append((
            match.group(2),      # Chain 1
            int(match.group(4)), # Pos res 1
            match.group(7),      # Chain 2
            int(match.group(9)), # Pos res 2
            float(match.group(11))))  # distance
        except (IndexError, AttributeError):
          pass
    return res


def is_back_bone(atom:Atom) -> bool:
  """
  Decides if an atom belongs to the backbone of a prototein by their name.

  Args:
    atom (Atom): An atom.

  Returns:
    bool: True if the given atom belongs to the backbone of the protein.
  """
  return atom.id in ['N', 'CA', 'CB']

def all_atoms_selector(atom1:Atom, atom2:Atom) -> bool:
  """
  Accepts two any atoms.

  Args:
    atom1 (Atom): An Atom
    atom2 (Atom): An Atom

  Returns:
    bool: True, always.
  """
  #pylint: disable=unused-argument
  return True

def side_chain_selector(atom1:Atom, atom2:Atom) -> bool:
  """
  Accepts two atoms that are part of the sidechain of an aminoacid.

  Args:
    atom1 (Atom): An Atom.
    atom2 (Atom): An Atom.

  Returns:
    bool: True if both atom are part of the side chain of a residue.
  """
  return not is_back_bone(atom1) and not is_back_bone(atom2)

def carbon_alfa_selector(atom1:Atom, atom2:Atom) -> bool:
  """
  Accepts two alpha carbon atoms

  Args:
    atom1 (Atom): An Atom
    atom2 (Atom): An Atom

  Returns:
    bool: True if both atom are Alpha Carbons.
  """
  return atom1.id == 'CA' and atom2.id == 'CA'

def carbon_beta_selector(atom1:Atom, atom2:Atom) -> bool:
  """
  Accepts two beta carbon atoms

  Args:
    atom1 (Atom): An Atom
    atom2 (Atom): An Atom

  Returns:
    bool: True, if both atoms a Beta Carbons.
  """
  return atom1.id == 'CB' and atom2.id == 'CB'

def _pick_pdb_model(pdb_source) -> Optional[Model]:
  model = None
  if isinstance(pdb_source, Structure):
    struct = pdb_source
    model = list(struct.get_models())[0]
  elif isinstance(pdb_source, Model):
    model = pdb_source
  elif isinstance(pdb_source, str):
    parser = PDBParser()
    struct = parser.get_structure('XXXX', pdb_source)
    model = list(struct.get_models())[0]
  return model

def _shorter_distance_between_residues(
    res1: Residue,
    res2: Residue,
    atom_selector: AtomSelector
  ) -> Optional[DistanceElementLong]:
  min_dist = float('inf')
  min_res_data = None
  p_1 = res1.parent
  c_1 = str(p_1.id) if p_1 else ""
  p_2 = res2.parent
  c_2 = str(p_2.id) if p_2 else ""
  for atom1, atom2 in product(res1, res2):
    if (
      not atom1.id.startswith('H') and
      not atom2.id.startswith('H') and
      atom_selector(atom1, atom2)
    ):
      dist = atom1-atom2
      if dist < min_dist:
        min_dist = dist
        sorted_pair = sorted(
          [
            (c_1, res1.id[1], res1.resname, atom1.id),
            (c_2, res2.id[1], res2.resname, atom2.id)
          ]
        )
        min_res_data = (
          sorted_pair[0][0],
          sorted_pair[0][1],
          sorted_pair[0][2],
          sorted_pair[0][3],
          sorted_pair[1][0],
          sorted_pair[1][1],
          sorted_pair[1][2],
          sorted_pair[1][3],
          dist
        )
  if not min_res_data:
    return None
  return min_res_data

def calculate_distances(
    pdb_source:PDBSource,
    atom_selector:AtomSelector=all_atoms_selector,
    include_extra_info:bool=False
  ) -> DistanceDataSH:
  """
  Compute distances between residues

  Args:
    pdb_source (PDBSource): a path to a pdb file, a Bio.PDB.Structure or a
      Bio.PDB.Model
    atom_selector (AtomSelector): all_atoms_selector. a function that allows to
      select pairs of atoms to include into the distance calculation.
    include_extra_info (bool): False. If True adds residue name and atom name
      for each contacting atom to the output.

  Returns:
    DistanceDataSH: The distances calculated.

  Throws:
    ValueError: If a PDB model cannot be found in the PDB source.
  """
  model = _pick_pdb_model(pdb_source)
  if not model:
    raise ValueError("PDB source not recognized")
  chains = model.get_chains()
  out = []
  for chain1, chain2 in combinations_with_replacement(chains, 2):
    if chain1 is chain2:
      res_iter = combinations(chain1, 2)
    else:
      res_iter = product(chain1, chain2)
    for res1, res2 in res_iter:
      min_res_data = None
      if not res1 is res2:
        min_res_data = _shorter_distance_between_residues(
          res1, res2, atom_selector
        )
      if min_res_data:
        if include_extra_info:
          out.append(min_res_data)
        else:
          out.append((
            min_res_data[0],
            min_res_data[1],
            min_res_data[4],
            min_res_data[5],
            min_res_data[8]
          ))
  return out

def save_distances(
    dist_data:DistanceDataSH,
    outfile:str
  ):
  """
  Saves distance data to a file.

  Despite the content of the dist_data list, the output file will contain
  nine fields. Missing data fill filled with NA fields.

  Args:
    dist_data (DistanceDataSH): data generated with calculate_distance function.
    outfile (str): exported file.

  Throws:
    ValueError: If input data has wrong number of elements.
  """
  with open(outfile, 'w', encoding='utf8') as text_handle:
    for row in dist_data:
      if len(row) == 9: # Data with additional info.
        pass
      elif len(row) == 5: # Data with no additional info.
        row = [
          str(row[0]),
          str(row[1]),
          "NA",
          "NA",
          str(row[2]),
          str(row[3]),
          "NA",
          "NA",
          str(row[4])
        ]
      else:
        raise ValueError("Distance data has wrong number of element")
      text_handle.write(" ".join([str(x) for x in row]))
      text_handle.write("\n")

def read_distances(
    distance_file: str,
    add_extra_info:bool=False
  ) -> DistanceDataSH:
  """
  Read distance data file.

  Args:
    distance_file (str): The input file.
    add_extra_info (bool): Read extra information from input data.

  Returns:
    DistanceDataSH. A List of distances.
  """
  out = []
  with open(distance_file, "r", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=' ')
    for row in csv_reader:
      if len(row) == 9: # Data with additional info.
        if add_extra_info:
          out.append([
            row[0],
            int(row[1]),
            row[2],
            row[3],
            row[4],
            int(row[5]),
            row[6],
            row[7],
            float(row[8])
          ])
        else:
          out.append([
            row[0],
            int(row[1]),
            row[4],
            int(row[5]),
            float(row[8])
          ])
    return out

def contact_map_from_scpe(
    file_handle: TextIO,
    quaternary: bool = False,
    chars: str = "10"
  ) -> Dict[Tuple[int, int], bool]:
  """
  Read contact from SCPE output.

  The file content should have as many lines as positions in the protein.
  Each line should have characters from chars argument, separated by a space.
  There should be as many characters in every line as positions in the
  protein.

  Args:
    file_handle (TextIO): handle to the contact map file.
    quaternary (bool): a boolean value that indicates if quaternary contacts
      should be included.
    chars (str): Characters accepted in the contact map.
      This argument is expected to have a length of two characters.
      The first is the value for residue pairs in contact,
      the second one is the value for non contacts. Defaults to "10".

  Returns:
    Dict[Tuple[int, int], bool]. Returns a dict object from position pairs to
      boolean values that indicates that the corresponding pair is in contact or
      not. Position index start at 1.
  """
  contact_line_pattern = re.compile(f"[{chars}]( [{chars}])+$")
  qtag = "quaternary"
  ttag = "terciary"
  tags = [qtag, ttag]
  target_tag = qtag if quaternary else ttag
  correct_section = False
  position_index = 0
  contact_map = {}
  for line in file_handle:
    line = line.lower()
    c_match = re.match(contact_line_pattern, line)
    if c_match and correct_section:
      position_index += 1
      c_contacts = line.split()
      contact_map.update({
        (position_index, x+1): c == chars[0]
        for x, c in enumerate(c_contacts)})
    else:
      line = line.strip()
      if any(line == t for t in tags):
        correct_section = line == target_tag
  return contact_map

def contact_map_from_text(
    file_handle: TextIO,
    chars: str = "10"
  ) -> Dict[Tuple[int, int], bool]:
  """
  Reads the content of a file object as a contact map.

  The file content should have as many lines as positions in the protein.
  Each line should have characters from chars argument, separated by a space.
  There should be as many characters in every line as positions in the
  protein.

  Args:
    file_handle (TextIO):. handle to the contact map file.
    chars (str): Characters accepted in the contact map.
      This argument is expected to have a length of two characters.
      The first is the value for residue pairs in contact,
      the second one is the value for non contacts.

  Returns:
    Dict[Tuple[int, int], bool]. Returns a dict object from position pairs to
      boolean values that indicates that the corresponding pair is in contact or
      not. Position index start at 1.
  """
  contact_line_pattern = re.compile(f"[{chars}]( [{chars}])+$")
  position_index = 0
  contact_map = {}
  for line in file_handle:
    line = line.strip().lower()
    c_match = re.match(contact_line_pattern, line)
    if c_match:
      position_index += 1
      c_contacts = line.split()
      contact_map.update({
        (position_index, x+1): c == chars[0]
        for x, c in enumerate(c_contacts)})
  return contact_map


def calculate_distances_between_regions(
    pdbsrc:PDBSource,
    chain1:Chain,
    chain2:Chain,
    region1:List[Position],
    region2:List[Position]
  ) -> DistanceDataLong:
  """
  Calculate the distances between residues of two regions
  in a pdb structure.
  The distance between two residues is the shortest distance between any
  two atoms in those residues.

  Args:
    pdbsrc (PDBSource): An input pdb structure.
    chain1 (str): The chain ID of the first region.
    chain2 (str): The chain ID of the second region.
    region1 (List[int]): A list with the residue numbers of the first region.
    region2 (List[int]): A list with the residue numbers of the second region.

  Returns:
    DistanceDataLong: A list with the distances, atom information and
      residue information for all residue pairs. Between regions.
  """
  def _select_residues(struc, residues, c_chain):
    selected = []
    for st_chain in struc[0].get_chains():
      if not st_chain.id == c_chain:
        continue
      for res in st_chain.get_residues():
        _, rid, _ = res.id
        if not rid in residues:
          continue
        selected.append(res)
    return selected
  struct = pdb_structure_from(pdbsrc)
  res1 = _select_residues(struct, region1, chain1)
  res2 = _select_residues(
    struct, region2, chain2
  )
  distances = [
    maybe_dist
    for r1, r2 in product(res1, res2)
    for maybe_dist in [
      _shorter_distance_between_residues(r1, r2, all_atoms_selector)
    ]
    if maybe_dist is not None
  ]
  return distances
