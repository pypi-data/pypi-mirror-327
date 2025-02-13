"""
Tests for conservation module
"""
import math
import os
from pytest import approx
from xi_covutils.conservation import BackgroundFreq, entropy, plot_conservation


def test_entropy_without_gaps_and_with_clustering_and_maxdiff():
  """
  Test shannon entropy.
  The expected results are computed with MIToS.jl package
  with clustering at 62 percent.
  """
  seqs = [
    "ACTACTATCTAGCTAGC",
    "ACTACTGATGCACTGTG",
    "ACTACTGATCTACTGAG"
  ]
  results = entropy(seqs, BackgroundFreq.UNIFORM, 62, max_diff=True)
  expected_results = [
    -0.0, -0.0, -0.0, -0.0, -0.0, -0.0,
    0.6931471805599453, 0.6931471805599453,
    0.6931471805599453, 1.0397207708399179,
    1.0397207708399179, 0.6931471805599453,
    -0.0, -0.0,
    0.6931471805599453, 1.0397207708399179,
    0.6931471805599453
  ]
  expected_results = [
    math.log2(20) - x / math.log(2) if x is not None else x
    for x in expected_results
  ]
  assert all(
    a == approx(b)
    for a, b in zip(results, expected_results)
  )

def test_entropy_without_gaps_and_without_clustering():
  """
  Test shannon entropy.
  The expected results are computed with MIToS.jl package
  with no clustering and sequences with no gaps.
  """
  seqs = [
    "ACTACTATCTAGCTAGC",
    "ACTACTGATGCACTGTG",
    "ACTACTGATCTACTGAG"
  ]
  results = entropy(seqs, max_diff=False)
  expected_results = [
    -0.0, -0.0, -0.0, -0.0, -0.0, -0.0,
    0.6365141682948128, 0.6365141682948128,
    0.6365141682948128, 1.0986122886681096,
    1.0986122886681096, 0.6365141682948128,
    -0.0, -0.0,
    0.6365141682948128, 1.0986122886681096,
    0.6365141682948128]
  expected_results = [
    x / math.log(2) if x is not None else x
    for x in expected_results
  ]
  assert all(
    a == approx(b)
    for a, b in zip(results, expected_results)
  )

def test_entropy_with_gaps_and_with_clustering():
  """
  Test shannon entropy.
  The expected results are computed with MIToS.jl package
  with clustering at 50 percent.
  """
  seqs = [
    "-CTA-ACTGCTGACTTG",
    "--TACACTACTGACTTG",
    "---AAAGATGACTGAAC"
  ]
  results = entropy(seqs, BackgroundFreq.UNIFORM, 50, max_diff=False)
  expected_results = [
    None,
    -0.0, -0.0,
    -0.0, 0.6365141682948128,
    -0.0, 0.6931471805599453,
    0.6931471805599453, 1.0397207708399179,
    0.6931471805599453, 0.6931471805599453,
    0.6931471805599453, 0.6931471805599453,
    0.6931471805599453, 0.6931471805599453,
    0.6931471805599453, 0.6931471805599453]
  expected_results = [
    x / math.log(2) if x is not None else x
    for x in expected_results
  ]
  assert all(
    a == approx(b) if a and b else a == b
    for a, b in zip(results, expected_results)
  )


def test_entropy_with_gaps_and_without_clustering_and_maxdiff():
  """
  Test shannon entropy.
  The expected results are computed with MIToS.jl package
  with no clustering and sequences with no gaps.
  """
  seqs = [
    "-CTA-ACTGCTGACTTG",
    "--TACACTACTGACTTG",
    "---AAAGATGACTGAAC"
  ]
  results = entropy(seqs, BackgroundFreq.UNIFORM, None, max_diff=True)
  expected_results = [
    None,
    -0.0, -0.0,
    -0.0, 0.6931471805599453,
    -0.0, 0.6365141682948128,
    0.6365141682948128, 1.0986122886681096,
    0.6365141682948128, 0.6365141682948128,
    0.6365141682948128, 0.6365141682948128,
    0.6365141682948128, 0.6365141682948128,
    0.6365141682948128, 0.6365141682948128
  ]
  expected_results = [
    math.log2(20) - x / math.log(2) if x is not None else x
    for x in expected_results
  ]
  assert all(
    a == approx(b) if a and b else a == b
    for a, b in zip(results, expected_results)
  )

def test_entropy_with_gaps_and_without_clustering():
  """
  Test shannon entropy.
  The expected results are computed with MIToS.jl package
  with no clustering and sequences with no gaps.
  """
  seqs = [
    "-CTA-ACTGCTGACTTG",
    "--TACACTACTGACTTG",
    "---AAAGATGACTGAAC"
  ]
  results = entropy(seqs, BackgroundFreq.UNIFORM, None, max_diff=False)
  expected_results = [
    None,
    -0.0, -0.0,
    -0.0, 0.6931471805599453,
    -0.0, 0.6365141682948128,
    0.6365141682948128, 1.0986122886681096,
    0.6365141682948128, 0.6365141682948128,
    0.6365141682948128, 0.6365141682948128,
    0.6365141682948128, 0.6365141682948128,
    0.6365141682948128, 0.6365141682948128]
  expected_results = [
    x / math.log(2) if x is not None else x
    for x in expected_results
  ]
  assert all(
    a == approx(b) if a and b else a == b
    for a, b in zip(results, expected_results)
  )

