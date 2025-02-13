"""
Test smooth functions
"""
# pylint: disable=redefined-outer-name
from pytest import fixture
from pytest import approx
from xi_covutils.smooth import _smooth_cov_segment
from xi_covutils.smooth import smooth_cov
from xi_covutils.smooth import smooth_cov_paired

@fixture(scope='module')
def cov_paired_inter_chain():
  """
  Builds an interprotein segment of cov_data for two chains 'A' and 'B'
  """
  scores = [
    0.6, 0.4, 1.0, 0.9, 0.1, 0.0, 1.0, 0.9, 0.6, 0.8,
    0.1, 0.6, 0.0, 0.7, 0.7, 0.0, 0.8, 0.7, 0.0, 0.0,
    0.1, 0.4, 0.7, 0.8, 0.0, 0.8, 0.1, 0.5, 0.4, 0.2,
    0.9, 0.6, 0.7, 0.8, 0.4, 0.8, 0.5, 0.0, 0.8, 0.4,
    0.6, 0.3, 0.4, 0.6, 0.2, 1.0, 0.6, 1.0, 0.9, 0.3,
    0.4, 1.0, 0.8, 0.3, 0.3, 0.5, 0.4, 0.9, 0.4, 0.7,
    0.7, 0.1, 0.6, 0.3, 0.2, 0.0, 0.9, 1.0, 0.1, 0.2,
    0.9, 0.4, 0.9, 0.4, 0.1, 0.7, 1.0, 0.4, 0.0, 0.7,
    0.9, 1.0, 0.4, 0.4, 0.7, 1.0, 0.9, 0.1, 0.9, 0.6,
    0.0, 0.8, 0.1, 1.0, 0.9, 0.4, 0.8, 0.1, 0.1, 0.2
  ]
  results = {}
  index = 0
  for pos1 in range(10):
    for pos2 in range(10):
      results[(('A', pos1+1), ('B', pos2+1))] = scores[index]
      index += 1
  return results

@fixture(scope='module')
def cov_paired_two_chains():
  """
  Builds an cov data for two chains 'A' and 'B' with inter
  and intra covariation.
  """
  def _chain(pos):
    return (pos, 'A') if pos < 5 else (pos-5, 'B')
  # Note: scores is symmetric and 0.0 in the diagonal
  scores = [
    0.0, 0.3, 0.1, 0.3, 0.0, 1.0, 0.3, 0.8, 0.7, 0.8,
    0.3, 0.0, 0.2, 0.4, 0.2, 0.2, 0.5, 0.3, 0.7, 0.2,
    0.1, 0.2, 0.0, 0.8, 0.6, 0.8, 0.1, 0.4, 0.0, 0.7,
    0.3, 0.4, 0.8, 0.0, 0.9, 0.6, 0.6, 0.6, 0.2, 0.5,
    0.0, 0.2, 0.6, 0.9, 0.0, 0.0, 0.2, 0.3, 0.7, 0.6,
    1.0, 0.2, 0.8, 0.6, 0.0, 0.0, 0.5, 0.9, 0.8, 0.2,
    0.3, 0.5, 0.1, 0.6, 0.2, 0.5, 0.0, 0.3, 0.0, 0.6,
    0.8, 0.3, 0.4, 0.6, 0.3, 0.9, 0.3, 0.0, 0.3, 0.4,
    0.7, 0.7, 0.0, 0.2, 0.7, 0.8, 0.0, 0.3, 0.0, 0.1,
    0.8, 0.2, 0.7, 0.5, 0.6, 0.2, 0.6, 0.4, 0.1, 0.0
  ]
  results = {}
  index = 0
  for pos1 in range(10):
    for pos2 in range(10):
      pos1n, chain1 = _chain(pos1)
      pos2n, chain2 = _chain(pos2)
      if (chain1 == chain2 and pos1n < pos2n) or chain1 < chain2:
        results[((chain1, pos1n+1), (chain2, pos2n+1))] = scores[index]
      index += 1
  return results

