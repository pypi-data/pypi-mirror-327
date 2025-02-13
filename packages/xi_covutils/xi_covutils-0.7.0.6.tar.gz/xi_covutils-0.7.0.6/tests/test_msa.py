# pylint: disable=too-many-lines
"""
  Test MSA related functions
"""
from copy import copy
from os import remove
from os.path import join
from random import shuffle
from tempfile import NamedTemporaryFile
from typing import cast

import mock
from pytest import approx, fixture, raises, warns

# pylint: disable=redefined-outer-name
from xi_covutils.msa import (
  _count_gaps,
  _count_mismatches,
  as_desc_seq_dict,
  as_desc_seq_tuple,
  as_sequence_list,
  compare_two_msa,
  from_pfam,
  gap_content,
  gap_content_by_column,
  gapstrip,
  gapstrip_sequences,
  generate_cigar_string,
  get_terminal_gaps,
  map_ref_to_sequence,
  map_reference_to_sequence,
  map_sequence_to_reference,
  pairwise_aln_stats,
  pick_reference,
  pop_reference,
  read_msa,
  shuffle_msa,
  strip_terminal_gaps,
  subset,
  write_msa,
  extract_subsequences,
  pad,
  cut
)

def test_map_reference_to_sequence(test_data_folder):
  """
  Test that map_reference_to_sequence correctly maps the positions
  between the reference of an MSA and another ungapped sequence.
  """
  msa_file = join(test_data_folder, 'msa_01.fasta')
  with warns(DeprecationWarning):
    mapping = map_reference_to_sequence(msa_file, "ABCDE")
    assert mapping[1] == 1
    assert mapping[2] == 2
    assert mapping[3] == 3
    assert mapping[4] == 4
    assert mapping[5] == 5

    mapping = map_reference_to_sequence(msa_file, "XXXABCDE")
    assert mapping[1] == 4
    assert mapping[2] == 5
    assert mapping[3] == 6
    assert mapping[4] == 7
    assert mapping[5] == 8

    mapping = map_reference_to_sequence(msa_file, "XXXABCDE", start=2)
    assert mapping[1] == 4
    assert mapping[2] == 5
    assert mapping[3] == 6
    assert mapping[4] == 7
    assert mapping[5] == 8

    mapping = map_reference_to_sequence(msa_file, "XXXABCDE", start=2, end=4)
    assert mapping[1] == 4
    assert mapping[2] == 5

    msa_file = join(
      test_data_folder,
      'DI1000297_D_P18827_128_A_Q13009_493.fasta'
    )
    seq = (
      'MGNAESQHVEHEFYGEKHASLGRKHTSRSLRLSHKTRRTRHASSGKVIHRNSEVST'
      'RSSSTPSIPQSLAENGLEPFSQDGTLEDFGSPIWVDRVDMGLRPVSYTDSSVTPSV'
      'DSSIVLTAASVQSMPDTEESRLYGDDATYLAEGGRRQHSYTSNGPTFMETASFKKK'
      'RSKSADIWREDSLEFSLSDLSQEHLTSNEEILGSAEEKDCEEARGMETRASPRQLS'
      'TCQRANSLGDLYAQKNSGVTANGGPGSKFAGYCRNLVSDIPNLANHKMPPAAAEET'
      'PPYSNYNTLPCRKSHCLSEGATNPQISHSNSMQGRRAKTTQDVNAGEGSEFADSGI'
      'EGATTDTDLLSRRSNATNSSYSPTTGRAFVGSDSGSSSTGDAARQGVYENFRRELE'
      'MSTTNSESLEEAGSAHSDEQSSGTLSSPGQSDILLTAAQGTVRKAGALAVKNFLVH'
      'KKNKKVESATRRKWKHYWVSLKGCTLFFYESDGRSGIDHNSIPKHAVWVENSIVQA'
      'VPEHPKKDFVFCLSNSLGDAFLFQTTSQTELENWITAIHSACATAVARHHHKEDTL'
      'RLLKSEIKKLEQKIDMDEKMKKMGEMQLSSVTDSKKKKTILDQIFVWEQNLEQFQM'
      'DLFRFRCYLASLQGGELPNPKRLLAFASRPTKVAMGRLGIFSVSSFHALVAARTGE'
      'TGVRRRTQAMSRSASKRRSRFSSLWGLDTTSKKKQGRPSINQVFGEGTEAVKKSLE'
      'GIFDDIVPDGKREKEVVLPNVHQHNPDCDIWVHEYFTPSWFCLPNNQPALTVVRPG'
      'DTARDTLELICKTHQLDHSAHYLRLKFLIENKMQLYVPQPEEDIYELLYKEIEICP'
      'KVTQSIHIEKSDTAADTYGFSLSSVEEDGIRRLYVNSVKETGLASKKGLKAGDEIL'
      'EINNRAADALNSSMLKDFLSQPSLGLLVRTYPELEEGVELLESPPHRVDGPADLGE'
      'SPLAFLTSNPGHSLCSEQGSSAETAPEETEGPDLESSDETDHSSKSTEQVAAFCRS'
      'LHEMNPSDQSPSPQDSTGPQLATMRQLSDADKLRKVICELLETERTYVKDLNCLME'
      'RYLKPLQKETFLTQDELDVLFGNLTEMVEFQVEFLKTLEDGVRLVPDLEKLEKVDQ'
      'FKKVLFSLGGSFLYYADRFKLYSAFCASHTKVPKVLVKAKTDTAFKAFLDAQNPKQ'
      'QHSSTLESYLIKPIQRILKYPLLLRELFALTDAESEEHYHLDVAIKTMNKVASHIN'
      'EMQKIHEEFGAVFDQLIAEQTGEKKEVADLSMGDLLLHTTVIWLNPPASLGKWKKE'
      'PELAAFVFKTAVVLVYKDGSKQKKKLVGSHRLSIYEDWDPFRFRHMIPTEALQVRA'
      'LASADAEANAVCEIVHVKSESEGRPERVFHLCCSSPESRKDFLKAVHSILRDKHRR'
      'QLLKTESLPSSQQYVPFGGKRLCALKGARPAMSRAVSAPSKSLGRRRRRLARNRFT'
      'IDSDAVSASSPEKESQQPPGGGDTDRWVEEQFDLAQYEEQDDIKETDILSDDDEFC'
      'ESVKGASVDRDLQERLQATSISQRERGRKTLDSHASRMAQLKKQAALSGINGGLES'
      'ASEEVIWVRREDFAPSRKLNTEI'
    )
    mapping = map_reference_to_sequence(msa_file, seq, start=129)
    assert mapping[1] == 845
    assert mapping[2] == 846
    assert mapping[80] == 924
    assert mapping[81] == 925
    seq = (
      'MRRAALWLWLCALALSLQPALPQIVATNLPPEDQDGSGDDSDNFSGSGAGALQDITL'
      'SQQTPSTWKDTQLLTAIPTSPEPTGLEATAASTSTLPAGEGPKEGEAVVLPEVEPGL'
      'TAREQEATPRPRETTQLPTTHLASTTTATTAQEPATSHPHRDMQPGHHETSTPAGPS'
      'QADLHTPHTEDGGPSATERAAEDGASSQLPAAEGSGEQDFTFETSGENTAVVAVEPD'
      'RRNQSPVDQGATGASQGLLDRKEVLGGVIAGGLVGLIFAVCLVGFMLYRMKKKDEGS'
      'YSLEEPKQANGGAYQKPTKQEEFYA')
    mapping = map_reference_to_sequence(msa_file, seq, start=1, end=128)
    assert mapping[1] == 245
    assert mapping[2] == 246
    assert mapping[63] == 307
    assert mapping[64] == 308

