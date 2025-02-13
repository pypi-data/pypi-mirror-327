from xi_covutils.primers.infer import (
  EndSequenceExtractor,
  FivePrimeSequenceExtractor,
  NucleicSequenceEnd,
  PrimerGuesser,
  PrimerMatchCounter,
  ThreePrimeSequenceExtractor
)
from xi_covutils.seqs.seq_collection import (
  BioAlphabet,
  BioSeq,
  SequenceCollection
)

def test_end_sequence_extractor():
  end = NucleicSequenceEnd.FIVEPRIME
  instance = EndSequenceExtractor.build(end, 10)
  assert isinstance(instance, FivePrimeSequenceExtractor)
  end = NucleicSequenceEnd.THREEPRIME
  instance = EndSequenceExtractor.build(end, 10)
  assert isinstance(instance, ThreePrimeSequenceExtractor)

def test_five_prime_sequence_extractor():
  extractor = FivePrimeSequenceExtractor(5)
  seq = BioSeq(
    identifier="seq1",
    alphabet=BioAlphabet.DNA,
    sequence="AAAAATTTTT"
  )
  expected = "AAAAA"
  extracted = extractor.subsequence(seq)
  assert expected == extracted.sequence
  assert seq.identifier == extracted.identifier
  assert seq.alphabet == extracted.alphabet

def test_three_prime_sequence_extractor():
  extractor = ThreePrimeSequenceExtractor(5)
  seq = BioSeq(
    identifier="seq1",
    alphabet=BioAlphabet.DNA,
    sequence="AAAAATTTTT"
  )
  expected = "TTTTT"
  extracted = extractor.subsequence(seq)
  assert expected == extracted.sequence
  assert seq.identifier == extracted.identifier
  assert seq.alphabet == extracted.alphabet

