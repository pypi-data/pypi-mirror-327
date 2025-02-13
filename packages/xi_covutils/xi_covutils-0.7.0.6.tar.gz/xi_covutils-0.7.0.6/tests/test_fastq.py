"""
Test Fastq module
"""
# pylint: disable=too-few-public-methods

# @SIM:1:FCX:1:15:6329:1045 1:N:0:2
# TCGCACTCAACGCCCTGCATATGACAAGACAGAATC
# +
# <>;##=><9=AAAAAAAAAA9#:<#<;<<<????#=

# @SIM:1:FCX:1:15:6329:1045 1:N:0:2
# TCGCACTCAACGCCCTGCATATGACAAGACAGAATC
# +
# <>;##=><9=AAAAAAAAAA9#:<#<;<<<????#=

from io import StringIO
import os
from xi_covutils.fastq import FastqEntry, FastqReader, FastqWriter

class TestFastqEntry:
  def test_trim3(self):
    """
    Test trim3 method.
    """
    entry = FastqEntry(
      identifier = "read01",
      sequence = "AAAAAAAAAATTTTT",
      description = "Field1,field2,field3",
      quality  = "QQQQQQQQQQABCGD"
    )
    entry = entry.trim3(5)
    assert entry.sequence == "AAAAAAAAAA"
    assert entry.quality == "QQQQQQQQQQ"

  def test_trim5(self):
    """
    Test trim3 method.
    """
    entry = FastqEntry(
      identifier = "read01",
      sequence = "TTTTTAAAAAAAAAA",
      description = "Field1,field2,field3",
      quality  = "ABCGDQQQQQQQQQQ"
    )
    entry = entry.trim5(5)
    assert entry.sequence == "AAAAAAAAAA"
    assert entry.quality == "QQQQQQQQQQ"

