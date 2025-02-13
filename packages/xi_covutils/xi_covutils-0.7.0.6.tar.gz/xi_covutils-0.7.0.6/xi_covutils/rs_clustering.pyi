"""
Type hints for rs_clustering.py
"""
from typing import Optional

# pylint: disable=too-few-public-methods
class IdentityCalculator:
  """
  Calculates Identity fraction between to sequences
  """
  def __init__(self):
    ...
  def identity_fraction(self, seq1:str, seq2:str) -> Optional[float]:
    """
    Calculates Identity fraction between to sequences
    """

class Gapstripper:
  """
  Class to strip gaps from sequences
  """
  def __init__(self) -> None:
    ...
  def gapstrip_sequence(self, sequence:str) -> str:
    """
    Strips gaps from a single sequence.
    """
  def gapstrip_sequences(self, sequences:list[str]) -> list[str]:
    """
    Strips gaps from multiple sequences.

    Args:
      sequences (list[str]): The input sequences.

    Returns:
      list[str]: The sequences with gaps removed.
    """

class Cluster:
  """
  Simple class to represent sequence clusters.
  """
  representative:Optional[str]
  representative_index:Optional[int]
  sequences:list[str]
  indexes:list[int]
  nseq:int
  def __init__(self) -> None:
    ...
  def __repr__(self) -> str:
    ...
  def add(self, sequence:str, index:int) -> None:
    """
    Adds a sequence to the cluster.

    Args:
      sequence (str): The sequence to be added.
      index (int): The index of the sequence.
    """

class Hobohm1:
  """
  Performs a sequence clustering using Hobohm algorithm 1.

  Implementation of clusternig algorithm 1 published in:
  Hobohm U, Scharf M, Schneider R, Sander C. Selection of representative protein
  data sets.
  Protein Sci. 1992;1(3):409-17.
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2142204/pdf/1304348.pdf

  Args:
    sequences (list[str]): Input sequences.
    identity_cutoff (float, optional): A float between 0 and 1, used as cutoff
      for including a new sequence in a cluster. . Defaults to 0.62.
    use_gapstrip (bool, optional): If True, columns of all sequences that are
      gaps in every sequence are removed. This not affect the results
      and may improve the performance. Defaults to False.
    use_c_extension (bool, optional): If true, C language extension is used to
      compute sequence identity. If False, pure python implementation is used.
      Defaults to True.
    max_clusters (float, optional): The max number of clusters to return.
      Defaults to float('inf').

  Returns:
    list[Cluster]: A list of clusters.
  """
  def with_cutoff(self, cutoff:float):
    """
    Sets the identity cutoff for clustering.

    Args:
      cutoff (float): A float between 0 and 1, used as cutoff
        for including a new sequence in a cluster. . Defaults to 0.62.
    """
  def get_clusters(self) -> list[Cluster]:
    """
    Returns the clusters after clustering.

    Returns:
      list[Cluster]: A list of clusters.
    """
  def with_sequences(self, sequences:list[str]):
    """
    Sets the sequences to clusterize.
    """
  def with_max_clusters(self, max_clusters:float):
    """
    Sets the maximum number of clusters to return.
    """

class KmerClustering:
  """
  Makes a simple sequence clustering bases on kmer content.

  The kmers identity of two sequence is the number of equal kmers divided by
  the number of kmers of the sequence that has fewer kmers.
  Repeated kmers in a sequences are counted once.
  """
  def __init__(self) -> None:
    """
    Creates a new KmerClustering object.
    """
  def with_kmer_length(self, kmer_length:int):
    """
    Sets the kmer length for clustering.

    Returns:
      KmerClustering: The updated KmerClustering object.
    """
  def with_cutoff(self, cutoff:float):
    """
    Sets the cutoff for clustering.

    Args:
      cutoff (float): A float greateer than 0, used as cutoff
        for including a new sequence in a cluster. Defaults to 0.05.
    """
  def compute_clusters(self, sequences:list[str]):
    """
    Computes the clusters based on the input sequences.

    Args:
      sequences (list[str]): The input sequences.
    """
  def get_clusters(self) -> list[Cluster]:
    """
    Returns the clusters after clustering.

    Returns:
      list[Cluster]: A list of clusters.
    """
  def take_clusters(self) -> list[Cluster]:
    """
    Returns the clusters after clustering and resets the object.

    Returns:
      list[Cluster]: A list of clusters.
    """
