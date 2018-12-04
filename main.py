import time
import numpy as np

from helpers import *
from curses import wrapper
from renderer import Renderer
from model import Model

def main(stdscr):

    # animation variables
    fs = 0.1   # scale frequency
    scale = 2

    # running flag
    running = True

    renderer = Renderer(stdscr)     # init renderer
    model = Model()                 # model to be displayed

    # program main loop
    while running:
        stdscr.clear()  # clear screen

        renderer.render(model)
        model.rot += np.array([0.03, 0.02, 0.05])
        model.scale = scale * np.array([ucos(2*np.pi*fs*time.time()), usin(2*np.pi*2*fs*time.time()), 1])

        time.sleep(0.1)     # limit framerate to 10fps to avoid glitching


if __name__ == '__main__':
    wrapper(main)
