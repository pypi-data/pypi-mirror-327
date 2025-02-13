"""
  Test distance functions
"""
from io import StringIO
from itertools import combinations, combinations_with_replacement, product
from os.path import join
from typing import cast

from Bio.PDB.PDBParser import PDBParser
from pytest import approx

from xi_covutils.distances import (
  DistanceDataLong,
  Distances,
  all_atoms_selector,
  calculate_distances,
  calculate_distances_between_regions,
  carbon_alfa_selector,
  carbon_beta_selector,
  contact_map_from_scpe,
  contact_map_from_text,
  from_mitos, read_distances,
  side_chain_selector
)

# pylint: disable=too-many-locals
def test_neighborsearch(test_data_folder):
  """
  Test neighbor search
  """
  def validate_atoms_alpha_carbon(atom1, atom2):
    return atom1.id == 'CA' and atom2.id == 'CA'

  pdb_file = join(test_data_folder, 'with_hetero.pdb')
  parser = PDBParser()
  struct = parser.get_structure('XXXX', pdb_file)
  model = list(struct.get_models())[0]
  chains = model.get_chains()

  validator = validate_atoms_alpha_carbon
  for chain1, chain2 in combinations_with_replacement(chains, 2):
    if chain1 is chain2:
      res_iter = combinations(chain1, 2)
    else:
      res_iter = product(chain1, chain2)
    for res1, res2 in res_iter:
      if not res1 is res2:
        for atom1, atom2 in product(res1, res2):
          if validator(atom1, atom2):
            dist = atom1-atom2
            outline = [
              item for res in sorted(
                [
                  (chain1.id, res1.id[1], res1.resname, atom1.id),
                  (chain2.id, res2.id[1], res2.resname, atom2.id)
                ]
              )
              for item in res
            ]
            outline = outline + [dist]

def test_read_distances_without_additional_info(test_data_folder):
  """
  Test read distances without additional info.
  """
  distance_file = join(test_data_folder, 'distances_xi')
  dist = read_distances(distance_file)
  assert len(dist) == 5
  assert (
    dist[0][:4] == ['A', 55, 'A', 56] and
    dist[0][4] == approx(1.3247309160731473)
  )
  assert (
    dist[1][:4] == ['A', 55, 'A', 57] and
    dist[1][4] == approx(2.4696904664350146)
  )
  assert (
    dist[2][:4] == ['A', 55, 'A', 58] and
    dist[2][4] == approx(6.5654210070642085)
  )
  assert (
    dist[3][:4] == ['A', 55, 'A', 59] and
    dist[3][4] == approx(8.9199209077211)
  )
  assert (
    dist[4][:4] == ['A', 55, 'A', 60] and
    dist[4][4] == approx(12.173748354553744)
  )

def test_read_distances_with_additional_info(test_data_folder):
  """
  Test reading sequences with additional info
  """
  distance_file = join(test_data_folder, 'distances_xi')
  dist = read_distances(distance_file, add_extra_info=True)
  dist = cast(DistanceDataLong, dist)
  assert len(dist) == 5
  assert len(dist[0]) == 9
  assert len(dist[1]) == 9
  assert len(dist[2]) == 9
  assert len(dist[3]) == 9
  assert len(dist[4]) == 9
  assert (
    dist[0][:8] == ['A', 55, 'LEU', 'CA', 'A', 56, 'LEU', 'CA'] and
    dist[0][8] == approx(1.3247309160731473)
  )
  assert (
    dist[1][:8] == ['A', 55, 'LEU', 'CA', 'A', 57, 'PRO', 'CA'] and
    dist[1][8] == approx(2.4696904664350146)
  )
  assert (
    dist[2][:8] == ['A', 55, 'LEU', 'CA', 'A', 58, 'THR', 'CA'] and
    dist[2][8] == approx(6.5654210070642085)
  )
  assert (
    dist[3][:8] == ['A', 55, 'LEU', 'CA', 'A', 59, 'PRO', 'CA'] and
    dist[3][8] == approx(8.9199209077211)
  )
  assert (
    dist[4][:8] == ['A', 55, 'LEU', 'CA', 'A', 60, 'PRO', 'CA'] and
    dist[4][8] == approx(12.173748354553744)
  )

