"""
Test BlastP wrapper class
"""
from io import StringIO
import os
from shutil import which
import pandas as pd
from pytest import mark, raises
from xi_covutils.blast.wrappers import BlastP, BlastResult

class TestBlastResult:
  """
  This class is used to test the BlastResult class methods. It contains unit
  tests that help in checking the correctness of different methods present in
  the BlastResult class such as from_tabular_with_headers and
  from_tabular_without_headers.
  """
  def test_from_tabular_with_headers_with_file(self, test_data_folder):
    """
    Tests from_tabular_with_headers method of BlastResult class by providing a
    file as input.
    """
    infile = os.path.join(test_data_folder, "blastp_result.txt")
    with open(infile, "r", encoding="utf-8") as fin:
      result = BlastResult.from_tabular_with_headers(fin)
      assert len(result.data) == 1
      assert len(result.headers) == 14
      expected_hit_data = [
        "Query_1", "Protein_4", 100.000, 16, 0, 0, 1, 16, 1, 16, 8.71e-09,
        33.5, 100, "N/A",
      ]
      assert result.data[0] == expected_hit_data
      expected_fields = [
        "query acc.ver", "subject acc.ver", "% identity", "alignment length",
        "mismatches", "gap opens", "q. start", "q. end", "s. start",
        "s. end", "evalue", "bit score", "% query coverage per subject",
        "subject tax id",
      ]
      assert result.headers == expected_fields

  def test_from_tabular_with_headers_with_string(self):
    """
    Tests from_tabular_with_headers method of BlastResult class by providing a
    string as input.
    """
    input_data = (
      "# BLASTP 2.10.0+\n"
      "# Query: \n"
      "# Database: User specified sequence set (Input: blastp_subject.fasta)\n"
      "# Fields: query acc.ver, subject acc.ver, % identity, alignment length, "
      "mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, "
      "bit score, % query coverage per subject, subject tax id\n"
      "# 1 hits found\n"
      "Query_1\tProtein_4\t100.000\t16\t0\t0\t1\t16\t"
      "1\t16\t8.71e-09\t33.5\t100\tN/A\n"
      "# BLAST processed 1 queries\n"
    )
    input_data = StringIO(input_data)
    result = BlastResult.from_tabular_with_headers(input_data)
    assert len(result.data) == 1
    assert len(result.headers) == 14
    expected_hit_data = [
      "Query_1", "Protein_4", 100.000, 16, 0, 0, 1, 16, 1, 16, 8.71e-09, 33.5,
      100, "N/A",
    ]
    assert result.data[0] == expected_hit_data
    expected_fields = [
      "query acc.ver", "subject acc.ver", "% identity", "alignment length",
      "mismatches", "gap opens", "q. start", "q. end", "s. start", "s. end",
      "evalue", "bit score", "% query coverage per subject", "subject tax id",
    ]
    assert result.headers == expected_fields

  def test_from_tabular_without_headers_with_string(self):
    """
    Tests from_tabular_without_headers method of BlastResult class by providing
    a string as input.
    """
    input_data = (
      "Query_1\tProtein_4\t100.000\t16\t0\t0\t1\t16\t"
      "1\t16\t8.71e-09\t33.5\t100\tN/A"
    )
    input_data = StringIO(input_data)
    result = BlastResult.from_tabular_without_headers(
      headers = [f"field_{x}" for x in range(14)],
      input_data = input_data
    )
    assert len(result.data) == 1
    assert len(result.headers) == 14
    expected_hit_data = [
      "Query_1", "Protein_4", 100.000, 16, 0, 0, 1, 16, 1, 16, 8.71e-09, 33.5,
      100, "N/A",
    ]
    assert result.data[0] == expected_hit_data
    expected_fields = [f"field_{x}" for x in range(14)]
    assert result.headers == expected_fields

  def test_from_tabular_without_headers_with_mixed_string(self):
    """
    Tests from_tabular_without_headers method of BlastResult class by providing
    a string as input. The subject and query ids contains spaces.
    """
    input_data = (
      "Query 1\tProtein 4\t100.000\t16\t0\t0\t1\t16\t"
      "1\t16\t8.71e-09\t33.5\t100\tN/A"
    )
    input_data = StringIO(input_data)
    result = BlastResult.from_tabular_without_headers(
      headers = [f"field_{x}" for x in range(14)],
      input_data = input_data
    )
    assert len(result.data) == 1
    assert len(result.headers) == 14
    expected_hit_data = [
      "Query 1", "Protein 4", 100.000, 16, 0, 0, 1, 16, 1, 16, 8.71e-09, 33.5,
      100, "N/A",
    ]
    assert result.data[0] == expected_hit_data
    expected_fields = [f"field_{x}" for x in range(14)]
    assert result.headers == expected_fields

  def test_as_dataframe(self):
    input_data = (
      "Query_1\tProtein_4\t100.000\t16\t0\t0\t1\t16\t"
      "1\t16\t8.71e-09\t33.5\t100\tN/A"
    )
    input_data = StringIO(input_data)
    result = BlastResult.from_tabular_without_headers(
      headers = [f"field_{x}" for x in range(14)],
      input_data = input_data
    )
    df = result.as_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 14)
    assert len(df) == 1
    assert df["field_0"].iloc[0] == "Query_1"

  def test_exclude_with_one_match(self):
    """
    Test exclude method.
    """
    input_data = (
      "Query_1\tProtein_4\t100.000\t16\t0\t0\t1\t16\t"
      "1\t16\t8.71e-09\t33.5\t100\tN/A"
    )
    input_data = StringIO(input_data)
    result = BlastResult.from_tabular_without_headers(
      headers = [f"field_{x}" for x in range(14)],
      input_data = input_data
    )
    new_results = result.exclude("field_0", {"Query_1"})
    assert len(new_results) == 0

  def test_exclude_with_wrong_header(self):
    """
    Test exclude method passing a wrong header.
    """
    input_data = (
      "Query_1\tProtein_4\t100.000\t16\t0\t0\t1\t16\t"
      "1\t16\t8.71e-09\t33.5\t100\tN/A"
    )
    input_data = StringIO(input_data)
    result = BlastResult.from_tabular_without_headers(
      headers = [f"field_{x}" for x in range(14)],
      input_data = input_data
    )
    new_results = result.exclude("field_Non_exising", {"Query_1"})
    assert len(new_results) == 1

  def test_exclude_with_no_matches(self):
    """
    Test exclude method with a set of values that are not present in the
    BlastResult header.
    """
    input_data = (
      "Query_1\tProtein_4\t100.000\t16\t0\t0\t1\t16\t"
      "1\t16\t8.71e-09\t33.5\t100\tN/A"
    )
    input_data = StringIO(input_data)
    result = BlastResult.from_tabular_without_headers(
      headers = [f"field_{x}" for x in range(14)],
      input_data = input_data
    )
    new_results = result.exclude("field_0", {"Query_2"})
    assert len(new_results) == 1

