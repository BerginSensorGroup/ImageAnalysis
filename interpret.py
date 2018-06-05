import json
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

def get_dict_from_json(path):
	try:
		json_file = open(path)
	except:
		raise ValueError("Cannot open " + path)
	
	json_str = json_file.read()
	json_data = json.loads(json_str)
	return json_data

def findSentiments(faces, EPSILON):
	joyCount = [0,0,0,0,0,0]
	sorrowCount = [0,0,0,0,0,0]
	angerCount = [0,0,0,0,0,0]
	surpriseCount = [0,0,0,0,0,0]
	accepted_faces_count = 0
	for face in faces:
		if faces[face]["detection_confidence"]*faces[face]["landmarking_confidence"] < EPSILON:
			continue
		accepted_faces_count += 1
		joyCount[faces[face]["joy_likelihood"]] += 1
		sorrowCount[faces[face]["sorrow_likelihood"]] += 1
		angerCount[faces[face]["anger_likelihood"]] += 1
		surpriseCount[faces[face]["surprise_likelihood"]] += 1
	return (accepted_faces_count, joyCount, sorrowCount, angerCount, surpriseCount)

def displaySentiment(emotion, likelihood_name, face_tally):
	bars = np.arange(len(likelihood_name))
	plt.bar(bars, height = face_tally)
	plt.xticks(bars, likelihood_name)
	plt.suptitle(emotion + " Distribution")
	plt.xlabel("Likelihood")
	plt.ylabel("# Accepted Faces with Likelihood")
	plt.show()

def crawl(base_str, start, end, EPSILON):
	'''
	Assumptions:
	Base string should be of the form 'SOMETEXT{{}}SOMETEXT.json'
	the curly braces ({{}}) will be replaced with a number to form the json path
	the json should not contain any other curly braces
	example use: 
	crawling world3.json, world4.json, world5.json
		base_str = world{{}}.json
		start = 3
		end = 5
	'''
	replace_index = base_str.find("{{}}")
	new_base_str = base_str.replace("{{}}","")
	print(new_base_str)

	accepted_faces_count = 0
	joyCountTotal = [0,0,0,0,0,0]
	sorrowCountTotal = [0,0,0,0,0,0]
	angerCountTotal = [0,0,0,0,0,0]
	surpriseCountTotal = [0,0,0,0,0,0]
	
	picture_number = start
	while picture_number <= end:
		this_path = new_base_str[:replace_index] + str(picture_number) + new_base_str[replace_index:]
		faces = get_dict_from_json(this_path)
		localAccepted, localJoy, localSorrow, localAnger, localSurprise = findSentiments(faces, EPSILON)
		accepted_faces_count += localAccepted
		joyCountTotal = [joyCountTotal[i] + localJoy[i] for i in range(len(joyCountTotal))]
		sorrowCountTotal = [sorrowCountTotal[i] + localSorrow[i] for i in range(len(sorrowCountTotal))]
		angerCountTotal = [angerCountTotal[i] + localAnger[i] for i in range(len(angerCountTotal))]
		surpriseCountTotal = [surpriseCountTotal[i] + localSurprise[i] for i in range(len(surpriseCountTotal))]
		picture_number += 1
	return (accepted_faces_count, joyCountTotal, sorrowCountTotal, angerCountTotal, surpriseCountTotal)
	
if __name__ == "__main__":
	#path = "angleMETA/G0011576_META.json"
	#path = "framesMETA/frame102_META.json"

	#to be indexed with likelihoods 0-5
	likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

	#Our error tolerance. Faces with detection_confidence*landmarking_confidence > EPSILON
	#are accepted
	EPSILON = 0

	#base_path = "framesMETA/frame{{}}_META.json"
	base_path = "angleMETA/G0011{{}}_META.json"
	accepted_faces_count, joyCount, sorrowCount, angerCount, surpriseCount = crawl(base_path, 576, 585, EPSILON)
	displaySentiment('Joy', likelihood_name, joyCount)
	displaySentiment('Sorrow', likelihood_name, sorrowCount)
	displaySentiment('Anger', likelihood_name, angerCount)
	displaySentiment('Surprise', likelihood_name, surpriseCount)
	#TODO: find average confidence coefficient and variance, plot them as a range
	
