"""
Test PSSM creatin form MSA data.
"""

from typing import Dict
from pytest import approx
from xi_covutils.msa._pssm import (
  normalize_dna, normalize_rna, normalize_protein,
  build_dna_pssm, build_rna_pssm, build_protein_pssm,
  filter_pssm_by_freq, filter_pssm_max_freq
)

def test_normalize_dna():
  """Test normalize DNA function"""
  def test_with_ungapped_sequence():
    seq = "ATGHBNMXXNOPU"
    norm_seq = normalize_dna(seq)
    assert norm_seq == "ATGHBNMNNNNNT"
  def test_with_gapped_sequence():
    seq = "ATGHBNM--XXNOPU"
    norm_seq = normalize_dna(seq)
    assert norm_seq == "ATGHBNM--NNNNNT"
  test_with_ungapped_sequence()
  test_with_gapped_sequence()

def test_normalize_rna():
  """Test normalize RNA function"""
  def test_with_ungapped_sequence():
    seq = "ATGHBNMXXNOPU"
    norm_seq = normalize_rna(seq)
    assert norm_seq == "AUGHBNMNNNNNU"
  def test_with_gapped_sequence():
    seq = "ATGHBNM--XXNOPU"
    norm_seq = normalize_rna(seq)
    assert norm_seq == "AUGHBNM--NNNNNU"
  test_with_ungapped_sequence()
  test_with_gapped_sequence()

def test_normalize_protein():
  """Test normalize Protein function"""
  def test_with_ungapped_sequence():
    seq = "QWERTYZBXJ"
    norm_seq = normalize_protein(seq)
    assert norm_seq == "QWERTYXXXX"
  def test_with_gapped_sequence():
    seq = "QWERTY--ZBXJ"
    norm_seq = normalize_protein(seq)
    assert norm_seq == "QWERTY--XXXX"
  test_with_ungapped_sequence()
  test_with_gapped_sequence()

def test_build_dna_pssm():
  """
  Test build DNA PSSM
  """
  def test_simple_case():
    msa_data = ["A", "T", "C", "G"]
    pssm = build_dna_pssm(msa_data)
    assert pssm == [
      {"A": 0.25, "T": 0.25, "C": 0.25, "G": 0.25}
    ]
  def test_case_with_gaps():
    msa_data = ["A", "T", "C", "G", "-"]
    pssm = build_dna_pssm(msa_data)
    assert pssm == [
      {"A": 0.25, "T": 0.25, "C": 0.25, "G": 0.25}
    ]
  def test_case_with_deg_bases():
    msa_data = ["A", "T", "C", "W"]
    pssm = build_dna_pssm(msa_data)
    assert pssm == [
      {"A": (1.5)/4, "T": (1.5/4), "C": 0.25, "G": 0}
    ]
  def test_case_with_strange_chars():
    msa_data = ["A", "T", "C", "Q"]
    pssm = build_dna_pssm(msa_data)
    assert pssm == [
      {"A": (1.25)/4, "T": (1.25/4), "C": (1.25/4), "G": 0.25/4}
    ]
  def test_case_with_pseudo_freq():
    msa_data = ["A", "T", "C", "C"]
    pssm = build_dna_pssm(msa_data, pseudo_freq = 0.5)
    assert pssm == [
      {
        "A": ((1/4)+0.5)/3,
        "T": ((1/4)+0.5)/3,
        "C": ((2/4)+0.5)/3,
        "G": 0.5/3
      }
    ]
  test_simple_case()
  test_case_with_gaps()
  test_case_with_deg_bases()
  test_case_with_strange_chars()
  test_case_with_pseudo_freq()

