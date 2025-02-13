# Change Log

All notable changes to this project will be documented in this file.

## 0.7.0.6 2025-02-12

- Added precomputed_boxplot_data function.
- Generate fastq files with reverse complement sequences.
- Added BioSeq and BioAlphabet as rust module.
- Added some utilities to the taxonomy module.
- Added some utilities for plotting with matplotlib.
- Fix typing_extensions requeriment.
- Moved from setup.py to pyproject.toml.
- Added support for rust modules.
- Added a PrimerMatchCounter class.

## 0.6.3.5 2024-04-08

- Added a PrimerGuesser class.
- Fixed a bug in FastqWriter class.
- Added a writer for Fastq files.
- Corrected a bug where blast results with spaces and in query ids or
  subject ids couldn't be parsed.
- Read and parse Fastq files
- Refactored Sequence Collection

## 0.6.2.15 2023-09-28

- Added functions to generate patterns and consensus sequences from MSA data.
- Added functions to build DNA, RNA and protein PSSM from MSA data.
- Added pad, cut and extract_subsequences function from msa data.
- Added Rules to match sequences with regex and IUPAC codes.
- Added Boolean operators for fasta sequence filters
- Added Fasta sequence filtering
- Added a exclude method to BlastResult
- BlastResults can be converted to pandas DataFrame.
- Added blast wrappers for command line blast.
- Fixed a bug in create_taxid_to_names_mapping function.
- Added a new create_names_to_taxid_mapping function.
- Added TaxonomyTree class to work with NCBI taxonomy.
- Added configuration file to run tests inside VIM editor.
- Refactored msa submodule.
- Added a SequenceMapper class.
- Added a function to generate CIGAR strings.
- Added Support for Blast API.
- Updated .pylintrc file.
- Fixed some typos in documentation.

## 0.6.1 2023-03-27

- Updated documentation
- Fixed a bug in the bump version script.

## 0.6.0 2023-03-02

- Updated documentation.
- Silenced internal deprecation warnings.
- Adapted code to the depreaction of Biopython three_to_one function.
- Minimum Python Version supported is 3.8.16
- Added Calculate distance between regions.

## 0.5.3.12 2023-02-24

- Create a PDBSeqMapper to manage alignments between a PDB and a sequence.
- Align and partially align two PDB structures.
- Replace use of biopython pairwise2.align method
  by PairwiseAligner class.
- Added icon to documentation side bar
- Enhanced documentation
- Fix MSA compare output
- Ignore BiopythonDeprecationWarning
- Removed development branch
- Change release mode.

## 0.5.2 2023-01-17

- Added plot conservations
- Added funtions to homogeneize MSA inputs.
- Added a function to compare two MSA.

## 0.5.1 2022-11-07

- pdb module, changed to pdbank module.
- MKDSSP module update to new output format.
- New documentation library
- pdoc3 replaces pdoc as documentation geneartion library
- Calculate conservation
- Added a new conservation module
- Added an entropy function to calculate conservation
- Gap content by column
- Added gap_content_by_column function in msa module
- Added Logo
- Added Logo.png and Logo.svg
- Updated requeriments.txt and development_requeriments.txt
- Created gap_content function in msa module.
- Added a static method in Distances to create a new
    instances from a contact map.
- Added a method in Distances to retrieve raw distances.

## 0.4.2 2020-02-20 Read contact maps

- Created a function in distances module to read plane
    text contact map files.
- Created a function in distances module to read contact
    map files from scpe files.

## 0.4.1 2019-12-04 Added CI pipeline

- Add .gitlab-ci.yml files.
- Created rule to run tests on every non-master commit.
- Created rute to create source distributable
    for tags and master.

## 0.4.0 2019-12-04 First Version with change log, license and contributing guide

- Add CHANGELOG.md file.  - Add CONTRIBUTING.md file.
- Add LICENSE file.
