"""
  Test the mkdssp runner and parser
"""
from os import environ
from os.path import exists, join
from shutil import which
import pytest

from xi_covutils.mkdssp import _parse_mkdssp_line, mkdssp


def _exists_mkdssp():
  mkdssp_path = environ.get("MKDSSP_PATH", "")
  mkdssp_path = mkdssp_path if mkdssp_path else which("mkdssp")
  return mkdssp_path and exists(mkdssp_path)

@pytest.mark.skipif(not _exists_mkdssp(), reason="This test requires mkdssp")
def test_mkdssp(test_data_folder):
  """
  test mkdssp function
  :param test_data_folder: fixture with the path of the package test data
    folder
  """
  pdb_file = join(test_data_folder, '3A5E.pdb')
  content = mkdssp(pdb_file)
  assert len(content) == 15
  assert content[('A', 1)]["aa"] == 'K'
  assert content[('A', 1)]["structure"] == ''
  assert content[('A', 8)]["structure"] == 'G'
  assert content[('A', 11)]["structure"] == 'S'
  assert content[('A', 13)]["structure"] == 'T'

# pylint: disable=too-many-locals
def test_parse_mkdssp_line():
  """
  Test _parse_mkdsssp_line function
  """
  #pylint: disable=line-too-long
  line_1 = (
    "    1    1 A S              0   0   85      0, 0.0     2,-0.4     0, 0.0    "
    "72,-0.2   0.000 360.0 360.0 360.0 163.2   25.9   -1.5   29.7                A         A"
  )
  result_1 = _parse_mkdssp_line(line_1)
  assert result_1
  assert result_1['index'] == 1
  assert result_1['pdb_num'] == 1
  assert result_1['chain'] == 'A'
  assert result_1['aa'] == 'S'
  assert result_1['structure'] == ''

  line_2 = ("    2    2 A E  E     -A   72   0A 128     70,-1.1    70,-0.9     2,-0.0    " +
        " 2,-0.3  -0.962 360.0-123.5-129.6 147.5   24.3   -3.5   26.8                A         A")
  result_2 = _parse_mkdssp_line(line_2)
  assert result_2
  assert result_2['index'] == 2
  assert result_2['pdb_num'] == 2
  assert result_2['chain'] == 'A'
  assert result_2['aa'] == 'E'
  assert result_2['structure'] == 'E'

  line_3 = ("   10   10 A G  S    S+     0   0   66      1,-0.4     2,-0.2     0, 0.0    " +
        "-2,-0.1   0.579  84.7  24.0  97.0  10.7   13.0  -19.8   15.2                A         A")
  result_3 = _parse_mkdssp_line(line_3)
  assert result_3
  assert result_3['index'] == 10
  assert result_3['pdb_num'] == 10
  assert result_3['chain'] == 'A'
  assert result_3['aa'] == 'G'
  assert result_3['structure'] == 'S'

  line_4 = ("   22   22 A T  T 3  S+     0   0   88     -2,-0.3    31,-0.2     1,-0.2    " +
        " 3,-0.1  -0.669 115.0  14.8 -85.0 134.6   18.3   -7.3   40.3                A         A")
  result_4 = _parse_mkdssp_line(line_4)
  assert result_4
  assert result_4['index'] == 22
  assert result_4['pdb_num'] == 22
  assert result_4['chain'] == 'A'
  assert result_4['aa'] == 'T'
  assert result_4['structure'] == 'T'

  line_5 = ("   23   23AA G  T 3  S+     0   0   46     29,-1.4     2,-0.4    -2,-0.4    " +
        "-1,-0.2   0.454  94.7 132.6  84.6  -2.6   21.8   -6.2   41.5                A         A")
  result_5 = _parse_mkdssp_line(line_5)
  assert not result_5

  line_6 = ("   25   24 A L  B     -B   51   0A 126     -2,-0.4    26,-0.3    26,-0.2    " +
        "24,-0.1  -0.729  25.0-167.0 -87.2 121.8   26.2  -10.5   39.6                A         A")
  result_6 = _parse_mkdssp_line(line_6)
  assert result_6
  assert result_6['index'] == 25
  assert result_6['pdb_num'] == 24
  assert result_6['chain'] == 'A'
  assert result_6['structure'] == 'B'

  line_7 = ("1403        !              0   0    0      0, 0.0     0, 0.0     0, 0.0     " +
        "0, 0.0   0.000 360.0 360.0 360.0 360.0    0.0    0.0    0.0                           ")
  result_7 = _parse_mkdssp_line(line_7)
  assert not result_7

  line_8 = ("1403        !*             0   0    0      0, 0.0     0, 0.0     0, 0.0     " +
        "0, 0.0   0.000 360.0 360.0 360.0 360.0    0.0    0.0    0.0                           ")
  result_8 = _parse_mkdssp_line(line_8)
  assert not result_8
