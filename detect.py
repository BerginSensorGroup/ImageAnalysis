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

#saves a faces' metadata to an empty JSON (or overwrites an existing one)
def save_metadata(faces, output_filename):
	#the current version of google vision api is not directly serializable to json
	# this means this line doesn't work: json.dump(faces, outfile)
	#we must manually assign respective values to each key
	#Also note that some of the docs indicate camel casing, this is incorrect.
	#the correct format is with underscores: 'detection_confidence' not detectionConfidence
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
	#given a picture's path and folder, it generates paths and filenames for
	#metadata and highlighting
	
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

def getFaces(file_name):
	# Instantiates a client
	client = vision.ImageAnnotatorClient()

	# Loads the image into memory
	with io.open(file_name, 'rb') as image_file:
		content = image_file.read()

	image = types.Image(content=content)
	# Performs label detection on the image file
	response = client.face_detection(image=image)
	faces = response.face_annotations
	return faces


if __name__ == "__main__":
	imagePath = 'G0011577.JPG'
	folder = 'angle'
	#to be indexed with likelihoods 0-5
	likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

	file_name, meta_file_name, edited_file_name = generatePaths(imagePath, folder)

	faces = getFaces(file_name)
	#eventually we want to throw out if blurry, underexposed, or low score

	save_metadata(faces, meta_file_name)
	highlight_faces(file_name, faces, edited_file_name)