# pylint: disable=too-many-statements
def test_calculate_distances(test_data_folder):
  """
  Test calculate distance function
  """
  pdb_file = join(test_data_folder, '3A5E.pdb')
  struct = PDBParser().get_structure('XXXX', pdb_file)
  distances = calculate_distances(
    struct,
    carbon_alfa_selector,
    include_extra_info=True
  )
  x_1, y_1, z_1 = -7.610, -12.373, -9.735
  x_2, y_2, z_2 = -8.291, -9.315, -7.550
  expected_distance = ((x_1-x_2)**2 + (y_1-y_2)**2 + (z_1-z_2)**2)**(1/2)
  found = False
  for dist_data in distances:
    if dist_data[0:8] == ('A', 1, 'LYS', 'CA', 'A', 2, 'VAL', 'CA'):
      found = True
      assert len(dist_data) == 9
      assert dist_data[8] == approx(expected_distance)
  assert found
  assert len(distances) == 15*14/2 # There are 15 residues, and ∑15 pairs.
  assert all(x == 'CA' for x in list(zip(*distances))[3]) # All atoms should
  assert all(x == 'CA' for x in list(zip(*distances))[7]) # be Alpha Carbon

  distances = calculate_distances(
    pdb_file,
    carbon_alfa_selector,
    include_extra_info=True)
  x_1, y_1, z_1 = -7.610, -12.373, -9.735
  x_2, y_2, z_2 = -8.291, -9.315, -7.550
  expected_distance = ((x_1-x_2)**2 + (y_1-y_2)**2 + (z_1-z_2)**2)**(1/2)
  found = False
  for dist_data in distances:
    if dist_data[0:8] == ('A', 1, 'LYS', 'CA', 'A', 2, 'VAL', 'CA'):
      found = True
      assert len(dist_data) == 9
      assert dist_data[8] == approx(expected_distance)
  assert found
  assert len(distances) == 15*14/2 # There are 15 residues, and ∑15 pairs.
  assert all(x == 'CA' for x in list(zip(*distances))[3]) # All atoms should
  assert all(x == 'CA' for x in list(zip(*distances))[7]) # be Alpha Carbon

  distances = calculate_distances(
    pdb_file,
    carbon_alfa_selector,
    include_extra_info=False)
  x_1, y_1, z_1 = -7.610, -12.373, -9.735
  x_2, y_2, z_2 = -8.291, -9.315, -7.550
  expected_distance = ((x_1-x_2)**2 + (y_1-y_2)**2 + (z_1-z_2)**2)**(1/2)
  found = False
  for dist_data in distances:
    if dist_data[0:4] == ('A', 1, 'A', 2):
      found = True
      assert dist_data[4] == approx(expected_distance)
  assert found
  assert len(distances) == 15*14/2 # There are 15 residues, and ∑15 pairs.

  distances = calculate_distances(
    pdb_file,
    side_chain_selector,
    include_extra_info=False)
  expected_distance = 4.0521824
  found = False
  for dist_data in distances:
    assert len(dist_data) == 5
    if dist_data[0:4] == ('A', 6, 'A', 11):
      found = True
      assert dist_data[4] == approx(expected_distance)
  assert found
  assert len(distances) == 15*14/2 # There are 15 residues, and ∑15 pairs.

  distances = calculate_distances(
    pdb_file,
    carbon_beta_selector,
    include_extra_info=False)
  expected_distance = 3.9129025
  found = False
  for dist_data in distances:
    assert len(dist_data) == 5
    if dist_data[0:4] == ('A', 11, 'A', 15):
      found = True
      assert dist_data[4] == approx(expected_distance)
  assert found
  assert len(distances) == 14*13/2
  # There are 15 residues, and ∑14 pairs.
  # One resiude is Gly with no beta carbon.

  distances = calculate_distances(
    pdb_file,
    all_atoms_selector,
    include_extra_info=False)
  expected_distance = 3.7939344
  found = False
  for dist_data in distances:
    assert len(dist_data) == 5
    if dist_data[0:4] == ('A', 7, 'A', 11):
      found = True
      assert dist_data[4] == approx(expected_distance)
  assert found
  assert len(distances) == 15*14/2 # There are 15 residues, and ∑15 pairs.

def test_from_mitos(test_data_folder):
  """
  Test that output from MIToS distances can be imported correctly
    :param test_data_folder: a fixture with the test data folder path
  """
  dist_file = join(test_data_folder, "distances")
  dist = from_mitos(dist_file)
  assert len(dist) == 5
  assert (
    dist[0][:4] == ('A', 55, 'A', 56) and
    dist[0][4] == approx(1.3247309160731473)
  )
  assert (
    dist[1][:4] == ('A', 55, 'A', 57) and
    dist[1][4] == approx(2.4696904664350146)
  )
  assert (
    dist[2][:4] == ('A', 55, 'A', 58) and
    dist[2][4] == approx(6.5654210070642085)
  )
  assert (
    dist[3][:4] == ('A', 55, 'A', 59) and
    dist[3][4] == approx(8.9199209077211)
  )
  assert (
    dist[4][:4] == ('A', 55, 'A', 60) and
    dist[4][4] == approx(12.173748354553744)
  )

