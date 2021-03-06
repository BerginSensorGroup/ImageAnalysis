import io
import os
import json

# Imports the Google Cloud client library
from PIL import Image, ImageDraw
from google.cloud import vision
from google.cloud.vision import types


#this function is from: https://cloud.google.com/vision/docs/face-tutorial 
def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
    im.save(output_filename)


def save_metadata(faces, output_filename):
	'''
	saves facial metadata to an empty JSON (or overwrites an existing one)
	
	faces: the list of faces to save
	output_filename: the path, ending in .json that should contain the metadata
	
	Notes:
	the current version of google vision api is not directly serializable to json
	this means this line doesn't work: json.dump(faces, outfile)
	we must manually assign respective values to each key
	Also note that some of the docs indicate camel casing, this is incorrect.
	the correct format is with underscores: 'detection_confidence' not detectionConfidence
	'''
	
	faces_data = {}
	
	#the commented out fields need preprocessing to prepare them for json conversion
	for face_num in range(len(faces)):
		face_data = {}
		#face_data["bounding_poly"] = faces[face_num].bounding_poly
		#face_data["fd_bounding_poly"] = faces[face_num].fd_bounding_poly
		#face_data["landmarks"] = faces[face_num].landmarks
		face_data["roll_angle"] = faces[face_num].roll_angle
		face_data["pan_angle"] = faces[face_num].pan_angle
		face_data["tilt_angle"] = faces[face_num].tilt_angle
		face_data["detection_confidence"] = faces[face_num].detection_confidence
		face_data["landmarking_confidence"] = faces[face_num].landmarking_confidence
		face_data["joy_likelihood"] = faces[face_num].joy_likelihood
		face_data["sorrow_likelihood"] = faces[face_num].sorrow_likelihood
		face_data["anger_likelihood"] = faces[face_num].anger_likelihood
		face_data["surprise_likelihood"] = faces[face_num].surprise_likelihood
		face_data["under_exposed_likelihood"] = faces[face_num].under_exposed_likelihood
		face_data["blurred_likelihood"] = faces[face_num].blurred_likelihood
		face_data["headwear_likelihood"] = faces[face_num].headwear_likelihood
		faces_data["{}".format(face_num)] = face_data
		
	os.makedirs(os.path.dirname(output_filename), exist_ok=True)
	with open(output_filename, 'w') as outfile:
		json.dump(faces_data, outfile)

def generatePaths(imagePath, folder, metaKey = "META", editKey = "EDITED"):
	'''
	Generates paths and filenames for metadata and highlighting
	
	imagePath: the name of the image
	folder: the folder wherein the image lies
	metaKEY and editKey are descriptors of the generated path names
	'''
	cutoff = imagePath.find('.')
	if cutoff == -1:
		return None
	name = imagePath[:cutoff]
	ext = imagePath[cutoff:]
	
	file_name = os.path.join(os.path.dirname(__file__), folder+'/'+imagePath)
	
	metaDataPath = name + '_' + metaKey + '.json'
	metaFolder = folder + metaKey
	meta_file_name = os.path.join(os.path.dirname(__file__), metaFolder+'/'+metaDataPath)
	os.makedirs(os.path.dirname(meta_file_name), exist_ok=True)
	
	editedPath = name + '_' + editKey + ext
	editedFolder = folder + editKey
	edited_file_name = os.path.join(os.path.dirname(__file__), editedFolder+'/'+editedPath)
	os.makedirs(os.path.dirname(edited_file_name), exist_ok=True)
	
	return (file_name, meta_file_name, edited_file_name)

def getFaces(file_name, client):
	'''
	Queries Google for facial data about an image
	
	file_name is the path of the picture file
	client is an ImageAnnotatorClient with which to query Google
	'''
	# Loads the image into memory
	with io.open(file_name, 'rb') as image_file:
		content = image_file.read()

	image = types.Image(content=content)
	# Performs label detection on the image file
	response = client.face_detection(image=image)
	faces = response.face_annotations
	return faces

def  crawl(base_str, start, end, client):
	'''
	Queries Google for the the picture data numbered start to end in the path base_str. 
	Saves the metadeta for each picture into distinct sequential JSON files
	
	base_str is the path from which to acquire the images
	start is the number of the first picture
	end is the number of the final picture
	client is an ImageAnnotatorClient with which to query Google
	
	Assumptions:
	Base string should be of the form 'SOMETEXT{{}}SOMETEXT.SOMETEXT'
	all pictures should have the same extension as the provided base_string template
	the pictures must be in a folder
	the curly braces ({{}}) will be replaced with a number to form the json path
	the picture should not contain any other curly braces
	the curly braces should not be followed by the '/' character
	example use: 
	crawling hello/world3.jpg, hello/world4.jpg, hello/world5.jpg
		base_str = hello/world{{}}.jpg
		start = 3
		end = 5
	'''
	folder_cutoff = base_str.rfind("/")
	folder = base_str[:folder_cutoff]
	base_str = base_str[folder_cutoff+1:]
	replace_index = base_str.rfind("{{}}")
	new_base_str = base_str.replace("{{}}","")
	
	picture_number = start
	while picture_number <= end:
		this_path = new_base_str[:replace_index] + str(picture_number) + new_base_str[replace_index:]
		file_name, meta_file_name, edited_file_name = generatePaths(this_path, folder)
		faces = getFaces(file_name, client)
		save_metadata(faces, meta_file_name)
		highlight_faces(file_name, faces, edited_file_name)
		picture_number += 1

def confirm(start, end):
	decision = input("WARNING: will send {} pictures, enter Y to confirm or N to abort: ".format(1+end-start))
	if decision != "Y":
		print("Aborting")
		quit()
	print("Confirmed, sending pictures to Google")

if __name__ == "__main__":	
	path = 'nonFaces/not_a_face{{}}.jpg'
	start = 1
	end = 1
	confirm(start, end)
		
	# Instantiates a client
	client = vision.ImageAnnotatorClient()
	
	crawl(path, start, end, client)
