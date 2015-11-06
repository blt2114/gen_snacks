from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import numpy
import os
import sys

# Find positions of character, ch, in string, s
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr ==ch]
    
# Finds nucleotide composition and indel counts for file
def filter_file(xml, organism_features):
    gaps = []
    indels = {base: 0 for base in ['A', 'C', 'G', 'T']}
    
    result_handle = open(xml)
    blast_records = NCBIXML.parse(result_handle)
    
    #checks for empty xml files
    try:
        blast_record = next(blast_records)
    except ValueError:
        return indels, gaps

    # Loop through alignments of file
    alignments = blast_record.alignments
    for alignment in alignments:
        description = alignment.hit_def
        description = str(description).split("|")
        names = description[len(description)-1]
        names = names.split(",")[0]
        names = names.split()
        
        # Only check hits corresponding to organism
        contains_features = True
        for feature in organism_features:
            if feature not in names:
                contains_features = False

        if contains_features:
            for hsp in alignment.hsps:
                gaps.append(hsp.gaps)
                query = hsp.query  # query
                target = hsp.sbjct # target
                query_dashes = find(query, "-")
                target_dashes = find(target, "-")
                
                # Appends all bases of query/target at positions of dashes in target/query
                for position in query_dashes:
                    try:
                        indels[target[position]] += 1    
                    except KeyError:
                        pass
                for position in target_dashes:
                    try:
                        indels[query[position]] += 1
                    except KeyError:
                        pass
    return indels, gaps

def indel_analysis(organism_features, xml_root):
    indels = {base: 0 for base in ['A', 'C', 'G', 'T']}
    gaps = []
    
    files = os.listdir( xml_root )
    files = [f for f in files if f[-4:] == '.xml'] # only get .xml files

    # Get insertion-deletion analysis for each file
    for xml in files:
        xml_file = xml_root + '/' + xml
        file_indels, file_gaps = filter_file(xml_file, organism_features)
        for key in indels:
            indels[key] += file_indels[key]
        gaps += file_gaps
    
    #Convert to proportions
    total_bases = float(sum(indels.values()))
    for key in indels:  
        indels[key] /= total_bases
        
    # Get distributions
    gap_average = sum(gaps)/float(len(gaps))
    gap_std = numpy.std(gaps)    
    
    return indels, gap_average, gap_std

def main():
    mussels_identifiers = ['Mus', 'musculus']
    human_identifiers = ['Homo', 'sapiens']
    salmon_identifiers = ['Salmo', 'salar']
    choices = {'salmon': salmon_identifiers, 'human': human_identifiers, 'mussels': mussels_identifiers}

    if len(sys.argv) > 2:
        path = sys.argv[1]
        organism = sys.argv[2]
        identifier = choices[organism]
        print indel_analysis(identifier, path)
        #print indel_analysis(salmon_identifiers, path)
    else:
        print "Improper Use: Add arguement of path to .xml files and choice organism (E.g. 'salmon', 'human', and 'mussels')"
if __name__ == "__main__": main()