def test_entropy_without_gaps_and_with_clustering_and_blosum62():
  """
  Test shannon entropy corrected by blosum62.
  The expected results are computed with MIToS.jl package
  with clustering at 62 percent.
  """
  seqs = [
    "ACTACTATCTAGCTAGC",
    "ACTACTGATGCACTGTG",
    "ACTACTGATCTACTGAG"
  ]
  results = entropy(seqs, BackgroundFreq.BLOSUM62, 62)
  expected_results = [
      2.600772755511218, 3.701459971291624,
      2.978062025019379, 2.600772755511218,
      3.701459971291624, 2.978062025019379,
      1.9080924268751152, 2.0962702097053536,
      2.6466138175955565, 2.0251018493324033,
      1.930546105993442, 1.9080924268751152,
      3.701459971291624, 2.978062025019379,
      1.9080924268751152, 1.6558411539721825,
      2.458436034765318
    ]
  expected_results = [
    x / math.log(2) if x is not None else x
    for x in expected_results
  ]
  assert all(
    a == approx(b)
    for a, b in zip(results, expected_results)
  )

def test_entropy_without_gaps_and_without_clustering_and_blosum62():
  """
  Test shannon entropy.
  The expected results are computed with MIToS.jl package
  with no clustering and sequences with no gaps.
  """
  seqs = [
    "ACTACTATCTAGCTAGC",
    "ACTACTGATGCACTGTG",
    "ACTACTGATCTACTGAG"
  ]
  results = entropy(seqs, BackgroundFreq.BLOSUM62, None)
  expected_results = [
    2.600772755511218, 3.701459971291624,
    2.978062025019379, 2.600772755511218,
    3.701459971291624, 2.978062025019379,
    1.9648810564481947, 2.090021677052459,
    2.5826805054819815, 1.9951305298885254,
    1.9948192952726305, 1.9645698218323,
    3.701459971291624, 2.978062025019379,
    1.9648810564481947, 1.6282347912950568,
    2.3317767950416632
  ]
  expected_results = [
    x / math.log(2) if x is not None else x
    for x in expected_results
  ]
  assert all(
    a == approx(b)
    for a, b in zip(results, expected_results)
  )

def test_entropy_with_gaps_and_with_clustering_and_blosum62():
  """
  Test shannon entropy.
  The expected results are computed with MIToS.jl package
  with clustering at 50 percent.
  """
  seqs = [
    "-CTA-ACTGCTGACTTG",
    "--TACACTACTGACTTG",
    "---AAAGATGACTGAAC"
  ]
  results = entropy(seqs, BackgroundFreq.BLOSUM62, 50)
  expected_results = [
    None,
    3.701459971291624, 2.978062025019379,
    2.600772755511218, 2.331154325809874,
    2.600772755511218, 2.458436034765318,
    2.0962702097053536, 1.749930045387302,
    2.458436034765318, 2.0962702097053536,
    2.458436034765318, 2.0962702097053536,
    2.458436034765318, 2.0962702097053536,
    2.0962702097053536, 2.458436034765318
  ]
  expected_results = [
    x / math.log(2) if x is not None else x
    for x in expected_results
  ]
  assert all(
    a == approx(b) if a and b else a == b
    for a, b in zip(results, expected_results)
  )

def test_entropy_with_gaps_and_without_clustering_and_blosum62():
  """
  Test shannon entropy.
  The expected results are computed with MIToS.jl package
  with no clustering and sequences with no gaps.
  """
  seqs = [
    "-CTA-ACTGCTGACTTG",
    "--TACACTACTGACTTG",
    "---AAAGATGACTGAAC"
  ]
  results = entropy(seqs, BackgroundFreq.BLOSUM62, None)
  expected_results = [
    None,
    3.701459971291624, 2.978062025019379,
    2.600772755511218, 2.457969182841476,
    2.600772755511218, 2.698361299019237,
    2.215784766888513, 1.6282347912950565,
    2.698361299019237, 2.215784766888513,
    2.3317767950416632, 2.090021677052459,
    2.698361299019237, 2.215784766888513,
    2.215784766888513, 2.3317767950416632
  ]
  expected_results = [
    x / math.log(2) if x is not None else x
    for x in expected_results
  ]
  assert all(
    a == approx(b) if a and b else a == b
    for a, b in zip(results, expected_results)
  )

def test_conservation_plot(test_data_folder):
  """
  Test conservation plot.
  Only tests that the file outfile file is created
  without errors. Cannot check file content.
  """
  expected_file = os.path.join(
    test_data_folder,
    "conservation_plot.png"
  )
  sequences = [
    "MGQACTGACTGACT--GTCGATACGACTGAC--",
    "MGQACTGACTGACT--GTCGAAACGACTG----",
    "MGQACTGACTGACT--FFCGAAACGACT-----",
    "MGNVITPKH----A--SDFGHKLWPVSS-----",
    "MGNVISPRH----A--SDFGHKLWPISS-----",
  ]
  if os.path.exists(expected_file):
    os.remove(expected_file)
  assert not os.path.exists(expected_file)
  plot_conservation(
    sequences = sequences,
    outfile=expected_file,
  )
  assert os.path.exists(expected_file)
  os.remove(expected_file)

  if os.path.exists(expected_file):
    os.remove(expected_file)
  assert not os.path.exists(expected_file)
  plot_conservation(
    sequences = sequences,
    outfile=expected_file,
    background_frq=BackgroundFreq.BLOSUM62
  )
  assert os.path.exists(expected_file)
  os.remove(expected_file)

  if os.path.exists(expected_file):
    os.remove(expected_file)
  assert not os.path.exists(expected_file)
  plot_conservation(
    sequences = sequences,
    outfile=expected_file,
    background_frq=BackgroundFreq.BLOSUM62,
    clustering_id = 50
  )
  assert os.path.exists(expected_file)
  os.remove(expected_file)
