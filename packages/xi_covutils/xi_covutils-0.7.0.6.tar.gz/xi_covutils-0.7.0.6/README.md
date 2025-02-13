# Utilities to compute and analyze protein covariation

## Description

This pack has some tools to make easier to work with protein covariation.

This package is compatible with python 3.

## Package content

### PDB to sequence mapper

```python
    from xi_covutils.pdbmapper import PDBSeqMapper
    pdb_file = "WXYZ.pdb"
    mapper = PDBSeqMapper()
    sequence = "ACDEFGHIKLM"
    chain = "A"
    # Makes the alignment between the sequence and the PDB file.
    mapper.align_sequence_to_pdb(sequence, pdb_file, chain)
    # Retrieves the original sequence.
    query = mapper.get_sequence() == sequence
    # Retrieves the aligned original sequene to the PDB sequence.
    aln_seq = mapper.get_aln_sequence()
    # Retrieves the amino acid pdb sequence
    # Non standard, HOH and HETERO are removed
    pdb_seq = mapper.get_pdb_sequence()
    # Rerieves the aligned pdb sequence
    aln_pdb_seq = mapper.get_aln_pdb_sequence()
    # Retrieves the sequence position index from the residue number
    # annotated the the PDB file.
    # The index starts in 1.
    assert mapper.from_residue_number_to_seq(0) == 4
    assert mapper.from_residue_number_to_seq(1) == 5
    # Retrieves the residue number from the index position of te sequence.
    # The index starts in 1.
    assert mapper.from_seq_to_residue_number(4) == 0
    assert mapper.from_seq_to_residue_number(5) == 1

```
### Calculate distances over two regions in a pdb structure

```python
    from xi_covutils.distances import calculate_distances_between_regions
    pdb_file = join("5IZE.pdb")
    chain1 = "A"
    reg1 = [1, 2]
    chain2 = "B"
    reg2 = [7, 8]
    distances = calculate_distances_between_regions(
      pdb_file,
      chain1,
      chain2,
      reg1,
      reg2
    )
    assert distances == [
        ('A', 1, 'MET', 'CE', 'B', 7, 'ILE', 'CD1', 76.32719),
        ('A', 1, 'MET', 'SD', 'B', 8, 'HIS', 'CD2', 76.88578),
        ('A', 2, 'ASP', 'N', 'B', 7, 'ILE', 'CD1', 81.55944),
        ('A', 2, 'ASP', 'N', 'B', 8, 'HIS', 'CD2', 81.966064)
    ]
```

### Load distances from MIToS

### Compute mean number of intramolecular contacts for every chain

```python
    dist_data = [
        ('A', 1, 'A', 2, 1),
        ('A', 1, 'A', 3, 1),
        ('A', 1, 'A', 4, 1),
        ('A', 1, 'A', 5, 1),
        ('A', 2, 'A', 3, 1),
        ('A', 2, 'A', 4, 9),
        ('A', 2, 'A', 5, 1),
        ('A', 3, 'A', 4, 9),
        ('A', 3, 'A', 5, 9),
        ('A', 4, 'A', 5, 1),
        ('B', 1, 'A', 2, 10)
    ]
    dist = Distances(dist_data)
    mean_ic = dist.mean_intramolecular()
    # After execution:
    mean_ic = {'A': 2.8, 'B': 0.0}
```

### MSA to sequence mapper

### Sequence to MSA mapper

