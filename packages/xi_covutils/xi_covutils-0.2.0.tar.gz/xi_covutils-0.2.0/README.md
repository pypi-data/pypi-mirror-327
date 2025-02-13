# Utilities to compute and analyze protein covariation

## Description

This pack has some tools to make easier to work with protein covariation.

This package is compatible with python 3.

## Package content

### PDB to sequence mapper

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

### Download MSA from pfam

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

### Load results from ccmpred output

### Calculate smoothed covariation

```python
cov_data = from_ccmpred(cov_file)
smoothed = smooth_cov(cov_data)
```

### Split results of paired MSA in inter and intra chain covariation

### Sequence clustering using Hobohm-1 algorithm

## How to install

    > pip install dist/xi_covutils-x.y.z

## Dependencies

- biopython 1.72
- enum34
- requests

## Development dependencies

In development_requirements.txt

## Running tests

    > pytest tests
    
## Documentation

Automatic documentation from code is in the 'docs' folder.

## Examples

## Contributing

For a new feature / bug fix:

1. Report an issue.
1. Create a new i/issue_number branch
1. After resolve issue, check this before pushing a new branch.
    1. Run tests / pylint
    1. Update documentation
    1. Update README.md
    1. Update requeriments.txt file
    1. Update setup.py requirements
    1. Update development_requirements.txt
    1. Update MANIFEST.in
    1. DO NOT update version number yet
1. Create a merge request to dev branch
1. Merge the branch or wait to other to merge it

For a new release:

1. Create a merge request from dev to master.
1. Merge the branch or wait to other to merge it
1. Pull master from remote to local repo
1. Update version in setup.py
1. Make a commit
1. Add a new TAG
1. Push commit and tag to remote repo

