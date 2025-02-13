"""
Function and classes to guess primer from sequences.
"""
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
import sys
from typing import Literal, Protocol, Union, cast, runtime_checkable

import click
import numpy as np
import pandas as pd
from typing_extensions import override

from xi_covutils.seqs.seq_collection import (
  BioAlphabet,
  BioSeq,
  SequenceCollection
)

class NucleicSequenceEnd(Enum):
  """
  The termini of a DNA sequence.
  """
  FIVEPRIME = 0
  THREEPRIME = 1

deg_indexes = list("ACGTMRWSYKVHDBN")
rev_indexes = list("ACMGRSVTWYHKDBN")

deg_bases = [
  ["A"], ["C"], ["G"], ["T"],
  ["A", "C"], ["A", "G"], ["A", "T"],
  ["C", "G"], ["C", "T"], ["G", "T"],
  ["A", "C", "G"], ["A", "C", "T"],
  ["A", "G", "T"], ["C", "G", "T"],
  ["A", "C", "G", "T"]
]
deg_bases = pd.Series(
  [np.array(x) for x in deg_bases],
  deg_indexes
)



@dataclass
class CountResult:
  """
  Represents the result of counting matches and mismatches for a primer.

  Attributes:
    primer (BioSeq): The primer sequence.
    matches (int): The number of matches found.
    mismatches (int): The number of mismatches found.
  """
  primer: BioSeq
  matches: int
  mismatches: int

class PrimerMatchCounter:
  """
  Count matches and mismatches of a primer to a collection of sequences.
  """
  def count(
    self,
    sequences:SequenceCollection,
    primer:BioSeq,
    end: NucleicSequenceEnd
  ) -> CountResult:
    """
    Count matches and mismatches of a primer to a collection of sequences.

    Args:
      sequences (SequenceCollection): A Sequence collection
      primer (BioSeq): A primer to check
      end (NucleicSequenceEnd): The end of the sequence to check the primer.

    Returns:
      CountResult: The result of the counts.
    """
    if end == NucleicSequenceEnd.THREEPRIME:
      primer = primer.reverse_complement()
    guess_seq = list(primer.sequence)
    sequence_extractor = EndSequenceExtractor.build(
      subsequence_length = len(guess_seq),
      end=end
    )
    seqs = [
      list(sequence_extractor.subsequence(s).sequence)
      for s in sequences
    ]
    deg_matrix = pd.DataFrame(
      [
        reversed([int(x) for x in (f"{i+1:04b}")])
        for i in range(15)
      ],
      columns = list("ACGT"),
      index = rev_indexes
    )
    guessed_matrix = deg_matrix.loc[guess_seq, :].to_numpy()
    matches = sum(
      (
        deg_matrix
          .loc[seq, :]
          .to_numpy() *
          guessed_matrix
      )
      .sum(axis=1)
      .prod()
      for seq in seqs
    )
    mismatches = len(sequences) - matches
    return CountResult(primer, matches, mismatches)
  def histogram(
    self,
    sequences:SequenceCollection,
    primer:BioSeq,
    end: NucleicSequenceEnd
  ) -> pd.Series:
    """
    Makes an histogram of mismatches of a primer to a collection of sequences.

    Args:
      sequences (SequenceCollection): A Sequence collection
      primer (BioSeq): A primer to check
      end (NucleicSequenceEnd): The end of the sequence to check the primer.

    Returns:
      CountResult: The result of the counts.
    """
    if end == NucleicSequenceEnd.THREEPRIME:
      primer = primer.reverse_complement()
    guess_seq = list(primer.sequence)
    sequence_extractor = EndSequenceExtractor.build(
      subsequence_length = len(guess_seq),
      end=end
    )
    seqs = [
      list(sequence_extractor.subsequence(s).sequence)
      for s in sequences
    ]
    deg_matrix = pd.DataFrame(
      [
        reversed([int(x) for x in (f"{i+1:04b}")])
        for i in range(15)
      ],
      columns = list("ACGT"),
      index = rev_indexes
    )
    guessed_matrix = deg_matrix.loc[guess_seq, :].to_numpy()
    mismatches = [
      np.count_nonzero(
        (
          deg_matrix
            .loc[seq, :]
            .to_numpy() *
            guessed_matrix
        )
        .sum(axis=1) == 0
      )
      for seq in seqs
    ]
    return pd.Series(mismatches).value_counts()

