# AUTHOR: Diego Paris drp2121@columbia.edu

import os
from Bio.Blast import NCBIXML as xmlparse

# xmls must be an array of absolute file paths to .xmls
# Returns dictionary with Species names (strings) as keys
# .xml files that did not report any alignments are reported under the key "Unaligned"
# the 'mode' argument decides what the keys will be
# if it is 0, the number of files corresponding to that key (int) will be the values
# if it is 1, the list of filenames corresponding to that key (list of strings of absolute filepaths) will be the values

def getSpeciesFromXMLs(xmls, mode) :

	# Dictionary for containing parsed information from xmls
	species = {}

	for xmlfile in xmls:

		# Open xmls and parse
		xmlhandle = open(xmlfile)
		blast_recs = xmlparse.parse(xmlhandle)

		# Iterate through blast recs
		for blast_rec in blast_recs:

			# Get alignments, iterate through them
			aligns = blast_rec.alignments
			for hit in range(0,len(aligns)):
				align = aligns[hit]

				# Extract species name
				description = align.hit_def
				description = str(description).split("|")
				names = description[len(description)-1]
				names = names.split(",")[0]
				names = names.split()

				# Correct for known typos/inconsistencies in dataset
				if ":" in names[0] : names.pop(0)
				if names[0] == "Pig" : name = "Sus scrofa"
				elif names[0] == "Atlantic" : name = "Salmo salar"
				elif names[0] == "Altantic" : name = "Salmo salar"
				elif names[0] == "Zebrafish" : name = "Danio rerio"
				else : name = names[0] + " " + names[1]

				# Collect hsp bitscores
				hsps = align.hsps
				bit_scores = [hsp.bits for hsp in hsps]

				# Add values to dictionary
				if name in species:
					species[name]["bitsum"] += sum(bit_scores)
					if xmlfile not in species[name]["samples"]:
						species[name]["samples"].append(xmlfile)
				if name not in species:
					species[name] = {}
					species[name]["bitsum"] = sum(bit_scores)
					species[name]["samples"] = [xmlfile]

	# Convert dictionary to array for triples for sorting
	speciestrip = [[key, species[key]["samples"], species[key]["bitsum"]] for key in species]
	speciestrip = sorted(speciestrip, key = lambda trip: trip[2], reverse = True)

	# Array of samples that were successfully aligned
	xmlaligned = []

	# Output dictionary, will contain names as keys, number of samples aligned as the values
	outdict = {}

	# Filtering so that samples are not double-counted, selecting the best possible allignment for each sample
	while speciestrip:
		toptrip = speciestrip.pop(0)
		for tripind in range(0,len(speciestrip)):
			trip = speciestrip[tripind]
			trip[1] = [sample for sample in trip[1] if sample not in toptrip[1]]
		speciestrip = [trip for trip in speciestrip if trip[1]]
		xmlaligned.extend(toptrip[1])
		outdict[toptrip[0]] = len(toptrip[1])

	# Adding unaligned xmls
	xmlnotaligned = [xml for xml in xmls if xml not in xmlaligned]
	outdict["Unaligned"] = len(xmlnotaligned)

	return outdict