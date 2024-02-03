# import the necessary packages
import numpy as np
import csv

class Searcher:
	def __init__(self, facePresent):
		# store our index path
		self.facePresent = facePresent
		
	def score(self, features, queryFeatures):
		return (features[0], features[1], self.chi2_distance(features[2:], queryFeatures))

	def search(self, distFeatures, queryFeatures, limit):
		# initialize our dictionary of results
		# heap = []
		results = distFeatures.map(lambda x : self.score(x, queryFeatures))
	    # if self.facePresent == 'True':
		# 	results = results.filter(lambda x : x[1] > 0)
			
		# elif self.facePresent == 'False':
		# 	results = results.filter(lambda x : x[1] == 0)
			
		# sort our results, so that the smaller distances (i.e. the
		# more relevant images are at the front of the list)
		# return results.take(10)
		return results.takeOrdered(limit, lambda x : x[2])

	def chi2_distance(self, histA, histB, eps = 1e-10):
		# compute the chi-squared distance

		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])
		# return the chi-squared distance
		return d