def test_map_ref_to_sequence():
  """
  Test map_ref_to_sequence
  """
  msadata = [
    ('S1', 'TGCATGCTACTGACATGTGACTATGCTGACTGACTGACTG'),
    ('S2', '---ATGCTACTGACATGTGA-T-TGC--AGTGACTGA---')
  ]
  mapping = map_ref_to_sequence(
    msa_data=msadata,
    sequence='TGCATGCTACTGACATGTGA',
    start=1,
    end=20
  )
  assert mapping[1] == 1
  assert mapping[20] == 20

@mock.patch('xi_covutils.msa._msa.requests')
def test_from_pfam_success(mock_requests):
  """
  Simulates a connection to pfam and test that the method can
  decompress correctly the gzipped data.
  """
  with NamedTemporaryFile(delete=False) as tmp_out:
    mock_requests.get.return_value.iter_content.return_value = [
      b'\x1f\x8b\x08\x086\x0c\xe0[\x00\x03msa_01.fasta'+
      b'\x00\xb3+N-4\xe4\xd2ut\xd2uvq\xe5\xb2\x03\xf2'+
      b'\x8c\xb8*\x1c\x9d*a<c\x14\x9e\t\x8c\x07\x00$c\x17\xe17\x00\x00\x00']
  status = from_pfam('PF00131', tmp_out.name)
  with open(tmp_out.name, "r", encoding="utf-8") as f_in:
    out_content = f_in.read()
    assert out_content == (
      '>seq1\n-AB-CDE\n'
      '>seq2\nxAByCDE\n'
      '>seq3\nxAByCDE\n'
      '>seq4\nxAByCDE'
    )
    assert status
  remove(tmp_out.name)

@mock.patch('xi_covutils.msa._msa.requests')
def test_from_pfam_fail(mock_requests):
  """
  Simulates a connection to pfam that breaks leading to uncomplete gzipped data
  and test that the method returns a False value.
  """
  with NamedTemporaryFile(delete=False) as tmp_out:
    mock_requests.get.return_value.iter_content.return_value = [
      b'\x1f\x8b\x08\x086\x0c\xe0[\x00\x03msa_01.fasta'+
      b'\x00\xb3+N-4\xe4\xd2ut\xd2uvq\xe5\xb2\x03\xf2']
    status = from_pfam('PF00131', tmp_out.name)
    assert not status
    tmp_out.close()
    remove(tmp_out.name)

def test_map_sequence_to_reference(test_data_folder):
  """
  Tests that a map_sequence_to_reference creates correctly a
  mapping from a custom sequence to the reference sequence of an MSA.
  """
  msa_file = join(test_data_folder, 'msa_02.fasta')
  motif = "RRDGWLMG"
  mapped = map_sequence_to_reference(msa_file, motif)
  assert len(mapped) == 8
  assert mapped[1]['position'] == 17
  assert mapped[2]['position'] == 18
  assert mapped[3]['position'] == 19
  assert mapped[4]['position'] == 23
  assert mapped[5]['position'] == 30
  assert mapped[6]['position'] == 34
  assert mapped[7]['position'] == 35
  assert mapped[8]['position'] == 36

  assert mapped[1]['source'] == 'R'
  assert mapped[2]['source'] == 'R'
  assert mapped[3]['source'] == 'D'
  assert mapped[4]['source'] == 'G'
  assert mapped[5]['source'] == 'W'
  assert mapped[6]['source'] == 'L'
  assert mapped[7]['source'] == 'M'
  assert mapped[8]['source'] == 'G'

  assert mapped[1]['target'] == 'R'
  assert mapped[2]['target'] == 'R'
  assert mapped[3]['target'] == 'E'
  assert mapped[4]['target'] == 'G'
  assert mapped[5]['target'] == 'W'
  assert mapped[6]['target'] == 'L'
  assert mapped[7]['target'] == 'M'
  assert mapped[8]['target'] == 'G'

  motif = "RRDGWIMG"
  mapped = map_sequence_to_reference(msa_file, motif, mismatch_tolerance=0)
  assert mapped == {}

  mapped = map_sequence_to_reference(msa_file, motif, mismatch_tolerance=1)
  assert mapped == {}

  mapped = map_sequence_to_reference(msa_file, motif, mismatch_tolerance=2)
  assert len(mapped) == 8

  motif = "RRDWLMG"
  mapped = map_sequence_to_reference(msa_file, motif, gap_tolerance=0)
  assert mapped == {}

  motif = "RREWLMG"
  mapped = map_sequence_to_reference(msa_file, motif, gap_tolerance=1)
  assert len(mapped) == 7

def test_read_msa(test_data_folder):
  """
  Test read_msa
    :param test_data_folder:
  """
  msa_file = join(test_data_folder, "msa_01.fasta")
  msa_data = read_msa(msa_file, msa_format='fasta')
  assert isinstance(msa_data, list)
  assert len(msa_data) == 4
  assert msa_data[0] == ('seq1', '-AB-CDE')
  assert msa_data[3] == ('seq4', 'xAByCDE')

  msa_data = read_msa(msa_file, msa_format='fasta', as_dict=True)
  assert isinstance(msa_data, dict)
  assert len(msa_data) == 4
  assert msa_data['seq1'] == '-AB-CDE'
  assert msa_data['seq4'] == 'xAByCDE'

def test_write_msa():
  """
  Test write_msa
  """
  with NamedTemporaryFile(delete=False) as tmp_out:
    msa_data = [
      ('s1', 'ACTG'),
      ('s3', 'CTGA')
    ]
  write_msa(msa_data, tmp_out.name)
  with open(tmp_out.name, "r", encoding="utf8") as f_in:
    out_content = f_in.read()
    assert out_content == '>s1\nACTG\n>s3\nCTGA\n'
  remove(tmp_out.name)

