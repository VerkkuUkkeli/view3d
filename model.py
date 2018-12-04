import numpy as np

class Model:
	# location, rotation, scale
	loc 	= np.array([0, 0, 0], dtype=np.float32)
	rot 	= np.array([0, 0, 0], dtype=np.float32)
	scale 	= np.array([1, 1, 1], dtype=np.float32)

	vertices = np.array([
		# lower vertices
		np.array([1, -1, -1, 1], dtype=np.float32),
		np.array([1, 1, -1, 1], dtype=np.float32),
		np.array([-1, 1, -1, 1], dtype=np.float32),
		np.array([-1, -1, -1, 1], dtype=np.float32),
		# upper vertices
		np.array([1, -1, 1, 1], dtype=np.float32),
		np.array([1, 1, 1, 1], dtype=np.float32),
		np.array([-1, 1, 1, 1], dtype=np.float32),
		np.array([-1, -1, 1, 1], dtype=np.float32),
	])

	# list of 4-tuples containing the indices of the vertices belonging to a face quad
	faces = [(0, 1, 2, 3), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 6, 7)]

	def __init__(self):
		...