```python
    # MSA contains this:
    # >Reference
    # --------eeQ--D--rrE---G------W---LMG-----Vkesdw---
    # >SEQ_1
    # amnsrlsklqR--D--rrEatrG------W---LMG-----Vkesdw---
    # >SEQ_2
    # --------eeQ--D--rrE---Gas--llWc--LMGwiovnVkesdwmet
    # >SEQ_3
    # --------eeQ--Dth--E---G------W---LMG-----Vkesdw---
    # >SEQ_4
    # --------eeQaaDth--E---G------W---LMG-----Vkesdw---
    msa_file = "my_msa.fasta"
    motif = "RRDGWLMG"
    mapped = map_sequence_to_reference(msa_file, motif)

    # After execution:
    mapped = {
        1: {'position': 17, 'source': 'R', 'target': 'R'},
        2: {'position': 18, 'source': 'R', 'target': 'R'},
        3: {'position': 19, 'source': 'D', 'target': 'E'},
        4: {'position': 23, 'source': 'G', 'target': 'G'},
        5: {'position': 30, 'source': 'W', 'target': 'W'},
        6: {'position': 34, 'source': 'L', 'target': 'L'},
        7: {'position': 35, 'source': 'M', 'target': 'M'},
        8: {'position': 36, 'source': 'G', 'target': 'G'}
    }
```
### MSA gapstrip
```python
    # MSA contains this:
    # >Reference
    # --------eeQ--D--rrE---G------W---LMG-----Vkesdw---
    # >SEQ_1
    # amnsrlsklqR--D--rrEatrG------W---LMG-----Vkesdw---
    # >SEQ_2
    # --------eeQ--D--rrE---Gas--llWc--LMGwiovnVkesdwmet
    # >SEQ_3
    # --------eeQ--Dth--E---G------W---LMG----stripped-Vkesdw---
    # >SEQ_4
    # --------eeQaaDth--E---G------W---LMG-----Vkesdw---
    msa_file = "my_msa.fasta"
    stripped = gapstrip(msa_file, use_reference=True)

    # After execution:
    stripped = [
        SeqRecord(seq='eeQDrrEGWLMGVkesdw', id='Reference',
            name='Reference', description='Reference', dbxrefs=[]),
        SeqRecord(seq='lqRDrrEGWLMGVkesdw', id='SEQ_1',
            name='SEQ_1', description='SEQ_1', dbxrefs=[]),
        SeqRecord(seq='eeQDrrEGWLMGVkesdw', id='SEQ_2',
            name='SEQ_2', description='SEQ_2', dbxrefs=[]),
        SeqRecord(seq='eeQD--EGWLMGVkesdw', id='SEQ_3', 
            name='SEQ_3', description='SEQ_3', dbxrefs=[]),
        SeqRecord(seq='eeQD--EGWLMGVkesdw', id='SEQ_4', 
            name='SEQ_4', description='SEQ_4', dbxrefs=[])]

    stripped = gapstrip(msa_file, use_reference=False)
    # After execution:
    stripped = [
        SeqRecord(seq='--------eeQ--D--rrE---G----W-LMG-----Vkesdw---',
            id='Reference', name='Reference', description='Reference', dbxrefs=[]),
        SeqRecord(seq='amnsrlsklqR--D--rrEatrG----W-LMG-----Vkesdw---',
            id='SEQ_1', name='SEQ_1', description='SEQ_1', dbxrefs=[]),
        SeqRecord(seq='--------eeQ--D--rrE---GasllWcLMGwiovnVkesdwmet',
            id='SEQ_2', name='SEQ_2', description='SEQ_2', dbxrefs=[]),
        SeqRecord(seq='--------eeQ--Dth--E---G----W-LMG-----Vkesdw---',
            id='SEQ_3', name='SEQ_3', description='SEQ_3', dbxrefs=[]),
        SeqRecord(seq='--------eeQaaDth--E---G----W-LMG-----Vkesdw---',
            id='SEQ_4', name='SEQ_4', description='SEQ_4', dbxrefs=[])]
```

### Sequences gapstrip
```python
    sequences = ["QW-RT-AS-F",
            "-WEXTYAS-F",
            "-WEYTYAS-F",
            "-WEZTYAS-F"]
    stripped = gapstrip_sequences(sequences)

    # After execution:
    stripped = ["QWRTASF", "-WXTASF", "-WYTASF" ,"-WZTASF"]

    stripped = gapstrip_sequences(sequences, use_reference=False)
    # After execution:
    stripped = ["QW-RT-ASF", "-WEXTYASF", "-WEYTYASF", "-WEZTYASF"]
```

### Pop reference of MSA sequence

```python
    msa_data = [
        ('s1', 'ATCTGACA'),
        ('s2', 'ATCTGACC'),
        ('s3', 'ATCTGACG'),
        ('s4', 'ATCTGACT')
    ]
    msa_data = pop_reference(msa_data, 's3')
    # After execution
    msa_data = [
        ('s3', 'ATCTGACG'),
        ('s1', 'ATCTGACA'),
        ('s2', 'ATCTGACC'),
        ('s4', 'ATCTGACT')
    ]

    msa_data = {
        's1': 'ACTACG',
        's2': 'CATCTG'
    }
    msa_data = pop_reference(msa_data, 's2')
    # After execution
    msa_data = [
        ('s1': 'ACTACG'),
        ('s2': 'CATCTG')
    ]
```

