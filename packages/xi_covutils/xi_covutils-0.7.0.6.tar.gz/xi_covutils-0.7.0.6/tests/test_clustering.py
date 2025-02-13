"""
Test clustering functions
"""
from pytest import approx
from pytest import raises
from xi_covutils.clustering import sequence_identity
from xi_covutils.clustering import hobohm1
from xi_covutils.clustering import _build_kmers
from xi_covutils.clustering import _build_kmer_map
from xi_covutils.clustering import _closest_kmer
from xi_covutils.clustering import kmer_clustering

def test_sequence_identity():
  """
  Test sequence_identity function in many scenarios
  """
  seq1 = "A"*100
  seq2 = "A"*100
  seq3 = "A"*98 + "B"*2
  seq4 = "A"*62 + "B"*38
  seq5 = "A"*50 + "-"*50
  seq6 = "A"*75 + "-"*25
  seq7 = "A"*101
  seq8 = "-"*100
  seq9 = "-"*100
  seq10 = "."*100
  seq11 = ""
  seq12 = ""

  # seq should be the proportion of identical characters in two strings
  assert sequence_identity(seq1, seq2) == approx(1.0)
  assert sequence_identity(seq1, seq3) == approx(0.98)
  assert sequence_identity(seq1, seq4) == approx(0.62)

  # gap should not be taken into account to compute seq id
  assert sequence_identity(seq1, seq5) == approx(0.5)
  assert sequence_identity(seq5, seq6) == approx(float(2)/3)

  # ValueError should be thrown if the sequences length is not the same
  with raises(ValueError) as err:
    sequence_identity(seq1, seq7)
  assert "ValueError" in str(err)

  # Seq id should be 0 if there are not non-gap chars in sequence
  assert sequence_identity(seq8, seq9) == 0
  assert sequence_identity(seq8, seq10) == 0
  assert sequence_identity(seq11, seq12) == 0

def test_hobohm1():
  """
  Test that hobohm1 makes correct clustering.
  Using gapstripping may improve performance in some contexts but shouldn't
  modify the results.
  """
  sequences = [
    "AAAAA----",
    "AAAAB----",
    "AAABB----",
    "AAABC----",
    "AACDE----",
    "AACFG----",
  ]
  clustering = hobohm1(sequences, use_gapstrip=False)
  assert len(clustering) == 4
  assert clustering[0].nseq == 2
  assert clustering[1].nseq == 2
  assert clustering[2].nseq == 1
  assert clustering[3].nseq == 1

  clustering = hobohm1(sequences, use_gapstrip=True)
  assert len(clustering) == 4
  assert clustering[0].nseq == 2
  assert clustering[1].nseq == 2
  assert clustering[2].nseq == 1
  assert clustering[3].nseq == 1

  clustering = hobohm1(sequences, use_gapstrip=True, max_clusters=3)
  assert len(clustering) == 3

def test_build_kmers():
  """ Test Build KMers from sequence """
  seq = "ABCDEG"
  kmers = _build_kmers(seq, 2)
  assert sorted(list(kmers)) == ["AB", "BC", "CD", "DE", "EG"]
  kmers = _build_kmers(seq, 3)
  assert sorted(list(kmers)) == ["ABC", "BCD", "CDE", "DEG"]
  kmers = _build_kmers(seq, 6)
  assert sorted(list(kmers)) == ["ABCDEG"]

def test_build_kmer_map():
  """ Test Creation of kmer map"""
  kmers = {0: {"AB", "BC"}, 1: {"BC", "CD"}, 2:{"CD"}}
  kmer_map = _build_kmer_map(kmers)
  assert kmer_map["AB"] == {0}
  assert kmer_map["BC"] == {0, 1}
  assert kmer_map["CD"] == {1, 2}

def test_closest_kmer():
  """
  Seqs:
  0 : ABCDE
  1 : ABGDE
  2 : ABGDF
  """
  # seqs = ['ABCDE', 'ABGDE', 'ABGDF']
  # seqs = _build_kmer_map({x:_build_kmers(s, 2) for x, s in enumerate(seqs)})
  kmer_set = {'AB', 'CD', 'BC', 'DE'}
  kmer_index = 0
  seq_map = {
    0: {'AB', 'CD', 'BC', 'DE'},
    1: {'AB', 'CD', 'BG', 'DE'},
    2: {'AB', 'GD', 'BG', 'DF'}
  }
  kmers_map = {
    'AB': {0, 1, 2},
    'BC': {0},
    'BG': {1, 2},
    'CD': {0},
    'DE': {0, 1},
    'DF': {2},
    'GD': {1, 2}}
  include = {0, 1, 2}
  closest = _closest_kmer(kmer_set, kmer_index, kmers_map, seq_map, include)
  assert closest
  assert closest[0] == 1
  closest = _closest_kmer(kmer_set, None, kmers_map, seq_map, include)
  assert closest
  assert closest[0] == 0

def test_kmer_clustering():
  """Test Clustering using kmers"""
  sequences = [
    "ACTSDYFGAJBASMCVASILGCHASDLGHADFASFKNASFNDASDAFKSADFIAJSDASFJAKSDF",
    "AATADYDFAJBASMCHASALGGHAJDLAHAGFAJFKNKSFNAASHAFKSAAFIJJSMASXJABSAF",
    "AQTSEYFRAJTSYUCVISIOGCPASDAGHSDFADFKFASGNDAHDAJKSKDFLAJLDASZJCKVDB",
    "ACTSDYFGAJBASMCVASILGCHASDLGHADFASFKNASFNDASDAFKSADFIAJSDASF",
    "ACDSQYFWAJHZSMCVAVILBCHNSMLAMFAAASDKNHSFHNDASDDGKSHDJIKLJSLFJFKHDS"
  ]
  clustering = kmer_clustering(sequences)
  assert len(clustering) == 4
  assert sorted([x.nseq for x in clustering]) == [1, 1, 1, 2]

  sequences = [
    "ACTSDYFGAJBASMCVASILGCHASDLGHADFASFKNASFNDASDAFKSADFIAJSDASFJAKSDH",
    "ACTSDYFGAJBASMCVASILGCHASDLGHADFASFKNASFNDASDAFKSADFIAJSDASFJAKSDF",
    "ACTSDYFGAJBASMCVASILGCHASDLGHADFASFKNASFNDASDAFKSADFIAJSDASFJAKSDF",
    "AATADYDFAJBASMCHASALGGHAJDLAHAGFAJFKNKSFNAASHAFKSAAFIJJSMASXJABSAF",
    "AQTSEYFRAJTSYUCVISIOGCPASDAGHSDFADFKFASGNDAHDAJKSKDFLAJLDASZJCKVDB",
    "ACTSDYFGAJBASMCVASILGCHASDLGHADFASFKNASFNDASDAFKSADFIAJSDASF",
    "ACDSQYFWAJHZSMCVAVILBCHNSMLAMFAAASDKNHSFHNDASDDGKSHDJIKLJSLFJFKHDS"
  ]
  clustering = kmer_clustering(sequences)
  assert len(clustering) == 4
  assert sorted([x.nseq for x in clustering]) == [1, 1, 1, 4]
