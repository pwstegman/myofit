import numpy as np 
from sklearn.neighbors import NearestNeighbors

def rms(arr):
	return np.sqrt(np.average(np.square(np.array(arr)))) #np.square maps square on every element of an np.array

def extractFeatures(arr):
	"""
		root mean square on each element of arr
		Take list of lists
		Map root mean square on each list within list
		return a list of singleton values
	"""
	# res = []
	# for l in arr:
	# 	res.push(np.sqrt(np.average(np.square(np.array(l)))))
	# return res

	# list because http://stackoverflow.com/a/1303354/3861396
	return list(map(rms, arr))

# In the following example, we construct a NeighborsClassifier class from an array representing our data set and ask who’s the closest point to [1,1,1]
# >>>
# >>> samples = [[0., 0., 0.], [0., .5, 0.], [1., 1., .5]]
# >>> from sklearn.neighbors import NearestNeighbors
# >>> neigh = NearestNeighbors(n_neighbors=1)
# >>> neigh.fit(samples) 
# NearestNeighbors(algorithm='auto', leaf_size=30, ...)
# >>> print(neigh.kneighbors([1., 1., 1.])) 
# (array([[ 0.5]]), array([[2]]...))
# As you can see, it returns [[0.5]], and [[2]], which means that the element is at distance 0.5 and is the third element of samples (indexes start at 0).

#http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html#sklearn.neighbors.KNeighborsClassifier
def classify(knownsSamples, knownsOutputs, unknown):
	"""
		knownsSamples: all the data points used for the kneighbors
		knownsOutputs: a mapping between a knownsSamples and the type of movement. return is an element of this array
		unknown: what you search for with kkn
		return: search knownsSamples for unknown, get that index, and use that index to find the mapping in the knownsOutputs
	"""
	neigh = NearestNeighbors(weights='distance', n_neighbors=1)

	neigh.fit(knownsSamples)

	i = neigh.kneighbors(unknown)[1][0][0]

	return knownsOutputs[i]