import os

from classifier import getSpeciesFromXMLs
from confusionMat import getConfusionMatrix

# Python's open() assumes current working directory, so relative path is okay for this call.
# Otherwise, absolute path is needed.
xmls = []
for file in os.listdir(os.getcwd()):
	if file.endswith(".xml"):
		xmls.append(file)

speciesDict = getSpeciesFromXMLs(xmls,1)

confusionMat = getConfusionMatrix("Salmo salar", xmls, speciesDict)

# Prints out answer to question 3
for key in confusionMat:
	print key + " : " + str(confusionMat[key])