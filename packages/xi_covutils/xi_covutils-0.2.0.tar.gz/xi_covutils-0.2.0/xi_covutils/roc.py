"""
    Functions to compute ROC curves and calculate AUC scores.
"""
from functools import reduce #pylint: disable=redefined-builtin
from operator import add
from itertools import groupby

def curve(binary_result):
    '''
    Computes the ROC curve, not the AUC for a ordered list of  a binary classifier result.

    :param binary_result: a list of True or False values.
    '''
    positives = 0
    negatives = 0
    c_curve = [(negatives, positives)]
    for binary in binary_result:
        positives += 1 if binary else 0
        negatives += 1 if not binary else 0
        c_curve.append((negatives, positives))
    c_curve = [(float(x)/max(negatives, 1), float(y)/max(positives, 1)) for x, y in c_curve]
    if not c_curve[-1] == (1.0, 1.0):
        c_curve.append((1.0, 1.0))
    return c_curve

def simplify(a_curve):
    '''
    Remove redundant points over a horizontal or vertical lines in the curve.

    :param curve: is a list of two element tuples of float, between 0 and 1.
    '''
    points_by_x = {k:[y for (_, y) in g] for k, g in groupby(a_curve, lambda x: x[0])}
    points_by_x = [[(x, ys[0])] if len(ys) == 1 else [(x, min(ys)), (x, max(ys))]
                   for x, ys in sorted(points_by_x.items())]
    points_by_x = [xy for l in points_by_x for xy in l]

    points_by_y = {k:[x for (x, _) in g] for k, g in groupby(points_by_x, lambda x: x[1])}
    points_by_y = [[(xs[0], y)] if len(xs) == 1 else [(min(xs), y), (max(xs), y)]
                   for y, xs in sorted(points_by_y.items())]
    points_by_y = [xy for l in points_by_y for xy in l]
    return points_by_y

def auc(a_curve):
    '''
    Computes the area under a ROC curve.
    Assumes that the first element is (0,0), the last element is (1,1) and that
    has more than one element.

    :param curve: is a list of two element tuples of float, between 0 and 1.
    '''
    if len(a_curve) <= 1:
        raise ValueError("The curve needs two or more points to compute an area.")
    subareas = [(x2-x1)*(y2) for (x2, y2), (x1, _) in zip(a_curve[1:], a_curve[:-1])]
    return reduce(add, subareas, 0)

def auc_n(a_curve, fpr_limit=0.05):
    '''
    Computes the area under a ROC curve from the origin until a given value of FPR.
    Assumes that the first element is (0,0), the last element is (1,1) and that
    has more than one element.

    :param curve: is a list of two element tuples of float, between 0 and 1.
    '''
    a_curve = [(x, y) for x, y in a_curve if x <= fpr_limit]
    if not a_curve[-1][0] == fpr_limit:
        a_curve.append((fpr_limit, a_curve[-1][1]))
    return auc(a_curve)


def curve_to_str(a_curve):
    '''
    Generates a string representation of the curve intended to be exported into a text file.
    :param curve:
    '''
    return "\n".join(["{}, {}".format(x, y) for x, y in a_curve])

def merge_scores_and_distances(scores, distances):
    """
    Merges covariation scores and distances object data into a single
    list.

    Covariation pairs of the covariation score that do not have an associated
    distance are eliminated from the result.
    The output list has no order.

        :param scores: a dictionary with keys of the form ((chain1, pos1), (chain2, pos2)) and scores as values.
        :param distances: a xi_covutils.distances.Distance object
    """
    score_contacts = [(score, distances.is_contact(c1, p1, c2, p2))
                      for ((c1, p1), (c2, p2)), score in scores.items()
                      if distances.of(c1, p1, c2, p2)]
    return score_contacts

def binary_from_merged(merged, greater_is_better=True):
    """
    Creates a sorted list of a binary classification (True, False) of contacts
    from a merged list of (score, contact) tuples.

    The input list can be generated using merge_scores_and_distances function.

        :param merged: a list of tuples, each tuple element is of the
            form: (float, bool) , where the float is the cov score and
            the bool is if correspond to a covariation pair that is in
            contact.
        :param greater_is_better: if True, cov scores of merged are assumed to be
            better when they are greater and worst if smaller.
    """
    return [v for _, v in sorted(merged, key=lambda x: x[0], reverse=greater_is_better)]