def test_pop_reference():
  """
  Test pop_reference
  """
  msa_data = [
    ('s1', 'ATCTGACA'),
    ('s2', 'ATCTGACC'),
    ('s3', 'ATCTGACG'),
    ('s4', 'ATCTGACT')
  ]
  results = pop_reference(msa_data, 's3')
  assert len(results) == 4
  assert results[0] == ('s3', 'ATCTGACG')
  assert results[1] == ('s1', 'ATCTGACA')
  assert results[2] == ('s2', 'ATCTGACC')
  assert results[3] == ('s4', 'ATCTGACT')

  msa_data = {
    's1': 'ACTACG',
    's2': 'CATCTG'
  }
  results = pop_reference(msa_data, 's2')
  assert len(results) == 2
  assert results[0] == ('s2', 'CATCTG')
  assert results[1] == ('s1', 'ACTACG')

  with raises(ValueError) as error:
    results = pop_reference(msa_data, 's3')
  assert "not in msa data" in str(error)

  msa_data = ('s1', 'ATGC')
  msa_data = cast(list[tuple[str, str]], msa_data)
  with raises(ValueError) as error:
    results = pop_reference(msa_data, 's2')
  assert "msa_data should be a list or dict" in str(error)

def test_count_gaps():
  """
  Test the number of mismatches between two sequences in a sequence mapping
  is correct.
  """
  # ASDQWEASDRTYASD
  # ---QWE---RTY---
  mapping = {
    4 : 1,
    5 : 2,
    6 : 3,
    10 : 4,
    11 : 5,
    12 : 6
  }
  gaps = _count_gaps(mapping, "ASDQWEASDRTYASD", "QWERTY")
  assert gaps == 3

  # AB-DEF
  # -BC-E-
  mapping = {
    2 : 1,
    4 : 3,
  }
  gaps = _count_gaps(mapping, "ABDEF", "BCE")
  assert gaps == 2

  # AB-DEF
  # --C-E-
  mapping = {
    4 : 2,
  }
  gaps = _count_gaps(mapping, "ABDEF", "CE")
  assert gaps == 2

  # ABD-FHG
  # -B-E---
  mapping = {
    2 : 1,
  }
  gaps = _count_gaps(mapping, "ABDEFHG", "BE")
  assert gaps == 2


def test_count_mismatches():
  """
  Test the number of mismatches between two sequences in a sequence mapping
  is correct.
  """
  seq1 = "ASDQWEASDRTYASD"
  seq2 = "QWERTY"
  seq3 = "QWDRTY"
  mapping = {
    4 : 1,
    5 : 2,
    6 : 3,
    10 : 4,
    11 : 5,
    12 : 6
  }
  mismatches = _count_mismatches(mapping, seq1, seq2)
  assert mismatches == 0

  mismatches = _count_mismatches(mapping, seq1, seq3)
  assert mismatches == 1

def test_map_seq_to_ref_w_tolerance(test_data_folder):
  """
  Tests that a map_sequence_to_reference creates correctly a
  mapping from a custom sequence to the reference sequence of an MSA.
  """
  msa_file = join(test_data_folder, 'msa_02.fasta')
  motif = "RRDGWLMG"
  mapped = map_sequence_to_reference(msa_file, motif, mismatch_tolerance=0)
  assert mapped == {}

  motif = "RR-GWLMG"
  mapped = map_sequence_to_reference(msa_file, motif, gap_tolerance=0)
  assert mapped == {}

def test_gapstrip_sequences_ref():
  """
  Test that gapstrip_sequences function correctly removes gaps according to the
  reference sequence.
  """
  seqs = ["QW-RT-AS-F",
      "-WEXTYAS-F",
      "-WEYTYAS-F",
      "-WEZTYAS-F"]
  gs_results = gapstrip_sequences(seqs)
  assert len(gs_results) == 4
  assert gs_results[0] == "QWRTASF"
  assert gs_results[1] == "-WXTASF"
  assert gs_results[2] == "-WYTASF"
  assert gs_results[3] == "-WZTASF"

  gs_results = gapstrip_sequences(seqs, use_reference=False)
  assert len(gs_results) == 4
  assert gs_results[0] == "QW-RT-ASF"
  assert gs_results[1] == "-WEXTYASF"
  assert gs_results[2] == "-WEYTYASF"
  assert gs_results[3] == "-WEZTYASF"

def test_gapstrip_reference(test_data_folder):
  """
  Test that gapstrip function correctly removes gaps according to the
  reference sequence.
  """
  msa_file = join(test_data_folder, 'msa_02.fasta')
  stripped = gapstrip(msa_file, use_reference=True)
  assert stripped[0].id == "Reference"
  assert str(stripped[0].seq) == "eeQDrrEGWLMGVkesdw"
  assert stripped[1].id == "SEQ_1"
  assert str(stripped[1].seq) == "lqRDrrEGWLMGVkesdw"
  assert stripped[2].id == "SEQ_2"
  assert str(stripped[2].seq) == "eeQDrrEGWLMGVkesdw"
  assert stripped[3].id == "SEQ_3"
  assert str(stripped[3].seq) == "eeQD--EGWLMGVkesdw"
  assert stripped[4].id == "SEQ_4"
  assert str(stripped[4].seq) == "eeQD--EGWLMGVkesdw"

def test_gapstrip_complete(test_data_folder):
  """
  Test that gapstrip function correctly removes gaps if
  the whole column is gap
  """
  msa_file = join(test_data_folder, 'msa_02.fasta')
  stripped = gapstrip(msa_file, use_reference=False)
  assert stripped[0].id == "Reference"
  assert str(stripped[0].seq) == (
    "--------eeQ--D--rrE---G----W-LMG-----Vkesdw---"
  )
  assert stripped[1].id == "SEQ_1"
  assert str(stripped[1].seq) == (
    "amnsrlsklqR--D--rrEatrG----W-LMG-----Vkesdw---"
  )
  assert stripped[2].id == "SEQ_2"
  assert str(stripped[2].seq) == (
    "--------eeQ--D--rrE---GasllWcLMGwiovnVkesdwmet"
  )
  assert stripped[3].id == "SEQ_3"
  assert str(stripped[3].seq) == (
    "--------eeQ--Dth--E---G----W-LMG-----Vkesdw---"
  )
  assert stripped[4].id == "SEQ_4"
  assert str(stripped[4].seq) == (
    "--------eeQaaDth--E---G----W-LMG-----Vkesdw---"
  )

def test_subset():
  """
  Test subset function
  """
  msa_data = [
    ('s1', 'ACTACTGAGTTCGTA'),
    ('s2', 'GCTGCTGAGTTCGTC'),
    ('s3', 'TCTTCTGAGTTCGTC'),
    ('s4', 'CCTCCTGAGTTCGTC')
  ]
  columns = set([1, 4, 8, 15, 43])
  columns = cast(list[int], columns)
  new_msa = subset(msa_data, columns)
  assert new_msa == [
    ('s1', 'AAAA'),
    ('s2', 'GGAC'),
    ('s3', 'TTAC'),
    ('s4', 'CCAC')
  ]

