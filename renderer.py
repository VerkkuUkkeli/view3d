import curses
from helpers import *
from model import Model

class Renderer:
	# member variables
	__stdscr = None		# curses screen handle
	__width = None		# screen width
	__height = None		# screen height
	__aspect = None		# screen aspect ratio

	# camera
	__eye = np.array([5, 0, 0, 1], dtype=np.float32)	# camera position
	__up = np.array([0, 0, 1, 1], dtype=np.float32)		# camera up-direction


	def __init__(self, stdscr):
		self.__stdscr = stdscr

		# hide cursor
		curses.curs_set(0)

		# find out screen dimensions
		self.__height, self.__width = self.__stdscr.getmaxyx()
		self.__aspect = self.__width/self.__height

		# define curses colours
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)


	def render(self, model):
		# compute transformation matrix from object space to screen space
		T = translation_matrix(model.loc)														# translation matrix
		S = scale_matrix(model.scale)															# scaling matrix
		R = rotation_matrix(model.rot[0], model.rot[1], model.rot[2])							# rotation matrix
		L = look_at(self.__eye, self.__up)														# gluLookAt (camera transform)
		P = perspective(45, self.__aspect/1.9, 0.1, 10)											# gluPerspective (projective transformation)
		V = viewport(0, self.__width, 0, self.__height)

		M = P @ L @ T @ R @ S  # resultant transformation matrix

		# compute normalised device coordinates
		normalised = []
		for v in model.vertices:
			clip_coord = M @ v
			normalised.append(clip_coord/clip_coord[3])  # normalise by dividing by w

		# discard vertices outside cube with sides in range [-1, 1] and apply viewport transformation
		final_vertices = []
		for n in normalised:
			for i in range(len(n)):
				if n[i] <= -1.0:
					continue
				if n[i] >= 1.0:
					continue
			final_vertices.append(V @ n)

		# draw lines at face edges for vertices in world space
		for v in final_vertices:
			self.draw_point(v[0], v[1], symbol='#', color_str='red')
		for f in model.faces:
			for i in range(len(f)):
				v1 = final_vertices[f[i-1]]
				v2 = final_vertices[f[i]]
				self.draw_line(v1, v2, color_str='red')

		self.__stdscr.refresh()


	# draw a symbol at the coordinate (x, y) with the color given in color_str
	def draw_point(self, x, y, symbol='*', color_str='white'):
		# set drawing colour
		color = curses.color_pair(0)
		if color_str == 'red':
			color = curses.color_pair(1)
		if color_str == 'green':
			color = curses.color_pair(2)
		if color_str == 'blue':
			color = curses.color_pair(3)

		# make sure x and y are integers
		x = int(x)
		y = int(y)

		# return if point is out of screen coordinates
		if y >= self.__height or y < 0 or x >= self.__width-1 or x < 0:
			return

		self.__stdscr.addstr(y, x, symbol, color)


	# draw a line between p1 and p2
	def draw_line(self, p1, p2, symbol='*', color_str='white'):
		x1 = int(p1[0])
		x2 = int(p2[0])
		y1 = int(p1[1])
		y2 = int(p2[1])

		dx = x2-x1
		dy = y2-y1

		linechar = '*'

		# check which axis has the most steps and loop over it
		# use linear interpolation to determine the other component

		# draw a point
		if dx == 0 and dy == 0:
			self.draw_point(x1, y2, symbol, color_str)
		# y axis has more steps
		elif 0 < np.abs(dx) < np.abs(dy):
			for y in range(y1, y2, np.sign(dy)):
				x = int(dx/dy*(y-y1) + x1)
				self.draw_point(x, y, symbol, color_str)
		# equal number of steps
		elif dy == dx:
			for y in range(y1, y2, np.sign(dy)):
				x = int(dx/dy*(y-y1) + x1)
				self.draw_point(x, y, symbol, color_str)
		# x has more steps
		elif 0 < np.abs(dy) < np.abs(dx):
			for x in range(x1, x2, np.sign(dx)):
				y = int(dy/dx*(x-x1) + y1)
				self.draw_point(x, y, symbol, color_str)
		# vertical line
		elif np.abs(dx) == 0:
			for y in range(y1, y2, np.sign(dy)):
				self.draw_point(x1, y, symbol, color_str)
		# horizontal line
		elif np.abs(dy) == 0:
			for x in range(x1, x2, np.sign(dx)):
				self.draw_point(x, y1, symbol, color_str)
