import argparse
from Bio.Blast import NCBIWWW

#Argparser stuff for command-line usage

parser = argparse.ArgumentParser()
parser.add_argument("SEQ", help="The nucleotide sequence string to search.")

TEST_SEQ = 'TCGAAGCTATCTGTCTTCGTGTAACGTCGTAACGGCGACCCGACAAGGCTCATATCCTCGATGTGCCTCTTATAACAACCATACTTATCCGTCGGTCAGAAATCCGCGCAACCATGATGCCTTCAAGCTCTCTGCCTCATAGAATGCGGCACTCTGTTTGGTTTCGTGAAACATCTGTAAACCTTACATCGTCGCCCAAGAGGCGGCAGCGTAGTATAGCCATGCGTCGAAAGATTCAGCCATGCTCTTCCA'

def main(seq=TEST_SEQ):
    """
    Temporary main. Rename as needed.

    Disable the NCBIWWW.qblast for now to save queries.

    """
    #result_handle = NCBIWWW.qblast("blastn", "nr", seq, megablast = True)
    #print(result_handle)

if __name__ == "__main__":
    args = parser.parse_args()
    if(len(args.SEQ) == 0):
        main()
    else:
        main(args.SEQ)

