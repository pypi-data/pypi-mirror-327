"""
  Benchmark of clustering function
"""
from random import choice
from random import random as rand
import pytest
from xi_covutils import auxl
from xi_covutils.clustering import hobohm1
from xi_covutils.clustering import sequence_identity
from xi_covutils.clustering import kmer_clustering

@pytest.mark.parametrize("length", [100, 1000, 2000])
def test_identity_fraction(benchmark, length):
  """
  Benchmarks the time response to compare two sequences in function of the
  length of the sequence.
  """
  letters = ["A", "C", "T", "G", "-"]
  seq1 = "".join([choice(letters) for _ in range(length)])
  seq2 = "".join([choice(letters) for _ in range(length)])
  #pylint: disable=c-extension-no-member
  benchmark.pedantic(auxl.identity_fraction, args=(seq1, seq2), rounds=10)

@pytest.mark.parametrize("length", [100, 1000, 2000])
def test_sequence_identity(benchmark, length):
  """
  Benchmarks the time response to compare two sequences in function of the
  length of the sequence.
  """
  letters = ["A", "C", "T", "G", "-"]
  seq1 = "".join([choice(letters) for _ in range(length)])
  seq2 = "".join([choice(letters) for _ in range(length)])
  benchmark.pedantic(sequence_identity, args=(seq1, seq2), rounds=10)

@pytest.mark.parametrize("length", [100, 500, 1000, 2000, 5000])
def test_hobohm1_by_length(benchmark, length):
  """
  Benchmarks hobohm1 algorithm
  """
  letters = ["A", "C", "T", "G", "-"]
  height = 100
  seqs = ["".join([choice(letters) for _ in range(length)])
      for _ in range(height)]
  benchmark.pedantic(hobohm1, args=(seqs, 0.5), rounds=3)

@pytest.mark.parametrize("height", [100, 200, 400, 800])
def test_hobohm1_by_height(benchmark, height):
  """
  Benchmarks hobohm1 algorithm
  """
  letters = ["A", "C", "T", "G", "-"]
  length = 100
  seqs = ["".join([choice(letters) for _ in range(length)])
      for _ in range(height)]
  benchmark.pedantic(hobohm1, args=(seqs, 0.5), rounds=3)

@pytest.mark.parametrize("p_id", [0.2, 0.4, 0.6, 0.8])
def test_hobohm1_by_id(benchmark, p_id):
  """
  Benchmarks hobohm1 algorithm.
  """
  letters = ["A", "C", "T", "G", "-"]
  length = 100
  height = 400
  seqs = ["".join([choice(letters) for _ in range(length)])
      for _ in range(height)]
  benchmark.pedantic(hobohm1, args=(seqs, p_id), rounds=3)

@pytest.mark.parametrize("use_gapstrip", [True, False])
def test_hobohm1_gapstrip(benchmark, use_gapstrip):
  """
  Benchmarks hobohm1 algorithm.
  """
  letters = ["A", "C", "T", "G", "-", "-", "-"]
  # Want to create sequences with many gaps
  length = 5000
  height = 200
  seqs = ["".join([choice(letters) for _ in range(length)])
      for _ in range(height)]
  benchmark.pedantic(hobohm1, args=(seqs, 0.62, use_gapstrip), rounds=3)

@pytest.mark.parametrize("use_c_extension", [True, False])
def test_hobohm1_c(benchmark, use_c_extension):
  """
  Benchmarks hobohm1 algorithm.
  """
  letters = ["A", "C", "T", "G", "-"]
  length = 5000
  height = 200
  seqs = ["".join([choice(letters) for _ in range(length)])
      for _ in range(height)]
  benchmark.pedantic(hobohm1, args=(seqs, 0.62, True, use_c_extension), rounds=3)

@pytest.mark.parametrize("kmer_length", range(3, 6))
def test_kmer_clustering(benchmark, kmer_length):
  """
  Benchmarks kmer_clustering algorithm.
  """
  letters = [
    "A", "C", "T", "G", "Q",
    "W", "E", "R", "Y", "I",
    "P", "S", "D", "F", "H",
    "K", "L", "V", "N", "M"]
  length = 5000
  height = 200
  seqs = ["".join([choice(letters) for _ in range(length)])
      for _ in range(height)]
  benchmark.pedantic(kmer_clustering, args=(seqs, kmer_length, 0.62), rounds=3)

@pytest.mark.parametrize("kmer_length", range(3, 6))
def test_kmer_clustering_hierarchy(benchmark, kmer_length):
  """
  Benchmarks kmer_clustering algorithm.
  """
  letters = [
    "A", "C", "T", "G", "Q",
    "W", "E", "R", "Y", "I",
    "P", "S", "D", "F", "H",
    "K", "L", "V", "N", "M"]
  length = 5000
  seqs = hierarchy_seqs("".join([choice(letters) for _ in range(length)]), 0.06)
  benchmark.pedantic(kmer_clustering, args=(seqs, kmer_length, 0.62), rounds=3)

@pytest.mark.parametrize('generations', [5, 6, 7, 8, 9, 10])
@pytest.mark.parametrize('length', [100, 200, 400, 800, 1600, 3200])
def test_kmer_clustering_hierarchy_width_vs_height(
    benchmark,
    generations,
    length
  ):
  """
  Benchmarks kmer_clustering algorithm.
  """
  letters = [
    "A", "C", "T", "G", "Q",
    "W", "E", "R", "Y", "I",
    "P", "S", "D", "F", "H",
    "K", "L", "V", "N", "M"]
  # length = 5000
  kmer_length = 3
  seqs = hierarchy_seqs(
    "".join(
      [choice(letters) for _ in range(length)]
    ),
    0.06,
    generations
  )
  benchmark.pedantic(kmer_clustering, args=(seqs, kmer_length, 0.62), rounds=3)


def mut_seq(seq, mut_prob, alphabet):
  """
  Mutate a protein sequence
  """
  return "".join([choice(alphabet) if rand() < mut_prob else c
          for c in seq])

def hierarchy_seqs(seed, mut_prob, generations=8):
  """
  Create a collection of sequences in a hierarchy mutating a sequence
  in the root of the hierarchy.
  """
  current_sequences = [seed]
  new_sequences = []
  alphabet = "QWERTYIOASDFGHKLCVNM"
  while generations > 0:
    new_sequences.extend(
      [
        mut_seq(seq, mut_prob, alphabet)
        for seq in current_sequences
        for _ in range(2)
      ]
    )
    current_sequences = new_sequences
    new_sequences = []
    generations -= 1
  return current_sequences

def test_hierarchy_seqs():
  """
  Check the number of sequences in generated hierarchies.
  """
  seq1 = "QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ"
  new_seqs = hierarchy_seqs(seq1, 0.05, 1)
  assert len(new_seqs) == 2

  seq1 = "QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ"
  new_seqs = hierarchy_seqs(seq1, 0.05, 2)
  assert len(new_seqs) == 4

  seq1 = "QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ"
  new_seqs = hierarchy_seqs(seq1, 0.05, 3)
  assert len(new_seqs) == 8

  seq1 = "QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ"
  new_seqs = hierarchy_seqs(seq1, 0.05, 8)
  assert len(new_seqs) == 256


def test_mut_seq():
  """
  Test mutate sequence.
  """
  seq1 = "QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ"
  alphabet = "QWERTYIOASDFGHKLCVNM"
  seq2 = mut_seq(seq1, 0, alphabet)
  assert seq1 == seq2
  alphabet = "M"
  seq2 = mut_seq(seq1, 1, alphabet)
  assert seq2 == "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
