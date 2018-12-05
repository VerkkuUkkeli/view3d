import time
import numpy as np

from helpers import *
from curses import wrapper
from renderer import Renderer
from model import Model

def main(stdscr):

    fs = 0.1   # scale frequency

    # running flag
    running = True

    renderer = Renderer(stdscr)     # init renderer
    model = Model()                 # model to be displayed
    model.scale = 1.5*np.ones(3)

    # program main loop
    while running:
        stdscr.clear()  # clear screen

        renderer.render(model)
        model.rot += np.array([0.1, 0.03, 0.07])
        model.scale = np.ones(3)*ucos(2*fs*np.pi*time.time())

        time.sleep(0.1)     # limit framerate to 10fps to avoid glitching


if __name__ == '__main__':
    wrapper(main)