class TestFastqReader:
  """
  Test FastqReader class.
  # """
  def test_fastq_entry_from_lines(self):
    """
    Test fastq_entry_from_lines method
    """
    def simple_case():
      lines = (
        "@SIM:1:FCX:1:15:6329:1045 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC",
        "+",
        "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#="
      )
      reader = FastqReader()
      entry = reader.fastq_entry_from_lines(lines)
      assert isinstance(entry, FastqEntry)
      assert entry.sequence == lines[1]
      assert entry.identifier == "SIM:1:FCX:1:15:6329:1045"
      assert entry.description == "1:N:0:2"
      assert entry.quality == lines[3]
      assert len(entry) == len(lines[1])
    def wrong_case():
      lines = (
        "SIM:1:FCX:1:15:6329:1045 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC",
        "+",
        "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#="
      )
      reader = FastqReader()
      entry = reader.fastq_entry_from_lines(lines)
      assert entry is None
    simple_case()
    wrong_case()
  def test_read_next_fastq_entry(self):
    """
    Test read_next_fastq_entry method
    """
    def with_one_right_entry():
      text = [
        "@SIM:1:FCX:1:15:6329:1045 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC",
        "+",
        "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#="
      ]
      text = "\n".join(text)
      reader = FastqReader()
      text_src = StringIO(text)
      entry = reader.read_next_fastq_entry(text_src)
      assert isinstance(entry, FastqEntry)
      assert entry.sequence == "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC"
      assert entry.identifier == "SIM:1:FCX:1:15:6329:1045"
      assert entry.description == "1:N:0:2"
      assert entry.quality == "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#="
    def with_one_wrong_entry():
      text = [
        "SIM:1:FCX:1:15:6329:1045 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC",
        "+",
        "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#="
      ]
      text = "\n".join(text)
      reader = FastqReader()
      text_src = StringIO(text)
      entry = reader.read_next_fastq_entry(text_src)
      assert entry is None
    def with_one_incomplete_entry():
      text = [
        "SIM:1:FCX:1:15:6329:1045 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC",
        "+",
      ]
      text = "\n".join(text)
      reader = FastqReader()
      text_src = StringIO(text)
      entry = reader.read_next_fastq_entry(text_src)
      assert entry is None
    def with_two_right_entry():
      text = [
        "@SIM:1:FCX:1:15:6329:1045 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC",
        "+",
        "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#=",
        "@SIM:1:FCX:1:15:6329:1046 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC",
        "+",
        "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#="
      ]
      text = "\n".join(text)
      reader = FastqReader()
      text_src = StringIO(text)
      entry = reader.read_next_fastq_entry(text_src)
      assert isinstance(entry, FastqEntry)
      assert entry.sequence == "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC"
      assert entry.identifier == "SIM:1:FCX:1:15:6329:1045"
      assert entry.description == "1:N:0:2"
      assert entry.quality == "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#="
      entry = reader.read_next_fastq_entry(text_src)
      assert isinstance(entry, FastqEntry)
      assert entry.sequence == "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC"
      assert entry.identifier == "SIM:1:FCX:1:15:6329:1046"
      assert entry.description == "1:N:0:2"
      assert entry.quality == "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#="
      entry = reader.read_next_fastq_entry(text_src)
      assert entry is None
    with_one_right_entry()
    with_one_wrong_entry()
    with_one_incomplete_entry()
    with_two_right_entry()
  def test_read_fastq_from_text_source(self):
    """
    Test read_fastq_from_text_source method.
    """
    def with_two_right_entry():
      text = [
        "@SIM:1:FCX:1:15:6329:1045 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC",
        "+",
        "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#=",
        "@SIM:1:FCX:1:15:6329:1046 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC",
        "+",
        "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#="
      ]
      text = "\n".join(text)
      reader = FastqReader()
      text_src = StringIO(text)
      entries = list(reader.read_fastq_from_text_source(text_src))
      assert len(entries) == 2
      assert [
        x.identifier for x in entries
      ] == [
        "SIM:1:FCX:1:15:6329:1045",
        "SIM:1:FCX:1:15:6329:1046"
      ]
    def with_two_entry_plus_incomplete():
      text = [
        "@SIM:1:FCX:1:15:6329:1045 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC",
        "+",
        "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#=",
        "@SIM:1:FCX:1:15:6329:1046 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC",
        "+",
        "<>;##=><9=AAAAAAAAAA9#:<#<;<<<????#=",
        "@SIM:1:FCX:1:15:6329:1047 1:N:0:2",
        "TCGCACTCAACGCCCTGCATATGACAAGACAGAATC"
      ]
      text = "\n".join(text)
      reader = FastqReader()
      text_src = StringIO(text)
      entries = list(reader.read_fastq_from_text_source(text_src))
      assert len(entries) == 2
      assert [
        x.identifier for x in entries
      ] == [
        "SIM:1:FCX:1:15:6329:1045",
        "SIM:1:FCX:1:15:6329:1046"
      ]
    with_two_right_entry()
    with_two_entry_plus_incomplete()
  def test_read_fastq_from_file(self, test_data_folder):
    """
    Test read_fastq_from_file method.
    """
    def test_with_file():
      testfile = os.path.join(test_data_folder, "fastq_file.fastq")
      reader = FastqReader()
      entries = list(reader.read_fastq_from_file(testfile))
      assert len(entries) == 2
      assert [
        x.identifier for x in entries
      ] == [
        "SIM:1:FCX:1:15:6329:1045",
        "SIM:1:FCX:1:15:6329:1046"
      ]
    test_with_file()

class TestFastqWriter:
  def test_write_fastq_to_text_source(self, test_data_folder):
    """
    Test FastqWriter context manager
    """
    outfile = os.path.join(test_data_folder, "tmp_out.fastq")
    if os.path.exists(outfile):
      os.remove(outfile)
    with FastqWriter(outfile) as writer:
      entry = FastqEntry(
        identifier = "read01",
        sequence = "ATCGACTGACTGACT",
        description = "Field1,field2,field3",
        quality  = "QQQQQQQQQQQQQQQ"
      )
      writer.write(entry=entry)
    with open(outfile, "r", encoding="utf-8") as f_in:
      input_data = f_in.read()
      expected =  (
        "@read01 Field1,field2,field3\n"
        "ATCGACTGACTGACT\n+\nQQQQQQQQQQQQQQQ\n"
      )
      assert input_data == expected
    if os.path.exists(outfile):
      os.remove(outfile)
