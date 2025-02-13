"""
Functions to compute smooth covariation scores
"""
from xi_covutils.read_results import inter_covariation
from xi_covutils.read_results import intra_covariation

def _smooth_cov_segment(cov_data, windows_size=3):
    """
    docstring here
        :param cov_data:
        :param windows_size=3:
    """
    def _get_global_guards(cov_data):
        chain1_id = list(cov_data.keys())[0][0][0]
        chain2_id = list(cov_data.keys())[0][1][0]
        global_guards = {
            'min': {chain1_id: float('inf'), chain2_id: float('inf')},
            'max': {chain1_id: 0, chain2_id: 0}
        }
        for ((chain1, pos1), (chain2, pos2)) in cov_data:
            global_guards['min'][chain1] = min(global_guards['min'][chain1], pos1)
            global_guards['min'][chain2] = min(global_guards['min'][chain2], pos2)
            global_guards['max'][chain1] = max(global_guards['max'][chain1], pos1)
            global_guards['max'][chain2] = max(global_guards['max'][chain2], pos2)
        return global_guards
    def _compute_smoothed(chain1, chain2, locals_guards):
        cumm_scores = 0
        summables = 0
        chain1_range = range(locals_guards['min']['chain1'], locals_guards['max']['chain1']+1)
        chain2_range = range(locals_guards['min']['chain2'], locals_guards['max']['chain2']+1)
        for lpos1 in chain1_range:
            for lpos2 in chain2_range:
                if (chain1, lpos1) != (chain2, lpos2):
                    summables += 1
                    index_1 = ((chain1, lpos1), (chain2, lpos2))
                    index_2 = ((chain2, lpos2), (chain1, lpos1))
                    current_score = cov_data.get(index_1, cov_data.get(index_2))
                    cumm_scores += current_score
        return float(cumm_scores) / max(1, summables)

    global_guards = _get_global_guards(cov_data)
    semi_w = int((windows_size - 1)/2)
    results = {}

    for ((chain1, pos1), (chain2, pos2)) in cov_data:
        locals_guards = {
            'min':{
                'chain1': max(global_guards['min'][chain1], pos1-semi_w),
                'chain2': max(global_guards['min'][chain2], pos2-semi_w)
            },
            'max':{
                'chain1': min(global_guards['max'][chain1], pos1+semi_w),
                'chain2': min(global_guards['max'][chain2], pos2+semi_w)
            }
        }
        results[((chain1, pos1), (chain2, pos2))] = _compute_smoothed(chain1, chain2, locals_guards)
    return results

def smooth_cov(cov_data, windows_size=3):
    """
    Calculate smoothed covariation data of a single protein.

    Covariation data is assumed to be a dictionary of tuples of
    indices (i,j) where i<=j as keys and score as value.

        :param cov_data: covariation data dict.
        :param windows_size: the size of the window to compute the average.
    """
    def _as_paired(cov_data):
        return {(('A', i), ('A', j)): v for (i, j), v in cov_data.items()}
    def _from_paired(cov_data):
        return {(i, j): v for ((_, i), (_, j)), v in cov_data.items()}
    smoothed = _smooth_cov_segment(_as_paired(cov_data), windows_size)
    return _from_paired(smoothed)

def smooth_cov_paired(cov_data, windows_size=3):
    """
    Computes smoothed covariation for paired cov data.

    Covariation data is assumed to be a dictionary of tuples of
    indices ((chain1, i) ,(chain2, j)) as keys and score as value.

        :param cov_data: covariation data dict.
        :param windows_size=3: the size of the window to compute the average.
    """
    intra_cov = intra_covariation(cov_data)
    inter_cov = inter_covariation(cov_data)
    segments = [v for _, v in intra_cov.items()]
    segments = segments + [v for _, v in inter_cov.items()]
    smoothed = [_smooth_cov_segment(s, windows_size) for s in segments]
    return {k: v for s in smoothed for k, v in s.items()}
