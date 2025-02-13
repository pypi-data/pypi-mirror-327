"""
Test functions to generate patterns and consensus from MSA data.
"""
from xi_covutils.msa._patterns import build_rna_pattern, build_dna_consensus

def test_build_rna_pattern():
  """
  Test building RNA patterns
  """
  def test_simple_pattern():
    msa_data = [
      "ATG",
      "ATM",
      "AGG"
    ]
    obs = build_rna_pattern(msa_data)
    expected = "A[GU][ACG]"
    assert obs == expected
  def test_pattern_with_min_frq():
    msa_data = [
      "ATG",
      "ATM",
      "AGG"
    ]
    obs = build_rna_pattern(msa_data, min_freq = 0.4)
    expected = "AUG"
    assert obs == expected
  test_simple_pattern()
  test_pattern_with_min_frq()

def test_build_dna_consensus():
  """
  Test Building Consensus sequence from MSA data
  """
  def test_simple_consensus():
    msa_data = [
      "ATG",
      "ATM",
      "AGG"
    ]
    obs = build_dna_consensus(msa_data)
    expected = "ATG"
    assert obs == expected
  def test_with_ties():
    msa_data = [
      "ATW",
      "ATW",
      "TGH",
      "TCG",
    ]
    obs = build_dna_consensus(msa_data)
    expected = "WTW"
    assert obs == expected
  test_simple_consensus()
  test_with_ties()