class TestBlastWrapper:
  """
  This class is used to test the BlastP wrapper class. It contains unit tests
  that check the correctness of different methods present in the BlastP class
  such as creation, running command, specifying output fields, etc.
  """
  def test_creation_with_no_args(self):
    """
    Tests the creation of BlastP object with no arguments.
    """
    blastp = BlastP()
    assert not blastp.args
    assert isinstance(blastp.args, list)
    assert blastp.command == "blastp"
    assert blastp.evalue == 1E-5
    assert blastp.fields == ['std']
    assert not blastp.database
    assert not blastp.subject
    assert not blastp.outfile
    assert not blastp.query
    assert not blastp.query_string

  def test_running_commmand_fails_with_no_db_and_not_subject(self):
    """
    Tests whether running a command fails when no database and subject is
    provided.
    """
    blastp = (
      BlastP()
        .with_query("query.fasta")
    )
    with raises(ValueError) as err:
      _ = blastp.running_command()
    assert "db" in str(err)
    assert "subject" in str(err)

  def test_running_commmand_fails_with_db_and_subject(self):
    """
    Tests whether running a command fails when both database and subject are
    provided.
    """
    blastp = (
      BlastP()
        .with_db("nt")
        .with_subject("subject.fasta")
    )
    with raises(ValueError) as err:
      _ = blastp.running_command()
    assert "db" in str(err)
    assert "subject" in str(err)

  def test_running_commmand_fails_with_not_query_and_not_querystring(self):
    """
    Tests whether running a command fails when neither a query nor a query
    string is provided.
    """
    blastp = (
      BlastP()
        .with_db("nt")
    )
    with raises(ValueError) as err:
      _ = blastp.running_command()
    assert "query" in str(err)
    assert "query_string" in str(err)

  def test_running_command_requires_a_query_and_a_target_to_succeed(self):
    """
    Tests whether running a command requires both a query and a target.
    """
    blastp = (
      BlastP()
        .with_db("nt")
        .with_query("a.fasta")
    )
    cmd = blastp.running_command()
    assert "-query" in cmd
    assert "-db" in cmd
    assert "blastp"  in cmd
    assert "-outfmt" in cmd
    blastp = (
      BlastP()
        .with_subject("subject.fast")
        .with_query_string("MGQKKLN")
    )
    cmd = blastp.running_command()
    assert "-query" in cmd
    assert "-" in cmd
    assert "-subject" in cmd
    assert "blastp"  in cmd
    assert "-outfmt" in cmd
    assert "7 std" in cmd
    assert "-evalue" in cmd
    assert "1e-05" in cmd

  def test_running_command_without_outfile(self):
    """
    Tests the running command when no output file is provided.
    """
    blastp = (
      BlastP()
        .with_subject("subject.fast")
        .with_query_string("MGQKKLN")
    )
    cmd = blastp.running_command()
    assert "-outfile" not in cmd

  def test_running_command_with_outfile(self):
    """
    Tests the running command when an output file is provided.
    """
    blastp = (
      BlastP()
        .with_subject("subject.fast")
        .with_query_string("MGQKKLN")
        .with_output_file("result.txt")
    )
    cmd = blastp.running_command()
    assert "-outfile" not in cmd

  def test_running_command_with_output_fields(self):
    """
    Tests the running command with the specification of output fields.
    """
    blastp = (
      BlastP()
        .with_subject("subject.fast")
        .with_query_string("MGQKKLN")
        .with_output_file("result.txt")
        .with_output_fields_std()
    )
    cmd = blastp.running_command()
    assert "7 std" in cmd
    blastp = (
      BlastP()
        .with_subject("subject.fast")
        .with_query_string("MGQKKLN")
        .with_output_file("result.txt")
        .with_output_fields_std_plus(["qcovs"])
    )
    cmd = blastp.running_command()
    assert "7 std qcovs" in cmd
    blastp = (
      BlastP()
        .with_subject("subject.fast")
        .with_query_string("MGQKKLN")
        .with_output_file("result.txt")
        .with_output_fields(["qcovs", "staxid"])
    )
    cmd = blastp.running_command()
    assert "7 qcovs staxid" in cmd
    blastp = (
      BlastP()
        .with_subject("subject.fast")
        .with_query_string("MGQKKLN")
        .with_output_file("result.txt")
        .with_output_fields_recommended()
    )
    cmd = blastp.running_command()
    assert "7 std qcovs staxid" in cmd

  def test_running_command_with_extra_arguments(self):
    """
    Tests the running command with extra arguments.
    """
    blastp = (
      BlastP()
        .with_subject("subject.fast")
        .with_query_string("MGQKKLN")
        .with_output_file("result.txt")
        .with_output_fields_recommended()
        .with_arguments("-subject_besthit", "-best_hit_score_edge", 0.1)
    )
    cmd = blastp.running_command()
    assert "-subject_besthit" in cmd
    assert "-best_hit_score_edge" in cmd
    assert "0.1" in cmd

  @mark.skipif(
    not which("blastp"),
    reason="blastp should be accessible in PATH"
  )
  def test_run_with_input_query_string_and_standard_output(
      self,
      test_data_folder
    ):
    """
    Tests the run method with an input query string and checks if it produces a
    standard output.
    """
    subject_file = os.path.join(test_data_folder, "blastp_subject.fasta")
    blastp = (
      BlastP()
        .with_subject(subject_file)
        .with_query_string("MSTNSYLRLSPKSKLR")
        .with_output_fields_recommended()
        .with_arguments("-subject_besthit", "-best_hit_score_edge", 0.1)
    )
    print(blastp.running_command_string())
    result, error = blastp.run()
    assert result is not None
    print(result)
    print(error)
    assert len(result)==1
