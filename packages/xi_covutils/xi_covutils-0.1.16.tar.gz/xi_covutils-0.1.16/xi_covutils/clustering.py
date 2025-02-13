from functools import reduce
from pprint import pprint

class cluster(object):
    def __init__(self):
        self.representative=None
        self.sequences=[]
        self.nseq=0
    def __repr__(self):
        return "Cluster:[{}][{}] {}".format(self.nseq,self.representative, ", ".join(self.sequences))

def hobohm1(sequences, identity_cutoff=0.62):
    """
    Performs a sequence clustering using Hobohm algorithm 1.

    Adaptation of cluster algorithm 1 published on:
    Hobohm U, Scharf M, Schneider R, Sander C. Selection of representative protein data sets. 
    Protein Sci. 1992;1(3):409-17. 
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2142204/pdf/1304348.pdf
    """
    select = []
    for seq in sequences:
        should_add_new_cluster=True
        add_to_cluster=None
        for cl in select:
            representative = cl.representative
            identity = sequence_identity(seq, representative)
            if identity>=identity_cutoff:
                should_add_new_cluster=False
                add_to_cluster=cl
                break
        if should_add_new_cluster:
            c = cluster()
            c.representative=seq
            c.sequences.append(seq)
            c.nseq=1
            select.append(c)
        if add_to_cluster:
            add_to_cluster.sequences.append(seq)
            add_to_cluster.nseq+=1
    return select

def _are_identical(a, b):
    if ((a=="-" or a==".") and (b=="-" or b==".")):
        return None
    if a==b:
        return 1
    return 0

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
    identicals = [_are_identical(y1, y2) for y1, y2 in zip(seq1, seq2)]
    equals = reduce(lambda x, y: x+(y if y else 0), identicals, 0)
    total = max(1, reduce(lambda x, y: x+(1 if not y is None else 0), identicals, 0))
    return float(equals) / total