def test_build_rna_pssm():
  """
  Test build RNA PSSM
  """
  def test_simple_case():
    msa_data = ["A", "U", "C", "G"]
    pssm = build_rna_pssm(msa_data)
    assert pssm == [
      {"A": 0.25, "U": 0.25, "C": 0.25, "G": 0.25}
    ]
  def test_case_with_gaps():
    msa_data = ["A", "T", "C", "G", "-"]
    pssm = build_rna_pssm(msa_data)
    assert pssm == [
      {"A": 0.25, "U": 0.25, "C": 0.25, "G": 0.25}
    ]
  def test_case_with_deg_bases():
    msa_data = ["A", "U", "C", "W"]
    pssm = build_rna_pssm(msa_data)
    assert pssm == [
      {"A": (1.5)/4, "U": (1.5/4), "C": 0.25, "G": 0}
    ]
  def test_case_with_strange_chars():
    msa_data = ["A", "U", "C", "Q"]
    pssm = build_rna_pssm(msa_data)
    assert pssm == [
      {"A": (1.25)/4, "U": (1.25/4), "C": (1.25/4), "G": 0.25/4}
    ]
  def test_case_with_pseudo_freq():
    msa_data = ["A", "U", "C", "C"]
    pssm = build_rna_pssm(msa_data, pseudo_freq = 0.5)
    assert pssm == [
      {
        "A": ((1/4)+0.5)/3,
        "U": ((1/4)+0.5)/3,
        "C": ((2/4)+0.5)/3,
        "G": 0.5/3
      }
    ]
  test_simple_case()
  test_case_with_gaps()
  test_case_with_deg_bases()
  test_case_with_strange_chars()
  test_case_with_pseudo_freq()

def test_build_protein_pssm():
  """
  Test build protein PSSM
  """
  def test_simple_case():
    msa_data = ["A", "V", "C", "G"]
    pssm = build_protein_pssm(msa_data)
    expected: Dict[str, float] = {
      c : 0
      for c in "QWERTYIPASDFGHKLCVNM"
    }
    update = {"A": 0.25, "V": 0.25, "C": 0.25, "G": 0.25}
    for k, val in update.items():
      expected[k] = val
    assert pssm == [expected]
  def test_case_with_gaps():
    msa_data = ["A", "T", "C", "G", "-"]
    pssm = build_protein_pssm(msa_data)
    expected: Dict[str, float] = {
      c : 0
      for c in "QWERTYIPASDFGHKLCVNM"
    }
    update = {"A": 0.25, "T": 0.25, "C": 0.25, "G": 0.25}
    for k, val in update.items():
      expected[k] = val
    assert pssm == [expected]
  def test_case_with_deg_bases():
    msa_data = ["A", "V", "C", "X"]
    pssm = build_protein_pssm(msa_data)
    expected: Dict[str, float] = {
      c : 0.0125
      for c in "QWERTYIPASDFGHKLCVNM"
    }
    update = {"A": 0.2625, "V": 0.2625, "C": 0.2625}
    for k, val in update.items():
      expected[k] = val
    assert pssm[0] == approx(expected)
  def test_case_with_pseudo_freq():
    msa_data = ["A", "V", "C"]
    pssm = build_protein_pssm(msa_data, pseudo_freq = 0.5)
    expected: Dict[str, float] = {
      c : 0.5/11
      for c in "QWERTYIPASDFGHKLCVNM"
    }
    update = {
        "A": ((1/3)+0.5)/11,
        "V": ((1/3)+0.5)/11,
        "C": ((1/3)+0.5)/11,
        "G": 0.5/11
      }
    for k, val in update.items():
      expected[k] = val
    assert pssm[0] == approx(expected)
  test_simple_case()
  test_case_with_gaps()
  test_case_with_deg_bases()
  test_case_with_pseudo_freq()

def test_filter_pssm_by_freq():
  """
  Test filter PSSM by minimum frequency
  """
  def test_simple_case():
    pssm = [{"A": 0.75, "C": 0.25, "T":0, "G":0}]
    pssm = filter_pssm_by_freq(pssm, min_freq=0.5)
    expected: Dict[str, float] = {"A" : 0.75}
    assert pssm == [expected]
  test_simple_case()


def test_filter_pssm_max_freq():
  """
  Test Filter PSSM to keep only the maximum frequency values.
  """
  pssm = [{"A": 0.4, "C": 0.4, "T":0.2, "G":0}]
  pssm = filter_pssm_max_freq(pssm)
  expected: Dict[str, float] = {"A" : 0.4, "C": 0.4}
  assert pssm == [expected]
