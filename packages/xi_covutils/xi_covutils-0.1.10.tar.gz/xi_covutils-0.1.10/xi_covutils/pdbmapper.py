from os.path import join
import re
from Bio import pairwise2
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Polypeptide import three_to_one
from Bio.PDB.Polypeptide import standard_aa_names

def build_pdb_sequence(pdb_file, chain):
    '''
    Creates a dictionary that maps the position of a pdb chain to the one-letter-code residue.
    Water molecules and residues marked as HETERO are not included.
    :param pdb_file: A string path to a pdb file.
    :param chain: A one-letter string chain code. 
    '''

    model = PDBParser().get_structure('', pdb_file)[0]
    current_chain = [c for c in model.get_chains() if c.id == chain]
    residues = {r.id[1]:(three_to_one(r.resname) if r.resname in standard_aa_names else "X") 
                for c in current_chain for r in c.get_residues() 
                if r.id[0] == " " and not r.resname == 'HOH'}
    return residues

def align_pdb_to_sequence(pdb_file, chain, sequence):
    '''
    Align a pdb chain to a protein sequence and generates a map from pdb position 
    to sequence position.
    :param pdb_file: pdb_file: A string path to a pdb file.
    :param sequence: A string representing a ungapped protein sequence.
    '''
    residues = build_pdb_sequence(pdb_file, chain)
    if residues:
        aligned_residues = align_dict_to_sequence(residues, sequence)
        return {r:aligned_residues[i+1] 
                for i, r in enumerate(sorted(residues.keys())) 
                if i+1 in aligned_residues}
        
        
def build_seq_from_dict(dic):
    '''
    Creates a sequence from a dict. 
    :param dic: The dict should have integers as keys, and strings as values.
    '''
    return "".join([dic[n] for n in sorted(dic.keys())])

def align_dict_to_sequence(dic, sequence):
    '''
    Makes an alignment from a dict and another ungapped sequence.
    :param dic: The dict should have integers as keys, and strings as values
    :param sequence: A string representing a ungapped protein sequence.
    '''
    seq_in_dict = build_seq_from_dict(dic)
    return align_sequence_to_sequence(seq_in_dict, sequence)

def align_sequence_to_sequence(seq_1, seq_2):
    '''
    Makes an alignment from two sequences.
    Returns a dict that maps positions from sequence 1 to sequence 2
    :param seq_1: A string representing a ungapped protein sequence.
    :param seq_2: A string representing a ungapped protein sequence.
    '''
    alignment = pairwise2.align.globalxs(seq_1, seq_2 ,-0.5, -0.1)
    dict_aln, seq_aln, _, _ , _ = alignment[0]
    return map_align(dict_aln, seq_aln)
    
def map_align(seq1, seq2):
    '''
    Align two sequences, and generates a dictionaty that maps aligned indices from the 
    first sequences onto the second sequence. 
    :param seq1: A string representing a potentially gapped protein sequence.
    :param seq2: A string representing a potentially gapped protein sequence.
    '''
    d1 = map_to_ungapped(seq1)
    d2 = map_to_ungapped(seq2)
    return align_dict_values(d1, d2)
    
def align_dict_values(d1, d2):
    '''
    Creates a new dictionary from two input dictionaries, values of first input dict are keys, 
    while values of second input dict are values. Values from two input dicts are aligned if they 
    correspond to the same key. INput keys are assumed to have unique values. 
    :param d1:
    :param d2:
    '''
    return {d1[k]:d2[k] for k in d1 if k in d2}
    
def map_to_ungapped(seq):
    '''
    Creates a dictionary from a gapped sequence. This dictionary maps the position (starting in 1)
    from the gapped position to the ungapped position 
    :param seq:
    '''
    return {i+1:j+1 for j, i in enumerate([i for i, c in enumerate(seq) if not c == "-"])}

