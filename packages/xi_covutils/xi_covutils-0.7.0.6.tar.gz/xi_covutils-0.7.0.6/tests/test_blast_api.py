"""
Test NCBI Blast calls
"""
import os
from typing import Any
from pytest import raises
import pytest
from xi_covutils.blast_api import (
  NcbiBlast,
  NcbiDatabase,
  NcbiProgram,
  BlastOutput,
  BlastReport,
  BlastParams,
  BlastResults,
  BlastHit,
  BlastStats
)

@pytest.mark.requires_connection
class TestNcbiBlast:
  """
  Test NCBI Blast class
  """
  @pytest.mark.requires_connection
  def test_build(self):
    """
    Tests build method
    """
    def _with_all_data():
      ncbi = (
        NcbiBlast()
          .set_program(NcbiProgram.BLASTN)
          .set_database(NcbiDatabase.NR)
          .build()
      )
      assert ncbi is not None
    def _without_db():
      with raises(ValueError) as err:
        _ = (
          NcbiBlast()
            .set_program(NcbiProgram.BLASTN)
            .build()
        )
      assert "No database specified" in str(err.value)
    def _with_wrong_megablast():
      with raises(ValueError) as err:
        _ = (
          NcbiBlast()
            .set_database(NcbiDatabase.NR)
            .set_megablast()
            .set_program(NcbiProgram.BLASTP)
            .build()
        )
      assert "Megablast can only be set with blastn program" in str(err.value)
    _with_all_data()
    _without_db()
    _with_wrong_megablast()

  @pytest.mark.requires_connection
  def test_query(self):
    """
    Tests query method
    """
    ncbi = (
      NcbiBlast()
        .set_program(NcbiProgram.BLASTN)
        .set_database(NcbiDatabase.NT)
        .build()
    )
    query_sec = (
      "CAGACTTTGAGGAGGCAATTTTCTCCAAGTACGTGGGTAACAAAATTATTGAAGTGGATGAGTACATGAA"
      "AGAGGCAGTAGACCACTATGCTGGCCAGCTCATGTCACTAGACATCAACACAGAACAAATGTGCTTGGAG"
      "GATGCCATGTATGGCACTGATGGTCTAGAAGCACTTGATT"
    )
    rid, rtoe = ncbi.query(query_sec)
    print(rid)
    assert isinstance(rid, str)
    assert isinstance(rtoe, str)
    assert len(rid)>=5

  @pytest.mark.requires_connection
  def test_check_status(self):
    """
    Test Check status method.
    """
    def _with_unknown_rid():
      rid = 'sdgfsdfgsdfg'
      status = NcbiBlast.job_is_ready(rid)
      assert not status
    _with_unknown_rid()

  @pytest.mark.requires_connection
  def test_full_call_pipeline(self, test_data_folder: str):
    """
    Test the full pipeline to make a Blast to NCBI servers.
    """
    ncbi = (
      NcbiBlast()
        .set_program(NcbiProgram.BLASTN)
        .set_database(NcbiDatabase.NT)
        .build()
    )
    query_sec = (
      "CAGACTTTGAGGAGGCAATTTTCTCCAAGTACGTGGGTAACAAAATTATTGAAGTGGATGAGTACATGAA"
      "AGAGGCAGTAGACCACTATGCTGGCCAGCTCATGTCACTAGACATCAACACAGAACAAATGTGCTTGGAG"
      "GATGCCATGTATGGCACTGATGGTCTAGAAGCACTTGATT"
    )
    ncbi.query(query_sec)
    result = ncbi.wait_until_finnish(max_time=10)
    assert result
    assert len(ncbi.get_output_buffer()) > 0
    outfile = os.path.join(
      test_data_folder,
      "blast_results.zip"
    )
    bytes_written = ncbi.write_results(outfile)
    assert bytes_written > 0
    if os.path.exists(outfile):
      os.remove(outfile)


@pytest.fixture
def blast_output(test_data_folder):
  """
  Creates a blast output for testing.
  """
  json_test_file = os.path.join(
    test_data_folder,
    "blast_result.json"
  )
  return BlastOutput.from_json(json_test_file)


class TestBlastOutput2:
  """
  Test BlastOutput2 class.
  """
  # pylint: disable=redefined-outer-name
  def test_from_json(self, blast_output:Any):
    """
    Test from_json static method.
    """
    assert isinstance(blast_output, BlastOutput)

  def test_report(self, blast_output:BlastOutput):
    """
    Test BlastReport class"""
    report = blast_output.report
    assert isinstance(report, BlastReport)
    assert report.program == "blastn"
    assert report.version == "BLASTN 2.14.0+"
    assert report.reference == (
      "Stephen F. Altschul, Thomas L. Madden, Alejandro A. Sch&auml;ffer, "
      "Jinghui Zhang, Zheng Zhang, Webb Miller, and David J. Lipman (1997), "
      "\"Gapped BLAST and PSI-BLAST: a new generation of protein database "
      "search programs\", Nucleic Acids Res. 25:3389-3402."
    )

  def test_params(self, blast_output:BlastOutput):
    """
    Test BlastParams class.
    """
    params = blast_output.report.params
    assert isinstance(params, BlastParams)
    assert params.expect == 10
    assert params.sc_match == 2
    assert params.sc_mismatch == -3
    assert params.gap_open == 5
    assert params.gap_extend == 2
    assert params.filter == "L;m;"

  def test_results(self, blast_output:BlastOutput):
    """
    Test BlastResults class"""
    results = blast_output.results
    assert isinstance(results, BlastResults)
    assert len(results.hits) == 1

  def test_hit(self, blast_output: BlastOutput):
    """
    Test BlastHit class"""
    hit = blast_output.results.hits[0]
    assert isinstance(hit, BlastHit)
    assert hit.num == 1
    assert len(hit.description) == 1
    assert hit.description[0].identifier == "gi|331376|gb|M64452.1|LCVPOLD"
    assert hit.description[0].accession == "M64452"
    assert hit.description[0].title == (
      "Lymphocytic choriomeningitis virus polymerase gene, partial cds"
    )
    assert hit.description[0].taxid == 11623
    assert hit.description[0].sciname == (
      "Lymphocytic choriomeningitis mammarenavirus"
    )
    assert hit.len == 210
    assert len(hit.hsps) == 1

  def test_stats(self, blast_output:BlastOutput):
    """
    Test BlastStats class"""
    stats = blast_output.results.stat
    assert isinstance(stats, BlastStats)
    assert stats.db_num == 91732311
    assert stats.db_len == 1076183408570
    assert stats.hsp_len == 38
    assert stats.eff_space == 184503983889344
    assert stats.kappa == 0.41
    assert stats.lambda_ == 0.625
    assert stats.entropy == 0.78
