"""
Tests for the SequenceCollection and ConsumableSeqCol classes.
"""

from xi_covutils.seqs.seq_collection import (
  BioSeq, ConsumableSeqCol, SequenceCollection, filter_by_identifier
)

from xi_covutils.rs_sequence_collection import (
  BioSeq as RsBioSeq,
  BioAlphabet as RsBioAlphabet
)

class TestSequenceCollection:
  def test_iter(self):
    def can_create_empty_collection():
      seqs = []
      scol = SequenceCollection(seqs)
      assert [s for s in scol] == seqs
    def can_create_three_sequences():
      seqs = [
        BioSeq.unknownBioSeq("S1", "ACTA"),
        BioSeq.unknownBioSeq("S2", "ACTG"),
        BioSeq.unknownBioSeq("S3", "ACTC")
      ]
      scol = SequenceCollection(seqs)
      scol2 = [s for s in scol]
      assert seqs == scol2
      scol2 = [s for s in scol]
      assert seqs == scol2
    can_create_three_sequences()
    can_create_empty_collection()
  def test_map(self):
    seqs = [
      BioSeq.unknownBioSeq("S1", "ACTA"),
      BioSeq.unknownBioSeq("S2", "ACTG"),
      BioSeq.unknownBioSeq("S3", "ACTC")
    ]
    scol = SequenceCollection(seqs)
    scol2 = (
      scol
        .map(
          lambda seq: BioSeq.unknownBioSeq(
            seq.identifier,
            seq.sequence[::-1]
          )
        )
        .collect()
    )
    assert isinstance(scol2, SequenceCollection)
    assert [s for s in scol2] == [
      BioSeq.unknownBioSeq("S1", "ATCA"),
      BioSeq.unknownBioSeq("S2", "GTCA"),
      BioSeq.unknownBioSeq("S3", "CTCA")
    ]
  def test_len(self):
    seqs = [
      BioSeq.unknownBioSeq("S1", "ACTA"),
      BioSeq.unknownBioSeq("S2", "ACTG"),
      BioSeq.unknownBioSeq("S3", "ACTC")
    ]
    scol = SequenceCollection(seqs)
    assert len(scol) == 3
  def test_append(self):
    def with_empty_seqcol():
      seqs = []
      scol = SequenceCollection(seqs)
      assert len(scol) == 0
      scol.append(
        BioSeq.unknownBioSeq("S1", "ACTG")
      )
      assert len(scol) == 1
    def with_one_seq():
      seqs = [
        BioSeq.unknownBioSeq("S1", "ACTG")
      ]
      scol = SequenceCollection(seqs)
      assert len(scol) == 1
      scol.append(
        BioSeq.unknownBioSeq("S2", "ACTT")
      )
      assert len(scol) == 2
      scol2 = [s for s in scol]
      assert scol2 == [
        BioSeq.unknownBioSeq("S1", "ACTG"),
        BioSeq.unknownBioSeq("S2", "ACTT")
      ]
    with_empty_seqcol()
    with_one_seq()
  def test_filter(self):
    def with_custom_filter():
      seqs = [
        BioSeq.unknownBioSeq("S1", "ACTA"),
        BioSeq.unknownBioSeq("S2", "ACTG"),
        BioSeq.unknownBioSeq("S3", "ACTC")
      ]
      scol = SequenceCollection(seqs)
      scol2 = (
        scol
          .filter(lambda b: b.sequence.endswith("A"))
          .collect()
      )
      assert len(scol2) == 1
      assert list(scol2)[0] == BioSeq.unknownBioSeq("S1", "ACTA")
    def with_filter_by_identifier():
      seqs = [
        BioSeq.unknownBioSeq("S1", "ACTA"),
        BioSeq.unknownBioSeq("S2", "ACTG"),
        BioSeq.unknownBioSeq("S3", "ACTC")
      ]
      scol = SequenceCollection(seqs)
      fil_id = filter_by_identifier(set(["S1", "S2"]))
      scol2 = (
        scol
          .filter(fil_id)
          .collect()
      )
      assert list(scol2) == [
        BioSeq.unknownBioSeq("S1", "ACTA"),
        BioSeq.unknownBioSeq("S2", "ACTG")
      ]
    with_custom_filter()
    with_filter_by_identifier()

class TestConsumableSequenceCollection:
  def test_iter(self):
    def with_three_sequences():
      oseqs = [
        BioSeq.unknownBioSeq("S1", "ACTA"),
        BioSeq.unknownBioSeq("S2", "ACTG"),
        BioSeq.unknownBioSeq("S3", "ACTC")
      ]
      seqs = (s for s in oseqs)
      scol = ConsumableSeqCol(seqs)
      scol2 = [s for s in scol]
      assert oseqs == scol2
      scol2 = [s for s in scol]
      assert [] == scol2
    with_three_sequences()


class TestRsBioSeq:
  def test_reverse_complement_with_dna(self):
    bs1 = RsBioSeq("S1", "ACTG", RsBioAlphabet.DNA)
    bs2 = bs1.reverse_complement()
    assert bs2.get_identifier() == "S1"
    assert bs2.get_sequence() == "CAGT"
    assert bs2.get_alphabet() == RsBioAlphabet.DNA

  def test_reverse_complement_with_rna(self):
    bs1 = RsBioSeq("S1", "ACUG", RsBioAlphabet.RNA)
    bs2 = bs1.reverse_complement()
    assert bs2.get_identifier() == "S1"
    assert bs2.get_sequence() == "CAGU"
    assert bs2.get_alphabet() == RsBioAlphabet.RNA

  def test_reverse_complement_with_protein(self):
    bs1 = RsBioSeq("S1", "ACUG", RsBioAlphabet.PROTEIN)
    try:
      bs1.reverse_complement()
      assert False
    except ValueError as e:
      assert str(e) == "Protein sequences cannot have reverse complement sequence."