class TestPrimerGuesser:
  def test_inspect(self):
    def _with_non_deg_bases():
      guesser = PrimerGuesser(
        end=NucleicSequenceEnd.FIVEPRIME,
        primer_length=5
      )
      sequences = [
        "AAAAAN",
        "AAAAAN",
        "CCCCCN",
        "CCCCCN",
        "TTTTTN",
        "TTTTTN",
        "GGGGGN",
        "GGGGGN"
      ]
      sequences = SequenceCollection([
        BioSeq(f"seq_{i}", s, BioAlphabet.DNA)
        for i, s in enumerate(sequences)
      ])
      df = guesser.inspect(sequences)
      assert df.shape == (5, 4)
      assert df["A"].tolist() == [0.25] * 5
      assert df["T"].tolist() == [0.25] * 5
      assert df["C"].tolist() == [0.25] * 5
      assert df["G"].tolist() == [0.25] * 5
    def _with_deg_bases():
      guesser = PrimerGuesser(
        end=NucleicSequenceEnd.FIVEPRIME,
        primer_length=5
      )
      sequences = [
        "WBSAAN",
        "CCCCCN",
        "TTTTTN",
        "GGGGGN"
      ]
      sequences = SequenceCollection([
        BioSeq(f"seq_{i}", s, BioAlphabet.DNA)
        for i, s in enumerate(sequences)
      ])
      df = guesser.inspect(sequences)
      assert df.shape == (5, 4)
      assert df["A"].tolist() == [0.20, 0.00, 0.00, 0.25, 0.25]
      assert df["T"].tolist() == [0.40, 1/3 , 0.20, 0.25, 0.25]
      assert df["C"].tolist() == [0.20, 1/3 , 0.40, 0.25, 0.25]
      assert df["G"].tolist() == [0.20, 1/3 , 0.40, 0.25, 0.25]
    _with_non_deg_bases()
    _with_deg_bases()
  def test_guess(self):
    def _with_identical_nondeg():
      guesser = PrimerGuesser(
        end=NucleicSequenceEnd.FIVEPRIME,
        primer_length=5
      )
      sequences = [ "ACTGGA" ] * 100
      sequences = SequenceCollection([
        BioSeq(f"seq_{i}", s, BioAlphabet.DNA)
        for i, s in enumerate(sequences)
      ])
      primer = guesser.guess(sequences)
      assert isinstance(primer, BioSeq)
      assert primer.sequence == "ACTGG"
    def _with_non_identical_nondeg():
      guesser = PrimerGuesser(
        end=NucleicSequenceEnd.FIVEPRIME,
        primer_length=5
      )
      sequences = (
        [ "ACTGGA" ] * 50 +
        [ "TCTGGA" ] * 50 +
        [ "TCGGGA" ]
      )
      sequences = SequenceCollection([
        BioSeq(f"seq_{i}", s, BioAlphabet.DNA)
        for i, s in enumerate(sequences)
      ])
      primer = guesser.guess(sequences)
      assert isinstance(primer, BioSeq)
      assert primer.sequence == "WCTGG"
    def _with_identical_deg_bases():
      guesser = PrimerGuesser(
        end=NucleicSequenceEnd.FIVEPRIME,
        primer_length=15
      )
      sequences = (
        [ "ACTGWRYSMDHKVBN" ] * 5
      )
      sequences = SequenceCollection([
        BioSeq(f"seq_{i}", s, BioAlphabet.DNA)
        for i, s in enumerate(sequences)
      ])
      primer = guesser.guess(sequences)
      assert isinstance(primer, BioSeq)
      assert primer.sequence == "ACTGWRYSMDHKVBN"
    def _with_nonidentical_bases():
      guesser = PrimerGuesser(
        end=NucleicSequenceEnd.FIVEPRIME,
        primer_length=15
      )
      sequences = [
        "ACTGAACCAAAGACA",
        "ACTGAACCAAAGACC",
        "ACTGTGTGCGCTCGT",
        "ACTGTGTGCTTTGTG"
      ]
      sequences = SequenceCollection([
        BioSeq(f"seq_{i}", s, BioAlphabet.DNA)
        for i, s in enumerate(sequences)
      ])
      primer = guesser.guess(sequences)
      assert isinstance(primer, BioSeq)
      assert primer.sequence == "ACTGWRYSMDHKVBN"
    def _when_picking_three_prime_primers():
      guesser = PrimerGuesser(
        end=NucleicSequenceEnd.THREEPRIME,
        primer_length=5
      )
      sequences = [
        "ACTGAACCAAAGACA",
        "ACTGAACCAAAGACC",
        "ACTGTGTGCGCTCGT",
        "ACTGTGTGCTTTGTG"
      ]
      sequences = SequenceCollection([
        BioSeq(f"seq_{i}", s, BioAlphabet.DNA)
        for i, s in enumerate(sequences)
      ])
      primer = guesser.guess(sequences)
      assert isinstance(primer, BioSeq)
      assert primer.sequence == "NVBMD"
    _with_identical_nondeg()
    _with_non_identical_nondeg()
    _with_identical_deg_bases()
    _with_nonidentical_bases()
    _when_picking_three_prime_primers()
  def test_count(self):
    def _with_perfect_matching_seqs():
      counter = PrimerMatchCounter()
      sequences = [
        "ACTGAACCAAAGACA",
        "ACTGAACCAAAGACC",
        "ACTGTGTGCGCTCGT",
        "ACTGTGTGCTTTGTG"
      ]
      sequences = SequenceCollection([
        BioSeq(f"seq_{i}", s, BioAlphabet.DNA)
        for i, s in enumerate(sequences)
      ])
      primer = BioSeq("primer", "ACTGW", BioAlphabet.DNA)
      result = counter.count(sequences, primer, NucleicSequenceEnd.FIVEPRIME)
      assert result.matches == 4
      assert result.mismatches == 0
    def _with_mismatching_seqs():
      counter = PrimerMatchCounter()
      sequences = [
        "ACTGAACCAAAGACA",
        "ACTGAACCAAAGACC",
        "ACTGTGTGCGCTCGT",
        "ACTGTGTGCTTTGTG"
      ] * 100 + ["TCTGA"]
      sequences = SequenceCollection([
        BioSeq(f"seq_{i}", s, BioAlphabet.DNA)
        for i, s in enumerate(sequences)
      ])
      primer = BioSeq("primer", "ACTGW", BioAlphabet.DNA)
      result = counter.count(sequences, primer, NucleicSequenceEnd.FIVEPRIME)
      assert result.matches == 400
      assert result.mismatches == 1
    def _with_mismatching_seqs_three():
      counter = PrimerMatchCounter()
      sequences = [
        "ACTGAACCAAAGGCA",
        "ACTGAACCAAAGGCA",
        "ACTGTGTGCGTTGCA",
        "ACTGTGTGCTTTGCA"
      ] * 100 + ["ACTGTGTGCTTTCCA"]
      sequences = SequenceCollection([
        BioSeq(f"seq_{i}", s, BioAlphabet.DNA)
        for i, s in enumerate(sequences)
      ])
      primer = BioSeq("primer", "TGCMW", BioAlphabet.DNA)
      result = counter.count(sequences, primer, NucleicSequenceEnd.THREEPRIME)
      assert result.matches == 400
      assert result.mismatches == 1
    _with_perfect_matching_seqs()
    _with_mismatching_seqs()
    _with_mismatching_seqs_three()
  def test_histogram(self):
    def _with_mismatching_seqs_three():
      counter = PrimerMatchCounter()
      sequences = [
        "ACTGAACCAAAGGCA",
        "ACTGAACCAAAGGCA",
        "ACTGTGTGCGTTGCA",
        "ACTGTGTGCTTTGCA"
      ] * 100 + ["ACTGTGTGCTTTCCA"] + ["ACTGTGTGCTTTCCG"]
      sequences = SequenceCollection([
        BioSeq(f"seq_{i}", s, BioAlphabet.DNA)
        for i, s in enumerate(sequences)
      ])
      primer = BioSeq("primer", "TGCMW", BioAlphabet.DNA)
      result = counter.histogram(sequences, primer, NucleicSequenceEnd.THREEPRIME)
      assert result[0] == 400
      assert result[1] == 1
      assert result[1] == 1
    _with_mismatching_seqs_three()
