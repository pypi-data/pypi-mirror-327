"""
  Test the read_results module functions
"""
from os.path import join

from pytest import approx, fixture

from xi_covutils.read_results import (
  from_ccmpred,
  from_gauss_dca,
  from_mitos_mi,
  inter_covariation,
  intra_covariation,
  merge,
  remap_paired,
  remap_tuple_positions,
  remove_trivial_tuple,
  to_tuple_positions
)

#pylint: disable=redefined-outer-name
@fixture(scope="module")
def paired_cov_data():
  """
  Fixture with paired covariation data
  """
  yield {
    (('A', 1), ('A', 2)): 0.1,
    (('A', 1), ('A', 5)): 0.2,
    (('A', 1), ('A', 6)): 0.3,
    (('A', 1), ('B', 2)): 0.4,
    (('A', 1), ('B', 3)): 0.5,
    (('A', 1), ('B', 4)): 0.6,
    (('A', 1), ('B', 5)): 0.7,
    (('A', 1), ('B', 6)): 0.8,
    (('B', 2), ('B', 1)): 0.9,
    (('B', 5), ('B', 1)): 0.10,
    (('B', 6), ('B', 1)): 0.11,
    (('C', 1), ('B', 1)): 0.12,
  }

def test_from_ccmpred(test_data_folder):
  """
  Test from_ccmpred function in a simple scenario where nothing can go wrong.
  """
  cov_file = join(test_data_folder, "cmmpred_results_01")
  scores = from_ccmpred(cov_file)
  assert scores[(1, 1)] == 0
  assert scores[(1, 2)] == 1
  assert scores[(1, 3)] == 0.5
  assert scores[(1, 4)] == 0.25
  assert scores[(1, 5)] == 1
  assert scores[(2, 2)] == 0
  assert scores[(2, 3)] == 0.55
  assert scores[(2, 4)] == 0.45
  assert scores[(2, 5)] == 0.1
  assert scores[(3, 3)] == 0
  assert scores[(3, 4)] == 0.15
  assert scores[(3, 5)] == 0.6
  assert scores[(4, 4)] == 0
  assert scores[(4, 5)] == 0.25
  assert scores[(5, 5)] == 0
  assert not scores.get((2, 1))

def test_remap_paired(test_data_folder):
  """
  Test remap_paired function.
  MSA has 7 columns, the first 3 are from chain 'A', the remaining 4 are from
  chain 'B'.
  The reference sequence is '-AB-CDE'
  """
  cov_file = join(test_data_folder, "cmmpred_results_01")
  msa_file = join(test_data_folder, "msa_01.fasta")
  new_scores = remap_paired(from_ccmpred(cov_file), msa_file, 3, 'A', 'B')
  assert new_scores[(('A', 1), ('A', 1))] == 0
  assert new_scores[(('A', 1), ('A', 2))] == 1
  assert new_scores[(('A', 1), ('B', 1))] == 0.5
  assert new_scores[(('A', 1), ('B', 2))] == 0.25
  assert new_scores[(('A', 1), ('B', 3))] == 1
  assert new_scores[(('A', 2), ('A', 2))] == 0
  assert new_scores[(('A', 2), ('B', 1))] == 0.55
  assert new_scores[(('A', 2), ('B', 2))] == 0.45
  assert new_scores[(('A', 2), ('B', 3))] == 0.1
  assert new_scores[(('B', 1), ('B', 1))] == 0
  assert new_scores[(('B', 1), ('B', 2))] == 0.15
  assert new_scores[(('B', 1), ('B', 3))] == 0.6
  assert new_scores[(('B', 2), ('B', 2))] == 0
  assert new_scores[(('B', 2), ('B', 3))] == 0.25
  assert new_scores[(('B', 3), ('B', 3))] == 0

