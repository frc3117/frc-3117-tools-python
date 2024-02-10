from tkinter import *

from frctools.frcmath import bezier


class BezierCurve:
    def __init__(self, start, end, control, canvas: Canvas, resolution: int = 100):
        self.__start = start
        self.__end = end
        self.__control = control

        self.__canvas = canvas
        self.__resolution = resolution

        self.__line = self.__canvas.create_line(*self.get_points(), fill="black", width=3)

    def set_start(self, start):
        self.__start = start

    def set_end(self, end):
        self.__end = end

    def set_control(self, control):
        self.__control = control

    def get_points(self):
        points = []
        for i in range(self.__resolution):
            t = i / self.__resolution

            x, y = bezier(self.__start, self.__end, self.__control, t)
            points.append(int(x))
            points.append(int(y))

        return points

    def update(self, update_canvas: bool = True):
        self.__canvas.coords(self.__line, *self.get_points())
        if update_canvas:
            self.__canvas.update()


class PathPlanningVisualization:
    def __init__(self):
        self.__win = Tk()
        self.__win.title("Camera Calibrator")
        self.__win.geometry("1200x800")

        self.__cv = Canvas(self.__win, bg="white")
        self.__cv.pack(expand=YES, fill=BOTH)

        self.__bezier_curve = BezierCurve((100, 100), (500, 100), (300, 300), self.__cv)

        self.__cv.bind("<Button-1>", self.__on_click_1__)
        self.__cv.bind("<Button-2>", self.__on_click_2__)
        self.__cv.bind("<Button-3>", self.__on_click_3__)

    def __on_click_1__(self, event):
        self.__bezier_curve.set_start((event.x, event.y))
        self.__bezier_curve.update()

    def __on_click_2__(self, event):
        self.__bezier_curve.set_end((event.x, event.y))
        self.__bezier_curve.update()

    def __on_click_3__(self, event):
        self.__bezier_curve.set_control((event.x, event.y))
        self.__bezier_curve.update()


PathPlanningVisualization()
mainloop()