### Pick a reference sequence from a MSA.
```python
    reference_sequence = "amnsrlsklqRDrrEatrGWLMGVkesdw"
    msa_file = "some_msa.fasta
    ref = pick_reference(reference_sequence, msa_file)
    assert len(ref) == 1
    ref_id, ref_seq, match_type = ref[0]
    assert ref_id == "SEQ_1"
    assert ref_seq == "AMNSRLSKLQRDRREATRGWLMGVKESDW"
    assert match_type == "IDENTICAL_MATCH"
```

### Compare two MSA sequences

```python
    msa1 = [
      ("seq1", "QWERTY"),
      ("seq2", "QWERTY"),
    ]
    msa2 = [
      ("seq1", "QWERTY"),
      ("seq2", "QWERTY"),
    ]
    result = compare_two_msa(msa1, msa2)
    assert result == {
        'msa1_n_sequences': 2,
        'msa2_n_sequences': 2,
        'has_same_number_of_sequences': True,
        'identical_descriptions': True,
        'identical_has_same_order': True,
        'ungapped': {
            'identical_seqs': True,
            'has_same_order': True,
            'corresponds_with_desc': True
        },
        'gapped': {
            'identical_seqs': True,
            'has_same_order': True,
            'corresponds_with_desc': True
        },
        'identical_msa': True
    }

```

### Download MSA from pfam

### Calculate gap content

```python
    msa_data = [
        ('s1', "QWERTY"),
        ('s2', "QWERTY"),
        ('s3', "------")
    ]
    assert gap_content(msa_data) == approx(1.0/3)
```

### Calculate gap content by column

```python
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
```

### ROC curve and auc calculation.

```python
    # Merge covariation scores and contact distance
    dist_elems = [
        ('A', 1, 'A', 2, 6.01),
        ('A', 1, 'A', 3, 6.02),
        ('A', 1, 'A', 4, 6.13),
        ('A', 2, 'A', 3, 6.24),
        ('A', 2, 'A', 4, 6.35),
    ]
    ditances = Distances(dist_elems)
    scores = {
        (('A', 1), ('A', 2)) : 0.11,
        (('A', 1), ('A', 3)) : 0.12,
        (('A', 1), ('A', 4)) : 0.13,
        (('A', 2), ('A', 3)) : 0.14,
        (('A', 2), ('A', 4)) : 0.15,
        (('A', 3), ('A', 4)) : 0.16,
    }
    merged = merge_scores_and_distances(scores, ditances)
    # After execution, the merged is not ordered
    merged = [
        (0.11, True),
        (0.12, True),
        (0.13, False),
        (0.14, False),
        (0.15, False),
    ]
```

```python
    # Get binary classification of contacts
    merged = [
        (0.11, True),
        (0.12, True),
        (0.13, False),
        (0.14, False),
        (0.15, False),
    ]
    binary = binary_from_merged(merged)
    # After execution:
    binary = [False, False, False, True, True]
```

```python
    # calculate curve roc from binary
    binary = [False, False, False, True, True]
    curve1 = curve(binary, method='roc')
    curve2 = curve(binary, method='precision_recall')
```

### Load results from ccmpred output

```python
cov_data = from_ccmpred(cov_file)
```

### Calculate smoothed covariation

```python
cov_data = from_ccmpred(cov_file)
smoothed = smooth_cov(cov_data)
```

### Run mkdssp

```python
from xi_covutils.mkdssp import mkdssp
results = mkdssp(a_pdb_file)

# After execution
# results =
# {('A', 1): {'aa': 'K', 'chain': 'A', 'index': 1, 'pdb_num': 1, 'structure': ''},
#  ('A', 2): {'aa': 'V', 'chain': 'A', 'index': 2, 'pdb_num': 2, 'structure': ''},
#  ('A', 3): {'aa': 'S', 'chain': 'A', 'index': 3, 'pdb_num': 3, 'structure': ''},
#  ('A', 4): {'aa': 'G', 'chain': 'A', 'index': 4, 'pdb_num': 4, 'structure': ''},
#  ('A', 5): {'aa': 'T', 'chain': 'A', 'index': 5, 'pdb_num': 5, 'structure': ''},
#  ('A', 6): {'aa': 'V', 'chain': 'A', 'index': 6, 'pdb_num': 6, 'structure': ''},
#  ('A', 7): {'aa': 'C', 'chain': 'A', 'index': 7, 'pdb_num': 7, 'structure': ''},
#  etc
# }
```

