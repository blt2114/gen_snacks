import os
import argparse
import threading
import time
import random
import Queue

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

    try:
        return NCBIWWW.qblast('blastn', 'nr', seq,
                format_type = 'Text',
                megablast = True)
    except Exception as e:
        return e

def multiquery(seqs):
    """
    Actually does the querying; limit one per three seconds, using multithreads.

    Limits:
    3 queries at any given point
    Queries spaced at least 3 seconds apart

    """
   # threads = threading.activeCount()
   # lastRun = time.time()
   # while(threads < 3 and time.time() - lastrun > 3):
   #     threading.thread(target:query(seqs[0]))
   #     lastrun = time.time()
   #     seqs = seqs[1:]

    for e in seqs:
        print(query(e).read())
        time.sleep(3)


def multiseq(filepath):
    """
    Snags all filepaths for files ending in fast5 and extracts FASTA sequence.
    """

    # Getting raw paths
    fileset = []
    for f in os.listdir(filepath):
        if f.endswith(".fast5"):
            fileset.append(filepath + "/" + f)

    # DEBUG - Reducing size
    fileset = fileset[:4]

    # Passing off to poretools
    fileset = poretools.Fast5FileSet(fileset)
    toReturn = []

    for f in fileset:
        lst = f.get_fastas("2D")
        fastas = [x.seq for x in lst]
        # TODO: What do we want to do with these sequences?
        toReturn.append(*fastas)

    multiquery(toReturn)

if __name__ == "__main__":
    args = parser.parse_args()
    if(args.filedir):
        multiseq(args.filedir[0])
    elif(args.seq):
        query(args.seq[0])

