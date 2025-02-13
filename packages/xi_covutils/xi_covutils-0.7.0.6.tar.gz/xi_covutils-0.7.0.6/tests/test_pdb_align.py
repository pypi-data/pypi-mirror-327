"""
Test PDB alignment functions.
"""
import os

from pytest import fixture, raises

from xi_covutils.pdb_align import align_partial_pdbs, align_pdbs
from xi_covutils.pdbbank import pdb_structure_from


@fixture()
def pdb_5ize_2(test_data_folder):
  """
  Access to file 5IZE_2.pdb in test data folder.
  """
  pdb_file = os.path.join(test_data_folder, "5IZE_2.pdb")
  return pdb_structure_from(pdb_file)

@fixture()
def pdb_5ize(test_data_folder):
  """
  Access to file 5IZE.pdb in test data folder.
  """
  pdb_file = os.path.join(test_data_folder, "5IZE.pdb")
  return pdb_structure_from(pdb_file)

# pylint: disable=redefined-outer-name
def test_align_pdbs(pdb_5ize, pdb_5ize_2):
  """
  Test align_pdbs function
  """
  st2 = align_pdbs(pdb_5ize, pdb_5ize_2, "A", "A")
  atom1 = pdb_5ize_2[0]["A"][1]["CA"]
  atom2 = pdb_5ize[0]["A"][1]["CA"]
  assert atom1 - atom2 > 2
  # Aligned structure should be close to the first structure
  atom3 = st2.structure[0]["A"][1]["CA"]
  assert atom2 - atom3 < 0.1
  # Alignment should be applied to the whole structure
  atom4 = pdb_5ize_2[0]["B"][4]["CA"]
  atom5 = pdb_5ize[0]["B"][4]["CA"]
  atom6 = st2.structure[0]["B"][4]["CA"]
  assert atom4 - atom5 > 30
  assert atom6 - atom5 < 15


# pylint: disable=redefined-outer-name
def test_align_partial_pdbs(pdb_5ize, pdb_5ize_2):
  """
  Test align_partial_pdbs function
  """
  def _with_three_residues_in_common():
    st2 = align_partial_pdbs(
      pdb_5ize,
      pdb_5ize_2,
      region1 = [0, 1, 2, 3, 4, 5, 6, 7],
      region2 = [3, 6, 7, 8],
      chain1="A",
      chain2="A"
    )
    atom1 = pdb_5ize_2[0]["A"][1]["CA"]
    atom2 = pdb_5ize[0]["A"][1]["CA"]
    assert atom1 - atom2 > 2
    # Aligned structure should be close to the first structure
    atom3 = st2.structure[0]["A"][1]["CA"]
    assert atom2 - atom3 < 0.1
    # Alignment should be applied to the whole structure
    atom4 = pdb_5ize_2[0]["B"][4]["CA"]
    atom5 = pdb_5ize[0]["B"][4]["CA"]
    atom6 = st2.structure[0]["B"][4]["CA"]
    assert atom4 - atom5 > 30
    assert atom6 - atom5 < 15
  def _with_two_residues_in_common():
    """
    Alignment can not be done with two points.
    ValueError should be thrown.
    """
    with raises(ValueError) as err:
      align_partial_pdbs(
        pdb_5ize,
        pdb_5ize_2,
        region1 = [0, 1, 2, 3, 4, 5, 6],
        region2 = [3, 6, 7],
        chain1="A",
        chain2="A"
      )
      assert "Alignment requires at teast three residues." == str(err)
  _with_three_residues_in_common()
  _with_two_residues_in_common()
