from pyspark import SparkConf, SparkContext

conf = (SparkConf().setMaster("local").setAppName("Index").set("spark.executor.memory", "12g"))
sc = SparkContext(conf = conf)
sc.addPyFile('Group16.Code/face_detect.py')
sc.addPyFile('Group16.Code/colordescriptor.py')

from face_detect import face_detect
from colordescriptor import ColorDescriptor
import argparse
import glob
import cv2



def descriptorExtract(imagePath, xmlPath):

	imageID = imagePath
	image = cv2.imread(imagePath)
	
	fd = face_detect(xmlPath)
	try:
		len_faces = fd.facePresent(imagePath)
	except:
		return [-1,-1,-1]
	# describe the image
	features = cd.describe(image)

	# write the features to file
	features = [float(f) for f in features]
	idList = [imageID.split("/")[-1], len_faces]
	features = idList + features

	return features

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the computed index will be stored")
ap.add_argument("-x", "--xmlPath", required = True,
	help = "Path to where the face detection xml file is stored")

args = vars(ap.parse_args())

# initialize the color descriptor
cd = ColorDescriptor((8, 12, 3))
xmlPath = args['xmlPath']
# open the output index file for writing
# output = open(args["index"], "w")

# use glob to grab the image paths and loop over them
imagePaths = sc.parallelize(glob.glob(args["dataset"] + "/*"))

distList = imagePaths.map(lambda x : descriptorExtract(x, xmlPath))
# print distList.count(), "Extract"
distList = distList.filter(lambda x : x[0] != -1)
# print distList.count(), "Filter"
distList.saveAsPickleFile(args['index'])
# print distList.take(8)