# pylint: disable=too-many-statements
def test_pick_reference(test_data_folder):
  """
  Test pick_reference function
  """
  msa_file = join(test_data_folder, 'msa_02.fasta')

  # test case with identical sequences
  reference_sequence = "amnsrlsklqRDrrEatrGWLMGVkesdw"
  ref = pick_reference(reference_sequence, msa_file)
  assert len(ref) == 1
  ref_id, ref_seq, match_type = ref[0]
  assert ref_id == "SEQ_1"
  assert ref_seq == "AMNSRLSKLQRDRREATRGWLMGVKESDW"
  assert match_type == "IDENTICAL_MATCH"

  reference_sequence = "eeQDrrEGasllWcLMGwiovnVkesdwmet"
  ref = pick_reference(reference_sequence, msa_file)
  assert len(ref) == 1
  ref_id, ref_seq, match_type = ref[0]
  assert ref_id == "SEQ_2"
  assert ref_seq == "EEQDRREGASLLWCLMGWIOVNVKESDWMET"
  assert match_type == "IDENTICAL_MATCH"

  # test case with identical sub-sequences
  reference_sequence = "lsklqRDrrEatrGWLMGV"
  ref = pick_reference(reference_sequence, msa_file)
  assert len(ref) == 1
  ref_id, ref_seq, match_type = ref[0]
  assert ref_id == "SEQ_1"
  assert ref_seq == "AMNSRLSKLQRDRREATRGWLMGVKESDW"
  assert match_type == "IDENTICAL_SUB_MATCH"

  reference_sequence = "GasllWcLMGwiovnVkesdw"
  ref = pick_reference(reference_sequence, msa_file)
  assert len(ref) == 1
  ref_id, ref_seq, match_type = ref[0]
  assert ref_id == "SEQ_2"
  assert ref_seq == "EEQDRREGASLLWCLMGWIOVNVKESDWMET"
  assert match_type == "IDENTICAL_SUB_MATCH"

  # test case with non-identical sub-sequences
  reference_sequence = "lsRlqRDKKEatrGWLMGVkDs"
  ref = pick_reference(reference_sequence, msa_file)
  assert len(ref) == 1
  ref_id, ref_seq, match_type = ref[0]
  assert ref_id == "SEQ_1"
  assert ref_seq == "AMNSRLSKLQRDRREATRGWLMGVKESDW"
  assert match_type == "NON_IDENTICAL_MATCH"

  reference_sequence = "EGGsllWMLMGwiovQVkesd"
  ref = pick_reference(reference_sequence, msa_file)
  assert len(ref) == 1
  ref_id, ref_seq, match_type = ref[0]
  assert ref_id == "SEQ_2"
  assert ref_seq == "EEQDRREGASLLWCLMGWIOVNVKESDWMET"
  assert match_type == "NON_IDENTICAL_MATCH"

  # test case when reference is larger than seqs in msa
  reference_sequence = "tagcralkamnsrlsklqRDrrEatrGWLMGVkesdwrrgalknm"
  ref = pick_reference(reference_sequence, msa_file)
  assert len(ref) == 1
  ref_id, ref_seq, match_type = ref[0]
  assert ref_id == "SEQ_1"
  assert ref_seq == "AMNSRLSKLQRDRREATRGWLMGVKESDW"
  assert match_type == "IDENTICAL_SUB_MATCH"

  reference_sequence = "tagcralkeeQDrrEGasllWcLMGwiovnVkesdwmetrrgalknm"
  ref = pick_reference(reference_sequence, msa_file)
  assert len(ref) == 1
  ref_id, ref_seq, match_type = ref[0]
  assert ref_id == "SEQ_2"
  assert ref_seq == "EEQDRREGASLLWCLMGWIOVNVKESDWMET"
  assert match_type == "IDENTICAL_SUB_MATCH"

  # test case when reference and seqs in msa have nonmatching terminal
  # residues
  reference_sequence = "tagcralksklqRDrrEatrGWLMrrgalknm"
  ref = pick_reference(reference_sequence, msa_file)
  assert len(ref) == 1
  ref_id, ref_seq, match_type = ref[0]
  assert ref_id == "SEQ_1"
  assert ref_seq == "AMNSRLSKLQRDRREATRGWLMGVKESDW"
  assert match_type == "NON_IDENTICAL_MATCH"

  reference_sequence = "tagcralkGasllWcLMGwiovnVkrrgalknm"
  ref = pick_reference(reference_sequence, msa_file)
  assert len(ref) == 1
  ref_id, ref_seq, match_type = ref[0]
  assert ref_id == "SEQ_2"
  assert ref_seq == "EEQDRREGASLLWCLMGWIOVNVKESDWMET"
  assert match_type == "NON_IDENTICAL_MATCH"

@mock.patch('xi_covutils.msa._msa.PairwiseAligner.align')
def test_pick_reference_warning(localms_mock, test_data_folder):
  """
  Test case when there is a warning because sequences cannot be aligned
  """
  localms_mock.side_effect = SystemError()
  reference_sequence = "EGGsllWMLMGwiovQVkesd"
  msa_file = join(test_data_folder, 'msa_02.fasta')
  with warns(UserWarning, match=r"Sequences.+$"):
    pick_reference(reference_sequence, msa_file)

def test_pairwise_aln_stats():
  """
  Test function count_gaps_and_mismatches_in_aln
  """
  seq1 = "CATACTGACTG"
  seq2 = "CATACTGACTG"
  gaps, matches, mismatches, longest_run = pairwise_aln_stats(seq1, seq2)
  assert gaps == 0
  assert matches == 11
  assert mismatches == 0
  assert longest_run == 11

  seq1 = "-ATACTGACT-"
  seq2 = "CATACTGACTG"
  gaps, matches, mismatches, longest_run = pairwise_aln_stats(seq1, seq2)
  assert gaps == 2
  assert matches == 9
  assert mismatches == 0
  assert longest_run == 9

  seq1 = "CATACCCACTG"
  seq2 = "CATACTGACTG"
  gaps, matches, mismatches, longest_run = pairwise_aln_stats(seq1, seq2)
  assert gaps == 0
  assert matches == 9
  assert mismatches == 2
  assert longest_run == 5

  seq1 = "----CCCACTG"
  seq2 = "CATACTGACTG"
  gaps, matches, mismatches, longest_run = pairwise_aln_stats(seq1, seq2)
  assert gaps == 4
  assert matches == 5
  assert mismatches == 2
  assert longest_run == 4

  seq1 = "CATACCCACT"
  seq2 = "CATACTGACTG"
  with raises(ValueError) as err:
    gaps, matches, mismatches, longest_run = pairwise_aln_stats(seq1, seq2)
    assert "different length" in str(err)

  seq1 = "-----CCA"
  seq2 = "CATA----"
  gaps, matches, mismatches, longest_run = pairwise_aln_stats(seq1, seq2)
  assert gaps == 8
  assert matches == 0
  assert mismatches == 0
  assert longest_run == 0

