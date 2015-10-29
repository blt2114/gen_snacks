# -*- coding: utf-8 -*-
"""
Usage: (python) group5_report1_question10.py <.fastq files>

Finds the nucleotide composition in a group of FASTQ files. 

Example:
        $ python group5_report1_question10.py fastq/2D-fail.fastq fastq/2D-pass.fastq
"""

import sys
import itertools
from collections import Counter

def nucleotide_composition(fastq_files):
    """Prints nucleotide composition for all FASTQ files combined"""
    nuc_count = Counter()
    total_nucs = 0
    for fastq_file in fastq_files:
        #print fastq_file
        with open(fastq_file, 'rb') as f:
            # skip first line
            for _ in itertools.islice(f, 0, 1):
                pass
            # Get every 4th line
            fourthlines = itertools.islice(f, 0, None, 4)
            for DNA_line in fourthlines:
                for n in DNA_line.strip():
                    nuc_count[n] += 1
                    total_nucs += 1

    for n in nuc_count:
		print '\t'.join(str(s) for s in [n, nuc_count[n], 
			total_nucs, float(nuc_count[n]) / float(total_nucs)])
   
if __name__ == '__main__':
    if len(sys.argv) != 1:
        fastq_files = sys.argv[1:]

        nucleotide_composition(fastq_files)
    else:
        print 'To run: python group5_report1_question10.py <<.fastq files>>'
        print 'Example: \
            python group5_report1_question10.py \
            fastq/2D-fail.fastq fastq/2D-pass.fastq'