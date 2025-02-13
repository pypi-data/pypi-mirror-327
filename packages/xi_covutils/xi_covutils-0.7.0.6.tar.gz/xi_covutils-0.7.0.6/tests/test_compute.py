"""
  Test functions of compute module.
"""
from os import close, remove
from os.path import exists, join
from tempfile import mkstemp
from shutil import which

import mock
import pytest
from pytest import approx, fixture

from xi_covutils.compute import (
  ccmpred,
  cummulative,
  gauss_dca,
  mutual_info,
  proximity
)
from xi_covutils.distances import Distances

# pylint: disable=redefined-outer-name

@fixture(scope="session")
def logfile():
  """
  Initializes an empy log file and removes it later
  """
  lfh, log_file = mkstemp()
  close(lfh)
  yield log_file
  remove(log_file)

@fixture(scope="session")
def outfile():
  """
  Initializes an empy log file and removes it later
  """
  lfh, log_file = mkstemp()
  close(lfh)
  yield log_file
  remove(log_file)

@mock.patch('xi_covutils.compute.which')
@mock.patch('xi_covutils.compute.check_output')
def test_ccmpred_setup_01(
    mock_co,
    mock_which,
    test_data_folder,
    outfile,
    logfile
  ):
  """
  Test the ccmpred function.

  """
  ofh, outfile = mkstemp()
  close(ofh)
  input_file = join(test_data_folder, "test_cov_msa.fasta")
  mock_which.return_value = 'ccmpred'
  mock_co.return_value = b"CCMPRED_OUTPUT"
  success, text = ccmpred(input_file, outfile, log_file=logfile)
  mock_co.assert_called_once()
  assert success
  assert text == "CCMPRED_OUTPUT"
  assert exists(logfile)
  assert exists(outfile)

@mock.patch('xi_covutils.compute.which')
def test_ccmpred_setup_02(mock_which, outfile, logfile):
  """
  Test the ccmpred function with non existent file
  """
  ofh, outfile = mkstemp()
  close(ofh)
  input_file = "non_existent_file"
  mock_which.return_value = "ccmpred"
  success, text = ccmpred(input_file, outfile, log_file=logfile)
  assert not success
  assert "No such file or directory" in text
  assert exists(logfile)
  assert exists(outfile)

def test_ccmpred_setup_03(test_data_folder, outfile, logfile):
  """
  Test the ccmpred function with no ccmpred in path
  """
  ofh, outfile = mkstemp()
  close(ofh)
  input_file = join(test_data_folder, "test_cov_msa.fasta")
  result = ccmpred(
    input_file, outfile, log_file=logfile,
    ccmpred_exec="ncaksuyfgnkadsfg"
  )
  assert result == (False,  "CCMpred program was not found in the path")

@mock.patch('xi_covutils.compute.which')
@mock.patch('xi_covutils.compute.check_output')
def test_ccmpred_setup_04(mock_which, outfile):
  """
  Test the ccmpred function with no log file
  """
  ofh, outfile = mkstemp()
  close(ofh)
  mock_which.return_value = 'ccmpred'
  input_file = "non_existent_file"
  success, text = ccmpred(input_file, outfile)
  assert not success
  assert "No such file or directory" in text
  assert exists(outfile)

@mock.patch('xi_covutils.compute.which')
@mock.patch('xi_covutils.compute.check_output')
def test_mutual_info_setup_01(
    mock_co, mock_which, test_data_folder, outfile, logfile):
  """
  Test the ccmpred function
  """
  ofh, outfile = mkstemp()
  close(ofh)
  input_file = join(test_data_folder, "test_cov_msa.fasta")
  mock_co.return_value = b"MI OUTPUT"
  mock_which.return_value = "Buslje09.jl"
  success, text = mutual_info(input_file, outfile, log_file=logfile)
  mock_co.assert_called_once()
  assert success
  assert text == "MI OUTPUT"
  assert exists(logfile)
  assert exists(outfile)

@pytest.mark.skipif(
  not which("julia"),
  reason="julia should be accessible in PATH"
)
def test_gauss_dca_setup_01(test_data_folder, outfile, logfile):
  """
  Test the ccmpred function
  """
  ofh, outfile = mkstemp()
  close(ofh)
  input_file = join(test_data_folder, "msa_03.fasta")
  success, _ = gauss_dca(input_file, outfile, log_file=logfile)
  assert success
  assert exists(logfile)
  assert exists(outfile)

