"""
  Test ROC functions
"""

from pytest import approx
from pytest import raises
from xi_covutils.roc import curve
from xi_covutils.roc import auc
from xi_covutils.roc import auc_n
from xi_covutils.roc import simplify
from xi_covutils.roc import curve_to_str
from xi_covutils.roc import merge_scores_and_distances
from xi_covutils.roc import binary_from_merged
from xi_covutils.distances import Distances

def test_curve_with_roc():
  """
  Test that the curves created by curve function are correct
  """
  with raises(ValueError) as err:
    binary_result = [True, True, True, True, True]
    curve_r = curve(binary_result)
    assert "Binary should have both False and True values." in str(err)

  with raises(ValueError) as err:
    binary_result = [False, False, False, False, False]
    curve_r = curve(binary_result)
    assert "Binary should have both False and True values." in str(err)

  binary_result = [False, True, False, True, False, False]
  curve_r = curve(binary_result)
  assert curve_r == [
    (0, 0), (0.25, 0), (0.25, 0.5), (0.5, 0.5), (0.5, 1), (0.75, 1), (1, 1)
  ]

  binary_result = []
  with raises(ValueError) as err:
    assert curve(binary_result)
    assert str(err).startswith("Can not create a curve")


def test_auc():
  """
  Test that the AUC values are correct
  """
  binary_result = [True, True, True, True, True, False]
  curve_r = curve(binary_result)
  curve_simple = simplify(curve_r)
  auc_value = auc(curve_r)
  auc_value_simple = auc(curve_simple)
  assert auc_value == 1
  assert auc_value_simple == 1

  binary_result = [False, False, False, False, False, True]
  curve_r = curve(binary_result)
  curve_simple = simplify(curve_r)
  auc_value = auc(curve_r)
  auc_value_simple = auc(curve_simple)
  assert auc_value == 0
  assert auc_value_simple == 0

  binary_result = [False, True, False, True, False, False]
  curve_r = curve(binary_result)
  curve_simple = simplify(curve_r)
  auc_value = auc(curve_r)
  auc_value_simple = auc(curve_simple)
  assert auc_value == float(5)/8
  assert auc_value_simple == float(5)/8

def test_auc_n():
  """
  Test auc_n function.
  """
  curve_r = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]
  auc_result = auc_n(curve_r)
  assert auc_result == 0

  curve_r = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0)]
  auc_result = auc_n(curve_r)
  assert auc_result == 0.05

  binary_result = [False, True]
  curve_r = curve(binary_result)
  auc_result = auc_n(curve_r)
  assert auc_result == 0.0

  binary_result = [True, False]
  curve_r = curve(binary_result)
  auc_result = auc_n(curve_r)
  assert auc_result == 0.05

  binary_result = [True]*10 + [False]*90
  curve_r = curve(binary_result)
  auc_result = auc_n(curve_r)
  assert auc_result == 0.05

  binary_result = [False] + [True]*9 + [False]*90
  curve_r = curve(binary_result)
  auc_result = auc_n(curve_r)
  # Note: 0.05 is the default pfr limit,
  # 91 is the total number of negatives
  # The result is the area of a rectangle:
  # Rect 1 : H=1 x W=(0.05-1/91)
  assert auc_result == approx(0.05 - float(1)/91)

  binary_result = [True] + [False] + [True]*8 + [False]*90
  curve_r = curve(binary_result)
  auc_result = auc_n(curve_r)
  # Note: 0.05 is the default pfr limit,
  # 91 is the total number of negatives
  # 9 is the total number of positives
  # The result is the sum of the area of two rectangles:
  # Rect 1 : H=1/9 x W=(1/91)
  # Rect 2 : H=1 x W=(0.05-1/91)
  assert auc_result == approx(0.05 - float(1)/91 + float(1)/91 * float(1)/9)

def test_simplify():
  """
  Test that simplify method creates smaller curves
  """
  curve1 = [(0, 0), (0, 0.2), (0, 0.5), (0.5, 0.5), (0.75, 0.5), (1, 0.5)]
  simple_curve = simplify(curve1)
  assert simple_curve == [(0, 0), (0, 0.5), (1, 0.5)]

