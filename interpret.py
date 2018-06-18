import json
import math
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import os

#a simple wrapper class to hold statistics about the confidences seen
class ConfidenceData(object):
	def __init__(self, landmarkSTDDEV, landmarkMEAN, detectSTDDEV, detectMEAN):
		self.landmark_STDDEV = landmarkSTDDEV
		self.landmark_MEAN = landmarkMEAN
		self.detect_STDDEV = detectSTDDEV
		self.detect_MEAN = detectMEAN
	#useful for exporting to JSON
	def getDict(self):
		return {"landmark_STDDEV": self.landmark_STDDEV, "landmark_MEAN": self.landmark_MEAN, 
			"detect_STDDEV": self.detect_STDDEV, "detect_MEAN": self.detect_MEAN}

#takes a path to a json file and returns a dictionary of the data therein contained
def get_dict_from_json(path):
	try:
		json_file = open(path)
	except:
		raise ValueError("Cannot open " + path)
	
	json_str = json_file.read()
	json_data = json.loads(json_str)
	return json_data

def findSentiments(faces, EPSILON, joyCount, sorrowCount, angerCount, surpriseCount, landmarkConfidenceCount, detectionConfidenceCount, accepted_faces_count=0):
	'''
	This function compiles together the sentiments and confidences for a picture.
	It assumes the <type>Count will be arrays of size 5 and the <type>Confidence will
	be arrays of size 10
	
	faces is a dictionary containing each face to be analyzed
	each face is a dictionary containing emotional likleness and confidence
	accepted faces count keeps track of how many faces have landmarking_confidence*detection_confidence >= EPSILON
	'''
	for face in faces:
		if faces[face]["detection_confidence"]*faces[face]["landmarking_confidence"] < EPSILON:
			continue
		accepted_faces_count += 1
		joyCount[faces[face]["joy_likelihood"]] += 1
		sorrowCount[faces[face]["sorrow_likelihood"]] += 1
		angerCount[faces[face]["anger_likelihood"]] += 1
		surpriseCount[faces[face]["surprise_likelihood"]] += 1
		#we need to adjust the confidences so they can be indexed 0 to 9
		l_confidence_bucket = math.floor(faces[face]["landmarking_confidence"]*10)
		if l_confidence_bucket >= 10:
			l_confidence_bucket = 9
		landmarkConfidenceCount[l_confidence_bucket] += 1
		d_confidence_bucket = math.floor(faces[face]["detection_confidence"]*10)
		if d_confidence_bucket >= 10:
			d_confidence_bucket = 9
		detectionConfidenceCount[d_confidence_bucket] += 1
		
	return accepted_faces_count

def compileConfidences(faces, landmark_confidences, detection_confidences):
	'''
	This function appends the confidence values for each face to 
	the respective confidence array parameters
	'''
	for face in faces:
		landmark_confidences.append(faces[face]["landmarking_confidence"])
		detection_confidences.append(faces[face]["detection_confidence"])

def displaySentiment(emotion, likelihood_name, face_tally):
	'''
	emotion: the pertinent emotion
	likelihood_name: the likelihoods shown on the x axis
	face_tally: the number of accepted faces shown on the y axis
	output: a histogram of the number accepted faces for each likelihood
	'''
	bars = np.arange(len(likelihood_name))
	plt.bar(bars, height = face_tally)
	plt.xticks(bars, likelihood_name)
	plt.suptitle(emotion + " Distribution")
	plt.xlabel("Likelihood")
	plt.ylabel("# Accepted Faces with Likelihood")
	plt.show()

	
