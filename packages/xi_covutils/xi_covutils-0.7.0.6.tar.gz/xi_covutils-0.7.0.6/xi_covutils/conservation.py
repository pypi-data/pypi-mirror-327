"""
Computes conservation for a collection of protein sequences.
"""

import math
from collections import defaultdict
from typing import Dict, List, Optional
from enum import Enum
import matplotlib.pyplot as plt
import click
from xi_covutils.clustering import hobohm1
from xi_covutils.matrices.common import RESIDUE_ORDER_MAP
from xi_covutils.matrices.blosum_45 import BLOSUM_45_BG
from xi_covutils.matrices.blosum_50 import BLOSUM_50_BG
from xi_covutils.matrices.blosum_62 import BLOSUM_62_BG
from xi_covutils.matrices.blosum_80 import BLOSUM_80_BG
from xi_covutils.matrices.blosum_90 import BLOSUM_90_BG
from xi_covutils.msa._msa import gap_content_by_column, read_msa

def _replace_non_standard_aa(seq_data: List[str]) -> List[str]:
  allowed_chars = set("QWERTYIPASDFGHKLCVNM-")
  return [
    "".join(
      [
        c if c in allowed_chars else "-"
        for c in seq.upper()
      ]
    )
    for seq in seq_data
  ]

def _count_table(
    sequences: List[str],
    clustering_id=None
  ) -> Dict[int, Dict[str, float]]:
  counts:Dict[int, Dict[str, float]] = defaultdict(
    lambda: defaultdict(lambda: 0)
  )
  if clustering_id:
    clusters = hobohm1(
      sequences=sequences,
      identity_cutoff=float(clustering_id)/100
    )
    weigths = {
      i:float(1) / len(c.indexes)
      for c in clusters
      for i in c.indexes
    }
  else:
    weigths = defaultdict(lambda: 1)
  for i, seq in enumerate(sequences):
    for col, char in enumerate(seq):
      char = char.upper()
      if char != "-":
        counts[col][char] += weigths[i]
  return counts

def _counts_by_column(
    count_table: Dict[int, Dict[str, float]]
  ) -> Dict[int, float]:
  return {
    col: sum(chars.values())
    for col, chars in count_table.items()
  }

def _frequency_table(
    count_table: Dict[int, Dict[str, float]]
  ) -> Dict[int, Dict[str, float]]:
  sums = _counts_by_column(count_table)
  return  {
    col: {
      char: float(count) / sums[col]
      for char, count in chars.items()
    }
    for col, chars in count_table.items()
  }

class BackgroundFreq(Enum):
  """
  Types of amino acid background frequency.
  """
  UNIFORM = 1
  BLOSUM45 = 2
  BLOSUM50 = 3
  BLOSUM62 = 4
  BLOSUM80 = 5
  BLOSUM90 = 6

def get_background_frequencies(mat: BackgroundFreq) -> Optional[List[float]]:
  """
  Retrieves amino acid background frequency vectors given a substitution matrix.

  Args:
    mat (BackgroundFreq): A subsitution matrix.

  Returns:
    List[float]: A list with the background frequencies for each amino acid,
      according to different substitution matrices.
  """
  freq = None
  if mat == BackgroundFreq.UNIFORM:
    freq = [1.0] * 20
  if mat == BackgroundFreq.BLOSUM45:
    freq =  BLOSUM_45_BG
  if mat == BackgroundFreq.BLOSUM50:
    freq =  BLOSUM_50_BG
  if mat == BackgroundFreq.BLOSUM62:
    freq =  BLOSUM_62_BG
  if mat == BackgroundFreq.BLOSUM80:
    freq =  BLOSUM_80_BG
  if mat == BackgroundFreq.BLOSUM90:
    freq =  BLOSUM_90_BG
  return freq

