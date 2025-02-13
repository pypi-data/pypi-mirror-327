import os

from xi_covutils.fastafilter import (
  CollectToFile,
  FastaSeqIteratorFromFile,
  FilterBuilder,
  RuleDescriptionContains,
  RuleRegexMatch
)

class TestFastaSeqIteratorFromFile():
  def test_simple_input_file(self, test_data_folder):
    msa_file = os.path.join(
      test_data_folder,
      "msa_01.fasta"
    )
    iterator = (
      FastaSeqIteratorFromFile()
        .set_file(msa_file)
        .iterator()
    )
    seqs = {seq[0]: seq[1] for seq in iterator}
    assert seqs == {
      "seq1": "-AB-CDE",
      "seq2": "xAByCDE",
      "seq3": "xAByCDE",
      "seq4": "xAByCDE"
    }
  def test_without_file(self):
    iterator = (
      FastaSeqIteratorFromFile()
        .iterator()
    )
    seqs = {seq[0]: seq[1] for seq in iterator}
    assert seqs == {}

class TestCollectToFile():
  def test_simple_output(self, test_data_folder):
    outfile = os.path.join(test_data_folder, "temp.file")
    if os.path.exists(outfile):
      os.remove(outfile)
    sequences = [
      ("s1", "AAA"),
      ("s2", "CCC"),
      ("s3", "DDD")
    ]
    collector = CollectToFile(outfile)
    for desc, seq in sequences:
      collector.receive((desc, seq))
    assert collector.result() is None
    with open(outfile, "r", encoding="utf-8") as f_in:
      content = [line.strip() for line in f_in]
    assert content == [">s1", "AAA", ">s2", "CCC", ">s3", "DDD"]
    if os.path.exists(outfile):
      os.remove(outfile)

class TestRuleDescriptionContains():
  def test_simple_case(self):
    case1 = ("Seq1 Description 1", "ADSASD")
    case2 = ("Seq2 Description 2, Not Valid", "ADASD")
    rule = RuleDescriptionContains().query("Not Valid")
    assert not rule.filter(case1)
    assert rule.filter(case2)

class TestFilterBuilder:
  def test_full_case(self, test_data_folder):
    infile = os.path.join(
      test_data_folder,
      "msa_01.fasta"
    )
    c_filter = (
      FilterBuilder()
        .with_infile(infile)
        .to_outlist()
        .add_rule(RuleDescriptionContains().query("seq1"))
        .build()
    )
    assert c_filter is not None
    result = c_filter.filter()
    assert result == [("seq1", "-AB-CDE")]

class TestRuleRegexMatch:
  def test_rule(self):
    query = "AC[^G]TTT"
    case1 = ("seq1", "ACXTTTTT")
    case2 = ("seq2", "ASDASDACMTTTXXX")
    case3 = ("seq3", "ACGTTT")
    rule = RuleRegexMatch().query(query)
    assert rule.filter(case1)
    assert rule.filter(case2)
    assert not rule.filter(case3)

class TestRuleIUPACMatch:
  def test_rule(self):
    query = "AC[^G]TTT"
    case1 = ("seq1", "ACXTTTTT")
    case2 = ("seq2", "ASDASDACMTTTXXX")
    case3 = ("seq3", "ACGTTT")
    rule = RuleRegexMatch().query(query)
    assert rule.filter(case1)
    assert rule.filter(case2)
    assert not rule.filter(case3)
