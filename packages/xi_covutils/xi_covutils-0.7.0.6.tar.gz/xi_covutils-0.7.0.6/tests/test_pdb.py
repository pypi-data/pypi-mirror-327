"""
    Test functions from pdb module
"""
from os.path import join
from Bio.PDB import PDBParser
from pytest import approx
from xi_covutils.pdbbank import gyration_radius

def test_gyration_radius(test_data_folder):
  "Test giration radius calculation"
  pdb_file = join(test_data_folder, '3A5E.pdb')
  structure = PDBParser().get_structure('3A5E', pdb_file)
  result = gyration_radius(structure)
  assert result['rg']['all'] == approx(1148.0400394835)
  assert result['compactness']['all'] == approx(76.5360026322333)
  result = gyration_radius(structure, by_chain=True)
  assert result['rg']['A'] == approx(1148.0400394835)
  assert result['compactness']['A'] == approx(76.5360026322333)
  pdb_file = join(test_data_folder, '5IZE.pdb')
  structure = PDBParser().get_structure('5IZE', pdb_file)
  result = gyration_radius(structure, by_chain=True)
  assert result['rg']['A'] == approx(177.509891428571)
  assert result['compactness']['A'] == approx(25.3585559183673)
  assert result['rg']['B'] == approx(59.8395376)
  assert result['compactness']['B'] == approx(11.96790752)
