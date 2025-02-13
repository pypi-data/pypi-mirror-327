from Bio import SeqIO
from xi_covutils.pdbmapper import align_sequence_to_sequence 

def map_reference_to_sequence(msa_file, sequence, start=1, end=None):
    '''
    Align the reference sequence of a substring from it to a another given sequence.
    Substring alignment is useful for paired MSA.
    :param msa_file: Path to a fasta file.
    :param start: Index of the starting position of the MSA which will be mapped. Starting at 1.
    :param end: Index of the last position of the MSA which will be mapped. Starting at 1.
    :param sequence: An ungapped protein sequence to be used as destination of mapping.
    '''
    ref = str(SeqIO.parse(msa_file, "fasta").next().seq)
    end = end if end else len(ref)
    ref = ref[start-1: end].replace("-", "")
    return align_sequence_to_sequence(ref, sequence)
