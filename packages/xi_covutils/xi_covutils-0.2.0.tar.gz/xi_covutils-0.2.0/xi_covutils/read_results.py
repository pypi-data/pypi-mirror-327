"""
    Read results from covariation files
"""
from Bio import SeqIO

def from_ccmpred(infile):
    '''
    Reads a the results of the covariation files from CCMPRED.
    Returns a dictionary of tuples of indices (i,j) where i<=j as keys
    and score as value. The indices i,j starts at 1.
    :param infile: A string with the path of the input file.
    '''
    raw = open(infile).readlines()
    scores = {(i+1, j+1):float(v)
              for i, l in enumerate(raw)
              for j, v in enumerate(l.split()) if i <= j}
    return scores

def remap_paired(cov_data, msa_file, chain_a_len, chain_a_id="1", chain_b_id="2"):
    '''
    Remaps the positions of the covariation scores of a paired MSA to each individual
    ungapped chain sequence.
    Return a new dict, which keys has the form ((chain_a, index_a), (chain_b, index_b)) and the
    values are the covariation scores.
    :param cov_data: The result of covariation scores, as a dict of indices as keys and scores as values
    :param msa_file: The path to a fasta file containing the MSA.
    :param chain_a_len: The number of positions of the MSA that corresponds to the first chain.
    :param chain_a_id: An identifier for the first chain.
    :param chain_b_id: An identifier for the second chain.
    '''
    records = SeqIO.parse(msa_file, "fasta")
    first_chain_seq = str(next(records).seq)[:chain_a_len]
    first_chain_ungapped_length = len(first_chain_seq.replace("-", ""))
    def _adapt_index(index):
        if index <= first_chain_ungapped_length:
            return (chain_a_id, index)
        return (chain_b_id, index-first_chain_ungapped_length)
    return {(_adapt_index(i), _adapt_index(j)):v for (i, j), v in cov_data.items()}

def remap_tuple_positions(cov_data, mapping):
    '''
    Remaps the positions of cov_data. Cov_data should be represented as a dict
    with keys of the form ((chain_a, index_a), (chain_b, index_b)) and scores as values.

    :param cov_data: a dict with covariation scores.
    :param mapping: A dict to map the positions, the dict should have chain ids as keys, and
    values should be dicts that maps from old positions to new positions.
    '''
    return {((c1, mapping[c1][p1]), (c2, mapping[c2][p2])):s
            for ((c1, p1), (c2, p2)), s in cov_data.items()
            if p1 in mapping[c1] and p2 in mapping[c2]}

def remove_trivial_tuple(cov_data, min_pos_dif=5):
    """
    Removes positions from covariation data from residue pairs that are
    a lesser distance than five positions in sequence.

    Covariation data is assumed to be a dict with keys of the form
    ((chain_a, index_a), (chain_b, index_b)) and scores as keys.

        :param cov_data: The input covariation data dict.
        :param min_pos_dif=5: Minimum distance that two residues should
        have to be included.
    """
    return {((c1, p1), (c2, p2)):score
            for ((c1, p1), (c2, p2)), score in cov_data.items()
            if not ((c1 == c2) and (abs(p2 - p1) < min_pos_dif))}

def intra_covariation(cov_data):
    """
    Extract intra-chain interactions from paired covariation data.

    Returns a new dict which chain ids are keys and values are subsets
    of cov_data that correspond to intra chain residue pairs.

        :param cov_data: Covariation data from a paired MSA.
    """
    chains = {c for ((c1, _), (c2, _)) in cov_data
              for c in [c1, c2]}
    intra_data = {c:{} for c in chains}
    for ((ch1, po1), (ch2, po2)), score in cov_data.items():
        if ch1 == ch2:
            intra_data[ch1][((ch1, po1), (ch2, po2))] = score
    return intra_data

def merge(cov_data_iter):
    """
    Merge covariation data.

        :param cov_data_iter: Is a iterator where each element is covariation data.
    """
    return {pair:s for cov in cov_data_iter
            for pair, s in cov.items()}

def inter_covariation(cov_data):
    """
    Extract inter-chain interactions from paired covariation data.

    Returns a new dict which chain id tuples are keys and values are subsets
    of cov_data that correspond to inter chain residue pairs.
    Chain ids in tuple keys are sorted lexicographically.

        :param cov_data: Covariation data from a paired MSA.
    """
    chain_pairs = {tuple(sorted([c1, c2])) for ((c1, _), (c2, _)) in cov_data
                   if not c1 == c2}
    inter_data = {c:{} for c in chain_pairs}
    for ((ch1, po1), (ch2, po2)), score in cov_data.items():
        if not ch1 == ch2:
            key_positions = tuple(sorted([(ch1, po1), (ch2, po2)], key=lambda x: x[0]))
            key_chains = tuple(sorted([ch1, ch2]))
            inter_data[key_chains][key_positions] = score
    return inter_data
