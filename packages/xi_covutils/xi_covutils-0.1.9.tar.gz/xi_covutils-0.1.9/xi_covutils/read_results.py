from Bio import SeqIO

def from_ccmpred(infile):
    '''
    Reads a the results of the covariation files from CCMPRED.
    Returns a dictionary of tuples of indices (i,j) where i<=j as keys 
    and score as value. The indices i,j starts at 1.
    :param infile: A string with the path of the input file.
    '''
    results = {}
    raw = open(infile).readlines()
    scores = {(i+1,j+1):float(v)
              for i,l in enumerate(raw)
              for j,v in enumerate(l.split()) if i<=j}
    return scores


def remap_paired(cov_data, msa_file, chain_a_len, chain_a_id="1", chain_b_id="2" ):
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
    first_chain_seq = str(records.next().seq)[:chain_a_len]
    first_chain_ungapped_length = len(first_chain_seq.replace("-","")) 
    def adapt_index(index):
        if index <= first_chain_ungapped_length:
            return (chain_a_id, index)
        else:
            return (chain_b_id, index-first_chain_ungapped_length)
    return {(adapt_index(i), adapt_index(j)):v for (i,j),v in cov_data.items()}