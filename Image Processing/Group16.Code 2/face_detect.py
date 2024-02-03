import cv2
import sys

# Get user supplied values
class face_detect:
	
	def __init__(self, xmlPath):
		self.xmlPath = xmlPath
		self.faceCascade = cv2.CascadeClassifier(xmlPath)

	def facePresent(self, imgPath):
	# Create the haar cascade
	# Read the image
		image = cv2.imread(imgPath)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# print self.xmlPath
		# Detect faces in the image
		faces = -1
		faces = self.faceCascade.detectMultiScale(
		    gray,
		    scaleFactor=1.3,
		    minNeighbors=5,
		    minSize=(30, 30),
		    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
		)
		# for (x, y, w, h) in faces:
		#     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

		# cv2.imshow("Faces found", image)
		# cv2.waitKey(0)
		if isinstance(faces, int):
			print imgPath
		return len(faces)
		