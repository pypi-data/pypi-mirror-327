"""
    Functions to work with MSA files
"""
from operator import add
from tempfile import mkdtemp
from os.path import join
from shutil import rmtree
import gzip
from functools import reduce
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import requests
from xi_covutils.pdbmapper import map_to_ungapped
from xi_covutils.pdbmapper import align_sequence_to_sequence

PFAM_URL = 'https://pfam.xfam.org'

def map_reference_to_sequence(msa_file, sequence, start=1, end=None):
    '''Align the reference sequence or a substring from it to a another given sequence.
    Substring alignment is useful for paired MSA.

    Reference sequence is assumed to be the first sequence in the alignment.

        :param msa_file: Path to a fasta file.
        :param start: Index of the starting position of the MSA which will be mapped. Starting at 1.
        :param end: Index of the last position of the MSA which will be mapped. Starting at 1.
        :param sequence: An ungapped protein sequence to be used as destination of mapping.
    '''
    ref = str(next(SeqIO.parse(msa_file, "fasta")).seq)
    end = end if end else len(ref)
    ref = ref[start-1: end].replace("-", "")
    return align_sequence_to_sequence(ref, sequence)

def _count_mismatches(aln_map, seq_src, seq_dst):
    seq_src = seq_src.upper()
    seq_dst = seq_dst.upper()
    matches_iter = (0 if (seq_src[x-1] == seq_dst[y-1]) else 1
                    for x, y in aln_map.items())
    return reduce(add, matches_iter)

def _count_gaps(aln_map, seq_src, seq_dst):
    src = (max(aln_map.keys())-min(aln_map.keys())+1)-len(aln_map)
    dst = (max(aln_map.values())-min(aln_map.values())+1)-len(aln_map)
    dangling_at_start = min(min(aln_map.keys()), min(aln_map.values()))-1
    dangling_at_end = min(len(seq_src)-max(aln_map.keys()), len(seq_dst)-max(aln_map.values()))
    return dst+src+dangling_at_start*2+dangling_at_end*2

def map_sequence_to_reference(
        msa_file, sequence, msa_format='fasta',
        mismatch_tolerance=float("inf"), gap_tolerance=float("inf")):
    """
    Creates a mapping from a custom ungapped sequence and the reference (first) sequence of and MSA.

    Returns a dict from positions of the custom sequence to the positions of the reference sequence.
    The values of the dict are dicts that contains the position number of the target sequence,
    the character of the custom source sequence and the character of the target sequences, under the
    keys: 'position', 'source' and 'target' respectively.

        :param msa_file: Path to a fasta file.
        :param sequence: An ungapped protein sequence to used as the source to the mapping.
    """
    handle = open(msa_file)
    reference = next(SeqIO.parse(handle, format=msa_format)).seq
    handle.close()
    ungapped_ref = "".join([s for s in reference if not s == '-'])
    aligned = align_sequence_to_sequence(sequence, ungapped_ref)
    if (_count_mismatches(aligned, sequence, ungapped_ref) <= mismatch_tolerance and
            _count_gaps(aligned, sequence, ungapped_ref) <= gap_tolerance):
        ungapped_map = {v: k for k, v in map_to_ungapped(reference).items()}
        positions = {a: ungapped_map[aligned[a]] for a in aligned}
        sources = {a: sequence[a-1] for a in aligned}
        targets = {a: reference[positions[a]-1].upper() for a in aligned}
        return {a:{
            'position': positions[a],
            'source': sources[a],
            'target': targets[a],
        } for a in aligned}
    return {}


def _gapstrip_template(sequences, use_reference):
    if use_reference:
        template = [char == "-" for char in sequences[0]]
    else:
        templates = [[char == "-" for char in seq] for seq in sequences]
        template = [True for _ in range(len(templates[0]))]
        for temp in templates:
            template = [x and y for x, y in zip(temp, template)]
    return template

def gapstrip_sequences(sequences, use_reference=True):
    """
    Strips the gaps of list of sequences.

    All sequences are assumed to have the same length

    Returns a list of stripped sequences in the same order as the input sequences.

        :param use_reference=True: if True the first sequence is used as reference and
            any position containing a gap in it is removed from all sequences.
            If False, only columns that contains gaps en every sequence are removed.
    """
    template = _gapstrip_template(sequences, use_reference)
    return ["".join([c for t, c in zip(template, seq) if not t]) for seq in sequences]

