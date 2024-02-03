# import the necessary packages
from colordescriptor import ColorDescriptor
import argparse
import glob
import cv2
 
# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-d", "--dataset", required = True,
#	help = "Path to the directory that contains the images to be indexed")
#ap.add_argument("-i", "--index", required = True,
#	help = "Path to where the computed index will be stored")
#args = vars(ap.parse_args())

args ={	
	'index' : "index.txt",
	'dataset' : "dataset",
}
 
# initialize the color descriptor
cd = ColorDescriptor((8, 12, 3))

# open the output index file for writing
output = open(args['index'], "w")

#print(glob.glob(args['dataset'] + "/*.jpg"))

# use glob to grab the image paths and loop over them
for imagePath in glob.glob(args['dataset'] + "/*.jpg"):
	# extract the image ID (i.e. the unique filename) from the image
	# path and load the image itsel
	
	imageID = imagePath[imagePath.rfind("dataset") + 8:]
	image = cv2.imread(imagePath)
	print(imagePath)
	# describe the image
	features = cd.describe(image)
	# write the features to file
	features = [str(f) for f in features]
	print(imageID)
	output.write("%s,%s\n" % (imageID, ",".join(features)))

# close the index file
output.close()
