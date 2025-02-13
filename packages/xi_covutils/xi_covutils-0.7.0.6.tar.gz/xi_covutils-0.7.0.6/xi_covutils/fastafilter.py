"""
Filter fasta sequences.
"""
from abc import ABC, abstractmethod
from typing import Iterator, Optional, Tuple, TypeVar, Generic, List
import os
import re

from Bio import SeqIO

Seq = str
Desc = str
FastaSeq = Tuple[Desc, Seq]
IUPAC_CODES = {
  'A': 'A',
  'C': 'C',
  'G': 'G',
  'T': 'T',
  'U': 'U',
  'R': '[AG]',      # A or G
  'Y': '[CT]',      # C or T
  'S': '[GC]',      # G or C
  'W': '[AT]',      # A or T
  'K': '[GT]',      # G or T
  'M': '[AC]',      # A or C
  'B': '[CGT]',     # C or G or T
  'D': '[AGT]',     # A or G or T
  'H': '[ACT]',     # A or C or T
  'V': '[ACG]',     # A or C or G
  'N': '[ACGT]',    # any base
}

def iupac_to_regex(pattern: str) -> str:
  """
  Convert a IUPAC code inte a regex
  """
  return ''.join(IUPAC_CODES.get(base, base) for base in pattern)

# pylint: disable = too-few-public-methods
class Rule(ABC):
  """
  Abstract rule to filter a single fasta sequence
  """
  @abstractmethod
  def filter(self, fasta: FastaSeq) -> bool:
    """
    Decides if a sequence pass the filtering process.
    """

class RuleSequenceContains(Rule):
  """
  Rule to filter sequences, if the sequence contains a given subsequence
  """
  def __init__(self) -> None:
    super().__init__()
    self.query_str:Optional[str] = None
  def query(self, query: str) -> "RuleSequenceContains":
    """
    Sets the query sequence.
    """
    self.query_str = query
    return self
  def filter(self, fasta: FastaSeq) -> bool:
    """
    Decides if a sequence pass the filtering process.
    The sequence pass the filter if the sequence contains
    the given subsequence (case insentitive).
    """
    _, seq = fasta
    if self.query_str:
      return self.query_str.lower() in seq.lower()
    return False

class RuleRegexMatch(Rule):
  """
  Rule to filter sequences by matching them to a regex pattern.
  """
  def __init__(self) -> None:
    super().__init__()
    self.pattern: Optional[str] = None

  def query(self, pattern: str) -> "RuleRegexMatch":
    """
    Sets the regex pattern for filtering.
    """
    self.pattern = pattern
    return self

  def filter(self, fasta: FastaSeq) -> bool:
    """
    Decides if a sequence pass the filtering process.
    The sequence passes the filter if it matches the given regex pattern.
    """
    _, seq = fasta
    if self.pattern:
      return bool(re.search(self.pattern, seq))
    return False

class RuleIUPACMatch(Rule):
  """
  Rule to filter sequences by matching them to a pattern with IUPAC codes.
  """
  def __init__(self) -> None:
    super().__init__()
    self.pattern: Optional[str] = None

  def query(self, pattern: str) -> "RuleIUPACMatch":
    """
    Sets the pattern with IUPAC codes for filtering.
    """
    self.pattern = iupac_to_regex(pattern)
    return self

  def filter(self, fasta: FastaSeq) -> bool:
    """
    Decides if a sequence passes the filtering process.
    The sequence passes the filter if it matches the given IUPAC pattern.
    """
    _, seq = fasta
    if self.pattern:
      return bool(re.search(self.pattern, seq))
    return False

class RuleNot(Rule):
  """
  Negates a rule
  """
  def __init__(self, rule:Rule) -> None:
    super().__init__()
    self.rule = rule
  def filter(self, fasta: FastaSeq) -> bool:
    """
    Negates the result of other rule
    """
    return not self.rule.filter(fasta)

class RuleAnd(Rule):
  """
  Bolean 'and' between two rules
  """
  def __init__(self, rule1: Rule, rule2: Rule) -> None:
    super().__init__()
    self.rule1 = rule1
    self.rule2 = rule2
  def filter(self, fasta) -> bool:
    """
    Boolean 'and' between two rules
    """
    return (
      self.rule1.filter(fasta) and
      self.rule2.filter(fasta)
    )

class RuleOr(Rule):
  """
  Boolean 'or' between two rules
  """
  def __init__(self, rule1: Rule, rule2: Rule) -> None:
    super().__init__()
    self.rule1 = rule1
    self.rule2 = rule2
  def filter(self, fasta) -> bool:
    """
    Boolean 'or' between two rules
    """
    return (
      self.rule1.filter(fasta) or
      self.rule2.filter(fasta)
    )

class RuleAll(Rule):
  """
  Boolean 'All' between many rules
  """
  def __init__(self, rules: List[Rule]) -> None:
    super().__init__()
    self.rules = rules
  def filter(self, fasta) -> bool:
    """
    Boolean 'All' between two rules
    """
    for rule in self.rules:
      if not rule.filter(fasta):
        return False
    return True