def saveSentiment(emotion, likelihood_name, face_tally, folder = ""):
	'''
	emotion: the pertinent emotion
	likelihood_name: the likelihoods shown on the x axis
	face_tally: the number of accepted faces shown on the y axis
	folder: the desired folder in which to save the histogram
	output: a .png histogram of the number accepted faces for each likelihood saved
		to the desired folder
	'''
	bars = np.arange(len(likelihood_name))
	plt.bar(bars, height = face_tally)
	plt.xticks(bars, likelihood_name)
	plt.suptitle(emotion + " Distribution")
	plt.xlabel("Likelihood")
	plt.ylabel("# Accepted Faces with Likelihood")
	plt.gcf().subplots_adjust(left = 0.125, right = 0.9)
	plt.gcf().set_size_inches(8.5, plt.gcf().get_size_inches()[1])
	path = emotion+'.png'
	if folder != "":
		path = folder + "/" + path
	os.makedirs(os.path.dirname(path), exist_ok=True)
	plt.savefig(path)
	plt.close()


def displayConfidence(confidence_type, percent_name, face_tally):
	'''
	confidence_type: the pertinent confidence
	percent_name: the percentage ranges shown on the x axis
	face_tally: the number of accepted faces shown on the y axis
	output: a histogram of the number accepted faces for each likelihood
	'''
	bars = np.arange(len(percent_name))
	plt.bar(bars, height = face_tally)
	plt.xticks(bars, percent_name)
	plt.suptitle(confidence_type + " Confidence Distribution")
	plt.xlabel("% Confidence")
	plt.ylabel("# Accepted Faces with Confidence Range")
	plt.show()

	
def saveConfidence(confidence_type, percent_name, face_tally, folder = ""):
	'''
	confidence_type: the pertinent confidence
	percent_name: the percentage ranges shown on the x axis
	face_tally: the number of accepted faces shown on the y axis
	folder: the desired folder in which to save the histogram
	output: a .png histogram of the number accepted faces for each percentage range saved
		to the desired folder
	'''
	bars = np.arange(len(percent_name))
	plt.bar(bars, height = face_tally)
	plt.xticks(bars, percent_name)
	plt.suptitle(confidence_type + " Confidence Distribution")
	plt.xlabel("% Confidence")
	plt.ylabel("# Accepted Faces with Confidence Range")
	plt.gcf().subplots_adjust(left = 0.125, right = 0.9)
	plt.gcf().set_size_inches(14, plt.gcf().get_size_inches()[1])
	path = confidence_type+'.png'
	if folder != "":
		path = folder + "/" + path
	os.makedirs(os.path.dirname(path), exist_ok=True)
	plt.savefig(path)
	plt.close()

def saveConfidenceStats(confidence_stats, folder):
	'''
	confidence_stats: a ConfidenceData object that contains the statistics
	folder: the desired folder in which the JSON should be contained
	output: a JSON file in the desired folder possessing the statistics held in confidence_stats
	'''
	path = "Confidence Stats.json"
	if folder != "":
		path = folder + "/" + path
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'w') as outfile:
		json.dump(confidence_stats.getDict(), outfile)

def confirm(base_path, folder, start, end):
	'''
	base_path: the path from which the json files will be drawn
	folder: the desired folder to save the histograms
	start: the first picture's index
	end: the last picture's index
	decision: user decision to continue the program
	output: program halt or continue execution
	'''
	decision = input("The json files will be drawn from pictures " + str(start) + " to " 
		+ str(end) + " in the path: " + base_path + "\nThe histograms will be saved to the folder: " 
		+ folder + "\nEnter Y to continue or N to abort: ")
	if decision != "Y":
		print("Aborting")
		quit()
	print("Confirmed")