def test_cummulative():
  """
  Test cummulative MI calculation function.
  """
  scores = {
    (('A', 1), ('A', 2)): 0.1,
    (('A', 1), ('A', 3)): 0.2,
    (('A', 1), ('A', 4)): 0.3,
    (('A', 1), ('A', 5)): 0.4,
    (('A', 2), ('A', 3)): 0.1,
    (('A', 2), ('A', 4)): 0.2,
    (('A', 2), ('A', 5)): 0.3,
    (('A', 3), ('A', 4)): 0.2,
    (('A', 3), ('A', 5)): 0.3,
    (('A', 4), ('A', 5)): 0.3,
    (('B', 1), ('B', 2)): 0.1,
    (('B', 1), ('B', 3)): 0.2,
    (('B', 2), ('B', 3)): 0.3,
    (('A', 1), ('B', 1)): 0.1,
    (('A', 1), ('B', 2)): 0.2,
    (('A', 1), ('B', 3)): 0.3,
    (('A', 2), ('B', 1)): 0.1,
    (('A', 2), ('B', 2)): 0.2,
    (('A', 2), ('B', 3)): 0.3,
    (('A', 3), ('B', 1)): 0.2,
    (('A', 3), ('B', 2)): 0.3,
    (('A', 3), ('B', 3)): 0.3,
    (('A', 4), ('B', 1)): 0.1,
    (('A', 4), ('B', 2)): 0.2,
    (('A', 4), ('B', 3)): 0.3,
    (('A', 5), ('B', 1)): 0.1,
    (('A', 5), ('B', 2)): 0.2,
    (('A', 5), ('B', 3)): 0.3,
  }
  cum_a = cummulative(scores, 6.5)
  assert len(cum_a) == 8
  assert cum_a[('A', 1)] == approx(0.0)
  assert cum_a[('A', 2)] == approx(0.0)
  assert cum_a[('A', 3)] == approx(0.0)
  assert cum_a[('A', 4)] == approx(0.0)
  assert cum_a[('A', 5)] == approx(0.0)
  assert cum_a[('B', 1)] == approx(0.0)
  assert cum_a[('B', 2)] == approx(0.0)
  assert cum_a[('B', 3)] == approx(0.0)

  cum_b = cummulative(scores, 0.2)
  assert len(cum_b) == 8
  assert cum_b[('A', 1)] == approx(0.9)
  assert cum_b[('A', 2)] == approx(0.5)
  assert cum_b[('A', 3)] == approx(0.7)
  assert cum_b[('A', 4)] == approx(1.0)
  assert cum_b[('A', 5)] == approx(1.3)
  assert cum_b[('B', 1)] == approx(0.2)
  assert cum_b[('B', 2)] == approx(0.3)
  assert cum_b[('B', 3)] == approx(0.5)

def test_proximity():
  """
  Test proximity MI calculation.
  """
  cum_scores = {('A', 1): 0.9,
          ('A', 2): 0.5,
          ('A', 3): 0.7,
          ('A', 4): 1.0,
          ('A', 5): 1.3,
          ('B', 1): 0.2,
          ('B', 2): 0.3,
          ('B', 3): 0.5}
  dist_data = [
    ('A', 1, 'A', 2, 4.0),
    ('A', 1, 'A', 3, 4.5),
    ('A', 1, 'A', 4, 5.0),
    ('A', 1, 'A', 5, 5.5),
    ('A', 2, 'A', 3, 6.0),
    ('A', 2, 'A', 4, 6.5),
    ('A', 2, 'A', 5, 7.0),
    ('A', 3, 'A', 4, 7.5),
    ('A', 3, 'A', 5, 4.0),
    ('A', 4, 'A', 5, 4.5),
    ('B', 1, 'B', 2, 5.0),
    ('B', 1, 'B', 3, 5.5),
    ('B', 2, 'B', 3, 6.0),
    ('A', 1, 'B', 1, 6.5),
    ('A', 1, 'B', 2, 7.0),
    ('A', 1, 'B', 3, 7.5),
    ('A', 2, 'B', 1, 4.0),
    ('A', 2, 'B', 2, 4.5),
    ('A', 2, 'B', 3, 5.0),
    ('A', 3, 'B', 1, 5.5),
    ('A', 3, 'B', 2, 6.0),
    ('A', 3, 'B', 3, 6.5),
    ('A', 4, 'B', 1, 7.0),
    ('A', 4, 'B', 2, 7.5),
    ('A', 4, 'B', 3, 8.0),
    ('A', 5, 'B', 1, 8.5),
    ('A', 5, 'B', 2, 4.0),
    ('A', 5, 'B', 3, 4.5),
  ]
  distances = Distances(dist_data)
  prox_a = proximity(cum_scores, distances, 3.5)
  assert len(prox_a) == 8
  assert prox_a[('A', 1)] == approx(0.0)
  assert prox_a[('A', 2)] == approx(0.0)
  assert prox_a[('A', 3)] == approx(0.0)
  assert prox_a[('A', 4)] == approx(0.0)
  assert prox_a[('A', 5)] == approx(0.0)
  assert prox_a[('B', 1)] == approx(0.0)
  assert prox_a[('B', 2)] == approx(0.0)
  assert prox_a[('B', 3)] == approx(0.0)

  prox_a = proximity(cum_scores, distances, 5.5)
  assert len(prox_a) == 8
  assert prox_a[('A', 1)] == approx((0.5+0.7+1.0+1.3)/4)
  assert prox_a[('A', 2)] == approx(0.9)
  assert prox_a[('A', 3)] == approx((0.9+1.3)/2)
  assert prox_a[('A', 4)] == approx((0.9+1.3)/2)
  assert prox_a[('A', 5)] == approx((0.9+0.7+1.0)/3)
  assert prox_a[('B', 1)] == approx((0.3+0.5)/2)
  assert prox_a[('B', 2)] == approx(0.2)
  assert prox_a[('B', 3)] == approx(0.2)