def test_terminal_gaps():
  """
  Test terminal gaps function
  """
  seq = "AAAA"
  terminal_gaps = get_terminal_gaps(seq)
  assert terminal_gaps == [False, False, False, False]

  seq = "AA-"
  terminal_gaps = get_terminal_gaps(seq)
  assert terminal_gaps == [False, False, True]

  seq = "-AA"
  terminal_gaps = get_terminal_gaps(seq)
  assert terminal_gaps == [True, False, False]

  seq = "-AA-"
  terminal_gaps = get_terminal_gaps(seq)
  assert terminal_gaps == [True, False, False, True]

  seq = "---A"
  terminal_gaps = get_terminal_gaps(seq)
  assert terminal_gaps == [True, True, True, False]

  seq = "----"
  terminal_gaps = get_terminal_gaps(seq)
  assert terminal_gaps == [True, True, True, True]

def test_strip_terminal_gaps():
  """
  Test strip_terminal_gaps function
  """
  seq1 = "ABCDEFG"
  seq2 = "-BCDEF-"
  seq3 = "--HLKF-"
  seq4 = "-BZXC--"
  seq5 = "ABVBNF-"
  all_seqs = [seq1, seq2, seq3, seq4, seq5]
  stripped = strip_terminal_gaps(all_seqs)
  assert len(stripped) == 5
  assert stripped[0] == "CDE"
  assert stripped[1] == "CDE"
  assert stripped[2] == "HLK"
  assert stripped[3] == "ZXC"
  assert stripped[4] == "VBN"

  seq1 = "ABCDEFG"
  seq2 = "----BCD"
  seq1, seq2 = strip_terminal_gaps([seq1, seq2])
  assert seq1 == "EFG"
  assert seq2 == "BCD"

@fixture(scope='module')
def simple_msa():
  """
  A simple MSA
  """
  return {
    's1' : "Q-E-T-",
    's2' : "ASDF-G",
    's3' : "ZXCV-B",
    's4' : "ZXCVTB",
    's5' : "ZXCVTB"
  }

def test_shuffle_msa(simple_msa):
  """
  Test shuffle_msa function
  """
  msa_col = shuffle_msa(simple_msa, by='column', keep_gaps=True)
  ncols = len(next(iter(simple_msa.values())))
  cols = [[s[i] for _, s in sorted(msa_col.items())]
      for i in range(ncols)]
  assert sorted(cols[0]) == ["A", "Q", "Z", "Z", "Z"]
  assert sorted(cols[1]) == ["-", "S", "X", "X", "X"] and cols[1][0] == '-'
  assert sorted(cols[2]) == ["C", "C", "C", "D", "E"]
  assert sorted(cols[3]) == ["-", "F", "V", "V", "V"] and cols[3][0] == '-'
  assert (
    sorted(cols[4]) == ["-", "-", "T", "T", "T"] and
    cols[4][1] == '-' and
    cols[4][2] == '-'
  )
  assert sorted(cols[5]) == ["-", "B", "B", "B", "G"] and cols[5][0] == '-'
  assert not msa_col == simple_msa

  msa_col = shuffle_msa(simple_msa, by='column', keep_gaps=False)
  ncols = len(next(iter(simple_msa.values())))
  cols = [
    [s[i] for _, s in sorted(msa_col.items())]
    for i in range(ncols)
  ]
  assert sorted(cols[0]) == ["A", "Q", "Z", "Z", "Z"]
  assert sorted(cols[1]) == ["-", "S", "X", "X", "X"]
  assert sorted(cols[2]) == ["C", "C", "C", "D", "E"]
  assert sorted(cols[3]) == ["-", "F", "V", "V", "V"]
  assert sorted(cols[4]) == ["-", "-", "T", "T", "T"]
  assert sorted(cols[5]) == ["-", "B", "B", "B", "G"]
  assert not (cols[1][0] == '-' and
        cols[3][0] == '-' and
        cols[4][1] == '-' and
        cols[4][2] == '-' and
        cols[5][0] == '-')
  print(
    "This test has a small chance to fail by random chance, "
    "run it again if this happen"
  )
  assert not msa_col == simple_msa

  msa_row = shuffle_msa(simple_msa, by='row', keep_gaps=True)
  assert (sorted(msa_row['s1']) == ['-', '-', '-', 'E', 'Q', 'T']
      and msa_row['s1'][1] == "-"
      and msa_row['s1'][3] == "-"
      and msa_row['s1'][5] == "-")
  assert (
    sorted(msa_row['s2']) == ['-', 'A', 'D', 'F', 'G', 'S'] and
    msa_row['s2'][4] == "-"
  )
  assert (
    sorted(msa_row['s3']) == ['-', 'B', 'C', 'V', 'X', 'Z'] and
    msa_row['s3'][4] == "-"
  )
  assert sorted(msa_row['s4']) == ['B', 'C', 'T', 'V', 'X', 'Z']
  assert sorted(msa_row['s5']) == ['B', 'C', 'T', 'V', 'X', 'Z']
  assert not msa_row == simple_msa

  msa_row = shuffle_msa(simple_msa, by='row', keep_gaps=False)
  assert sorted(msa_row['s1']) == ['-', '-', '-', 'E', 'Q', 'T']
  assert sorted(msa_row['s2']) == ['-', 'A', 'D', 'F', 'G', 'S']
  assert sorted(msa_row['s3']) == ['-', 'B', 'C', 'V', 'X', 'Z']
  assert sorted(msa_row['s4']) == ['B', 'C', 'T', 'V', 'X', 'Z']
  assert sorted(msa_row['s5']) == ['B', 'C', 'T', 'V', 'X', 'Z']
  assert not msa_row == simple_msa
  print(
    "This test has a small chance to fail by random chance, "
    "run it again if this happen"
  )
  assert not (msa_row['s1'][1] == "-"
        and msa_row['s1'][3] == "-"
        and msa_row['s1'][5] == "-"
        and msa_row['s2'][4] == "-"
        and msa_row['s3'][4] == "-")

  msa_row = shuffle_msa(simple_msa, by='both', keep_gaps=True)
  assert not msa_row == simple_msa
  assert (msa_row['s1'][1] == "-"
      and msa_row['s1'][3] == "-"
      and msa_row['s1'][5] == "-"
      and msa_row['s2'][4] == "-"
      and msa_row['s3'][4] == "-")

def test_gap_content():
  """
  Test gap_content function
  """
  msa_data = [
    ('s1', "QWERTY"),
    ('s2', "QWERTY"),
    ('s3', "------")
  ]
  assert gap_content(msa_data) == approx(1.0/3)

  msa_data = [
    ('s1', "QWERTY"),
    ('s2', "------"),
    ('s3', "------")
  ]
  assert gap_content(msa_data) == approx(2.0/3)

  msa_data = [
    ('s1', "------"),
    ('s2', "------"),
    ('s3', "------")
  ]
  assert gap_content(msa_data) == approx(1)

