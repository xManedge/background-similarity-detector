README

CS 8803 Big Data Systems
Fall 2015
Group 16 Course Project

Team Members:
Priyanka Ganesan
Sharmila Raghu
Harikumar Venkatesan

Files included:
Group16.Code/
--colordescriptor.py
--indexSpark.py
--searchSpark.py
--face_detect.py
--defFace.xml
--path.txt
--searcher.py
--Query Images/
	1.JPG
	3.JPG

--sDataset/
	--  multiple images --
	
Software:
Ubuntu 14.04
Spark 1.1.0
Python 2.7
OpenCV 2.4.X

Please copy paste the folder with the code into the same folder as spark bin is present.


Execution:
1. Indexing operation: Needs ~2 hours to run
    $ ./bin/spark-submit Group16.Code/indexSpark.py -d Group16.Code/Dataset/ -i Group16.Code/index -x Group16.Code/defFace.xml

2. Image search:
	i. Search for related images (return top 10 results):
		$ ./bin/spark-submit Group16.Code/searchSpark.py -i Group16.Code/index -r Group16.Code/Dataset/ -p Group16.Code/path.txt -n 10

			In order to change the input images to the code, please change the path specified in the "path.txt" file. This path points to the image that you want to search with. The second parameter in the line specifies whether the result images should have faces or not. "True" implies there are faces in the results, "False" implies that there are no faces in the results, and "None" means we do not care if the results contain faces or not.