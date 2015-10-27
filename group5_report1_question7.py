import itertools
import rpy2.robjects as robjects
                
def find_longest_read(all_fastq_files):
   
    sizes = []
    
    for fastq_file in all_fastq_files:
        with open(fastq_file, 'rb') as f:
            # skip first line
            for _ in itertools.islice(f, 0, 1):
                pass
            fourthlines = itertools.islice(f, 0, None, 4)
            for line in fourthlines:
                sizes.append(len(line))
            
            sizes_max = max(sizes)
    
        print "Longest read for", fastq_file, "is", sizes_max

all_fastq_files = ["fastq/template-pass.fastq", "fastq/complement-pass.fastq",\
                    "fastq/2D-pass.fastq"]

find_longest_read(all_fastq_files)