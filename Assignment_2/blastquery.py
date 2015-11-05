import os
import argparse
from pprint import pprint

import poretools

from Bio.Blast import NCBIWWW

#Argparser stuff for command-line usage

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--seq", nargs=1, help="The nucleotide sequence string to search.")
parser.add_argument("-fd", "--filedir", nargs=1, help="Path to FAST files to parse through.")


TEST_SEQ = 'ATATCCTCGATGTGCCTCTTATAACAACCATACTTATCCGTCGGTCAGAAATCCGCGCAACCATGATGCCTTCAAGCTCTCTGCCTCATAGAATGCGGCACTCTGTTTGGTTTCGTGAAACATCTGTAAACCTTACATCGTCGCCCAAGAGGCGGCAGCGTAGTATAGCCATGCGTCGAAAGATTCAGCCATGCTCTTCCA'


def query(seq=TEST_SEQ):
    """
    Our universal query.
    """
    # Quick check because NCBI will do it too.
    for c in seq:
        if c not in "ATCG":
            print("Invalid sequence.")
            exit(-1)

    # DEBUG - remove this
    print("Checking %s." % seq)
    exit()

    try:
        return NCBIWWW.qblast('blastn', 'nr', seq,
                format_type = 'Text',
                megablast = False)
    except Exception as e:
        print(e)

def multiquery(filepath):
    """
    Snags all filepaths for files ending in fast5 and extracts FASTA sequence.
    """

    # Getting raw paths
    fileset = []
    for f in os.listdir(filepath):
        if f.endswith(".fast5"):
            fileset.append(filepath + "/" + f)

    # DEBUG
    fileset = fileset[:10]

    # Passing off to poretools
    fileset = poretools.Fast5FileSet(fileset)

    for f in fileset:
        lst = f.get_fastas("2D")
        fastas = [x.seq for x in lst]
        # TODO: What do we want to do with these sequences?
        print(fastas)

if __name__ == "__main__":
    args = parser.parse_args()
    if(args.filedir):
        multiquery(args.filedir[0])
    elif(args.seq):
        query(args.seq[0])

