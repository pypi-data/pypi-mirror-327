"""
Clustering functions
"""
from collections import defaultdict
from typing import List, Optional

from xi_covutils import rs_clustering

from xi_covutils.msa import gapstrip_sequences

class Cluster(): # pylint: disable=too-few-public-methods
  """
  Simple class to represent sequence clusters.
  """
  def __init__(self):
    self.representative:Optional[str] = None
    self.representative_index:Optional[int] = None
    self.sequences = []
    self.indexes = []
    self.nseq = 0
  def __repr__(self):
    return (
      "Cluster:"
      f"[{self.nseq}]"
      f"[{self.representative}]"
      f" {', '.join(self.sequences)}"
    )

# pylint: disable=too-many-locals
def hobohm1(
    sequences:list[str],
    identity_cutoff:float=0.62,
    use_gapstrip:bool=False,
    use_c_extension:bool=True,
    max_clusters:float=float('inf')
  ) -> list[Cluster] :
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
  def rust_cluster_to_python_cluster(cluster: rs_clustering.Cluster):
    py_cl = Cluster()
    py_cl.representative = cluster.representative
    py_cl.representative_index = cluster.representative_index
    py_cl.sequences = cluster.sequences
    py_cl.indexes = cluster.indexes
    py_cl.nseq = cluster.nseq
    return py_cl
  if use_c_extension:
    hobohm1_cl = rs_clustering.Hobohm1()
    hobohm1_cl.with_cutoff(identity_cutoff)
    hobohm1_cl.with_sequences(sequences)
    hobohm1_cl.with_max_clusters(max_clusters)
    clusters = hobohm1_cl.get_clusters()
    new_clusters = [
      rust_cluster_to_python_cluster(cl) for cl in clusters
    ]
    return new_clusters
  select: List[Cluster] = []
  sequences = gapstrip_sequences(sequences) if use_gapstrip else sequences
  id_function = sequence_identity
  for i, seq in enumerate(sequences):
    should_add_new_cluster = True
    add_to_cluster = None
    for clu in select:
      representative = clu.representative
      if not representative:
        continue
      identity = id_function(seq, representative)
      if identity and identity >= identity_cutoff:
        should_add_new_cluster = False
        add_to_cluster = clu
        break
    if should_add_new_cluster:
      cluster = Cluster()
      cluster.representative = seq
      cluster.representative_index = i
      cluster.sequences.append(seq)
      cluster.indexes.append(i)
      cluster.nseq = 1
      select.append(cluster)
    if add_to_cluster:
      add_to_cluster.sequences.append(seq)
      add_to_cluster.indexes.append(i)
      add_to_cluster.nseq += 1
    if len(select) >= max_clusters:
      break
  return select

def sequence_identity(seq1:str, seq2:str) -> float:
  """
  Computes sequence identity for two sequences.

  Lower and upper case characters are assumed to be different.
  Gapped positions in both sequences are not considered for the calculation.

  Args:
    seq1 (str): A sequence.
    seq2 (str): A sequence.

  Raises:
    ValueError: If sequences have different lengths.

  Returns:
    float: A value between 0.0 (dissimilar sequences) and 1.0 (identical
      sequences).

  """
  if not len(seq1) == len(seq2):
    raise ValueError("Sequence length is not equal")
  equals = 0
  total = 0
  for i, char_a in enumerate(seq1):
    char_b = seq2[i]
    if not (char_a in ("-", ".") and (char_b in ("-", "."))):
      total += 1
      if char_a == char_b:
        equals += 1
  return float(equals) / max(1, total)

def _build_kmers(sequence, kmer_size=3):
  return {sequence[x:y] for x, y in zip(
    range(len(sequence)), range(kmer_size, len(sequence)+1))}

def _build_kmer_map(kmers):
  result = defaultdict(set)
  for seq_id, kmer_set in kmers.items():
    for kmer in kmer_set:
      result[kmer].add(seq_id)
  return result

def _closest_kmer(kmer_set, exclude, kmers_map, seq_map, include):
  index_counter = defaultdict(int)
  max_index = None
  max_count = 0
  for kmer in kmer_set:
    seq_indexes = (kmers_map[kmer]-{exclude}) & include
    for s_index in seq_indexes:
      index_counter[s_index] += 1
      if index_counter[s_index] > max_count:
        max_count = index_counter[s_index]
        max_index = s_index
  if max_index is not None:
    return (
      max_index,
      float(index_counter[max_index])
      / min(len(kmer_set), len(seq_map[max_index]))
    )
  return None

def kmer_clustering(
    sequences: List[str],
    kmer_length:int=3,
    identity_cutoff:float=0.62
  ) -> list[Cluster]:
  """
  Makes a simple sequence clustering bases on kmer content.

  The kmers identity of two sequence is the number of equal kmers divided by
  the number of kmers of the sequence that has fewer kmers.
  Repeated kmers in a sequences are counted once.

  Args:
    sequences (List[str]): A list of sequences.
    kmer_length (int, optional): The Kmer length. Defaults to 3.
    identity_cutoff (float, optional): Kmer cutoff value for sequences in the
      same cluster. Defaults to 0.62.

  Returns:
    list[Cluster]: A list of clusters.
  """
  sequences_map = dict(enumerate(sequences))
  seq_map = {
    x: _build_kmers(seq, kmer_length)
    for x, seq in sequences_map.items()
  }
  kmer_map = _build_kmer_map(seq_map)
  cluster_map = defaultdict(Cluster)
  for i, kmers in seq_map.items():
    closest = _closest_kmer(
      kmers, i, kmer_map, seq_map, cluster_map.keys()
    )
    if (
        closest is not None and
        closest[0] in cluster_map and
        closest[1] >= identity_cutoff
    ):
      cluster_map[closest[0]].sequences.append(sequences_map[i])
      cluster_map[closest[0]].nseq += 1
      cluster_map[i] = cluster_map[closest[0]]
    else:
      cluster_map[i].sequences.append(sequences_map[i])
      cluster_map[i].representative_index = i
      cluster_map[i].nseq = 1
  result:List[Cluster] = []
  visited = set()
  for cluster in cluster_map.values():
    if cluster.representative_index not in visited:
      visited.add(cluster.representative_index)
      result.append(cluster)
  for res in result:
    if res.representative_index is None:
      res.representative = None
      continue
    res.representative = sequences_map[res.representative_index]
  return result
