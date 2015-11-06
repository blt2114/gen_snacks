import os
import argparse
import threading
import time
import random
import Queue
from pprint import pprint

import poretools

from Bio.Blast import NCBIWWW

#Argparser stuff for command-line usage

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--seq", nargs=1, help="The nucleotide sequence string to search.")
parser.add_argument("-fd", "--filedir", nargs=1, help="Path to FAST files to parse through.")

# TODO: CHANGE THIS AS NECESSARY
DATADUMPPATH = '/home/eodnhoj/code/gen_snacks/datadump/'

def query(seq, fp=None):
    """
    DOES NOT RETURN if fp (filepath) is provided.
    """
    # Quick check because NCBI will do it too.
    for c in seq:
        if c not in "ATCG":
            print("Invalid sequence.")
            exit(-1)

    q = None
    try:
        q = NCBIWWW.qblast('blastn', 'nr', seq,
                format_type = 'XML',
                word_size = 20,
                megablast = True)
    except Exception as e:
        print(e)
    if(fp):
        with open(fp,"w") as f:
            f.write(q.read())
    else:
        return q

def multiquery(seqs, paths):
    """
    Actually does the querying; limit one per three seconds, using multithreads.

    Limits:
    Queries spaced at least 3 seconds apart
    """
   # threads = threading.activeCount()
   # lastRun = time.time()
   # while(threads < 3 and time.time() - lastrun > 3):
   #     threading.thread(target:query(seqs[0]))
   #     lastrun = time.time()
   #     seqs = seqs[1:]

    # We're swapping out the extension from fast5 to txt for permanent
    # search result storage
    paths = [p[:-5] + "xml" for p in paths]
    paths = [DATADUMPPATH + p.split("/")[-1] for p in paths]
    totalset = zip(seqs, paths)
    
    for seq,path in totalset:
        print("Writing to %s." % path)
        try:
            q = query(seq,path)
        except Exception as e:
            print("ERROR: %s\n%s" % (path,e))

def prune(fileset, filepath=DATADUMPPATH):
    """
    NOTE: filepath is the path to our datadump btsync NOT the download/pass/ folder.

    We're pruning all files that already have a .xml extension,
    i.e. it's already been megablast'ed and the query doesn't
    need to be run again.
    """
    done = os.listdir(DATADUMPPATH)
    done = [d[:-4] for d in done] # Base names
    done = filter(lambda x: x != '.', done)
    
    for i in range(len(fileset)):
        for d in done:
            if(d in fileset[i]):
                fileset[i] = 0 # Flagging as done
                break

    fileset = filter(lambda x:x != 0, fileset)
    
    return fileset

def multiseq(filepath):
    """
    Snags all filepaths for files ending in fast5 and extracts FASTA sequence.
    """

    # Getting raw paths
    fileset = []
    for f in os.listdir(filepath):
        if f.endswith(".fast5"):
            fileset.append(filepath + f)

    # DEBUG - Reducing size
    fileset = prune(fileset,filepath)
    fileset = fileset[:4]
    fastset = []
    
    # We're doing this because we don't know if Fast5FileSet does things in order
    for fp in fileset:
        tmp = [fp]
        tmp = poretools.Fast5FileSet(tmp)
        for elem in tmp:
            seq = elem.get_fastas("2D")[0].seq
            fastset.append(seq)

    # DEBUG: This assert makes sure things line up
    assert(len(fastset) == len(fileset))

    # Passing it off to the query function
    multiquery(fastset, fileset)

if __name__ == "__main__":
    args = parser.parse_args()
    if(args.filedir):
        multiseq(args.filedir[0])
    elif(args.seq):
        query(args.seq[0])