def read_msa(msa_file, msa_format='fasta', as_dict=False):
    """
    Reads a complete msa_file.

    Return a list of tuples with with id and sequences or a dict from id to
    sequences.

        :param msa_file: the path of the input msa file.
        :param msa_format: the format of the msa file. Can be any of the
            supported by biopython.
        :param as_dict=False: is True returns a dict from id to sequence.
    """
    with open(msa_file) as handle:
        records = [(r.id, str(r.seq)) for r in SeqIO.parse(handle, msa_format)]
    if as_dict:
        return {seq_id: sequence for seq_id, sequence in records}
    return records

def write_msa(msa_data, msa_file):
    """
    Writes a msa to file.

    Only support fasta format at the moment.
    Input data can be:
    - a list of tuples of sequence id and sequence.
    - a dict from sequence id to sequence.

        :param msa_data: input sequence data.
        :param msa_file: path of the output file.
    """
    if isinstance(msa_data, list):
        seq_iterable = msa_data
    elif isinstance(msa_data, dict):
        seq_iterable = msa_data.items()
    else:
        raise ValueError("msa_data should be a list or dict")
    with open(msa_file, 'w') as handle:
        for seq_id, seq in seq_iterable:
            handle.write(">{}\n{}\n".format(seq_id, seq))

def pop_reference(msa_data, reference_id):
    """
    Puts a reference sequence as the first sequence of a msa.

    Returns a list of tuples of sequence id and sequences.

        :param msa_data: input msa_data
        :param reference_id: sequece if of the reference
    """
    if isinstance(msa_data, list):
        pass
    elif isinstance(msa_data, dict):
        msa_data = [(seq_id, seq) for seq_id, seq in msa_data.items()]
    else:
        raise ValueError("msa_data should be a list or dict")

    results = [(seq_id, seq) for seq_id, seq in msa_data
               if not seq_id == reference_id]
    first = [(seq_id, seq) for seq_id, seq in msa_data
             if seq_id == reference_id]
    if first:
        return first + results
    raise ValueError("Sequence: {} not in msa data".format(reference_id))

def gapstrip(msa_file, use_reference=True, msa_format='fasta'):
    """
    Strips the gaps of an MSA.

    Returns a list of SeqRecord objects from biopython.

        :param msa_file: the input msa file.
        :param use_reference=True: if True the first sequence is used as reference and
            any position containing a gap in it is removed from all sequences.
            If False, only columns that contains gaps en every sequence are removed.
        :param msa_format="fasta": any format recognized by Bio.SeqIO
    """
    with open(msa_file) as handle:
        records = [(r.id, str(r.seq)) for r in SeqIO.parse(handle, msa_format)]
    gs_result = gapstrip_sequences([s for _, s in records], use_reference)
    seq_ids = (i for i, _ in records)
    return [SeqRecord(id=i, seq=s) for i, s in zip(seq_ids, gs_result)]

def _download_pfam(pfam_acc, msa_type, tmp_dir):
    full_url = "{}/family/{}/alignment/{}/gzipped".format(PFAM_URL, pfam_acc, msa_type)
    request = requests.get(full_url, stream=True)
    gz_temp = join(tmp_dir, 'tmp.gz')
    with open(gz_temp, 'wb') as tmp_fh:
        for chunk in request.iter_content(chunk_size=1024):
            tmp_fh.write(chunk)
    request.close()
    return gz_temp

def _extract_pfam(compressed_file, outfile):
    try:
        with gzip.open(compressed_file, 'rb') as gz_fh:
            with open(outfile, 'wb') as file_handle:
                while True:
                    chunk = gz_fh.read(1024)
                    if not chunk:
                        break
                    file_handle.write(chunk)
        return True
    except EOFError:
        return False

def from_pfam(pfam_acc, outfile, msa_type='full'):
    """
    Download an MSA from pfam database.

    Retrieves the requiered MSA for the accession given into a file.
    Returns True if the download was successful or False otherwise.

        :param pfam_acc:
        :outfile: the path to the output file
        :param msa_type='full': One of 'seed', 'full', 'rp15', 'rp35', 'rp55', 'rp75', 'uniprot', 'ncbi' or 'meta'.
    """
    tmp_dir = mkdtemp()
    gz_temp = _download_pfam(pfam_acc, msa_type, tmp_dir)
    status = _extract_pfam(gz_temp, outfile)
    rmtree(tmp_dir)
    return status
