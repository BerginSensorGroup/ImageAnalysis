import json
import math
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import os

def get_dict_from_json(path):
	try:
		json_file = open(path)
	except:
		raise ValueError("Cannot open " + path)
	
	json_str = json_file.read()
	json_data = json.loads(json_str)
	return json_data

def findSentiments(faces, EPSILON, joyCount, sorrowCount, angerCount, surpriseCount, landmarkConfidence, detectionConfidence, accepted_faces_count=0):
	'''
	This function compiles together the sentiments and confidences for a picture.
	It assumes the <type>Count will be arrays of size 5 and the <type>Confidence will
	be arrays of size 10
	'''
	for face in faces:
		if faces[face]["detection_confidence"]*faces[face]["landmarking_confidence"] < EPSILON:
			continue
		accepted_faces_count += 1
		joyCount[faces[face]["joy_likelihood"]] += 1
		sorrowCount[faces[face]["sorrow_likelihood"]] += 1
		angerCount[faces[face]["anger_likelihood"]] += 1
		surpriseCount[faces[face]["surprise_likelihood"]] += 1
		l_confidence_bucket = math.floor(faces[face]["landmarking_confidence"]*10)
		if l_confidence_bucket >= 10:
			l_confidence_bucket = 9
		landmarkConfidence[l_confidence_bucket] += 1
		d_confidence_bucket = math.floor(faces[face]["detection_confidence"]*10)
		if d_confidence_bucket >= 10:
			d_confidence_bucket = 9
		detectionConfidence[d_confidence_bucket] += 1
		
	return accepted_faces_count

def displaySentiment(emotion, likelihood_name, face_tally):
	bars = np.arange(len(likelihood_name))
	plt.bar(bars, height = face_tally)
	plt.xticks(bars, likelihood_name)
	plt.suptitle(emotion + " Distribution")
	plt.xlabel("Likelihood")
	plt.ylabel("# Accepted Faces with Likelihood")
	plt.show()

	
def saveSentiment(emotion, likelihood_name, face_tally, folder = ""):
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
	bars = np.arange(len(percent_name))
	plt.bar(bars, height = face_tally)
	plt.xticks(bars, percent_name)
	plt.suptitle(confidence_type + " Confidence Distribution")
	plt.xlabel("% Confidence")
	plt.ylabel("# Accepted Faces with Confidence Range")
	plt.show()

	
def saveConfidence(confidence_type, percent_name, face_tally, folder = ""):
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

def confirm(base_path, folder, start, end):
	decision = input("The json files will be drawn from pictures " + str(start) + " to " 
		+ str(end) + " in the path: " + base_path + "\nThe histograms will be saved to the folder: " 
		+ folder + "\nEnter Y to continue or N to abort: ")
	if decision != "Y":
		print("Aborting")
		quit()
	print("Confirmed")

def crawl(base_str, start, end, EPSILON, joyCount, sorrowCount, angerCount, surpriseCount, landmarkConfidence, detectionConfidence, accepted_faces_count=0):
	'''
	Assumptions:
	Base string should be of the form 'SOMETEXT{{}}SOMETEXT.json'
	the curly braces ({{}}) will be replaced with a number to form the json path
	the json should not contain any other curly braces
	example use: 
	crawling hello/world3.json, hello/world4.json, hello/world5.json
		base_str = hello/world{{}}.json
		start = 3
		end = 5
	'''
	replace_index = base_str.find("{{}}")
	new_base_str = base_str.replace("{{}}","")
	print(new_base_str)
	
	picture_number = start
	while picture_number <= end:
		this_path = new_base_str[:replace_index] + str(picture_number) + new_base_str[replace_index:]
		faces = get_dict_from_json(this_path)
		accepted_faces_count = findSentiments(faces, EPSILON, joyCount, sorrowCount, angerCount, surpriseCount, landmarkConfidence, detectionConfidence, accepted_faces_count)
		picture_number += 1
		
	return accepted_faces_count
	
if __name__ == "__main__":
	#path = "angleMETA/G0011576_META.json"
	#path = "framesMETA/frame102_META.json"

	#to be indexed with likelihoods 0-5
	likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
	confidence_name = ('0-9.999', '10-19.999','20-29.999','30-39.999','40-49.999',
						'50-59.999','60-69.999','70-79.999','80-89.999','90-99.999')
	
	#Our error tolerance. Faces with detection_confidence*landmarking_confidence > EPSILON
	#are accepted
	EPSILON = 0

	base_path = "nonFacesMETA/not_a_face{{}}_META.json"
	#base_path = "framesMETA/frame{{}}_META.json"
	#base_path = "angleMETA/G0011{{}}_META.json"
	folder = "nonFacesHISTOGRAMS"

	start = 1
	end = 3
	
	confirm(base_path, folder, start, end)
	
	joyCount = [0,0,0,0,0,0]
	sorrowCount = [0,0,0,0,0,0]
	angerCount = [0,0,0,0,0,0]
	surpriseCount = [0,0,0,0,0,0]
	landmarkConfidence = [0,0,0,0,0,0,0,0,0,0]
	detectionConfidence = [0,0,0,0,0,0,0,0,0,0]
	
	accepted_faces_count = crawl(base_path, start, end, EPSILON, joyCount, sorrowCount, angerCount, surpriseCount, landmarkConfidence, detectionConfidence)
	
	saveSentiment('Joy', likelihood_name, joyCount, folder)
	saveSentiment('Sorrow', likelihood_name, sorrowCount, folder)
	saveSentiment('Anger', likelihood_name, angerCount, folder)
	saveSentiment('Surprise', likelihood_name, surpriseCount, folder)
	#TODO: find average confidence coefficient and variance, plot them as a range
	saveConfidence('Landmarking', confidence_name, landmarkConfidence, folder)
	saveConfidence('Detection', confidence_name, detectionConfidence, folder)
	'''
	displaySentiment('Joy', likelihood_name, joyCount)
	displaySentiment('Sorrow', likelihood_name, sorrowCount)
	displaySentiment('Anger', likelihood_name, angerCount)
	displaySentiment('Surprise', likelihood_name, surpriseCount)
	displayConfidence('Landmarking', confidence_name, landmarkConfidence)
	displayConfidence('Detection', confidence_name, detectionConfidence)
	'''
	