def crawl(base_str, start, end, EPSILON, joyCount, sorrowCount, angerCount, surpriseCount, landmarkConfidenceCount, detectionConfidenceCount, accepted_faces_count=0):
	'''
	This function processes the picture data numbered start to end in the path base_str
	the arrays will be filled with the number of faces that fall into each liklihood range
	for emotions and percentage range for confidences
	
	landmark_confidences and detection_confidences will contain all the confidence values encountered
		for standard deviation and mean analysis using NumPy (O(N) memory overhead)
	
	The number of accepted faces and calculated confidence statistics are returned.
	
	Assumptions:
	Base string should be of the form 'SOMETEXT{{}}SOMETEXT.json'
	the curly braces ({{}}) will be replaced with a number to form the json path
	the json should not contain any other curly braces
	example use: 
	crawling hello/world3.json, hello/world4.json, hello/world5.json
		base_str = hello/world{{}}.json
		start = 3
		end = 5
	
	<type>Count will be arrays of size 5 and the <type>ConfidenceCount will be arrays of size 10
	accepted_faces_count is the number of faces 
	'''
	replace_index = base_str.find("{{}}")
	new_base_str = base_str.replace("{{}}","")
	
	picture_number = start
	
	landmark_confidences = []
	detection_confidences = []
	
	while picture_number <= end:
		this_path = new_base_str[:replace_index] + str(picture_number) + new_base_str[replace_index:]
		faces = get_dict_from_json(this_path)
		accepted_faces_count = findSentiments(faces, EPSILON, joyCount, sorrowCount, angerCount, surpriseCount, landmarkConfidenceCount, detectionConfidenceCount, accepted_faces_count)
		compileConfidences(faces, landmark_confidences, detection_confidences)
		picture_number += 1
	#convert to numpy array to handle statistical analysis
	NP_landmark = np.asarray(landmark_confidences)
	NP_detection = np.asarray(detection_confidences)
	confidence_stats = ConfidenceData(np.std(NP_landmark), np.mean(NP_landmark), np.std(NP_detection), np.mean(NP_detection))
	return accepted_faces_count, confidence_stats
	
if __name__ == "__main__":
	#to be indexed with likelihoods 0-5
	likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
	confidence_name = ('0-9.999', '10-19.999','20-29.999','30-39.999','40-49.999',
						'50-59.999','60-69.999','70-79.999','80-89.999','90-99.999')
	
	#Our error tolerance. Faces with detection_confidence*landmarking_confidence >= EPSILON
	#are accepted
	EPSILON = 0

	#base_path = "nonFacesMETA/not_a_face{{}}_META.json"
	base_path = "framesMETA/frame{{}}_META.json"
	#base_path = "angleMETA/G0011{{}}_META.json"
	folder = "framesBETA_HISTOGRAMS"
	
	start = 102
	end = 350
	
	confirm(base_path, folder, start, end)
	
	joyCount = [0,0,0,0,0,0]
	sorrowCount = [0,0,0,0,0,0]
	angerCount = [0,0,0,0,0,0]
	surpriseCount = [0,0,0,0,0,0]
	landmarkConfidence = [0,0,0,0,0,0,0,0,0,0]
	detectionConfidence = [0,0,0,0,0,0,0,0,0,0]
	
	accepted_faces_count, confidence_stats = crawl(base_path, start, end, EPSILON, joyCount, sorrowCount, angerCount, surpriseCount, landmarkConfidence, detectionConfidence)
	
	saveSentiment('Joy', likelihood_name, joyCount, folder)
	saveSentiment('Sorrow', likelihood_name, sorrowCount, folder)
	saveSentiment('Anger', likelihood_name, angerCount, folder)
	saveSentiment('Surprise', likelihood_name, surpriseCount, folder)
	saveConfidence('Landmarking', confidence_name, landmarkConfidence, folder)
	saveConfidence('Detection', confidence_name, detectionConfidence, folder)
	saveConfidenceStats(confidence_stats, folder)
	'''
	displaySentiment('Joy', likelihood_name, joyCount)
	displaySentiment('Sorrow', likelihood_name, sorrowCount)
	displaySentiment('Anger', likelihood_name, angerCount)
	displaySentiment('Surprise', likelihood_name, surpriseCount)
	displayConfidence('Landmarking', confidence_name, landmarkConfidence)
	displayConfidence('Detection', confidence_name, detectionConfidence)
	'''
	
