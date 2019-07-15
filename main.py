# --------------------------------------
# import
# --------------------------------------
import os
import tkinter.filedialog as tkfd

from PIL import Image
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation

# --------------------------------------
# define
# --------------------------------------

# --------------------------------------
# class
# --------------------------------------


class RandomErasingSim:
    AXCOLOR = 'lightgoldenrodyellow'
    BASE_WINDOW_WH = (9, 6)

    # widget position [left, bottom, width, height]
    AX_RECT_IMG = [0.1, 0.4, 0.8, 0.5]

    AX_RECT_SH_SLIDER = [0.1, 0.3, 0.8, 0.04]
    AX_RECT_R1_SLIDER = [0.1, 0.2, 0.8, 0.04]
    AX_RECT_INTERVAL_SLIDER = [0.1, 0.1, 0.8, 0.04]

    AX_RECT_OPEN_BUTTON = [0.1, 0.025, 0.1, 0.04]
    AX_RECT_QUIT_BUTTON = [0.2, 0.025, 0.1, 0.04]
    AX_RECT_START_BUTTON = [0.7, 0.025, 0.1, 0.04]
    AX_RECT_STOP_BUTTON = [0.8, 0.025, 0.1, 0.04]

    def __init__(self):

        self.with_randomerasing = True
        self.quit = False
        self.interval = 0.5

        # ---------------------------
        # random erasing init paramters
        # ---------------------------
        self.r1 = 0.3
        self.r2 = 1 / self.r1
        self.sl = 0.02
        self.sh = 0.4

        self.init_widgets()

    def init_widgets(self):
        # dummy image
        self.img = np.uint8(np.zeros((480, 640, 3)))
        self.prev_img = self.img

        self.fig = plt.figure(figsize=self.BASE_WINDOW_WH)
        self.ax_img = plt.axes(self.AX_RECT_IMG)
        plt.axes(self.ax_img)  # set img_ax
        self.img_plot = plt.imshow(self.img)

        # ---------------------------
        # make slider
        # ---------------------------
        self.sh_slider = self.make_slider(
            plt.axes(self.AX_RECT_SH_SLIDER, facecolor=self.AXCOLOR),
            'sh',
            0.1, 1, self.sh,
            self.event_slider_changed)

        self.r1_slider = self.make_slider(
            plt.axes(self.AX_RECT_R1_SLIDER, facecolor=self.AXCOLOR),
            'r1',
            0.1, 1, self.r1,
            self.event_slider_changed)

        self.interval_slider = self.make_slider(
            plt.axes(self.AX_RECT_INTERVAL_SLIDER, facecolor=self.AXCOLOR),
            'interval',
            0.1, 1, self.interval,
            self.event_slider_changed)

        # ---------------------------
        # make button
        # ---------------------------
        self.open_button = self.make_button(
            plt.axes(self.AX_RECT_OPEN_BUTTON, facecolor=self.AXCOLOR),
            'open',
            self.event_open_clicked)

        self.quit_button = self.make_button(
            plt.axes(self.AX_RECT_QUIT_BUTTON, facecolor=self.AXCOLOR),
            'quit',
            self.event_quit_clicked)

        self.start_button = self.make_button(
            plt.axes(self.AX_RECT_START_BUTTON, facecolor=self.AXCOLOR),
            'start',
            self.event_start_clicked)

        self.stop_button = self.make_button(
            plt.axes(self.AX_RECT_STOP_BUTTON, facecolor=self.AXCOLOR),
            'stop',
            self.event_stop_clicked)

    def run(self):

        while True:
            if self.quit:
                break

            if self.with_randomerasing:
                # draw img with random erasing
                img = self.random_erasing(self.img,
                                          p=1.0,
                                          sl=self.sl,
                                          sh=self.sh,
                                          r1=self.r1,
                                          r2=self.r2)

                plt.axes(self.ax_img)  # set img_ax
                self.img_plot.set_data(img)
                self.prev_img = img
                plt.pause(self.interval)  # seconds

            else:
                # draw img only
                self.img_plot.set_data(self.prev_img)
                plt.pause(1.0)  # seconds

    def event_slider_changed(self, val):
        # get all slider values
        self.interval = self.interval_slider.val
        self.sh = self.sh_slider.val
        self.r1 = self.r1_slider.val
        self.r2 = 1/self.r1
        print("params : sl={:.2f}  sh={:.2f}  r1={:.2f}  r2={:.2f}  disp_interval={:.2f} sec".format(
            self.sl, self.sh, self.r1, self.r2, self.interval))

    def event_open_clicked(self, event):
        print("ask filename")
        file_path = tkfd.askopenfilename()
        print(file_path)
        self.img = np.asarray(Image.open(file_path))
        self.img.flags.writeable = True

        plt.axes(self.ax_img)  # set img_ax
        plt.title(file_path)

        self.with_randomerasing = True

    def event_quit_clicked(self, event):
        print("quit")
        self.quit = True

    def event_start_clicked(self, event):
        print("random_erasing : {} -> {}".format(self.with_randomerasing, 'True'))
        self.with_randomerasing = True

    def event_stop_clicked(self, event):
        print("random_erasing : {} -> {}".format(self.with_randomerasing, 'False'))
        self.with_randomerasing = False

    def make_slider(self, axes, name, min_val, max_val, init_val, func):
        slider = Slider(axes, name, min_val, max_val, init_val)
        slider.on_changed(func)
        return slider

    def make_button(self, axes, name, func):
        button = Button(axes, name, color=self.AXCOLOR, hovercolor='0.975')
        button.on_clicked(func)
        return button

    def random_erasing(self, img, p=0.5, sl=0.02, sh=0.4, r1=0.3, r2=3.3):
        target_img = img.copy()

        if p < np.random.rand():
            return target_img

        h, w, _ = target_img.shape
        s = h * w

        cnt = 0
        while True:
            se = np.random.uniform(sl, sh) * s
            re = np.random.uniform(r1, r2)

            he = int(np.sqrt(se * re))
            we = int(np.sqrt(se / re))

            xe = np.random.randint(0, w)
            ye = np.random.randint(0, h)

            if xe + we <= w and ye + he <= h:
                break

            cnt += 1
            if 5000 < cnt:
                print("random erasing time out")
                return target_img

        mask = np.random.randint(0, 255, (he, we, 3))
        target_img[ye:ye + he, xe:xe + we, :] = mask

        return target_img

# --------------------------------------
# function
# --------------------------------------


# --------------------------------------
# main
# --------------------------------------
if __name__ == "__main__":
    sim = RandomErasingSim()
    sim.run()
