"""
Sequence Mapper
"""
from typing import Optional
from Bio.Align import Alignment, PairwiseAligner

from xi_covutils.msa import default_aligner

class SequenceMapper:
  """
  Maps positions between two aligned sequences.

  ```python
  # Example:
  seq1 = "-TGT-G"
  seq2 = "AT-TGG"
  mapper = SequenceMapper.from_aligned_sequences(seq1, seq2)
  aln_positions = list(range(1,7))
  seq1_positions = list(range(1,5))
  seq2_positions = list(range(1,6))
  aln_to_first = [mapper.from_aln_to_first(x) for x in aln_positions]
  assert aln_to_first == [None, 1, 2, 3, None, 4]
  aln_to_second = [mapper.from_aln_to_second(x) for x in aln_positions]
  assert aln_to_second == [1, 2, None, 3, 4, 5]
  first_to_aln = [mapper.from_first_to_aln(x) for x in seq1_positions]
  assert first_to_aln == [2, 3, 4, 6]
  first_to_second = [mapper.from_first_to_second(x) for x in seq1_positions]
  assert first_to_second == [2, None, 3, 5]
  second_to_aln = [mapper.from_second_to_aln(x) for x in seq2_positions]
  assert second_to_aln == [1, 2, 4, 5, 6]
  second_to_first = [mapper.from_second_to_first(x) for x in seq2_positions]
  assert second_to_first == [None, 1, 3, None, 4]
  ```
  """
  def __init__(self):
    self.storage: dict[str, str] = {}
    self.aligner: Optional[PairwiseAligner] = None
    self.seq1_mapping: dict[int, tuple[int, int]] = {}
    self.seq2_mapping: dict[int, tuple[int, int]] = {}
    self.aln_mapping: dict[int, tuple[int, int]] = {}

  def with_sequences(self, first:str, second:str) -> "SequenceMapper":
    """
    Sets the first and second sequences for alignment.

    Args:
      first (str): The first sequence to be aligned.
      second (str): The second sequence to be aligned.

    Returns:
      SequenceMapper: The updated SequenceMapper object.
    """
    self.storage["first"] = first
    self.storage["second"] = second
    return self

  def with_default_aligner(self) -> "SequenceMapper":
    """
    Sets the default aligner for the SequenceMapper object.

    Returns:
      SequenceMapper: The updated SequenceMapper object with the default
        aligner.
    """
    self.aligner = default_aligner()
    return self

  def with_aligner(self, aligner:PairwiseAligner) -> "SequenceMapper":
    """
    Sets a custom aligner for the SequenceMapper object.

    Args:
      aligner (PairwiseAligner): A custom aligner to be used for sequence
        alignment.

    Returns:
      SequenceMapper: The updated SequenceMapper object with the custom aligner.
    """
    self.aligner = aligner
    return self

  def build(self) -> "SequenceMapper":
    """
    Aligns the sequences using the assigned aligner and creates mappings.

    Returns:
      SequenceMapper: The updated SequenceMapper object with created mappings.

    Throws:
      ValueError: Raised if one or more sequences are missing or if there is an
        error creating alignment.
    """
    aligner = self.aligner
    if not aligner:
      aligner = default_aligner()
      self.aligner = aligner
    first = self.storage.get("first")
    second = self.storage.get("second")
    if not first or not second:
      raise ValueError("One or more sequences are missing")
    alns = aligner.align(first, second)
    alignment:Alignment = alns[0]
    first_aligned = alignment[0, :]
    second_aligned = alignment[1, :]
    if (
      not isinstance(first_aligned, str)
      or not isinstance(second_aligned, str)
    ):
      raise ValueError("There was an error creating alignment")
    self.storage["first_aligned"] = first_aligned
    self.storage["second_aligned"] = second_aligned
    return self

  @staticmethod
  def from_aligned_sequences(
      first_aligned:str,
      second_aligned:str
    ) -> "SequenceMapper":
    """
    Creates a SequenceMapper object from already aligned sequences.

    Args:
      first_aligned (str): The first aligned sequence.
      second_aligned (str): The second aligned sequence.

    Returns:
      SequenceMapper: A new SequenceMapper object created from the
        aligned sequences.

    Throws:
      ValueError: Raised if the sequences have different lengths.
    """
    if len(first_aligned) != len(second_aligned):
      raise ValueError("Sequences must have the same length")
    mapper = SequenceMapper()
    mapper.storage["first_aligned"] = first_aligned
    mapper.storage["second_aligned"] = second_aligned
    mapper.storage["first"] = first_aligned.replace("-", "")
    mapper.storage["second"] = second_aligned.replace("-", "")
    mapper = SequenceMapper._create_mappings(mapper)
    return mapper

  @staticmethod
  def _create_mappings(mapper:"SequenceMapper"):
    first_aligned = mapper.storage["first_aligned"]
    second_aligned = mapper.storage["second_aligned"]
    seq1p = 0
    seq2p = 0
    aln_mapping = {}
    seq1_mapping = {}
    seq2_mapping = {}
    seq_tuple_iterator = zip(first_aligned, second_aligned)
    for i, (char1, char2) in enumerate(seq_tuple_iterator):
      seq1p, next_c1 = (seq1p+1, seq1p+1) if char1 != "-" else (seq1p, None)
      seq2p, next_c2 = (seq2p+1, seq2p+1) if char2 != "-" else (seq2p, None)
      aln_mapping[i+1] = (next_c1, next_c2)
      if char1 != "-":
        seq1_mapping[next_c1] = (i+1, next_c2)
      if char2 != "-":
        seq2_mapping[next_c2] = (i+1, next_c1)
    mapper.aln_mapping = aln_mapping
    mapper.seq1_mapping = seq1_mapping
    mapper.seq2_mapping = seq2_mapping
    return mapper

  def from_first_to_aln(self, position:int) -> Optional[int]:
    """
    Maps a position from the first sequence to the aligned position.

    Args:
      position (int): The position in the first sequence.

    Returns:
      Optional[int]: The corresponding aligned position or None if the
        position is not found.
    """
    result = self.seq1_mapping.get(position)
    if not result:
      return None
    return result[0]

  def from_first_to_second(self, position:int) -> Optional[int]:
    """
    Maps a position from the first sequence to the corresponding position in the
      second sequence.

    Args:
      position (int): The position in the first sequence.

    Returns:
      Optional[int]: The corresponding position in the second sequence or
        None if the position is not found.
    """
    result = self.seq1_mapping.get(position)
    if not result:
      return None
    return result[1]

  def from_second_to_aln(self, position:int) -> Optional[int]:
    """
    Maps a position from the second sequence to the aligned position.

    Args:
      position (int): The position in the second sequence.

    Returns:
      Optional[int]: The corresponding aligned position or None if the
        position is not found.
    """
    result = self.seq2_mapping.get(position)
    if not result:
      return None
    return result[0]

  def from_second_to_first(self, position:int) -> Optional[int]:
    """
    Maps a position from the second sequence to the corresponding position in
      the first sequence.

    Args:
      position (int): The position in the second sequence.

    Returns:
      Optional[int]: The corresponding position in the first sequence or
        None if the position is not found.
    """
    result = self.seq2_mapping.get(position)
    if not result:
      return None
    return result[1]

  def from_aln_to_first(self, position:int) -> Optional[int]:
    """
    Maps a position from the alignment to the corresponding position in the
      first sequence.

    Args:
      position (int): The position in the alignment.

    Returns:
      Optional[int]: The corresponding position in the first sequence or
        None if the position is not found.
    """
    result = self.aln_mapping.get(position)
    if not result:
      return None
    return result[0]

  def from_aln_to_second(self, position:int) -> Optional[int]:
    """
    Maps a position from the alignment to the corresponding position in the
      second sequence.

    Args:
      position (int): The position in the alignment.

    Returns:
      Optional[int]: The corresponding position in the second sequence or
        None if the position is not found.
    """
    result = self.aln_mapping.get(position)
    if not result:
      return None
    return result[1]
