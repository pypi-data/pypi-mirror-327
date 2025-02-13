"""
  Functions to compute ROC curves and calculate AUC scores.
"""
from functools import reduce
from itertools import groupby
from operator import add
from typing import List, Literal, Tuple, Union

from xi_covutils.distances import Distances

CurveMethod = Union[Literal["roc"], Literal["precision_recall"]]
XYPoint = tuple[float, float]
Curve = list[XYPoint]

def curve(
    binary_result:list[bool],
    method:CurveMethod="roc"
  ) -> Curve:
  """
  Computes the ROC curve or the precision vs recall curve for a ordered list
  of a binary classifier result. Binary should not contain all True or all
  False values.

  Args:
    binary_result (list[bool]): A list of True and False values.
    method (CurveMethod): The method to build the curve: "roc" or
      "precision_recall"

  Returns:
    Curve: The points of the curve.

  Throws:
    ValueError: If the method is not recognized.
  """
  if method == 'roc':
    return _roc_curve(binary_result)
  if method == 'precision_recall':
    return _precision_recall_curve(binary_result)
  raise ValueError("Invalid method")


def _roc_curve(
    binary_result: list[bool]
  ) -> Curve:
  """
  Computes the ROC curve for a ordered list of a binary
  classifier result. Binary should not contain all True or all False values.

  Args:
    binary_result (list[bool]): A list of True and False values.

  Returns:
    Curve: The generated curve.

  Throws:
    ValueError: If binary_result is empty or has not any True value.
  """
  positives:float = 0
  negatives:float = 0
  c_curve = [(float(negatives), float(positives))]
  if not binary_result:
    raise ValueError("Can not create a curve from a empty binary list.")
  if all(binary_result) or not any(binary_result):
    raise ValueError("Binary should have both False and True values.")
  for binary in binary_result:
    positives += 1 if binary else 0
    negatives += 1 if not binary else 0
    c_curve.append((negatives, positives))
  c_curve = [
    (float(x)/max(negatives, 1), float(y)/max(positives, 1))
    for x, y in c_curve
  ]
  if not c_curve[-1] == (1.0, 1.0):
    c_curve.append((1.0, 1.0))
  return c_curve


def _precision_recall_curve(
    binary_result: list[bool]
  ) -> Curve:
  """
  Computes the ROC curve for a ordered list of a binary
  classifier result. Binary should not contain all True or all False values.

  Args:
    binary_result (list[bool]): A list of True and False values.

  Returns:
    Curve: The generated curve.

  Throws:
    ValueError: If binary_result is empty or has not any True value.
  """
  true_positives = 0
  total = reduce(lambda a, b: a + (1 if b else 0), binary_result)
  count = 0
  c_curve:List[Tuple[float, float]] = [(0, 1)]
  if not binary_result:
    raise ValueError("Can not create a curve from a empty binary list.")
  if all(binary_result) or not any(binary_result):
    raise ValueError("Binary should have both False and True values.")
  for binary in binary_result:
    count += 1
    true_positives += 1 if binary else 0
    precision = float(true_positives) / count
    recall = float(true_positives) / total
    c_curve.append((recall, precision))
  if c_curve[-1] != (1.0, 0.0):
    c_curve.append((1.0, 0.0))
  return c_curve

def simplify(
    a_curve:Curve
  ) -> Curve:
  """
  Remove redundant points over a horizontal or vertical line in the curve.

  Args:
    a_curve (Curve): A curve to simplify.

  Returns:
    Curve: The simplified curve.
  """
  points_by_x = {
    k:[y for (_, y) in g] for k, g in groupby(a_curve, lambda x: x[0])
  }
  points_by_x = [
    [(x, ys[0])] if len(ys) == 1 else [(x, min(ys)), (x, max(ys))]
    for x, ys in sorted(points_by_x.items())
  ]
  points_by_x = [xy for l in points_by_x for xy in l]

  points_by_y = {
    k:[x for (x, _) in g] for k, g in groupby(points_by_x, lambda x: x[1])
  }
  points_by_y = [
    [(xs[0], y)] if len(xs) == 1 else [(min(xs), y), (max(xs), y)]
    for y, xs in sorted(points_by_y.items())
  ]
  points_by_y = [xy for l in points_by_y for xy in l]
  return points_by_y

