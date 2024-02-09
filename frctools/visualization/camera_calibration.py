from tkinter import *
from PIL import Image, ImageTk
from frctools.vision import CameraThread, CameraCalibrator

import cv2 as cv


def resize_img(img, width, height):
    # Get the original width and height
    original_width, original_height = img.size

    # Calculate scale factors for width and height
    width_scale = width / original_width
    height_scale = height / original_height

    # Choose the minimum scale factor to fit within the specified dimensions
    scale_factor = min(width_scale, height_scale)

    # Calculate new width and height
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)

    # Resize the image
    resized_img = img.resize((new_width, new_height))

    return resized_img


def set_button_color(button: Button, default: str, hover: str, clicked: str):
    def on_enter(e):
        e.widget.configure(bg=hover)

    def on_exit(e):
        e.widget.configure(bg=default)

    button.configure(activebackground=clicked)
    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_exit)


class CameraCalibratorVisualization:
    def __init__(self):
        self.__win = Tk()
        self.__win.title("Camera Calibrator")
        self.__win.geometry("800x600")

        self.__left_frame = Frame(self.__win, bg="blue")
        self.__left_frame.place(relheight=1, relwidth=0.20, anchor="nw")

        self.__right_frame = Frame(self.__win, bg="red")
        self.__right_frame.place(relheight=1, relwidth=0.80, relx=0.20, anchor="nw")

        self.__img_preview = Label(self.__right_frame)
        self.__img_preview.pack(anchor="center", expand=True, fill="both")
        self.__img_preview.bind("<Configure>", self.__dyn_resize_preview__)

        self.__take_picture_button = Button(self.__right_frame,
                                            text='Take Picture',
                                            command=lambda: print('pressed'),
                                            activebackground='grey',
                                            background='white'
                                            )
        self.__take_picture_button.place(width=80, height=60, relx=0.5, rely=1, y=-10, anchor='s')
        set_button_color(self.__take_picture_button, 'white', 'green', 'grey')

        self.__frame_width = 0
        self.__frame_height = 0
        self.__current_img = None

        self.__img_generator = None

    def __dyn_resize_preview__(self, event):
        self.__frame_width = event.width
        self.__frame_height = event.height

        self.__update_preview__()

    def __update_preview__(self):
        result = next(self.__img_generator)
        if result is not None:
            _, img = result
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            self.__current_img = Image.fromarray(img)

        if self.__current_img is None or 0 in (self.__frame_width, self.__frame_height):
            return

        resized = resize_img(self.__current_img, self.__frame_width, self.__frame_height)
        resized = ImageTk.PhotoImage(resized)

        self.__img_preview.configure(image=resized)
        self.__img_preview.image = resized

    def run(self):
        cap = CameraThread(0)
        cap.start()

        self.__img_generator = cap.get_frame_generator()

        while True:
            self.__update_preview__()
            self.__win.update()
