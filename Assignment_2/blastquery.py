import os
import argparse
import threading
import time
import random

from Queue import Queue
from pprint import pprint

import poretools

from Bio.Blast import NCBIWWW

#Argparser stuff for command-line usage

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--seq", nargs=1, help="The nucleotide sequence string to search.")
parser.add_argument("-f", "--file", nargs=1, help="For single FAST5 files.")
parser.add_argument("-fd", "--filedir", nargs=1, help="Path to FAST files to parse through.")

# TODO: CHANGE THIS AS NECESSARY
DATADUMPPATH = '/Users/briantrippe/Documents/Columbia/Ubiquitous Genomics/data_dump/'

def query(seq, fp=None):
    """
    DOES NOT RETURN if fp (filepath) is provided.
    """
    # Quick check because NCBI will do it too.
    for c in seq:
        if c not in "ATCG":
            print("Invalid sequence.")
            exit(-1)
    
    print("Data check complete.")
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
    queue = Queue()
    max_threads = 1
    threadlist = range(max_threads)
    timecheck = time.time()

    # Creating the writepaths
    paths = [p[:-5] + "xml" for p in paths]
    paths = [DATADUMPPATH + p.split("/")[-1] for p in paths]
    totalset = zip(seqs, paths)

    for seq,path in totalset:
        try:
            q = query(seq,path)
        except Exception as e:
            print(e)

    exit()
    def threadFunc(q=queue):
        while(True):
            seq,path = q.get()
            print("Writing to %s." % path)
            try:
                results = query(seq,path)
                print("%s done." % path)
            except Exception as e:
                print("ERROR: %s\n%s" % (path,e))
                time.sleep(random.randint(3,5))
                continue
            q.task_done()

    # Loading up the Queue
    print("Loading up Queue.")
    for e in totalset:
        queue.put(e)
    
    print("Executing threads.")
    for t in range(max_threads):
        time.sleep(3)
        threadlist[t] = threading.Thread(target=threadFunc, args=(queue,))
        threadlist[t].daemon = True
        threadlist[t].start()

    print("Attempting to join threads.")
    queue.join()
    """ 
    for seq,path in totalset:
        print("Writing to %s." % path)
        try:
            q = query(seq,path)
        except Exception as e:
            print("ERROR: %s\n%s" % (path,e))
    """
def getWritePath(filepath, writepath=DATADUMPPATH):
    """
    Take in a .fast5 path and convert it to the writepath.
    """
    assert(filepath[-5:] == 'fast5')
    filepath = filepath[:-5]
    filepath = filepath.split("/")[-1]
    return DATADUMPPATH + filepath

def getSeq(filepath):
    """
    Take in a .fast5 path and get the 2D sequence back.
    """
    t = poretools.Fast5FileSet([filepath])
    for e in t:
        return e.get_fasts("2D")[0].seq

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
#    fileset = fileset[:50]
    fastset = []
    
    print("Getting sequences from FAST5 files.")
    # We're doing this because we don't know if Fast5FileSet does things in order
    for fp in fileset:
        tmp = [fp]
        tmp = poretools.Fast5FileSet(tmp)
        for elem in tmp:
            seq = elem.get_fastas("2D")[0].seq
            fastset.append(seq)

    # DEBUG: This assert makes sure things line up
    assert(len(fastset) == len(fileset))
    
    print("Beginning query process.")
    # Passing it off to the query function
    multiquery(fastset, fileset)

if __name__ == "__main__":
    args = parser.parse_args()
    if(args.file):
        # TODO: UNTESTED.
        arg = args.file[0]
        seq = getSeq(arg)
        writepath = getWritePath(args.file[0])
        query(seq,writepath)
    elif(args.filedir):
        multiseq(args.filedir[0])
    elif(args.seq):
        query(args.seq[0])

