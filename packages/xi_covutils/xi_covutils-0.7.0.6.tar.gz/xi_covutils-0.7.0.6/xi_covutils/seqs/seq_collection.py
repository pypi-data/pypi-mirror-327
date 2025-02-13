"""
Sequence collections
"""
from dataclasses import dataclass
from enum import Enum
from typing import (
  Callable, Dict, Iterable, Iterator, List, Optional, TypeVar
)
from abc import abstractmethod
import warnings

from Bio.Seq import reverse_complement

from xi_covutils import fastq, msa

class BioAlphabet(Enum):
  """
  Represents alphabets of biomolecules.
  """
  DNA=0
  RNA=1
  PROTEIN=2
  UNKNOWN=3

@dataclass
class BioSeq:
  """
  A Generic Biological sequence with and identifier.
  """
  identifier: str
  sequence: str
  alphabet: BioAlphabet
  def __eq__(self, other: object) -> bool:
    if not isinstance(other, BioSeq):
      return False
    return (
      self.identifier == other.identifier and
      self.sequence == other.sequence and
      self.alphabet == other.alphabet
    )
  @staticmethod
  def unknownBioSeq(identifier:str, sequence:str) -> "BioSeq":
    return BioSeq(identifier, sequence, BioAlphabet.UNKNOWN)
  def reverse_complement(self) -> "BioSeq":
    if self.alphabet == BioAlphabet.DNA:
      return BioSeq(
        identifier=self.identifier,
        sequence=str(reverse_complement(self.sequence)),
        alphabet=self.alphabet
      )
    if self.alphabet == BioAlphabet.RNA:
      return BioSeq(
        identifier=self.identifier,
        sequence=str(reverse_complement(self.sequence)),
        alphabet=self.alphabet
      )
    if self.alphabet == BioAlphabet.PROTEIN:
      raise ValueError(
        "Protein sequences cannot have reverse complement sequence."
      )
    raise ValueError(
      "Unknown type sequences cannot have reverse complement sequence."
    )


T = TypeVar("T")
class NonConsumableSeqCol:
  @abstractmethod
  def __len__(self):
    pass
  @abstractmethod
  def append(self, seq: BioSeq):
    pass

class AbstractIterableSeqCol(Iterator[BioSeq]):
  """
  A Collection of ordered biological sequences.
  """
  def __init__(self):
    self.bioseqs = []
    self.iterator = None
  def __iter__(self) -> Iterator[BioSeq]:
    self.iterator = iter(self.bioseqs)
    return self
  def __next__(self) -> BioSeq:
    assert self.iterator is not None
    return next(self.iterator)
  def map(self, func: Callable[[BioSeq], BioSeq]) -> "ConsumableSeqCol":
    return ConsumableSeqCol(
      func(bioseq) for bioseq in self
    )
  def map_with_index(self, func: Callable[[int, BioSeq], BioSeq]) -> "ConsumableSeqCol":
    return ConsumableSeqCol(
      func(i, bioseq) for i, bioseq in enumerate(self)
    )
  def filter(self, func: Callable[[BioSeq], bool]) -> "ConsumableSeqCol":
    return ConsumableSeqCol(
      bioseq for bioseq in self
      if func(bioseq)
    )
  def apply(self, func: Callable[[BioSeq], T]) -> Iterable[T]:
    return (func(bioseq) for bioseq in self)
  def fold(self, func: Callable[[T, BioSeq], T], initial: T) -> T:
    acc = initial
    for bioseq in self:
      acc = func(acc, bioseq)
    return acc
  def reduce(
    self,
    func: Callable[["SequenceCollection", BioSeq], "SequenceCollection"]
  ) -> "SequenceCollection":
    result = self.fold(func, SequenceCollection([]))
    return result
  def flat_map(self, func: Callable[[BioSeq], Iterable["SequenceCollection"]]) -> "ConsumableSeqCol":
    return ConsumableSeqCol(
      bioseq2
      for bioseq in self
      for bio_iter in func(bioseq)
      for bioseq2 in bio_iter
    )

