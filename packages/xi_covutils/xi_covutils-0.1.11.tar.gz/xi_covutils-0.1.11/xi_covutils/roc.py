from functools  import reduce
from operator import add
from itertools import groupby

def curve(binary_result):
    '''
    Computes the ROC curve, not the AUC for a ordered list of  a binary classifier result.
        
    :param binary_result: a list of True or False values.
    '''
    total = len(binary_result)
    positives = 0
    negatives = 0
    curve = [(negatives, positives)]
    for binary in binary_result:
        positives += 1 if binary else 0
        negatives += 1 if not binary else 0
        curve.append((negatives, positives))
    curve = [(float(x)/max(negatives,1), float(y)/max(positives,1)) for x,y in curve]
    if not curve[-1] == (1.0, 1.0):
        curve.append((1.0, 1.0))
    return curve

def simplify(curve):
    '''
    Remove redundant points over a horizontal or vertical lines in the curve.

    :param curve: is a list of two element tuples of float, between 0 and 1.
    '''
    points_by_x = {k:[y for (_, y) in g] for k, g in groupby(curve, lambda x: x[0])}
    points_by_x = [[(x, ys[0])] if len(ys) == 1 else [(x, min(ys)),(x, max(ys))] 
                   for x, ys in sorted(points_by_x.items())]
    points_by_x = [xy for l in points_by_x for xy in l]

    points_by_y = {k:[x for (x, _) in g] for k, g in groupby(points_by_x, lambda x: x[1])}
    points_by_y = [[(xs[0], y)] if len(xs) == 1 else [(min(xs), y),(max(xs), y)] 
                   for y, xs in sorted(points_by_y.items())]
    points_by_y = [xy for l in points_by_y for xy in l]
    return points_by_y

def auc(curve):
    '''
    Computes the area under a ROC curve.
    Assumes that the first element is (0,0), the last element is (1,1) and that 
    has more than one element.

    :param curve: is a list of two element tuples of float, between 0 and 1.
    '''
    if len(curve) <= 1:
         raise ValueError("The curve needs two or more points to compute an area.")
    subareas =  [(x2-x1)*(y2) for (x2, y2), (x1, y1) in zip(curve[1:],curve[:-1])]
    return reduce(add, subareas, 0)