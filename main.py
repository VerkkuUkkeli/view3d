from curses import wrapper
import numpy as np
from helpers import *
import time

t = 0
eye = np.array([0, -4, 3, 0], dtype=np.float32)


def init():
    ...


def handle():
    ...


def render(stdscr):
    global eye
    global t

    # get screen dimensions
    screen_height, screen_width = stdscr.getmaxyx()

    # compute screen aspect ratio
    aspect = screen_width/screen_height


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

    d_theta = 0.1
    t += 0.01
    R = rotation_matrix(0, 0, t)
    eye = 5*normalize4(R@eye)

    stdscr.addstr(0,30, "eye: {}".format(eye))


    # compute cube vertex coordinates in eye space
    eye_vertices = []
    L = look_at(eye, up)
    for v in vertices:
        eye_vertices.append(L @ v)

    clip_vertices = []
    P = perspective(np.pi / 4, aspect, 0.1, 10)
    for v in eye_vertices:
        clip_vertices.append(P @ v)

    normalised = []
    for v in clip_vertices:
        normalised.append(v / v[3])

    adjusted = []
    for n in normalised:
        for i in range(len(n)):
            adj = (n[i] + 1.0)/2
            if adj <= 0:
                adj = 0
            if adj >= 1.0:
                adj = 1.0
            n[i] = adj
        adjusted.append(n)

    line = ''.join([' ' for _ in range(screen_width-1)])
    for row in range(screen_height):
        ...
        #stdscr.addstr(row, 0, line)

    # debug messages
    stdscr.addstr(0, 0, "Screen dimensions: {}x{}".format(screen_width, screen_height))
    stdscr.addstr(1, 0, "Screen aspect: {:.2f}".format(aspect))
    for i in range(8):
        stdscr.addstr(3+i, 0, "Adjusted[{}]: [{:.2f}, {:.2f}, {:.2f}]".format(i, adjusted[i][0], adjusted[i][1], adjusted[i][2]))


    for n in adjusted:
        stdscr.addstr(2, 0, '          ')
        stdscr.addstr(2, 0, '({}, {})'.format(int(n[1]*(screen_height-1)), int(n[0]*(screen_width-1))))
        stdscr.addstr(int(n[1]*(screen_height-2)), int(n[0]*(screen_width-2)), '#')
        # stdscr.addch('*')

    time.sleep(0.017)


def main(stdscr):
    # running flag
    running = True

    # program main loop
    while running:

        stdscr.clear()

        render(stdscr)

        stdscr.refresh()
        # stdscr.getkey()


wrapper(main)