def test_gap_content_by_column():
  """
  Test gap_content_by_column function
  """
  msa_data = [
    ('s1', "-AAAA---"),
    ('s2', "--BBBA--"),
    ('s3', "---CCCC-"),
    ('s4', "----DCCD"),
  ]
  gaps = gap_content_by_column(msa_data)
  assert gaps[0] == 1
  assert gaps[1] == 0.75
  assert gaps[2] == 0.5
  assert gaps[3] == 0.25
  assert gaps[4] == 0
  assert gaps[5] == 0.25
  assert gaps[6] == 0.5
  assert gaps[7] == 0.75

def test_gap_content_by_column_with_sequence_list():
  """
  Test gap_content_by_column function using a list of sequences as input.
  """
  seq_data = [
    "-AAAA---",
    "--BBBA--",
    "---CCCC-",
    "----DCCD",
  ]
  gaps = gap_content_by_column(seq_data)
  assert gaps[0] == 1
  assert gaps[1] == 0.75
  assert gaps[2] == 0.5
  assert gaps[3] == 0.25
  assert gaps[4] == 0
  assert gaps[5] == 0.25
  assert gaps[6] == 0.5
  assert gaps[7] == 0.75

def test_compare_two_msa():
  """Test test_compare_two_msa function"""
  def with_msa_of_equal_size():
    msa1 = [
      ("seq1", "QWERTY"),
      ("seq2", "QWERTY"),
    ]
    msa2 = [
      ("seq1", "QWERTY"),
      ("seq2", "QWERTY"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert result["msa"]["has_same_number_of_sequences"]
    assert result["msa"]["msa1_n_sequences"] == 2
    assert result["msa"]["msa2_n_sequences"] == 2
    assert result["msa"]["identical_msas"]
  def with_msa_of_unequal_size():
    msa1 = [
      ("seq1", "QWERTY"),
      ("seq2", "QWERTY"),
    ]
    msa2 = [
      ("seq1", "QWERTY"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert not result["msa"]["has_same_number_of_sequences"]
    assert result["msa"]["msa1_n_sequences"] == 2
    assert result["msa"]["msa2_n_sequences"] == 1
    assert not result["msa"]["identical_msas"]
  def with_identical_description_in_order():
    msa1 = [
      ("seq1", "QWERTY"),
      ("seq2", "QWERTY"),
    ]
    msa2 = [
      ("seq1", "QWERTY"),
      ("seq2", "QWERTY"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert result["descriptions"]["identical"]
    assert result["descriptions"]["has_same_order"]
  def with_identical_description_out_of_order():
    msa1 = [
      ("seq1", "QWERTY"),
      ("seq2", "QWERTY"),
    ]
    msa2 = [
      ("seq2", "QWERTY"),
      ("seq1", "QWERTY"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert result["descriptions"]["identical"]
    assert not result["descriptions"]["has_same_order"]
  def with_identical_ungapped_sequences():
    msa1 = [
      ("seq1", "QW---ERTY"),
      ("seq2", "ASDFGH"),
    ]
    msa2 = [
      ("seq1", "QWERTY"),
      ("seq2", "AS--DF--GH"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert result["ungapped"]["identical_seqs"]
    assert result["ungapped"]["has_same_order"]
    assert result["ungapped"]["corresponds_with_desc"]
  def with_identical_ungapped_sequences_out_of_order():
    msa1 = [
      ("seq2", "ASDFGH"),
      ("seq1", "QW---ERTY"),
    ]
    msa2 = [
      ("seq1", "QWERTY"),
      ("seq2", "AS--DF--GH"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert result["ungapped"]["identical_seqs"]
    assert not result["ungapped"]["has_same_order"]
    assert result["ungapped"]["corresponds_with_desc"]
  def with_identical_ungapped_sequences_diff_desc():
    msa1 = [
      ("seq1", "QW---ERTY"),
      ("seq2", "ASDFGH"),
    ]
    msa2 = [
      ("seq 1", "QWERTY"),
      ("seq 2", "AS--DF--GH"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert result["ungapped"]["identical_seqs"]
    assert result["ungapped"]["has_same_order"]
    assert not result["ungapped"]["corresponds_with_desc"]
  def with_identical_gapped_sequences():
    msa1 = [
      ("seq1", "QW---ERTY"),
      ("seq2", "AS--DF--GH"),
    ]
    msa2 = [
      ("seq1", "QW---ERTY"),
      ("seq2", "AS--DF--GH"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert result["gapped"]["identical_seqs"]
    assert result["gapped"]["has_same_order"]
    assert result["gapped"]["corresponds_with_desc"]
  def with_identical_gapped_sequences_out_of_order():
    msa1 = [
      ("seq2", "AS--DF--GH"),
      ("seq1", "QW---ERTY"),
    ]
    msa2 = [
      ("seq1", "QW---ERTY"),
      ("seq2", "AS--DF--GH"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert result["gapped"]["identical_seqs"]
    assert not result["gapped"]["has_same_order"]
    assert result["gapped"]["corresponds_with_desc"]
  def with_identical_gapped_sequences_diff_desc():
    msa1 = [
      ("seq1", "AS--DF--GH"),
      ("seq2", "QW---ERTY"),
    ]
    msa2 = [
      ("seq1", "QW---ERTY"),
      ("seq2", "AS--DF--GH"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert result["gapped"]["identical_seqs"]
    assert not result["gapped"]["has_same_order"]
    assert not result["gapped"]["corresponds_with_desc"]
  def with_identical_msas():
    msa1 = [
      ("seq1", "AS--DF--GH"),
      ("seq2", "QW---ERTY"),
    ]
    msa2 = [
      ("seq1", "AS--DF--GH"),
      ("seq2", "QW---ERTY"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert result["msa"]["identical_msas"]
  with_msa_of_equal_size()
  with_msa_of_unequal_size()
  with_identical_description_in_order()
  with_identical_description_out_of_order()
  with_identical_ungapped_sequences()
  with_identical_ungapped_sequences_out_of_order()
  with_identical_ungapped_sequences_diff_desc()
  with_identical_gapped_sequences()
  with_identical_gapped_sequences_out_of_order()
  with_identical_gapped_sequences_diff_desc()
  with_identical_msas()

def test_as_sequence_list(test_data_folder):
  """Test test_as_sequence_list function"""
  def from_msa_file():
    msa_file = join(test_data_folder, "msa_01.fasta")
    result = as_sequence_list(msa_file)
    expected = [
      "-AB-CDE",
      "xAByCDE",
      "xAByCDE",
      "xAByCDE"
    ]
    assert result == expected
  def from_desc_seq_dict():
    input_msa = {
      "seq1": "-AB-CDE",
      "seq2": "xAByCDE",
      "seq3": "xAByCDE",
      "seq4": "xAByCDE"
    }
    expected = [
      "-AB-CDE",
      "xAByCDE",
      "xAByCDE",
      "xAByCDE"
    ]
    result = as_sequence_list(input_msa)
    assert set(result) == set(expected)
  def from_desc_seq_tuple_list():
    input_msa = [
      ("seq1", "-AB-CDE"),
      ("seq2", "xAByCDE"),
      ("seq3", "xAByCDE"),
      ("seq4", "xAByCDE"),
    ]
    expected = [
      "-AB-CDE",
      "xAByCDE",
      "xAByCDE",
      "xAByCDE"
    ]
    result = as_sequence_list(input_msa)
    assert set(result) == set(expected)
  def from_seq_list():
    input_msa = [
      "-AB-CDE",
      "xAByCDE",
      "xAByCDE",
      "xAByCDE",
    ]
    expected = [
      "-AB-CDE",
      "xAByCDE",
      "xAByCDE",
      "xAByCDE"
    ]
    result = as_sequence_list(input_msa)
    assert result == expected
  from_msa_file()
  from_desc_seq_dict()
  from_desc_seq_tuple_list()
  from_seq_list()

def test_as_desc_seq_dict(test_data_folder):
  """Test as_desc_seq_dict function"""
  def from_msa_file():
    msa_file = join(test_data_folder, "msa_01.fasta")
    result = as_desc_seq_dict(msa_file)
    expected = {
      "seq1": "-AB-CDE",
      "seq2": "xAByCDE",
      "seq3": "xAByCDE",
      "seq4": "xAByCDE"
    }
    assert result == expected
  def from_desc_seq_dict():
    input_msa = {
      "seq1": "-AB-CDE",
      "seq2": "xAByCDE",
      "seq3": "xAByCDE",
      "seq4": "xAByCDE"
    }
    expected = {
      "seq1": "-AB-CDE",
      "seq2": "xAByCDE",
      "seq3": "xAByCDE",
      "seq4": "xAByCDE"
    }
    result = as_desc_seq_dict(input_msa)
    assert set(result) == set(expected)
  def from_desc_seq_tuple_list():
    input_msa = [
      ("seq1", "-AB-CDE"),
      ("seq2", "xAByCDE"),
      ("seq3", "xAByCDE"),
      ("seq4", "xAByCDE"),
    ]
    expected = {
      "seq1": "-AB-CDE",
      "seq2": "xAByCDE",
      "seq3": "xAByCDE",
      "seq4": "xAByCDE"
    }
    result = as_desc_seq_dict(input_msa)
    assert result == expected
  def from_seq_list():
    input_msa = [
      "-AB-CDE",
      "xAByCDE",
      "xAByCDE",
      "xAByCDE",
    ]
    expected_desc = {
      "seq_1",
      "seq_2",
      "seq_3",
      "seq_4"
    }
    result = as_desc_seq_dict(input_msa)
    assert set(result.values()) == set(input_msa)
    assert set(result.keys()) == expected_desc
  from_msa_file()
  from_desc_seq_dict()
  from_desc_seq_tuple_list()
  from_seq_list()


def test_as_desc_seq_tuple(test_data_folder):
  """test test_as_desc_seq_tuple function"""
  def from_msa_file():
    msa_file = join(test_data_folder, "msa_01.fasta")
    result = as_desc_seq_tuple(msa_file)
    expected = [
      ("seq1", "-AB-CDE"),
      ("seq2", "xAByCDE"),
      ("seq3", "xAByCDE"),
      ("seq4", "xAByCDE")
    ]
    assert result == expected
  def from_desc_seq_dict():
    input_msa = {
      "seq1": "-AB-CDE",
      "seq2": "xAByCDE",
      "seq3": "xAByCDE",
      "seq4": "xAByCDE"
    }
    expected = [
      ("seq1", "-AB-CDE"),
      ("seq2", "xAByCDE"),
      ("seq3", "xAByCDE"),
      ("seq4", "xAByCDE")
    ]
    result = as_desc_seq_tuple(input_msa)
    assert set(result) == set(expected)
  def from_desc_seq_tuple_list():
    input_msa = [
      ("seq1", "-AB-CDE"),
      ("seq2", "xAByCDE"),
      ("seq3", "xAByCDE"),
      ("seq4", "xAByCDE"),
    ]
    expected = [
      ("seq1", "-AB-CDE"),
      ("seq2", "xAByCDE"),
      ("seq3", "xAByCDE"),
      ("seq4", "xAByCDE"),
    ]
    result = as_desc_seq_tuple(input_msa)
    assert set(result) == set(expected)
  def from_seq_list():
    input_msa = [
      "-AB-CDE",
      "xAByCDE",
      "xAByCDE",
      "xAByCDE",
    ]
    expected = [
      ("seq_1", "-AB-CDE"),
      ("seq_2", "xAByCDE"),
      ("seq_3", "xAByCDE"),
      ("seq_4", "xAByCDE"),
    ]
    result = as_desc_seq_tuple(input_msa)
    assert result == expected
  from_msa_file()
  from_desc_seq_dict()
  from_desc_seq_tuple_list()
  from_seq_list()

def test_generate_cigar_string():
  """
  Test Generate Cigar String
  """
  def _matching_sequences():
    reference = "ACGTAGTCAGT"
    query = "ACGTAGTCAGT"
    expected_cigar = "11M"
    cigar = generate_cigar_string(reference, query)
    assert cigar == expected_cigar
  def _insertions():
    reference = "ACGTAGTTCAGT"
    query =     "ACGTAGT-CAGT"
    expected_cigar = "7M1I4M"
    cigar = generate_cigar_string(reference, query)
    assert cigar == expected_cigar
  def _deletions():
    reference = "ACGTAG-TCAGT"
    query = "ACGTAGCTCAGT"
    expected_cigar = "6M1D5M"
    cigar = generate_cigar_string(reference, query)
    assert cigar == expected_cigar
  def _soft_clipping():
    reference = "ACGTAGTCAGT"
    query  = "---TAGTCAGT"
    expected_cigar = "3S8M"
    cigar = generate_cigar_string(reference, query)
    assert cigar == expected_cigar
  def _mismatching_sequences():
    reference = "ACGTAGTCAGT"
    query =     "ACCTAGTCAGT"
    expected_cigar = "2M1X8M"
    cigar = generate_cigar_string(reference, query)
    assert cigar == expected_cigar
  _mismatching_sequences()
  _insertions()
  _deletions()
  _soft_clipping()
  _matching_sequences()

def test_extract_subsequences():
  """
  Test extracting subsequences from an MSA by description with indexes.
  """
  def test_empty_msa():
    msa_data = {}
    desc = [
      ("s1", [0, 0])
    ]
    res = extract_subsequences(msa_data, desc)
    assert isinstance(res, list)
    assert not res
  def test_empty_descriptions():
    msa_data = [
      ("s1", "ACTAGCACTCATA"),
      ("s2", "ACYACTATACTACACACTTCCTACC")
    ]
    desc = {}
    res = extract_subsequences(msa_data, desc)
    assert isinstance(res, list)
    assert not res
  def test_simple_case():
    msa_data = [
      ("s1", "ACTAGCACTCATA"),
      ("s2", "ACYACTATACTACACACTTCCTACC")
    ]
    desc = {
      "s1": [0, 4]
    }
    res = extract_subsequences(msa_data, desc)
    assert res == [("s1", "ACTA")]
  def test_indexes_out_of_range():
    msa_data = [
      ("s1", "ACTAGCACTCATA"),
      ("s2", "ACYACTATACTACACACTTCCTACC")
    ]
    desc = {
      "s1": [0, 20]
    }
    res = extract_subsequences(msa_data, desc)
    assert res == [("s1", "ACTAGCACTCATA-------")]
  def test_negative_index():
    msa_data = [
      ("s1", "ACTA"),
    ]
    desc = {
      "s1": [-1, 3]
    }
    res = extract_subsequences(msa_data, desc)
    assert res == [("s1", "-ACT")]
  def test_descriptions_not_in_msa():
    msa_data = [
      ("s1", "ACTA"),
    ]
    desc = {
      "s1": [1, 3],
      "s3": [1, 3],
    }
    res = extract_subsequences(msa_data, desc)
    assert res == [("s1", "CT")]
  def test_missing_descriptions():
    msa_data = [
      ("s1", "ACTA"),
      ("s2", "ACTA"),
    ]
    desc = {
      "s1": [1, 3]
    }
    res = extract_subsequences(msa_data, desc)
    assert res == [("s1", "CT")]
  def test_inverted_indexes():
    msa_data = [
      ("s1", "ACTA"),
      ("s2", "GATA"),
    ]
    desc = {
      "s1": [4, 0],
      "s2": [4, 1]
    }
    res = extract_subsequences(msa_data, desc)
    assert res == [("s1", "ACTA"), ("s2", "ATA")]
  def test_equal_start_and_end_indexe():
    msa_data = [
      ("s1", "ACTA"),
    ]
    desc = {
      "s1": [0, 0],
    }
    res = extract_subsequences(msa_data, desc)
    assert isinstance(res, list)
    assert not res
  def test_order_should_be_kept():
    desc_num = list(f"{x}" for x in range(10000))
    desc_num2 = copy(desc_num)
    shuffle(desc_num)
    assert desc_num != desc_num2
    msa_data = [
      (f"{x}", "ACTG") for x in desc_num
    ]
    desc = {
      f"{x}": (0, 2)
      for x in desc_num2
    }
    res = [x for x, _ in extract_subsequences(msa_data, desc)]
    assert res == desc_num
  test_empty_msa()
  test_empty_descriptions()
  test_simple_case()
  test_indexes_out_of_range()
  test_negative_index()
  test_descriptions_not_in_msa()
  test_missing_descriptions()
  test_inverted_indexes()
  test_equal_start_and_end_indexe()
  test_order_should_be_kept()

def test_pad():
  def test_empty_msa():
    msa_data = []
    padded = pad(msa_data)
    assert isinstance(padded, list)
    assert not padded
  def test_single_sequence_without_terminal_gaps():
    msa_data = [
      ("s1", "ACTG")
    ]
    padded = pad(msa_data)
    assert padded == [("s1", "ACTG")]
  def test_single_sequence_with_terminal_gaps():
    msa_data = [
      ("s1", "ACTG---")
    ]
    padded = pad(msa_data)
    assert padded == [("s1", "ACTG")]
  def test_single_sequence_with_internal_gaps():
    msa_data = [
      ("s1", "AC--TG---")
    ]
    padded = pad(msa_data)
    assert padded == [("s1", "AC--TG")]
  def test_multiple_sequences_without_gaps_and_equal_length():
    msa_data = [
      ("s1", "ACTG"),
      ("s2", "ACTT"),
    ]
    padded = pad(msa_data)
    assert padded == [("s1", "ACTG"), ("s2", "ACTT")]
  def test_multiple_sequences_without_gaps_and_diff_length():
    msa_data = [
      ("s1", "ACTG"),
      ("s2", "ACTTA"),
    ]
    padded = pad(msa_data)
    assert padded == [("s1", "ACTG-"), ("s2", "ACTTA")]
  def test_order_should_be_kept():
    desc_num = list(f"{x}" for x in range(10000))
    desc_num2 = copy(desc_num)
    shuffle(desc_num)
    assert desc_num != desc_num2
    msa_data = [
      (f"{x}", "ACTG") for x in desc_num
    ]
    res = [x for x, _ in pad(msa_data)]
    assert res == desc_num

  test_empty_msa()
  test_single_sequence_without_terminal_gaps()
  test_single_sequence_with_terminal_gaps()
  test_single_sequence_with_internal_gaps()
  test_multiple_sequences_without_gaps_and_equal_length()
  test_multiple_sequences_without_gaps_and_diff_length()
  test_order_should_be_kept()

def test_cut():
  def test_with_empty_msa():
    msa_data = []
    res = cut(msa_data, 1, 100)
    assert isinstance(res, list)
    assert not res
  def test_with_single_sequence():
    msa_data = [
      ("s1", "ACTACTACT")
    ]
    res = cut(msa_data, 1, 3)
    assert res == [("s1", "ACT")]
  def test_with_single_sequence_extended_end():
    msa_data = [
      ("s1", "ACT")
    ]
    res = cut(msa_data, 1, 4)
    assert res == [("s1", "ACT-")]
  def test_with_start_greater_then_end():
    msa_data = [
      ("s1", "ACT")
    ]
    res = cut(msa_data, 4, 1)
    assert res == []
  def test_with_indexes_out_of_sequence():
    msa_data = [
      ("s1", "ACT")
    ]
    res = cut(msa_data, 4, 6)
    assert res == [("s1", "---")]
  def test_with_many_sequences():
    msa_data = [
      ("s1", "ACTATG"),
      ("s2", "ACT---"),
      ("s3", "A-----"),
      ("s4", "----AG"),
      ("s5", "--GTAG"),
    ]
    res = cut(msa_data, 3, 5)
    assert res == [
      ("s1", "TAT"),
      ("s2", "T--"),
      ("s3", "---"),
      ("s4", "--A"),
      ("s5", "GTA"),
    ]
  def test_with_many_sequences_of_different_lengths():
    msa_data = [
      ("s1", "ACTATGATATG"),
      ("s2", "ACTATGTG"),
      ("s3", "AATTCA"),
      ("s4", "AG"),
      ("s5", "G"),
    ]
    res = cut(msa_data, 3, 9)
    assert res == [
      ("s1", "TATGATA"),
      ("s2", "TATGTG-"),
      ("s3", "TTCA---"),
      ("s4", "-------"),
      ("s5", "-------"),
    ]
  test_with_empty_msa()
  test_with_single_sequence()
  test_with_single_sequence_extended_end()
  test_with_start_greater_then_end()
  test_with_indexes_out_of_sequence()
  test_with_many_sequences()
  test_with_many_sequences_of_different_lengths()