@fixture(scope='module')
def cov_paired_intra_chain():
  """
  Builds an intraprotein segment of cov_data for a chain 'A
  """
  scores = [
    0.4, 1.0, 0.9, 0.1, 0.0, 1.0, 0.9, 0.6, 0.8,
        0.0, 0.7, 0.7, 0.0, 0.8, 0.7, 0.0, 0.0,
              0.8, 0.0, 0.8, 0.1, 0.5, 0.4, 0.2,
                  0.4, 0.8, 0.5, 0.0, 0.8, 0.4,
                        1.0, 0.6, 1.0, 0.9, 0.3,
                            0.4, 0.9, 0.4, 0.7,
                                  1.0, 0.1, 0.2,
                                      0.0, 0.7,
                                            0.6
  ]
  results = {}
  chain1 = 'A'
  index = 0
  for pos1 in range(10):
    for pos2 in range(10):
      if pos1 < pos2:
        results[((chain1, pos1+1), (chain1, pos2+1))] = scores[index]
        index += 1
  return results

@fixture(scope='module')
def cov_single():
  """
  Builds an intraprotein segment of cov_data for a
  sigle protein
  """
  scores = [
    0.4, 1.0, 0.9, 0.1, 0.0, 1.0, 0.9, 0.6, 0.8,
        0.0, 0.7, 0.7, 0.0, 0.8, 0.7, 0.0, 0.0,
              0.8, 0.0, 0.8, 0.1, 0.5, 0.4, 0.2,
                  0.4, 0.8, 0.5, 0.0, 0.8, 0.4,
                        1.0, 0.6, 1.0, 0.9, 0.3,
                            0.4, 0.9, 0.4, 0.7,
                                  1.0, 0.1, 0.2,
                                      0.0, 0.7,
                                            0.6
  ]
  results = {}
  index = 0
  for pos1 in range(10):
    for pos2 in range(10):
      if pos1 < pos2:
        results[(pos1+1, pos2+1)] = scores[index]
        index += 1
  return results

def test__smooth_cov_segment_inter(cov_paired_inter_chain):
  """
  Test _smooth_cov_segment function when the input is a
  segment of interprotein covariation data.
  """
  results = _smooth_cov_segment(cov_paired_inter_chain)
  assert results[('A', 1), ('B', 1)] == float(0.6+0.4+0.1+0.6)/4
  assert results[('A', 10), ('B', 10)] == float(0.9+0.6+0.1+0.2)/4

def test__smooth_cov_segment_intra(cov_paired_intra_chain):
  """
  Test _smooth_cov_segment function when the input is a
  segment of intraproteina covariation data.
  """
  results = _smooth_cov_segment(cov_paired_intra_chain)
  assert results[('A', 1), ('A', 2)] == approx(float(0.4+0.4+0.0+1.0)/4)
  assert results[('A', 1), ('A', 3)] == approx(float(0.4+1.0+0.9+0.0+0.7)/5)
  assert results[('A', 2), ('A', 5)] == approx(
    float(
      0.9 + 0.1 + 0.0 + 0.7 + 0.7 + 0.0 + 0.8 + 0.0 + 0.8
    ) / 9
  )

def test_smooth_cov(cov_single):
  """
  Test _smooth_cov_segment function when the input is a
  segment of intraproteina covariation data.
  """
  results = smooth_cov(cov_single)
  assert results[(1, 2)] == approx(float(0.4+0.4+0.0+1.0)/4)
  assert results[(1, 3)] == approx(float(0.4+1.0+0.9+0.0+0.7)/5)
  assert results[(2, 5)] == approx(
    float(
      0.9 + 0.1 + 0.0 + 0.7 + 0.7 + 0.0 + 0.8 + 0.0 + 0.8
    ) / 9
  )

def test_smooth_cov_paired(cov_paired_two_chains):
  """
  Test
    :param cov_paired_two_chains:
  """
  smoothed = smooth_cov_paired(cov_paired_two_chains)
  assert smoothed[('A', 1), ('A', 2)] == approx(float(0.3+0.3+0.1+0.2)/4)
  assert smoothed[('A', 1), ('A', 5)] == approx(float(0.3+0.0+0.4+0.2)/4)
  assert smoothed[('A', 3), ('B', 1)] == approx(
    float(
      0.2+0.5+0.8+0.1+0.6+0.6
    ) / 6
  )