class PrimerGuesser:
  """
  Guess primer sequences from a collection of sequences.

  The primer guessed will start a 5' end or 3' end.
  """
  def __init__(
    self,
    end: NucleicSequenceEnd,
    primer_length:int,
    min_frq:float = 0.01
  ):
    self.end = end
    self.primer_length = primer_length
    self.sequence_estractor = EndSequenceExtractor.build(end, primer_length)
    if min_frq <0 or min_frq >=1:
      raise ValueError(f"min_frq should be in range [0, 1): {min_frq}")
    self.min_frq = min_frq


  def guess(self, sequences: SequenceCollection) -> BioSeq:
    """
    Guess a primer Sequence.

    Args:
      sequences (SequenceCollection): A collection of sequences.

    Returns:
      BioSeq: A BioSeq sequence representing the primer.
    """
    bases_df = (
      self
        .inspect(sequences)
        .apply(lambda x: x.mask(x<self.min_frq, 0))
        .apply(lambda x: x.mask(x>0, 1), axis=1)
        .apply(lambda x: x * np.array([1, 2, 4, 8]), axis=1)
        .apply(lambda x: x.sum()-1, axis=1)
        .apply(lambda x: rev_indexes[int(x)])
        .tolist()
    )
    seq = "".join(bases_df)
    if self.end == NucleicSequenceEnd.THREEPRIME:
      return BioSeq("primer", seq, BioAlphabet.DNA).reverse_complement()
    return BioSeq("primer", seq, BioAlphabet.DNA)

  def inspect(self, sequences: SequenceCollection) -> pd.DataFrame:
    """
    Computes bases frequencies for each position of the guessed primer.

    Args:
      sequences (SequenceCollection): A collection of sequences.

    Returns:
      pd.DataFrame: A Dataframe with the frequencies of each base at each
        position.
    """
    seqs = [
      list(self.sequence_estractor.subsequence(s).sequence)
      for s in sequences
    ]
    dataframe = pd.DataFrame(seqs)
    result = (
      dataframe.apply(
          lambda x:
            pd.Series(
              np.concatenate(deg_bases[x.tolist()].to_numpy())
                .flatten()
              )
              .value_counts(),
          axis=0
        )
        .fillna(0)
        .transpose()
        .apply(lambda x: x / sum(x), axis=1)
    )
    return cast(pd.DataFrame, result)

@runtime_checkable
class EndSequenceExtractor(Protocol):
  """
  End sequence extractor abstract class.
  """
  @abstractmethod
  def subsequence(self, seq: BioSeq) -> BioSeq:
    """
    Extract a subsequence from a BioSeq.
    """
  @staticmethod
  def build(
    end: NucleicSequenceEnd,
    subsequence_length: int
  ) -> "EndSequenceExtractor":
    """
    Builds a 5' sequence extractor or a 3' sequence extractor.

    Args:
      end (NucleicSequenceEnd): _description_
      subsequence_length (int): _description_

    Returns:
        EndSequenceExtractor: _description_
    """
    if end == NucleicSequenceEnd.FIVEPRIME:
      return FivePrimeSequenceExtractor(subsequence_length)
    return ThreePrimeSequenceExtractor(subsequence_length)

class FivePrimeSequenceExtractor(EndSequenceExtractor):
  """
  A 5's sequence extractor.
  """
  def __init__(self, subsequence_length:int):
    self.subsequence_length = subsequence_length
  @override
  def subsequence(self, seq: BioSeq) -> BioSeq:
    new_seq = seq.sequence[0:self.subsequence_length]
    return BioSeq(seq.identifier, new_seq, seq.alphabet)

