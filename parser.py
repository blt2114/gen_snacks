# AUTHOR: Diego Paris drp2121@columbia.edu Git: Thanatos996

import poretools
import sys
import os

# Run this in a director with Fast5 files and it will print:
# The sequences of each file, each sequences followed by a tab character, the time it took for that squence, and then a newline

# Get names of all fast5 files in current working directory
fast5names = []
for file in os.listdir(os.getcwd()):
    if file.endswith(".fast5"):
        fast5names.append(file)

# Iterate through fast5 files
for fast5 in poretools.Fast5FileSet(fast5names):

	# Get duration via timestamps
	read_start_time = fast5.get_start_time()
	read_end_time = fast5.get_end_time()
	duration = read_end_time - read_start_time

	# Extract fastas in order to access sequence
	# Note, this is an array, 
	# but since "2D" was selected, only one fasta per fast5 file will be output
	fas = fast5.get_fastas("2D")

	# Output the sequence plus duration, tab separated (print statment adds implicit newline)
	for fa in fas:
		if fa is None:
			fast5.close()		
			continue
		else:
			seq = fa.seq
			print seq + '\t' + str(duration)

	fast5.close()