class RuleAny(Rule):
  """
  Boolean 'Any' between many rules
  """
  def __init__(self, rules: List[Rule]) -> None:
    super().__init__()
    self.rules = rules
  def filter(self, fasta) -> bool:
    """
    Boolean 'Any' between two rules
    """
    for rule in self.rules:
      if rule.filter(fasta):
        return True
    return False

class RuleDescriptionContains(Rule):
  """
  Rule to filter sequences, if the sequence description contains a substring.
  """
  def __init__(self) -> None:
    super().__init__()
    self.query_str:Optional[str] = None
  def query(self, query:str) -> "RuleDescriptionContains":
    """
    Sets the query sequence.
    """
    self.query_str = query
    return self
  def filter(self, fasta: FastaSeq) -> bool:
    """
    Decides if a sequence pass the filtering process.
    The sequence pass the filter if the description contains
    the given substring (case sentitive).
    """
    desc, _ = fasta
    if self.query_str:
      return self.query_str in desc
    return False

RESULTTYPE = TypeVar("RESULTTYPE")
class FastaSeqCollector(ABC, Generic[RESULTTYPE]):
  """
  Abstract class to receive fasta sequences after the filtering process.
  """
  @abstractmethod
  def receive(self, fasta: FastaSeq):
    """
    Collects a new sequence
    """
  @abstractmethod
  def result(self) -> RESULTTYPE:
    """
    Retrieve the result of the sequence collection
    """

class CollectToList(FastaSeqCollector):
  """
  Collects filtered fasta sequences of a List
  """
  def __init__(self):
    self.storage = []
  def receive(self, fasta: FastaSeq):
    """
    Collects a new sequence
    """
    self.storage.append(fasta)
  def result(self) -> List[str]:
    """
    Retrieve the result of the sequence collection
    """
    return self.storage

class CollectToFile(FastaSeqCollector):
  """
  Collects fasta sequence into a file.
  """
  def __init__(self, outfile:str):
    self.outfile:Optional[str] = outfile
    if os.path.exists(outfile):
      os.remove(outfile)
  def receive(self, fasta: FastaSeq):
    """
    Collects a new fasta file. It appends to the output file immediatly.
    """
    if not self.outfile:
      return
    with open(self.outfile, "a", encoding="utf-8") as fout:
      fout.write(f">{fasta[0]}\n{fasta[1]}\n")
  def result(self):
    """
    It should collect all sequences to a file.
    However this is done after receiving each sequence, so there is no need to
    do anything here.
    """
    return None

FilterResult = TypeVar("FilterResult")
class Filter(Generic[FilterResult]):
  """
  Filter fasta sequences.
  """
  def __init__(
    self,
    inputs: Iterator[FastaSeq],
    output: FastaSeqCollector[FilterResult],
    rules: List[Rule]
  ):
    self.inputs = inputs
    self.output = output
    self.rules = rules
  def filter(self) -> FilterResult:
    """
    Filter all sequences in the iterator.
    """
    for fasta in self.inputs:
      pass_filter = True
      for rule in self.rules:
        if not pass_filter:
          continue
        if not rule.filter(fasta):
          pass_filter = False
      if pass_filter:
        self.output.receive(fasta)
    return self.output.result()


class FilterBuilder:
  """
  Factory object to create fasta filters.
  """
  def __init__(self) -> None:
    self.rules = []
    self.input_method: Optional[Iterator[FastaSeq]] = None
    self.output_method: Optional[FastaSeqCollector] = None
  def with_infile(self, infile:str) -> "FilterBuilder":
    """
    Sets the input to be a fasta file.
    """
    self.input_method = (
      FastaSeqIteratorFromFile()
        .set_file(infile)
        .iterator()
    )
    return self
  def with_input_list(self, inlist:List[FastaSeq]) -> "FilterBuilder":
    """
    Sets the input to be a list of FastaSeq.
    """
    self.input_method = iter(inlist)
    return self
  def to_outlist(self):
    """
    Sets the output to a List of FastaSeq
    """
    self.output_method = CollectToList()
    return self
  def with_outfile(self, outfile:str) -> "FilterBuilder":
    """
    Sets the output to be a file.
    """
    self.output_method = CollectToFile(outfile)
    return self
  def add_rule(self, rule: Rule) -> "FilterBuilder":
    """
    Adds a new rule to filter fasta files.
    """
    self.rules.append(rule)
    return self
  def build(self) -> Optional[Filter]:
    """
    Creates a new Filter object.
    """
    if not self.input_method or not self.output_method:
      return None
    return (
      Filter(
        inputs = self.input_method,
        output = self.output_method,
        rules = self.rules
      )
    )

class FastaSeqIteratorFromFile:
  """
  Creates an iterator from a fasta file.
  """
  def __init__(self) -> None:
    self.infile: Optional[str] = None
  def set_file(self, infile: str) -> "FastaSeqIteratorFromFile":
    """
    Sets the input fasta file.
    """
    self.infile = infile
    return self
  def iterator(self) -> Iterator[FastaSeq]:
    """
    Builds an iterator of fasta sequences.
    """
    if not self.infile:
      return
    with open(self.infile, "r", encoding="utf-8") as f_in:
      records = SeqIO.parse(f_in, format="fasta")
      for record in records:
        result = (
          f"{record.description}",
          str(record.seq)
        )
        yield result