def test_remap_paired_no_msa(test_data_folder):
  """
  MSA has 7 columns, the first 3 are from chain 'A', the remaining 4 are from
  chain 'B'.
  """
  cov_file = join(test_data_folder, "cmmpred_results_01")
  new_scores = remap_paired(from_ccmpred(cov_file), None, 3, 'A', 'B')
  assert new_scores[(('A', 1), ('A', 1))] == 0
  assert new_scores[(('A', 1), ('A', 2))] == 1
  assert new_scores[(('A', 1), ('A', 3))] == 0.5
  assert new_scores[(('A', 1), ('B', 1))] == 0.25
  assert new_scores[(('A', 1), ('B', 2))] == 1
  assert new_scores[(('A', 2), ('A', 2))] == 0
  assert new_scores[(('A', 2), ('A', 3))] == 0.55
  assert new_scores[(('A', 2), ('B', 1))] == 0.45
  assert new_scores[(('A', 2), ('B', 2))] == 0.1
  assert new_scores[(('A', 3), ('A', 3))] == 0
  assert new_scores[(('A', 3), ('B', 1))] == 0.15
  assert new_scores[(('A', 3), ('B', 2))] == 0.6
  assert new_scores[(('B', 1), ('B', 1))] == 0
  assert new_scores[(('B', 1), ('B', 2))] == 0.25
  assert new_scores[(('B', 2), ('B', 2))] == 0

def test_to_tuple_positions(test_data_folder):
  """
  Test to_tuple_positions method with simple data.
  """
  cov_file = join(test_data_folder, "cmmpred_results_01")
  new_scores = to_tuple_positions(from_ccmpred(cov_file), 'A')
  assert new_scores[(('A', 1), ('A', 1))] == 0
  assert new_scores[(('A', 1), ('A', 2))] == 1
  assert new_scores[(('A', 1), ('A', 3))] == 0.5
  assert new_scores[(('A', 1), ('A', 4))] == 0.25
  assert new_scores[(('A', 1), ('A', 5))] == 1
  assert new_scores[(('A', 2), ('A', 2))] == 0
  assert new_scores[(('A', 2), ('A', 3))] == 0.55
  assert new_scores[(('A', 2), ('A', 4))] == 0.45
  assert new_scores[(('A', 2), ('A', 5))] == 0.1
  assert new_scores[(('A', 3), ('A', 3))] == 0
  assert new_scores[(('A', 3), ('A', 4))] == 0.15
  assert new_scores[(('A', 3), ('A', 5))] == 0.6
  assert new_scores[(('A', 4), ('A', 4))] == 0
  assert new_scores[(('A', 4), ('A', 5))] == 0.25
  assert new_scores[(('A', 5), ('A', 5))] == 0


def test_remap_tuple_positions(test_data_folder):
  """
  Test remap_tuple_positions function with simple data.
  """
  cov_file = join(test_data_folder, "cmmpred_results_01")
  msa_file = join(test_data_folder, "msa_01.fasta")
  new_scores = remap_paired(from_ccmpred(cov_file), msa_file, 3, 'A', 'B')
  mapping = {
    'A':{1:11, 2:12},
    'B':{1:21, 2:22, 3:23}
  }
  new_scores = remap_tuple_positions(new_scores, mapping)
  assert new_scores[(('A', 11), ('A', 11))] == 0
  assert new_scores[(('A', 11), ('A', 12))] == 1
  assert new_scores[(('A', 11), ('B', 21))] == 0.5
  assert new_scores[(('A', 11), ('B', 22))] == 0.25
  assert new_scores[(('A', 11), ('B', 23))] == 1
  assert new_scores[(('A', 12), ('A', 12))] == 0
  assert new_scores[(('A', 12), ('B', 21))] == 0.55
  assert new_scores[(('A', 12), ('B', 22))] == 0.45
  assert new_scores[(('A', 12), ('B', 23))] == 0.1
  assert new_scores[(('B', 21), ('B', 21))] == 0
  assert new_scores[(('B', 21), ('B', 22))] == 0.15
  assert new_scores[(('B', 21), ('B', 23))] == 0.6
  assert new_scores[(('B', 22), ('B', 22))] == 0
  assert new_scores[(('B', 22), ('B', 23))] == 0.25
  assert new_scores[(('B', 23), ('B', 23))] == 0