class ThreePrimeSequenceExtractor(EndSequenceExtractor):
  """
  A 3's sequence extractor.
  """
  def __init__(self, subsequence_length:int):
    self.subsequence_length = subsequence_length
  @override
  def subsequence(self, seq: BioSeq) -> BioSeq:
    new_seq = seq.sequence[-self.subsequence_length:]
    return BioSeq(seq.identifier, new_seq, seq.alphabet)

SeqType = Union[Literal["fasta"], Literal["fastq"]]
@click.command()
@click.argument(
  'sequence_file',
  type=click.Path(exists=True),
)
@click.argument(
  'outfile',
  type=click.Path(),
)
@click.option(
  "--seq-type",
  default = "fasta",
  help="Input file type. Default: fasta",
  type=click.Choice(["fasta", "fastq"], case_sensitive=False)
)
@click.option(
  "--end",
  default = "both",
  help="Sequence end to search for primers. Default: both",
  type=click.Choice(["5", "3", "both"], case_sensitive=False)
)
@click.option(
  "--length",
  default = 20,
  help="Primer length",
  type=click.INT
)
@click.option(
  "--min-frq",
  default = 0.01,
  help="Minimum frequency for a base to be included in the primer sequence.",
  type=click.FLOAT
)
# pylint: disable=too-many-arguments
def guess(
  sequence_file: str,
  outfile:str,
  seq_type: str = "fasta",
  end:str = "both",
  length:int = 20,
  min_frq:float = 0.01
):
  """
  Guess primers from sequence.
  """
  seq_type = seq_type.lower()
  if seq_type not in ("fasta", "fastq"):
    sys.exit("Invalid sequence type")
  if seq_type == "fasta":
    seqs = SequenceCollection.from_fasta(sequence_file)
  if seq_type == "fastq":
    seqs = SequenceCollection.from_fastq(sequence_file)
  seq_end = end.lower()
  if seq_end not in ("5", "3", "both"):
    sys.exit("Invalid sequence type")
  if seq_end == "both":
    seq_end = [NucleicSequenceEnd.FIVEPRIME, NucleicSequenceEnd.THREEPRIME]
  elif seq_end == "5":
    seq_end = [NucleicSequenceEnd.FIVEPRIME]
  else:
    seq_end = [NucleicSequenceEnd.THREEPRIME]
  result = []
  for c_end in seq_end:
    guesser = PrimerGuesser(c_end, length, min_frq)
    primer = guesser.guess(seqs)
    primer.identifier = f"{primer.identifier}.{c_end}"
    result.append(primer)
  result_seq = SequenceCollection(result)
  result_seq.to_fasta(outfile)

@click.command()
@click.argument(
  'sequence_file',
  type=click.Path(exists=True),
)
@click.argument(
  'outfile',
  type=click.Path(),
)
@click.argument("primer")
@click.option(
  "--seq-type",
  default = "fasta",
  help="Input file type. Default: fasta",
  type=click.Choice(["fasta", "fastq"], case_sensitive=False)
)
@click.option(
  "--end",
  default = "both",
  help="Sequence end to search for primers. Default: both",
  type=click.Choice(["5", "3", "both"], case_sensitive=False)
)
# pylint: disable=too-many-arguments
def mismatch_histogram(
  sequence_file: str,
  outfile:str,
  primer:str,
  seq_type: str = "fasta",
  end:str = "5",
):
  """
  Makes an histogram of mismatches of guessed primers.
  """
  seq_type = seq_type.lower()
  if seq_type not in ("fasta", "fastq"):
    sys.exit("Invalid sequence type")
  if seq_type == "fasta":
    seqs = SequenceCollection.from_fasta(sequence_file)
  if seq_type == "fastq":
    seqs = SequenceCollection.from_fastq(sequence_file)
  seq_end = end.lower()
  if seq_end not in ("5", "3"):
    sys.exit("Invalid sequence type")
  elif seq_end == "5":
    seq_end = NucleicSequenceEnd.FIVEPRIME
  else:
    seq_end = NucleicSequenceEnd.THREEPRIME
  c_primer = BioSeq(f"primer.{seq_end}", primer, BioAlphabet.DNA)
  counter = PrimerMatchCounter()
  counts = counter.histogram(seqs, c_primer, seq_end)
  counts = counts.sort_index()
  counts.to_csv(outfile, header = False)

