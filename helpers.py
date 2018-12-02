import numpy as np
from numpy import sin, cos

# return length of x, y, z components of 4-vector
def norm4(v):
    return np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

# return 4-vector whose x, y, z components have been normalised and w is 1
def normalize4(v):
    v3 = v[:-1]/norm4(v)
    return np.array([v3[0], v3[1], v3[2], 1])

# take cross product of 4-vectors
def cross4(v1, v2):
    v3 = np.cross(v1[:-1], v2[:-1])
    return np.array([v3[0], v3[1], v3[2], 1])

# eye is the position vector of the camera in world frame
# up denotes camera up vector (direction of camera space y vector in world frame)
def look_at(eye, up):
    w = normalize4(eye)
    u = normalize4(cross4(up, w))
    v = cross4(w, u)

    T = np.array([
        [1, 0, 0, -eye[0]],
        [0, 1, 0, -eye[1]],
        [0, 0, 1, -eye[2]],
        [0, 0, 0,       1]
    ], dtype=np.float32)

    R = np.array([
        [v[0], v[1], v[2], 0],
        [u[0], u[1], u[2], 0],
        [w[0], w[1], w[2], 0],
        [   0,    0,    0, 1]
    ], dtype=np.float32)

    return R@T


def perspective(fovy, aspect, znear, zfar):
    theta = fovy/2
    d = 1/np.tan(theta)

    A = -(zfar+znear)/(zfar-znear)
    B = -(2*zfar*znear)/(zfar-znear)

    M = np.array([
        [d/aspect, 0, 0, 0],
        [0, d, 0, 0],
        [0, 0, A, B],
        [0, 0, -1, 0],
    ])

    return M


# returns a scaling matrix about the origin for a scale 4-vector s
def scale_matrix(s):
    S = np.array([
        [s[0],     0,    0,  0],
        [   0,  s[1],    0,  0],
        [   0,     0, s[2],  0],
        [   0,     0,    0,  1]
    ], dtype=np.float32)
    return S


# returns a translation matrix for displacement 4-vector disp
def translation_matrix(disp):
    T = np.array([
        [1, 0, 0, disp[0]],
        [0, 1, 0, disp[1]],
        [0, 0, 1, disp[2]],
        [0, 0, 0,       1]
    ], dtype=np.float32)
    return T


# returns the 4x4 rotation matrix for the given euler angles
def rotation_matrix(yaw, pitch, roll):
    # rotation about the z axis
    Rz = np.array([
        [cos(yaw), -sin(yaw), 0, 0],
        [sin(yaw), cos(yaw), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

    # rotation about the y axis
    Ry = np.array([
        [cos(pitch), 0, sin(pitch), 0],
        [0, 1, 0, 0],
        [-sin(pitch), 0, cos(pitch), 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

    # rotation about the x axis
    Rx = np.array([
        [1, 0, 0, 0],
        [0, cos(roll), -sin(roll), 0],
        [0, sin(roll), cos(roll), 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

    # apply the rotations in the order yaw, pitch, roll (from right to left)
    return Rx @ Ry @ Rz
