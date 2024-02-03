from pyspark import SparkConf, SparkContext
conf = (SparkConf().setMaster("local").setAppName("Index").set("spark.executor.memory", "8g"))
sc = SparkContext(conf = conf)
sc.addPyFile('Group16.Code/searcher.py')
sc.addPyFile('Group16.Code/colordescriptor.py')


# from pyspark import SparkContext
# sc = SparkContext("local", "Index", pyFiles=['examples/src/main/FaceDetect/colordescriptor.py','examples/src/main/FaceDetect/searcher.py'], "spark.executor.memory", "8g")

from colordescriptor import ColorDescriptor
from searcher import Searcher
import argparse
import cv2
import time
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the computed index will be stored")
# ap.add_argument("-q", "--query", required = True,
	# help = "Path to the query image")
ap.add_argument("-r", "--resultpath", required = True,
	help = "Path to the result path")
ap.add_argument("-p", "--filePath", required = True,
	help = "Path to the file path")
ap.add_argument("-n", "--numImages", 
	help = "Number of similar images")

args = vars(ap.parse_args())

if not args['numImages']:
	numImages = 9
else:
	numImages = int(args['numImages'])
	
# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

# load the query image and describe it
listFiles = sc.textFile(args['filePath'])
listFiles = listFiles.collect()

start_time = time.time()
distFeatures = sc.pickleFile(args["index"]).cache()
faceFeatures = distFeatures.filter(lambda x : x[1] > 0).cache()
noFaceFeatures = distFeatures.filter(lambda x : x[1] == 0).cache()
print (time.time() - start_time), "Filtering time"

for oneFile in listFiles:

	filePath, facePresent = oneFile.split(",")

	filePath = os.path.join(os.getcwd(),os.path.join("Group16.Code", filePath))
	query = cv2.imread(filePath)
	features = cd.describe(query)
	# perform the search

	start_time = time.time()
	searcher = Searcher(facePresent)
	if facePresent == 'True':
		results = searcher.search(faceFeatures, features, numImages)
	elif facePresent == 'False':
		results = searcher.search(noFaceFeatures, features, numImages)
	else:
		results = searcher.search(distFeatures, features, numImages)
	print time.time() - start_time, "Search Time", oneFile

	# display the query
	height, width, channels = query.shape
	while height > 1800 or width > 1080:
		query = cv2.resize(query, (0, 0), fx = 0.5, fy = 0.5)
		height, width, channels = query.shape

	cv2.imshow("Query", query)
	cv2.waitKey(4000)
	cv2.destroyWindow("Query")
	# loop over the results
	results = results[1:]

	for result in results[1:]:
		resultID = result[0]

		result = cv2.imread(args['resultpath'] + "/" + resultID)
		# print args['resultpath'] + "/" + resultID
		height, width, channels = result.shape
		
		while height > 1800 or width > 1080:
			result = cv2.resize(result, (0, 0), fx = 0.5, fy = 0.5)
			height, width, channels = query.shape

		
		cv2.imshow("Result - "+ resultID, result)
		cv2.waitKey(1000)
		cv2.destroyWindow("Result - "+ resultID)
	