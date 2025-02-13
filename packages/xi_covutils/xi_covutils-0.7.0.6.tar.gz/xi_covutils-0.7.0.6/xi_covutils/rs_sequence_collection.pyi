"""
Type hints and documentation for rs_sequence_collection rust module.
"""
# pylint: disable=no-name-in-module
from enum import Enum

# pylint: disable=too-few-public-methods
class BioAlphabet(Enum):
  """
  Enum to represent a biological alphabet. There are four possible values:
  DNA, RNA, PROTEIN, and UNKNOWN.
  """
  DNA = 0
  RNA = 1
  PROTEIN = 2
  UNKNOWN = 3

class BioSeq:
  """
  A Class to represent a biological sequence.
  """
  def __init__(
    self,
    identifier: str,
    sequence: str,
    alphabet: BioAlphabet
  ):
    """
    Create a new BioSeq object.
    """

  def get_identifier(self) -> str:
    """
    Returns the identifier of the sequence.
    """

  def get_sequence(self) -> str:
    """
    Returns the sequence.
    """

  def get_alphabet(self) -> BioAlphabet:
    """
    Returns the alphabet of the sequence.
    """

  def __eq__(self, other: "BioSeq") -> bool:
    """
    Compare two BioSeq objects for equality.
    """

  @staticmethod
  def unknown_bio_seq(identifier: str, sequence: str) -> "BioSeq":
    """
    Create a new BioSeq object with an unknown alphabet.
    """

  @staticmethod
  def dna(sequence: str) -> "BioSeq":
    """
    Create a new BioSeq object with a DNA alphabet and not identifier.
    """

  @staticmethod
  def rna(sequence: str) -> "BioSeq":
    """
    Create a new BioSeq object with a RNA alphabet and not identifier.
    """

  @staticmethod
  def protein(sequence: str) -> "BioSeq":
    """
    Create a new BioSeq object with a PROTEIN alphabet and not identifier.
    """

  @staticmethod
  def unknown(sequence: str) -> "BioSeq":
    """
    Create a new BioSeq object with an UNKNOWN alphabet and not identifier.
    """

  def to_rna(self) -> "BioSeq":
    """
    Convert the sequence to RNA.
    """

  def to_dna(self) -> "BioSeq":
    """
    Convert the sequence to DNA.
    """

  def reverse_complement(self) -> "BioSeq":
    """
    Returns the reverse complement of the sequence.
    """