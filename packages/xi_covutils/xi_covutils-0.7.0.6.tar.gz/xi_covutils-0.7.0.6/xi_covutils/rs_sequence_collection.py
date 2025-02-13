"""
Import all the sequence_collection related classes from the Rust implementation.
"""
# pylint: disable=no-name-in-module
from xi_covutils.rs_covutils import sequence_collection_rs
BioAlphabet = sequence_collection_rs.BioAlphabet
BioSeq = sequence_collection_rs.BioSeq