def entropy(
    seq_data: List[str],
    background_frq: BackgroundFreq = BackgroundFreq.UNIFORM,
    clustering_id: Optional[float] = None,
    max_diff: bool = True
  ) -> List[Optional[float]]:
  """
  Computes Shannon entropy for a collection of proteins.
  The calculation of Shannon entropy and Kullback/Leiber divergence for entropy
  correction is made using base 2 logarhytms. Therefore, the scores are bits.

  Args:
    seq_data (List[str]): Is a collection of protein sequences.
    background_frq (BackgroundFreq, optional): Is a BackgroundFreq enum value,
      indicating which substitution matrix is used to correct the entropy
      values. Defaults to BackgroundFreq.Uniform, that does not do any
      correction of Shannon Entropy,
    clustering_id (float, optional): A percentage to make a clustering of
      sequences previous to the calculation of Entropy. Defaults to None, no
      clustering is done.
    max_diff (bool): Only used with background_frq = BackgroundFreq.Uniform.
      The values returned are the difference between the maximum entropy and the
      actual entropy. This makes bigger values are more conserved. Defaults to
      True.

  Returns:
    List[float]: A list conservation scores in bits.
  """
  def _build_background_mapping(
        background_frq: List[float]
      ) -> Dict[str, float]:
    return  {
      aa: background_frq[order]
      for aa, order in RESIDUE_ORDER_MAP.items()
    }
  if not seq_data:
    return []
  seq_data = _replace_non_standard_aa(seq_data)
  bgfreqs = get_background_frequencies(background_frq)
  if not bgfreqs:
    return []
  background = _build_background_mapping(bgfreqs)
  sign = -1 if background_frq == BackgroundFreq.UNIFORM else 1
  ncols = len(seq_data[0])
  counts = _count_table(
    sequences=seq_data,
    clustering_id=clustering_id
  )
  freqs = _frequency_table(counts)
  entropy_values = [
    sign * float(
      sum(
        (
          freq * math.log2(freq / background[char])
          for char, freq in freqs[col].items()
        )
      )
    ) if col in freqs else None
    for col in range(ncols)
  ]
  if max_diff and background_frq == BackgroundFreq.UNIFORM:
    entropy_values = [
      (math.log2(20) - x) if x is not None else x
      for x in entropy_values
    ]
  return entropy_values

# pylint: disable=too-many-locals
def plot_conservation(
    sequences: List[str],
    background_frq: BackgroundFreq = BackgroundFreq.UNIFORM,
    clustering_id: Optional[float] = None,
    outfile: str = "plot_conservation.png",
    with_caption: bool = True
  ):
  """
  Generate
  Args:
    seq_data (List[str]): Is a collection of protein sequences.
    background_frq (BackgroundFreq, optional): Is a BackgroundFreq enum value,
    indicating which substitution matrix is used to correct the entropy
    values. Defaults to BackgroundFreq.Uniform, that does not do any
    correction of Shannon Entropy,
    clustering_id (float, optional): A percentage to make a clustering of
    sequences previous to the calculation of Entropy. Defaults to None, no
    clustering is done.
    outfile (str): The output file.
  """
  def _shannon_caption() -> str:
    return (
      "Conservation is calculated as the difference of Maximum Shannon "
      "Entropy\n"
      "for the amino acid alphabet and the actual Shannon Entropy."
    )
  def _blosum_caption(perc: int) -> str:
    return (
      "Conservation is calculated as the Shannon Entropy relative to \n"
      "(Kullback-Leibler) amino acid background frequencies derived from the \n"
      f"BLOSUM {str(perc)} substitution matrix."
    )
  def _get_xlabel(
      with_caption:bool,
      bg_frq: BackgroundFreq,
      clustering_id: Optional[float]
    ):
    base_label = "Amino acid position"
    if not with_caption:
      return base_label
    xlabel = ""
    if bg_frq == BackgroundFreq.UNIFORM:
      xlabel = _shannon_caption()
    if bg_frq == BackgroundFreq.BLOSUM45:
      xlabel = _blosum_caption(45)
    if bg_frq == BackgroundFreq.BLOSUM50:
      xlabel = _blosum_caption(50)
    if bg_frq == BackgroundFreq.BLOSUM62:
      xlabel = _blosum_caption(62)
    if bg_frq == BackgroundFreq.BLOSUM80:
      xlabel = _blosum_caption(80)
    if bg_frq == BackgroundFreq.BLOSUM90:
      xlabel = _blosum_caption(90)
    if clustering_id:
      xlabel = (
        f"{xlabel}\nSequences where clustered at {clustering_id} % identity."
      )
    return f"{base_label}\n\n{xlabel}"
  data = entropy(
    seq_data = sequences,
    background_frq = background_frq,
    clustering_id = clustering_id
  )
  fig, host = plt.subplots(figsize=(16,9))
  axes2 = host.twinx()
  host.set_ylabel("Conservation (bits)", fontsize = 16)
  host.set_title("Conservation Entropy", fontsize = 18)
  host.set_xlabel(
    _get_xlabel(with_caption, background_frq, clustering_id),
    fontsize=16
  )
  cons_plot = host.plot(
    [x+1 for x in range(len(data))],
    data,
    label = "Conservation",
    color = "red"
  )
  host.set_xlim(0, len(data)+1)
  max_value = max(x for x in data if x is not None)
  min_value = min(x for x in data if x is not None)
  if background_frq == BackgroundFreq.UNIFORM:
    host.set_ylim(0, math.log2(20)+.1)
  else:
    host.set_ylim(min_value-0.1, max_value+0.1)
  scatter_plot = []
  if any(x is None for x in data):
    scatter_plot = axes2.scatter(
      [i+1 for i,x in enumerate(data) if x is None],
      [1 for x in data if x is None],
      label = "All gap columns",
      color = "green"
    )
    scatter_plot = [scatter_plot]
  gap_frq = gap_content_by_column(sequences)
  gap_plot = axes2.plot(
    [x+1 for x in range(len(gap_frq))],
    gap_frq,
    label = "Gap frequency",
    color = "blue"
  )
  host.legend(
    cons_plot + gap_plot + scatter_plot,
    ["Conservation", "Gap frequency", "All Gap Columns"]
  )
  fig.tight_layout()
  fig.savefig(outfile)