class SequenceCollection(
  AbstractIterableSeqCol,
  NonConsumableSeqCol
):
  def __init__(self, seqs: List[BioSeq]):
    self.bioseqs: List[BioSeq] = seqs
    self.indexes: Dict[str, int] = {
      bs.identifier: i
      for i, bs in enumerate(self.bioseqs)
    }
    self.iterator = Optional[Iterator[BioSeq]]
    if len(self.bioseqs) != len(self.indexes):
      print(f"There are {len(self.bioseqs)} sequences and {len(self.indexes)} indexes")
      print(self.indexes)
      raise ValueError("Sequences has repeated identifiers")
    if len({s.alphabet for s in self.bioseqs}) > 1:
      raise ValueError("Sequences differ in alphabet")
  def append(self, seq: BioSeq):
    if seq.identifier in self.indexes:
      raise ValueError("Sequence has repeated identifier")
    if len(self) > 0 and seq.alphabet != self.bioseqs[0].alphabet:
      raise ValueError("New sequence has different alphabet")
    self.bioseqs.append(seq)
    self.indexes[seq.identifier] = len(self.bioseqs)
    return self
  def __len__(self) -> int:
    return len(self.bioseqs)
  def __eq__(self, other: object) -> bool:
    if not isinstance(other, SequenceCollection):
      return False
    if not len(self) == len(other):
      return False
    return all(
      s1 == s2 for s1, s2 in zip(
        self.bioseqs,
        other.bioseqs
      )
    )
  def __str__(self) -> str:
    return f"SequenceCollection[Size:{len(self)}]"
  def __repr__(self) -> str:
    max_seqs_to_repr = 20
    if len(self) < max_seqs_to_repr:
      warnings.warn(
        "SequenceCollection too large to be represented. Using 20",
        DeprecationWarning
      )
    seqs = [
      repr(s)
      for s in self.bioseqs[:max_seqs_to_repr]
    ]
    return f"SequenceCollection({repr(seqs)})"
  @staticmethod
  def from_fasta(
    fasta_file:str,
    alphabet: BioAlphabet = BioAlphabet.UNKNOWN
  ) -> "SequenceCollection":
    """
    Generates A Sequence Collection from a fasta file.

    Args:
      fasta_file (str): The input fasta file.
      alphabet (BioAlphabet, optional): The alphabet of the sequences.
        Defaults to BioAlphabet.UNKNOWN.

    Returns:
      SequenceCollection: The resulting sequence collection.
    """
    seqs = [
      BioSeq(sid, seq, alphabet)
      for (sid, seq) in msa.read_msa(fasta_file)
    ]
    return SequenceCollection(seqs)
  @staticmethod
  def from_fastq(
    fastq_file:str,
    alphabet: BioAlphabet = BioAlphabet.UNKNOWN
  ) -> "SequenceCollection":
    """
    Generates A Sequence Collection from a fastq file.

    Args:
      fastq_file (str): The input fastq file.
      alphabet (BioAlphabet, optional): The alphabet of the sequences.
        Defaults to BioAlphabet.UNKNOWN.

    Returns:
      SequenceCollection: The resulting sequence collection.
    """
    reader = fastq.FastqReader()
    seqs = [
      BioSeq(entry.identifier, entry.sequence, alphabet)
      for entry in reader.read_fastq_from_file(fastq_file)
    ]
    return SequenceCollection(seqs)
  def to_fasta(self, outfile:str):
    """
    Exports the sequence collection to a fasta file.

    Args:
      outfile (str): The output file.
    """
    seqs = [(x.identifier, x.sequence) for x in self]
    msa.write_msa(seqs, outfile)


class ConsumableSeqCol(AbstractIterableSeqCol):
  def __init__(self, data:Iterable[BioSeq]):
    self.bioseqs = data
    self.iterator = None
  def collect(self) -> "SequenceCollection":
    seq_col = SequenceCollection(list(self))
    return seq_col


def filter_by_identifier(allowed_identifiers:set[str]) -> Callable[[BioSeq], bool]:
  def filter(bioseq:BioSeq) -> bool:
    return bioseq.identifier in allowed_identifiers
  return filter