@click.command()
@click.argument(
  'sequence_file',
  type=click.Path(exists=True),
)
@click.argument(
  'outfile',
  type=click.Path(),
)
@click.argument("primer")
@click.option(
  "--seq-type",
  default = "fasta",
  help="Input file type. Default: fasta",
  type=click.Choice(["fasta", "fastq"], case_sensitive=False)
)
@click.option(
  "--end",
  default = "both",
  help="Sequence end to search for primers. Default: both",
  type=click.Choice(["5", "3", "both"], case_sensitive=False)
)
# pylint: disable=too-many-arguments
def count_matches(
  sequence_file: str,
  outfile:str,
  primer:str,
  seq_type: str = "fasta",
  end:str = "5",
):
  """
  Count matches and mismatches of guessed primers.
  """
  seq_type = seq_type.lower()
  if seq_type not in ("fasta", "fastq"):
    sys.exit("Invalid sequence type")
  if seq_type == "fasta":
    seqs = SequenceCollection.from_fasta(sequence_file)
  if seq_type == "fastq":
    seqs = SequenceCollection.from_fastq(sequence_file)
  seq_end = end.lower()
  if seq_end not in ("5", "3", "both"):
    sys.exit("Invalid sequence type")
  if seq_end == "both":
    seq_end = [NucleicSequenceEnd.FIVEPRIME, NucleicSequenceEnd.THREEPRIME]
  elif seq_end == "5":
    seq_end = [NucleicSequenceEnd.FIVEPRIME]
  else:
    seq_end = [NucleicSequenceEnd.THREEPRIME]
  result: list[CountResult] = []
  for c_end in seq_end:
    c_primer = BioSeq(f"primer.{c_end}", primer, BioAlphabet.DNA)
    counter = PrimerMatchCounter()
    counts = counter.count(seqs, c_primer, c_end)
    result.append(counts)
  pd.DataFrame(
    [
      (
        res.primer.identifier,
        res.primer.sequence,
        res.matches,
        res.mismatches
      )
      for res in result
    ],
    columns = ["Identifier", "sequence", "matches", "mismatches"]
  ).to_csv(outfile)
@click.command()
@click.argument(
  'sequence_file',
  type=click.Path(exists=True),
)
@click.argument(
  'outfile',
  type=click.Path(),
)
@click.option(
  "--seq-type",
  default = "fasta",
  help="Input file type. Default: fasta",
  type=click.Choice(["fasta", "fastq"], case_sensitive=False)
)
@click.option(
  "--end",
  default = "5",
  help="Sequence end to search for primers. Default: 5",
  type=click.Choice(["5", "3"], case_sensitive=False)
)
@click.option(
  "--length",
  default = 20,
  help="Primer length",
  type=click.INT
)
def inspect(
  sequence_file: str,
  outfile:str,
  seq_type: str = "fasta",
  end:str = "5",
  length:int = 20
):
  """
  Guess primers from sequence.
  """
  seq_type = seq_type.lower()
  if seq_type not in ("fasta", "fastq"):
    sys.exit("Invalid sequence type")
  if seq_type == "fasta":
    seqs = SequenceCollection.from_fasta(sequence_file)
  if seq_type == "fastq":
    seqs = SequenceCollection.from_fastq(sequence_file)
  seq_end = end.lower()
  if seq_end not in ("5", "3"):
    sys.exit("Invalid sequence type")
  elif seq_end == "5":
    seq_end = NucleicSequenceEnd.FIVEPRIME
  else:
    seq_end = NucleicSequenceEnd.THREEPRIME
  guesser = PrimerGuesser(seq_end, length)
  freqs = guesser.inspect(seqs)
  freqs.to_csv(outfile)
