import json
import math
import numpy as np
import os


class Face:
	def __init__(self, rollAngle, panAngle, tiltAngle, detectionConfidence, landmarkingConfidence, joyLikelihood,
				sorrowLikelihood, angerLikelihood, surpriseLiklihood, underexposedLikelihood, blurredLikelihood, headwearLikelihood):
		self.roll_angle = roll_angle
		self. pan_angle = panAngle
		self.tilt_angle = tiltAngle
		self.detection_confidence = detectionConfidence
		self.landmarking_confidence = landmarkingConfidence
		self.joy_likelihood = joyLikelihood
		self.sorrow_likelihood = sorrowLikelihood
		self.anger_likelihood = angerLikelihood
		self.surprise_likelihood = surpriseLiklihood
		self.under_exposed_likelihood = underexposedLikelihood
		self.blurred_likelihood = blurredLikelihood
		self.headwear_likelihood = headwearLikelihood

		def getRollAngle(self):
			return self.roll_angle
		def getPanAngle(self):
			return self.pan_angle
		def getTiltAngle(self):
			return self.tilt_angle
		def getDetectionConfidence(self):
			return self.detection_confidence
		def getLandmarkingConfidence(self):
			return self.landmarking_confidence
		def getJoyLikelihood(self):
			return self.getJoyLikelihood
		def getSorrowLikelihood(self):
			return self.sorrow_likelihood
		def getAngerLikelihood(self):
			return self.anger_likelihood
		def getSurpriseLikelihood(self):
			return self.surprise_likelihood
		def getUnderExposedLikelihood(self):
			return self.under_exposed_likelihood
		def getBlurredLikelihood(self):
			return self.blurred_likelihood
		def getHeadwearLikelihood(self):
			return self.getHeadwearLikelihood

		def setRollAngle(self, newRollAngle):
			return self.roll_angle
		def setPanAngle(self, newPanAngle):
			return self.pan_angle
		def setTiltAngle(self, newTiltAngle):
			return self.tilt_angle
		def setDetectionConfidence(self, newDetectionConfidence):
			return self.detection_confidence
		def setLandmarkingConfidence(self, newLandmarkingConfidence):
			return self.landmarking_confidence
		def setJoyLikelihood(self, newJoyLikelihood):
			return self.getJoyLikelihood
		def setSorrowLikelihood(self, newSorrowLikelihood):
			return self.sorrow_likelihood
		def setAngerLikelihood(self, newAngerLikelihood):
			return self.anger_likelihood
		def setSurpriseLikelihood(self, newSurpriseLikelihood):
			return self.surprise_likelihood
		def setUnderExposedLikelihood(self, newUnderExposedLikelihood):
			return self.under_exposed_likelihood
		def setBlurredLikelihood(self, newBlurredLikelihood):
			return self.blurred_likelihood
		def setHeadwearLikelihood(self, newHeadwearLikelihood):
			return self.getHeadwearLikelihood
