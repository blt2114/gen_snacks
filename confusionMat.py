# AUTHOR: Diego Paris drp2121@columbia.edu

import os
from Bio.Blast import NCBIXML as xmlparse

# searchSpecies must be a string, the name of the species being searched for as reported by the classifier
# xmls must be an array of absolute file paths to .xmls
# speciesDict must be the output of the xmls having been run through the classifier with mode 1
# Returns dictionary with confusion matrix titles (strings) as keys
# number of files in each category as values

def getConfusionMatrix(searchSpecies, xmls, speciesDict) :

	# Dictionary for containing top hits from xmls
	topSpecies = {}

	for xmlfile in xmls:

		# Open xmls and parse
		xmlhandle = open(xmlfile)
		blast_recs = xmlparse.parse(xmlhandle)

		# Iterate through blast recs
		for blast_rec in blast_recs:

			# Get top hit (maximum confidence alignment as reported by blast)
			if len(blast_rec.alignments) > 0:
				tophit = blast_rec.alignments[0]

				# Extract species name
				description = tophit.hit_def
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

				# Add values to dictionary
				if name in topSpecies:
					if xmlfile not in topSpecies[name]:
						topSpecies[name].append(xmlfile)
				if name not in topSpecies:
					topSpecies[name] = [xmlfile]

	# Dictionary for each sample's classifier output and top hit from BLAST
	tuplesDict = {}

	# Loading dictionary. Note: files unaligned by 
	for species in speciesDict:
		for sample in speciesDict[species]:
			if species == "Unaligned" : pass
			else : tuplesDict[sample] = [species]

	for species in topSpecies:
		for sample in topSpecies[species]:
			tuplesDict[sample].append(species)


	# Labels for confusion matrix
	TP = "Is " + searchSpecies + " in both BLAST and our classifier"
	TN = "Is not " + searchSpecies + " in both BLAST and our classifier"
	FP = "Is " + searchSpecies + " in BLAST but not our classifier"
	FN = "Is not " + searchSpecies + " in BLAST but is in our classifier"

	# Initializing confusion matrix
	confusionMatrix = dict.fromkeys([TP, TN,FP,FN], 0)

	# Load confusion matrix
	for sample in tuplesDict:
		if tuplesDict[sample][0] == searchSpecies:
			if tuplesDict[sample][1] == searchSpecies:
				confusionMatrix[TP] += 1
			else:
				confusionMatrix[FN] += 1
		else:
			if tuplesDict[sample][1] == searchSpecies:
				confusionMatrix[FP] += 1
			else:
				confusionMatrix[TN] += 1

	return confusionMatrix






