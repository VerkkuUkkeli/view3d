import time

from curses import wrapper
from renderer import Renderer
from model import Model



def main(stdscr):
    # running flag
    running = True

    renderer = Renderer(stdscr)     # init renderer
    model = Model()                 # model to be displayed

    # program main loop
    while running:
        stdscr.clear()  # clear screen

        renderer.render(model)
        model.orientation[0] += 0.1

        time.sleep(0.1)     # limit framerate to 10fps to avoid glitching


if __name__ == '__main__':
    wrapper(main)
