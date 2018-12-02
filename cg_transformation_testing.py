import numpy as np
from numpy import sin, cos, pi
from helpers import *
import matplotlib.pyplot as plt

# state vectors of the cube
pos = np.array([3.5, 3.5, 3.5, 1], dtype=np.float32)   # position vector
R = np.array([0, 0, 0], dtype=np.float32)              # vector of euler angles (yaw, pitch, roll)
s = np.array([0.5, 0.5, 0.5], dtype=np.float32)        # scaling vector in local coordinates (object space)


# compute modelview matrix
S = scale_matrix(s)
R = rotation_matrix(R[0], R[1], R[2])
T = translation_matrix(pos)
modelview = T @ R @ S  # scale first, then rotate and translate

# print(modelview)

# draw lines at face edges for vertices in world space
"""
for f in faces:
    for i in range(len(f)):
        v1 = world_vertices[f[i-1]]
        v2 = world_vertices[f[i]]
        # draw_line(v1, v2)
"""



def main():
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

    eye = np.array([0, -3, 5, 0], dtype=np.float32)
    up = np.array([0, 0, 1, 0], dtype=np.float32)

    # compute cube vertex coordinates in eye space
    eye_vertices = []
    L = look_at(eye, up)
    for v in vertices:
        eye_vertices.append(L@v)

    clip_vertices = []
    P = perspective(np.pi/4, 1, 0.1, 10)
    for v in eye_vertices:
        clip_vertices.append(P@v)

    normalised = []
    for v in clip_vertices:
        normalised.append(v/v[3])

    plt.figure(1)
    x = []
    y = []
    for v in normalised:
        x.append(v[0])
        y.append(v[1])

        print(v)
    plt.scatter(y, x)
    plt.show()


if __name__ == '__main__':
    main()
