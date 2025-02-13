"""
  Test Pdb Mapper functions
"""
from os.path import join
from xi_covutils.pdbmapper import (
  PDBSeqMapper, align_two_sequences, build_pdb_sequence
)
from xi_covutils.pdbmapper import build_seq_from_dict
from xi_covutils.pdbmapper import align_dict_to_sequence
from xi_covutils.pdbmapper import map_align
from xi_covutils.pdbmapper import align_dict_values
from xi_covutils.pdbmapper import map_to_ungapped
from xi_covutils.pdbmapper import align_pdb_to_sequence
from xi_covutils.pdbmapper import align_sequence_to_sequence

def test_build_pdb_sequence(test_data_folder):
  """
  Test build pdb sequence
  """
  pdb_file = join(test_data_folder, "5IZE.pdb")
  case_1_res = build_pdb_sequence(pdb_file, "A")
  assert case_1_res == {0:"G", 1:"M", 2:"D", 3:"K", 6:"E", 7:"I", 8:"H"}
  case_2_res = build_pdb_sequence(pdb_file, "B")
  assert case_2_res == {4:"Y", 5:"R", 7:"I", 8:"H", 9:"N"}

def test_build_pdb_sequence_with_hetero(test_data_folder):
  """
  Test build pdb sequence with Hetero groups
  """
  pdb_file = join(test_data_folder, "with_hetero.pdb")
  case_1_res = build_pdb_sequence(pdb_file, "A")
  assert case_1_res == {837:"G", 838:"A"}

def test_build_seq_from_dict():
  """
  Test build sequence from dict.
  """
  seq1_dict = {0:"A", 3:"C", 2:"B", 8:"D"}
  assert build_seq_from_dict(seq1_dict) == "ABCD"
  seq2_dict = {4:"A", 3:"C", 2:"B", 1:"D"}
  assert build_seq_from_dict(seq2_dict) == "DBCA"

def test_align_dict_to_sequence():
  """
  Test Align dict to sequence
  """
  seq1_dict = {0:"A", 3:"C", 2:"B", 8:"D"}
  seq1 = "ABXXXCDE"
  map1 = align_dict_to_sequence(seq1_dict, seq1)
  assert map1 == {1: 1, 2: 2, 3: 6, 4: 7}

def test_map_align():
  """
  Test Align Map
  """
  seq1_dict = "-ABC-"
  seq2 = "Z-BCD"
  data3 = map_align(seq1_dict, seq2)
  assert data3 == {2:2, 3:3}
  seq1_dict = "-ABC-EFG"
  seq2 = "AABCDE-G"
  data3 = map_align(seq1_dict, seq2)
  assert data3 == {1:2, 2:3, 3:4, 4:6, 6:7}

def test_align_dict_values():
  """
  Test Align Dict Values
  """
  # from alignmet:
  # -ABC-
  # Z-BCD
  data1 = {2:1, 3:2, 4:3}
  data2 = {1:1, 3:2, 4:3, 5:4}
  data3 = align_dict_values(data1, data2)
  assert data3 == {2:2, 3:3}
  # from alignmet:
  # -ABC-EFG
  # AABCDE-G
  data1 = {2:1, 3:2, 4:3, 6:4, 7:5, 8:6}
  data2 = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 8:7}
  data3 = align_dict_values(data1, data2)
  assert data3 == {1:2, 2:3, 3:4, 4:6, 6:7}

def test_map_to_ungapped():
  """
  Test Map to Ungappoed
  """
  seq = "---ABC---"
  mapping = map_to_ungapped(seq)
  assert mapping == {4: 1, 5: 2, 6: 3}
  seq = "---A-C-D-"
  mapping = map_to_ungapped(seq)
  assert mapping == {4: 1, 6: 2, 8: 3}