def test_create_and_retrieve():
  """
  Test that an instance of Distance can be created and accesed correctly
  """
  dist_data = [
    ('A', 2, 'B', 5, 3.14159),
    ('A', 4, 'B', 15, 6.0022),
    ('A', 8, 'B', 2, 2.7182)
  ]
  dist = Distances(dist_data)
  chain_1 = 'A'
  chain_2 = 'B'
  p11 = 2
  p12 = 5
  p21 = 4
  p22 = 15
  p31 = 8
  p32 = 2
  assert dist.of(chain_1, p11, chain_1, p11) == approx(0)
  assert dist.of(chain_1, p11, chain_2, p12) == approx(3.14159)
  assert dist.of(chain_2, p12, chain_1, p11) == approx(3.14159)
  assert dist.of(chain_1, p21, chain_2, p22) == approx(6.0022)
  assert dist.of(chain_2, p22, chain_1, p21) == approx(6.0022)
  assert dist.of(chain_1, p31, chain_2, p32) == approx(2.7182)
  assert dist.of(chain_2, p32, chain_1, p31) == approx(2.7182)

def test_remap_positions(test_data_folder):
  """
  Positions in a Distances object can be remapped to different positions
  with an appropiate dict object.

    :param test_data_folder: a fixture with the test data folder
  """
  dist_file = join(test_data_folder, "distances")
  dist = Distances(from_mitos(dist_file))
  mapping = {'A':{55:1, 56:2, 57:3, 58:4, 59:5, 60:6}}
  dist.remap_positions(mapping)
  assert not dist.of('A', 55, 'A', 56)
  assert dist.of('A', 1, 'A', 2) == approx(1.3247309160731473)
  assert dist.of('A', 1, 'A', 3) == approx(2.4696904664350146)
  assert dist.of('A', 1, 'A', 4) == approx(6.5654210070642085)

def test_is_contact(test_data_folder):
  """
  Positions with close distance should be detected as contacts.
    :param test_data_folder: a fixture with the test data folder
  """
  dist_file = join(test_data_folder, "distances")
  dist = Distances(from_mitos(dist_file))
  assert dist.is_contact('A', 55, 'A', 55)
  assert dist.is_contact('A', 55, 'A', 56)
  assert dist.is_contact('A', 55, 'A', 57)
  assert not dist.is_contact('A', 55, 'A', 58)
  assert not dist.is_contact('A', 55, 'A', 59)
  assert not dist.is_contact('A', 55, 'A', 60)

def test_mean_intramolecular():
  """
  A Distances object should be able to compute the
  mean number of intramolecular contacts for every chain
  """
  # Res 1 has 4 contacts,
  # Res 2 has 3 contacts,
  # Res 3 has 2 contacts,
  # Res 4 has 2 contacts,
  # Res 5 has 3 contacts,
  dist_data = [
    ('A', 1, 'A', 2, 1),
    ('A', 1, 'A', 3, 1),
    ('A', 1, 'A', 4, 1),
    ('A', 1, 'A', 5, 1),
    ('A', 2, 'A', 3, 1),
    ('A', 2, 'A', 4, 9),
    ('A', 2, 'A', 5, 1),
    ('A', 3, 'A', 4, 9),
    ('A', 3, 'A', 5, 9),
    ('A', 4, 'A', 5, 1),
    ('B', 1, 'A', 2, 10)
  ]
  dist = Distances(dist_data)
  mean_ic = dist.mean_intramolecular()
  assert len(mean_ic) == 2
  assert mean_ic["A"] == approx(float(4+3+2+2+3)/5)
  assert mean_ic["B"] == approx(0)

