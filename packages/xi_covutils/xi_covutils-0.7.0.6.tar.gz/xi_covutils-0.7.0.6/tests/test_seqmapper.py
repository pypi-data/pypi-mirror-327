"""
Test for seqmapper class
"""

from Bio.Align import Alignment
from pytest import raises
import mock
from xi_covutils.seqmapper import SequenceMapper
# pylint: disable=no-value-for-parameter

def test_build_seqmapper():
  """
  Tests for SequenceMapper
  """
  def _build_without_sequences():
    mapper = SequenceMapper()
    with raises(ValueError) as err:
      mapper.build()
    assert isinstance(err.value, ValueError)
    assert True
    assert "sequences are missing" in str(err)
  @mock.patch("xi_covutils.seqmapper.default_aligner")
  def _build_without_aligner(mock_aligner):
    mock_aligner().align.return_value = [Alignment(["-ATG", "GATG"])]
    mapper = (
      SequenceMapper()
        .with_sequences("ATG", "GATG")
        .build()
    )
    assert mapper.storage["first_aligned"] == "-ATG"
    assert mapper.storage["second_aligned"] == "GATG"
    mock_aligner().align.assert_called_once_with("ATG", "GATG")
  def _build_with_custom_aligner():
    mock_aligner = mock.MagicMock()
    mock_aligner.align.return_value = [Alignment(["ATG--", "ATGCC"])]
    mapper = (
      SequenceMapper()
        .with_sequences("ATG", "ATGCC")
        .with_aligner(mock_aligner)
        .build()
    )
    assert mapper.storage["first_aligned"] == "ATG--"
    assert mapper.storage["second_aligned"] == "ATGCC"
    mock_aligner.align.assert_called_once_with("ATG", "ATGCC")
  _build_without_sequences()
  _build_without_aligner()
  _build_with_custom_aligner()

def test_mapping_from_aln_sequencese():
  """
  Test Mapping created from aligned sequences.
  """
  def _without_gaps():
    seq1 = "ATGTG"
    seq2 = "GTGTA"
    mapper = SequenceMapper.from_aligned_sequences(seq1, seq2)
    positions = [1, 2, 3, 4, 5]
    aln_to_first = [mapper.from_aln_to_first(x) for x in positions]
    assert aln_to_first == positions
    aln_to_second = [mapper.from_aln_to_second(x) for x in positions]
    assert aln_to_second == positions
    first_to_aln = [mapper.from_first_to_aln(x) for x in positions]
    assert first_to_aln == positions
    first_to_second = [mapper.from_first_to_second(x) for x in positions]
    assert first_to_second == positions
    second_to_aln = [mapper.from_second_to_aln(x) for x in positions]
    assert second_to_aln == positions
    second_to_first = [mapper.from_second_to_first(x) for x in positions]
    assert second_to_first == positions
  def _with_gaps_in_second():
    seq1 = "ATGTG"
    seq2 = "-TGT-"
    mapper = SequenceMapper.from_aligned_sequences(seq1, seq2)
    positions = [1, 2, 3, 4, 5]
    aln_to_first = [mapper.from_aln_to_first(x) for x in positions]
    assert aln_to_first == positions
    aln_to_second = [mapper.from_aln_to_second(x) for x in positions]
    assert aln_to_second == [None, 1, 2, 3, None]
    first_to_aln = [mapper.from_first_to_aln(x) for x in positions]
    assert first_to_aln == positions
    first_to_second = [mapper.from_first_to_second(x) for x in positions]
    assert first_to_second == [None, 1, 2, 3, None]
    second_to_aln = [mapper.from_second_to_aln(x) for x in [1, 2, 3]]
    assert second_to_aln == [2, 3, 4]
    second_to_first = [mapper.from_second_to_first(x) for x in [1, 2, 3]]
    assert second_to_first == [2, 3, 4]
  def _with_gaps_in_first():
    seq1 = "-TGT-G"
    seq2 = "ATGTGG"
    mapper = SequenceMapper.from_aligned_sequences(seq1, seq2)
    positions = [1, 2, 3, 4, 5, 6]
    aln_to_first = [mapper.from_aln_to_first(x) for x in positions]
    assert aln_to_first == [None, 1, 2, 3, None, 4]
    aln_to_second = [mapper.from_aln_to_second(x) for x in positions]
    assert aln_to_second == positions
    first_to_aln = [mapper.from_first_to_aln(x) for x in range(1,5)]
    assert first_to_aln == [2, 3, 4, 6]
    first_to_second = [mapper.from_first_to_second(x) for x in range(1,5)]
    assert first_to_second == [2, 3, 4, 6]
    second_to_aln = [mapper.from_second_to_aln(x) for x in positions]
    assert second_to_aln == positions
    second_to_first = [mapper.from_second_to_first(x) for x in positions]
    assert second_to_first == [None, 1, 2, 3, None, 4]
  def _with_gaps_in_both():
    seq1 = "-TGT-G"
    seq2 = "AT-TGG"
    mapper = SequenceMapper.from_aligned_sequences(seq1, seq2)
    aln_positions = list(range(1,7))
    seq1_positions = list(range(1,5))
    seq2_positions = list(range(1,6))
    aln_to_first = [mapper.from_aln_to_first(x) for x in aln_positions]
    assert aln_to_first == [None, 1, 2, 3, None, 4]
    aln_to_second = [mapper.from_aln_to_second(x) for x in aln_positions]
    assert aln_to_second == [1, 2, None, 3, 4, 5]
    first_to_aln = [mapper.from_first_to_aln(x) for x in seq1_positions]
    assert first_to_aln == [2, 3, 4, 6]
    first_to_second = [mapper.from_first_to_second(x) for x in seq1_positions]
    assert first_to_second == [2, None, 3, 5]
    second_to_aln = [mapper.from_second_to_aln(x) for x in seq2_positions]
    assert second_to_aln == [1, 2, 4, 5, 6]
    second_to_first = [mapper.from_second_to_first(x) for x in seq2_positions]
    assert second_to_first == [None, 1, 3, None, 4]
  _without_gaps()
  def _with_gaps_in_columns():
    seq1 = "-TGT-G"
    seq2 = "AT-T-G"
    mapper = SequenceMapper.from_aligned_sequences(seq1, seq2)
    aln_positions = list(range(1,7))
    seq1_positions = list(range(1,5))
    seq2_positions = list(range(1,5))
    aln_to_first = [mapper.from_aln_to_first(x) for x in aln_positions]
    assert aln_to_first == [None, 1, 2, 3, None, 4]
    aln_to_second = [mapper.from_aln_to_second(x) for x in aln_positions]
    assert aln_to_second == [1, 2, None, 3, None, 4]
    first_to_aln = [mapper.from_first_to_aln(x) for x in seq1_positions]
    assert first_to_aln == [2, 3, 4, 6]
    first_to_second = [mapper.from_first_to_second(x) for x in seq1_positions]
    assert first_to_second == [2, None, 3, 4]
    second_to_aln = [mapper.from_second_to_aln(x) for x in seq2_positions]
    assert second_to_aln == [1, 2, 4, 6]
    second_to_first = [mapper.from_second_to_first(x) for x in seq2_positions]
    assert second_to_first == [None, 1, 3, 4]
  _with_gaps_in_first()
  _with_gaps_in_second()
  _with_gaps_in_both()
  _with_gaps_in_columns()
