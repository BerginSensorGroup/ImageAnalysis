
def find_score_of_file(file_path):
	'''
	Calcuates a sentiment score for a group of facial meta_data
	Returns the start and end times the images were captured, the score, 
	the number of faces analyzed, and the number of faces without neutral/unknown sentiment
	
	Parameters
	'''
	end_of_file = False
	file = open(file_path, 'r')
	
	score_sum = 0
	faces_analyzed = 0
	non_neutral_faces = 0
	
	while not end_of_file:
		line = file.readline()
		if line == '':
			end_of_file = True
			continue
		line_data = line.split(' ')
		if line_data[0] = 'image':
			#TODO: handle timestamp
			continue
		else if line_data[0][:4] == 'face':
			joy = int(line_data[])
			sorrow = int(line_data[])
			anger = int(line_data[])
			sentiment = phi(joy, sorrow, anger)
			if sentiment != 0:
				non_neutral_faces += 1
			score_sum += sentiment
			faces_analyzed += 1
	#TODO: return start and end times images were captured
	return score_sum, faces_analyzed, non_neutral_faces

def phi(joy_likelihood, sorrow_likelihood, anger_likelihood,):
	'''
	Defined Likelihoods:
	0: 'UNKNOWN', 1: 'VERY_UNLIKELY', 2: 'UNLIKELY', 3: 'POSSIBLE', 4: 'LIKELY', 5: 'VERY_LIKELY'
	
	Joy:
	Very Unlikely:  0
	Unlikely to Very Likely: 1
	
	Anger, Sorrow:
	Very Unlikely: 0
	Unlikely to Very Likely: -1
	
	Possible return values:
	-1: face shows negative sentiment
	0: face shows neutral/unknown sentiment
	1: face shows positive sentiment
	'''
	MAX = 1
	MIN = -1
	
	total = 0
	if joy_likelihood > 1:
		total += 1
	if anger_likelihood > 1:
		total -= 1
	if sorrow_likelihood > 1:
		total -= 1
	
	if total > MAX:
		total = MAX
	else if total < MIN:
		total = MIN
	return total