def test_align_sequence_to_sequence():
  """
  Test align sequence to sequence.
  """
  seq1 = "ABCDE"
  seq2 = "XXXXXABCDEXXXXX"
  align = align_sequence_to_sequence(seq1, seq2)
  assert align[1] == 6
  assert align[2] == 7
  assert align[3] == 8
  assert align[4] == 9
  assert align[5] == 10
  align = align_sequence_to_sequence(seq2, seq1)
  assert align[6] == 1
  assert align[7] == 2
  assert align[8] == 3
  assert align[9] == 4
  assert align[10] == 5

def test_align_pdb_to_sequence(test_data_folder):
  """
  Test Align PDB to sequence
  """
  #        0........90.......9
  # pdb:   GMDK--EIH # Position matches pdb offset
  # seq:   GMDK--EIH
  pdb_file = join(test_data_folder, "5IZE.pdb")
  aligned = align_pdb_to_sequence(pdb_file, "A",  "GMDKEIH")
  assert aligned == {0:1, 1:2, 2:3, 3:4, 6:5, 7:6, 8:7}
  #        1...4...90.......9
  # pdb:   ----YR-IHN # Position matches pdb offset
  # seq:   ----YK-IHN
  aligned = align_pdb_to_sequence(pdb_file, "B",  "YKIHN")
  assert aligned == {4:1, 5:2, 7:3, 8:4, 9:5}

# pylint: disable=too-few-public-methods
class TestPDBSeqMapper:
  """Test PDBSeqMapper class"""
  def test_align_sequence_to_pdb(self, test_data_folder):
    """Test align_sequence_to_pdb function"""
    sequence = "METGMDKYYEIH"
    expented_pdb_seq_aln = "---GMDK--EIH"
    expented_pdb_seq = "GMDKEIH"
    chain = "A"
    pdb_file = join(test_data_folder, "5IZE.pdb")
    mapper = PDBSeqMapper()
    mapper.align_sequence_to_pdb(sequence, pdb_file, chain)
    assert mapper.get_sequence() == sequence
    assert mapper.get_aln_sequence() == sequence
    assert mapper.get_pdb_sequence() == expented_pdb_seq
    assert mapper.get_aln_pdb_sequence() == expented_pdb_seq_aln
    assert mapper.from_residue_number_to_seq(0) == 4
    assert mapper.from_residue_number_to_seq(1) == 5
    assert mapper.from_residue_number_to_seq(2) == 6
    assert mapper.from_residue_number_to_seq(3) == 7
    assert mapper.from_residue_number_to_seq(4) is None
    assert mapper.from_residue_number_to_seq(5) is None
    assert mapper.from_residue_number_to_seq(6) == 10
    assert mapper.from_residue_number_to_seq(7) == 11
    assert mapper.from_residue_number_to_seq(8) == 12
    assert mapper.from_seq_to_residue_number(1) is None
    assert mapper.from_seq_to_residue_number(2) is None
    assert mapper.from_seq_to_residue_number(3) is None
    assert mapper.from_seq_to_residue_number(4) == 0
    assert mapper.from_seq_to_residue_number(5) == 1
    assert mapper.from_seq_to_residue_number(6) == 2
    assert mapper.from_seq_to_residue_number(7) == 3
    assert mapper.from_seq_to_residue_number(8) is None
    assert mapper.from_seq_to_residue_number(9) is None
    assert mapper.from_seq_to_residue_number(10) == 6
    assert mapper.from_seq_to_residue_number(11) == 7
    assert mapper.from_seq_to_residue_number(12) == 8


def test_align_two_sequences():
  """Test test_align_two_sequences function"""
  seq1 = "QWERTYIPASD"
  seq2 = "ERSYIWPAS"
  res = align_two_sequences(seq1, seq2)
  assert res.aln_seq_1 == "QWERTYI-PASD"
  assert res.aln_seq_2 == "--ERSYIWPAS-"
  assert res.mapping.get(1) is None
  assert res.mapping.get(2) is None
  assert res.mapping[3] == 1
  assert res.mapping[4] == 2
  assert res.mapping[5] == 3
  assert res.mapping[6] == 4
  assert res.mapping[7] == 5
  assert res.mapping[8] == 7
  assert res.mapping[9] == 8
  assert res.mapping[10] == 9
  assert res.mapping.get(11) is None
