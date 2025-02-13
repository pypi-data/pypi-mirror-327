"""
    Clustering functions
"""
from xi_covutils import aux
from xi_covutils.msa import gapstrip_sequences
class Cluster(): # pylint: disable=too-few-public-methods
    """
    Simple class to represent clusters
        :param object:
    """
    def __init__(self):
        self.representative = None
        self.sequences = []
        self.nseq = 0
    def __repr__(self):
        return "Cluster:[{}][{}] {}".format(
            self.nseq,
            self.representative,
            ", ".join(self.sequences))

def hobohm1(sequences, identity_cutoff=0.62, use_gapstrip=False, use_c_extension=True):
    """
    Performs a sequence clustering using Hobohm algorithm 1.

    Implementation of clusternig algorithm 1 published in:
    Hobohm U, Scharf M, Schneider R, Sander C. Selection of representative protein data sets.
    Protein Sci. 1992;1(3):409-17.
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2142204/pdf/1304348.pdf

    Return a list of selected clusters.

        :param sequences: a list of string.
        :param identity_cutoff: a float between 0 and 1, used a cutoff for
            including a new sequence in a cluster.
        :param use_gapstrip: if True, columns of all sequences that are
            gaps in every sequence are removed. This not affect the results
            and may improve the performance.
        :param use_c_extension: If true, C language extension is used to
            compute sequence identity. If False, pure python implementation
            is used.
    """
    select = []
    sequences = gapstrip_sequences(sequences) if use_gapstrip else sequences
    #pylint: disable=c-extension-no-member
    id_function = aux.identity_fraction if use_c_extension else sequence_identity
    for seq in sequences:
        should_add_new_cluster = True
        add_to_cluster = None
        for clu in select:
            representative = clu.representative
            identity = id_function(seq, representative)
            if identity >= identity_cutoff:
                should_add_new_cluster = False
                add_to_cluster = clu
                break
        if should_add_new_cluster:
            cluster = Cluster()
            cluster.representative = seq
            cluster.sequences.append(seq)
            cluster.nseq = 1
            select.append(cluster)
        if add_to_cluster:
            add_to_cluster.sequences.append(seq)
            add_to_cluster.nseq += 1
    return select

def sequence_identity(seq1, seq2):
    """
    Computes sequence identity for two sequences.

    Lower and upper case characters are assumed to be different.
    Gapped positions in both sequences are not considered for the calculation.

    Return a float value between 0.0 (dissimilar sequences) and 1.0(identical sequences).
    Throws ValueError if the len of the sequences is not the same.

        :param seq1: a str
        :param seq2: a str
    """
    if not len(seq1) == len(seq2):
        raise ValueError("Sequence length is not equal")
    equals = 0
    total = 0
    for i, char_a in enumerate(seq1):
        char_b = seq2[i]
        if not (char_a in ("-", ".") and (char_b in ("-", "."))):
            total += 1
            if char_a == char_b:
                equals += 1
    return float(equals) / max(1, total)