def test_curve_to_str():
  """
  Test that curves are converted to text correctly
  """
  curve_r = [(0, 0), (0.2, 0), (0.4, 0), (0.6, 0), (0.8, 0), (1, 0), (1, 1)]
  curve_s = curve_to_str(curve_r)
  assert curve_s == "0, 0\n0.2, 0\n0.4, 0\n0.6, 0\n0.8, 0\n1, 0\n1, 1"

def test_merges_scores_dist():
  """
  Test that merge_scores_and_distances correctly merges scores and distances.
  """
  dist_elems = [
    ('A', 1, 'A', 2, 6.01),
    ('A', 1, 'A', 3, 6.02),
    ('A', 1, 'A', 4, 6.13),
    ('A', 2, 'A', 3, 6.24),
    ('A', 2, 'A', 4, 6.35),
  ]
  distances = Distances(dist_elems)
  scores = {
    (('A', 1), ('A', 2)) : 0.11,
    (('A', 1), ('A', 3)) : 0.12,
    (('A', 1), ('A', 4)) : 0.13,
    (('A', 2), ('A', 3)) : 0.14,
    (('A', 2), ('A', 4)) : 0.15,
    (('A', 3), ('A', 4)) : 0.16,
  }
  merged = merge_scores_and_distances(scores, distances)
  assert len(merged) == 5
  assert (0.11, True) in merged
  assert (0.12, True) in merged
  assert (0.13, False) in merged
  assert (0.14, False) in merged
  assert (0.15, False) in merged

  merged = merge_scores_and_distances(scores, distances, distance_cutoff=6.30)
  assert len(merged) == 5
  assert (0.11, True) in merged
  assert (0.12, True) in merged
  assert (0.13, True) in merged
  assert (0.14, True) in merged
  assert (0.15, False) in merged

  merged = merge_scores_and_distances(
    scores, distances, distance_cutoff=6.30, include_positions=True
  )
  assert len(merged) == 5
  assert (0.11, True, 'A', 1, 'A', 2) in merged
  assert (0.12, True, 'A', 1, 'A', 3) in merged
  assert (0.13, True, 'A', 1, 'A', 4) in merged
  assert (0.14, True, 'A', 2, 'A', 3) in merged
  assert (0.15, False, 'A', 2, 'A', 4) in merged

def test_binary_from_merged():
  """
  That binary_from_merged returns a correct list of boolean
  """
  merged_input = [
    (0.11, True),
    (0.13, False),
    (0.12, True),
    (0.15, False),
    (0.14, False),
  ]
  binary = binary_from_merged(merged_input, greater_is_better=False)
  assert binary == [True, True, False, False, False]

  binary = binary_from_merged(merged_input)
  assert binary == [False, False, False, True, True]

  merged_input = []
  binary = binary_from_merged(merged_input)
  assert binary == []

def test_curve_with_precision_recall_curve():
  """
  Test that the curves created by curve function are correct
  """
  with raises(ValueError) as err:
    binary_result = [True, True, True, True, True]
    curve_r = curve(binary_result)
    assert "Binary should have both False and True values." in str(err)

  with raises(ValueError) as err:
    binary_result = [False, False, False, False, False]
    curve_r = curve(binary_result)
    assert "Binary should have both False and True values." in str(err)

  binary_result = [True, True, False, False, True, True, False, False]
  curve_r = curve(binary_result, method='precision_recall')
  print(curve_r)
  assert curve_r == [
    (0, 1), (0.25, 1.0), (0.5, 1.0), (0.5, float(2/3)),
    (0.5, 0.5), (0.75, 0.6), (1, float(2/3)),
    (1, float(4/7)), (1.0, 0.5), (1.0, 0)
  ]
  binary_result = []
  with raises(ValueError) as err:
    assert curve(binary_result)
    assert str(err).startswith("Can not create a curve")