### Split results of paired MSA in inter and intra chain covariation

### Sequence clustering using Hobohm-1 algorithm

```python
    from xi_covutils.clustering import hobohm1
    sequences = [
        'ABCDEFGHIJ',
        'ABCDEFGHIZ',
        'ABCDEFZXCW',
        'ABCDEFZXCK'
    ]
    results = hobohm1(sequences)
    # After execution:
    # results = [
    #   Cluster:[2][ABCDEFGHIJ] ABCDEFGHIJ, ABCDEFGHIZ,
    #   Cluster:[2][ABCDEFZXCW] ABCDEFZXCW, ABCDEFZXCK
    # ]
```

### Sequence clustering using kmers
```python
    from xi_covutils.clustering import kmer_clustering
    sequences = [
        'ABCDEFGHIJ',
        'ABCDEFGHIZ',
        'ABCDEFZXCW',
        'ABCDEFZXCK'
    ]
    results = kmer_clustering(sequences)
    # After execution:
    # results = [
    #   Cluster:[2][ABCDEFGHIJ] ABCDEFGHIJ, ABCDEFGHIZ, 
    #   Cluster:[2][ABCDEFZXCW] ABCDEFZXCW, ABCDEFZXCK
    # ]
```

### Read contact map files from SCPE
```python
    content = StringIO("""Tertiary contact map
Warning!. Position 2 has 0 contacts
Quaternary contact map
Warning!. Position 2 has 0 contacts
Terciary
0 1 1
1 0 0
1 0 0
Quaternary
0 0 1
0 0 1
1 1 0
Tertiary Total contacts  Quaternary Total contacts
2           2  0
0           0  0
3           3  0
""")
    c_map = contact_map_from_scpe(content, quaternary=False)
    # After execution:
    # c_map = {
    #    (1, 1) : 0,
    #    (1, 2) : 1,
    #    (1, 3) : 1,
    #    (2, 1) : 1,
    #    (2, 2) : 0,
    #    (2, 3) : 0,
    #    (3, 1) : 1,
    #    (3, 2) : 0,
    #    (3, 3) : 0,
    # }
```

### Read contact map files from text file
```python
    content = StringIO("""
0 1 1
1 0 0
1 0 0
""")
    c_map = contact_map_from_text(content)
    # After execution:
    # c_map = {
    #    (1, 1) : 0,
    #    (1, 2) : 1,
    #    (1, 3) : 1,
    #    (2, 1) : 1,
    #    (2, 2) : 0,
    #    (2, 3) : 0,
    #    (3, 1) : 1,
    #    (3, 2) : 0,
    #    (3, 3) : 0,
    # }
```

### Create Distances objects from contact map
```python
    content = StringIO("""
0 1 1
1 0 0
1 0 0
""")
    c_map = contact_map_from_text(content)
    dist = Distances.from_contact_map(c_map)
```

### Create Distances objects from contact map
```python
    seqs = [
        "ACTACTATCTAGCTAGC",
        "ACTACTGATGCACTGTG",
        "ACTACTGATCTACTGAG"
    ]
    results = entropy(seqs, False, 62)
    # expected_results = [
    #     -0.0, -0.0, -0.0, -0.0, -0.0, -0.0,
    #     0.6931471805599453, 0.6931471805599453,
    #     0.6931471805599453, 1.0397207708399179,
    #     1.0397207708399179, 0.6931471805599453,
    #     -0.0, -0.0,
    #     0.6931471805599453, 1.0397207708399179,
    #     0.6931471805599453]
```


## How to install

    > pip install dist/xi_covutils-x.y.z

## Dependencies

- biopython >= 1.72
- requests

## Development dependencies

In development_requirements.txt

## Running tests

    > pytest tests

## Documentation

Automatic documentation from code is in the 'docs' folder.