def test_contact_map_from_scpe():
  """
  Test contact_map_from_scpe function
  """
  content = StringIO("""Tertiary contact map
Warning!. Position 2 has 0 contacts
Quaternary contact map
Warning!. Position 2 has 0 contacts
Terciary
0 1 1
1 0 0
1 0 0
Quaternary
0 0 1
0 0 1
1 1 0
Tertiary Total contacts  Quaternary Total contacts
2           2  0
0           0  0
3           3  0
""")
  c_map_1 = contact_map_from_scpe(content, quaternary=False)
  assert not c_map_1[(1, 1)]
  assert c_map_1[(1, 2)]
  assert c_map_1[(1, 3)]
  assert c_map_1[(2, 1)]
  assert not c_map_1[(2, 2)]
  assert not c_map_1[(2, 3)]
  assert c_map_1[(3, 1)]
  assert not c_map_1[(3, 2)]
  assert not c_map_1[(3, 3)]

  content = StringIO("""Tertiary contact map
Warning!. Position 2 has 0 contacts
Quaternary contact map
Warning!. Position 2 has 0 contacts
Terciary
0 1 1
1 0 0
1 0 0
Quaternary
0 0 1
0 0 1
1 1 0
Tertiary Total contacts  Quaternary Total contacts
2           2  0
0           0  0
3           3  0
""")
  c_map_1 = contact_map_from_scpe(content, quaternary=True)
  assert not c_map_1[(1, 1)]
  assert not c_map_1[(1, 2)]
  assert c_map_1[(1, 3)]
  assert not c_map_1[(2, 1)]
  assert not c_map_1[(2, 2)]
  assert c_map_1[(2, 3)]
  assert c_map_1[(3, 1)]
  assert c_map_1[(3, 2)]
  assert not c_map_1[(3, 3)]

def test_contact_map_from_text():
  """
  Test contact_map_from_text function
  """
  content = StringIO("""
0 1 1
1 0 0
1 0 0
""")
  c_map_1 = contact_map_from_text(content)
  assert not c_map_1[(1, 1)]
  assert c_map_1[(1, 2)]
  assert c_map_1[(1, 3)]
  assert c_map_1[(2, 1)]
  assert not c_map_1[(2, 2)]
  assert not c_map_1[(2, 3)]
  assert c_map_1[(3, 1)]
  assert not c_map_1[(3, 2)]
  assert not c_map_1[(3, 3)]


def test_distances_from_contact_map():
  """
  Test contact_map_from_text function
  """
  content = StringIO("""
0 1 1
1 0 0
1 0 0
""")
  c_map = contact_map_from_text(content)
  dist = Distances.from_contact_map(c_map)

  assert all(
    d in [1, 10]
    for (_, _, _, _, d) in dist.raw_distances()
  )

  assert dist.of('A', 1, 'A', 1) == 0
  assert dist.of('A', 1, 'A', 2) == 1
  assert dist.of('A', 3, 'A', 2) == 10

  assert dist.is_contact('A', 1, 'A', 1)
  assert dist.is_contact('A', 1, 'A', 2)
  assert not dist.is_contact('A', 3, 'A', 2)

def test_calculate_distances_between_regions(test_data_folder):
  """
  Test Calculation of distances between regions pdb regions.
  """
  def _with_two_non_empty_regions(test_data_folder):
    pdb_file = join(
      test_data_folder,
      "5IZE.pdb"
    )
    chain1 = "A"
    reg1 = [1, 2]
    chain2 = "B"
    reg2 = [7, 8]
    distances = calculate_distances_between_regions(
      pdb_file,
      chain1,
      chain2,
      reg1,
      reg2
    )
    assert len(distances) == 4
    observed_dist = [x[8] for x in distances]
    assert all(50 < x < 100 for x in observed_dist)
    observed_res_pairs = sorted(
      (x[0], x[1], x[4], x[5]) for x in distances
    )
    assert observed_res_pairs == [
      ("A", 1, "B", 7),
      ("A", 1, "B", 8),
      ("A", 2, "B", 7),
      ("A", 2, "B", 8),
    ]
  def _with_empty_regions(test_data_folder):
    pdb_file = join(test_data_folder, "5IZE.pdb")
    chain1 = "A"
    chain2 = "B"
    reg = [7, 8]
    distances = calculate_distances_between_regions(
      pdb_file,
      chain1,
      chain2,
      [],
      reg
    )
    assert distances == []
    distances = calculate_distances_between_regions(
      pdb_file,
      chain1,
      chain2,
      reg,
      [],
    )
    assert distances == []
    distances = calculate_distances_between_regions(
      pdb_file,
      chain1,
      chain2,
      [],
      [],
    )
    assert distances == []
  def _with_non_existing_resnumbers(test_data_folder):
    pdb_file = join(test_data_folder, "5IZE.pdb")
    chain1 = "A"
    chain2 = "B"
    reg = [17, 18]
    distances = calculate_distances_between_regions(
      pdb_file,
      chain1,
      chain2,
      [],
      reg
    )
    assert distances == []
  _with_two_non_empty_regions(test_data_folder)
  _with_empty_regions(test_data_folder)
  _with_non_existing_resnumbers(test_data_folder)