def auc(
    a_curve:Curve
  ) -> float:
  """
  Computes the area under a ROC curve.
  Assumes that the first element is (0,0), the last element is (1,1) and that
  has more than one element.

  Args:
    a_curve (Curve): A curve to calculate the area under.

  Returns:
    float: The area under the curve.

  Throws:
    ValueError: If curve has less than two points.
  """
  if len(a_curve) <= 1:
    raise ValueError("The curve needs two or more points to compute an area.")
  subareas = [
    (x2-x1)*(y2) for (x2, y2), (x1, _) in zip(a_curve[1:], a_curve[:-1])
  ]
  return reduce(add, subareas, 0)

def auc_n(
    a_curve:Curve,
    fpr_limit:float=0.05
  ) -> float:
  """
  Computes the area under a ROC curve from the origin until a given value of
  FPR.
  Assumes that the first element is (0,0), the last element is (1,1) and that
  has more than one element.

  Args:
    a_curve (Curve): Curve
    fpr_limit (float): A False Positive Rate limit.

  Returns:
    float: The Area under the curve from the origin until a given value of FPR.
  """
  a_curve = [(x, y) for x, y in a_curve if x <= fpr_limit]
  if not a_curve[-1][0] == fpr_limit:
    a_curve.append((fpr_limit, a_curve[-1][1]))
  return auc(a_curve)


def curve_to_str(
    a_curve:Curve
  ) -> str:
  """
  Generates a string representation of the curve intended to be exported into a
  text file.

  Args:
    a_curve (Curve): A curve to export to text.

  Returns:
    str: A string representation of the curve.
  """
  return "\n".join([f"{x}, {y}" for x, y in a_curve])

def merge_scores_and_distances(
    scores: dict[tuple[tuple[str, int], tuple[str, int]], float],
    distances:Distances,
    distance_cutoff:float=6.05,
    include_positions:bool=False
  ) -> Union[
    list[tuple[float, bool, str, int, str, int]],
    list[tuple[float, bool]]
  ]:
  """
  Merges covariation scores and distances object data into a single
  list.

  Covariation pairs of the covariation score that do not have an associated
  distance are eliminated from the result.
  The output list has no order.

  Args:
    scores (dict[tuple[tuple[str, int], tuple[str, int]], float]): Covariation
      Scores.
    distances (Distances): The inter residue distances.
    distance_cutoff (float): the distance cutoff to decide if two residues are
      in contact.
    include_positions (bool): If True information of the positions (residue
      number and chain) is included in the merged results. Otherwise, only
      distance and if it is a contact is included.

  Returns:
    Union[
      list[tuple[float, bool, str, int, str, int]],
      list[tuple[float, bool]]
    ]: The merged result.
  """
  score_contacts = [
    (
      score,
      distances.is_contact(c1, p1, c2, p2, distance_cutoff),
      c1,
      p1,
      c2,
      p2
    )
    for ((c1, p1), (c2, p2)), score in scores.items()
    if distances.of(c1, p1, c2, p2)
  ]
  contacts = []
  for values in score_contacts:
    if not include_positions:
      elem = (values[0], values[1])
    else:
      elem = values
    contacts.append(elem)
  return contacts

def binary_from_merged(
    merged:list[tuple[float, bool]],
    greater_is_better:bool=True
  ) -> list[bool]:
  """
  Creates a sorted list of a binary classification (True, False) of contacts
  from a merged list of (score, contact) tuples.

  The input list can be generated using merge_scores_and_distances function.

  Args:
    merged (list[tuple[float, bool]]): A list of tuples, each tuple element is
      of the form: (float, bool), where the float is the cov score and
      the bool is if correspond to a covariation pair that is in
      contact.
    greater_is_better (bool): If True higher values mean higher covariation.

  Returns:
    list[bool]: A list of bool values, each value states if a covariation value
      corresponds to a contact or not. Values are sorted by covariation score.
  """
  return [
    v
    for _, v in sorted(
      merged, key=lambda x: x[0],
      reverse=greater_is_better
    )
  ]