@click.command()
@click.argument('filename', default=None)
@click.option('--blosum', default=None)
@click.option('--clustering', default=None)
@click.option('--maxdiff/--no-maxdiff', default=True)
def calculate_conservation(filename, blosum, clustering, maxdiff):
  """
  Calculates conservation of a protein MSA.

  Args:
      filename (str): the input fasta MSA.
  """
  print("# Conservation")
  print(f"# Input filename: {filename}")
  if clustering:
    print(f"# Clustering weighting at {clustering}% id.")
  else:
    print("# No clustering weighting.")
  records = read_msa(filename, msa_format="fasta")
  bg_frq = None
  if not blosum:
    bg_frq = BackgroundFreq.UNIFORM
    if maxdiff:
      print("# Values = Max_Entropy - Shannon_Entropy")
  if blosum == 45:
    bg_frq = BackgroundFreq.BLOSUM45
    print("# Corrected with BLOSUM 45")
  if blosum == 50:
    bg_frq = BackgroundFreq.BLOSUM50
    print("# Corrected with BLOSUM 50")
  if blosum == 62:
    bg_frq = BackgroundFreq.BLOSUM62
    print("# Corrected with BLOSUM 62")
  if blosum == 80:
    bg_frq = BackgroundFreq.BLOSUM80
    print("# Corrected with BLOSUM 80")
  if blosum == 90:
    bg_frq = BackgroundFreq.BLOSUM90
    print("# Corrected with BLOSUM 90")
  sequences = [
    seq for _, seq in records
  ]
  if not bg_frq:
    print("# Error: No background frequencies.")
    return
  cons = entropy(
    sequences,
    background_frq=bg_frq,
    clustering_id=clustering,
    max_diff = maxdiff
  )
  gap_frq = gap_content_by_column(sequences)
  print("# Columns:")
  print("# Position, Conservation, Shannon Entropy")
  for i, (con, gap) in enumerate(zip(cons, gap_frq)):
    print(f"{i+1}, {con}, {gap}")

@click.command()
@click.argument('filename', default=None)
@click.option('--blosum', default=None)
@click.option('--clustering', default=None)
@click.option('--outfile', default="conservation_plot.png")
@click.option('--with-caption/--with-no-caption', default=True)
def conservation_plot(filename, blosum, clustering, outfile, with_caption):
  """
  Calculates conservation of a protein MSA.

  Args:
      filename (str): the input fasta MSA.
  """
  print("# Conservation")
  print(f"# Input filename: {filename}")
  if clustering:
    print(f"# Clustering weighting at {clustering}% id.")
  else:
    print("# No clustering weighting.")
  records = read_msa(filename, msa_format="fasta")
  bg_frq = None
  if not blosum:
    bg_frq = BackgroundFreq.UNIFORM
  if blosum == 45:
    bg_frq = BackgroundFreq.BLOSUM45
    print("# Corrected with BLOSUM 45")
  if blosum == 50:
    bg_frq = BackgroundFreq.BLOSUM50
    print("# Corrected with BLOSUM 50")
  if blosum == 62:
    bg_frq = BackgroundFreq.BLOSUM62
    print("# Corrected with BLOSUM 62")
  if blosum == 80:
    bg_frq = BackgroundFreq.BLOSUM80
    print("# Corrected with BLOSUM 80")
  if blosum == 90:
    bg_frq = BackgroundFreq.BLOSUM90
    print("# Corrected with BLOSUM 90")
  sequences = [
    seq for _, seq in records
  ]
  if not bg_frq:
    print("# Error: No background frequencies.")
    return
  plot_conservation(
    sequences = sequences,
    background_frq = bg_frq,
    clustering_id=clustering,
    outfile = outfile,
    with_caption = with_caption
  )