def test_remove_trivial_tuple(paired_cov_data):
  """
  Test remove_trivial_tuple function.

  """
  assert (('A', 1), ('A', 2)) in paired_cov_data
  assert (('A', 1), ('A', 5)) in paired_cov_data
  assert (('B', 2), ('B', 1)) in paired_cov_data
  assert (('B', 5), ('B', 1)) in paired_cov_data
  new_scores = remove_trivial_tuple(paired_cov_data)
  assert len(new_scores) == 8
  assert new_scores[(('A', 1), ('A', 6))] == 0.3
  assert new_scores[(('A', 1), ('B', 2))] == 0.4
  assert new_scores[(('A', 1), ('B', 3))] == 0.5
  assert new_scores[(('A', 1), ('B', 4))] == 0.6
  assert new_scores[(('A', 1), ('B', 5))] == 0.7
  assert new_scores[(('A', 1), ('B', 6))] == 0.8
  assert new_scores[(('B', 6), ('B', 1))] == 0.11
  assert new_scores[(('C', 1), ('B', 1))] == 0.12
  assert (('A', 1), ('A', 2)) not in new_scores
  assert (('A', 1), ('A', 5)) not in new_scores
  assert (('B', 2), ('B', 1)) not in new_scores
  assert (('B', 5), ('B', 1)) not in new_scores

def test_intra_covariation(paired_cov_data):
  """
  Test intra_covariation function.
  """
  new_scores = intra_covariation(paired_cov_data)
  assert len(new_scores) == 3
  assert "A" in new_scores and "B" in new_scores and "C" in new_scores
  assert len(new_scores["A"]) == 3
  assert len(new_scores["B"]) == 3
  assert not new_scores["C"]
  assert new_scores["A"][(('A', 1), ('A', 2))] == 0.1
  assert new_scores["A"][(('A', 1), ('A', 5))] == 0.2
  assert new_scores["A"][(('A', 1), ('A', 6))] == 0.3
  assert new_scores["B"][(('B', 2), ('B', 1))] == 0.9
  assert new_scores["B"][(('B', 5), ('B', 1))] == 0.10
  assert new_scores["B"][(('B', 6), ('B', 1))] == 0.11

def test_inter_covariation(paired_cov_data):
  """
  Test inter_covariation function.
  """
  new_scores = inter_covariation(paired_cov_data)
  assert len(new_scores) == 2
  assert ("A", "B") in new_scores and ("B", "C") in new_scores
  assert len(new_scores[("A", "B")]) == 5
  assert new_scores[("A", "B")][(('A', 1), ('B', 2))] == 0.4
  assert new_scores[("A", "B")][(('A', 1), ('B', 3))] == 0.5
  assert new_scores[("A", "B")][(('A', 1), ('B', 4))] == 0.6
  assert new_scores[("A", "B")][(('A', 1), ('B', 5))] == 0.7
  assert new_scores[("A", "B")][(('A', 1), ('B', 6))] == 0.8
  assert new_scores[("A", "B")][(('A', 1), ('B', 6))] == 0.8
  assert len(new_scores[("B", "C")]) == 1
  assert new_scores[("B", "C")][(('B', 1), ('C', 1))] == 0.12

def test_merge(paired_cov_data):
  """
  Test merge function.
  """
  new_scores = intra_covariation(paired_cov_data)
  merged_scores = merge(new_scores.values())
  assert len(merged_scores) == 6
  assert merged_scores[(('A', 1), ('A', 2))] == 0.1
  assert merged_scores[(('A', 1), ('A', 5))] == 0.2
  assert merged_scores[(('A', 1), ('A', 6))] == 0.3
  assert merged_scores[(('B', 2), ('B', 1))] == 0.9
  assert merged_scores[(('B', 5), ('B', 1))] == 0.10
  assert merged_scores[(('B', 6), ('B', 1))] == 0.11

def test_from_mitos_mi(test_data_folder):
  """
  Test reading Mutual information results given by MIToS package.
  """
  cov_file = join(test_data_folder, "mi_results_01")
  scores = from_mitos_mi(cov_file)
  assert scores[(1, 2)] == approx(-2.571201029577921)
  assert scores[(1, 17)] == approx(-0.7178613770512343)
  assert not scores.get((2, 1))
  assert len(scores) == 21

def test_from_gauss_dca(test_data_folder):
  """
  Test reading Gauss DCA results.
  """
  cov_file = join(test_data_folder, "gauss_results_01")
  scores = from_gauss_dca(cov_file)
  assert scores[(4, 5)] == approx(1.037925)
  assert scores[(79, 84)] == approx(1.019366)
  assert not scores.get((5, 4))
  assert len(scores) == 30
