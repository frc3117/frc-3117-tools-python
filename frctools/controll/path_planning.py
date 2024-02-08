from frctools.frcmath import Vector2, bezier, lerp_angle, inverse_lerp
from typing import List, Tuple


class PathPlanningPoint:
    def __init__(self, position: Vector2, heading: float, time: float):
        self.position = position
        self.heading = heading
        self.time = time


class PathPlanning:
    def __init__(self):
        self.__points: List[PathPlanningPoint] = []
        self.__control_points: List[Vector2] = []

    def get_time(self) -> float:
        return self.__points[-1].time

    def get_bezier(self, index: int) -> Tuple[PathPlanningPoint, PathPlanningPoint, Vector2]:
        start = self.__points[index]
        end = self.__points[index + 1]
        control = self.__control_points[index]

        return start, end, control

    def get_all_bezier(self) -> List[Tuple[PathPlanningPoint, PathPlanningPoint, Vector2]]:
        return [self.get_bezier(i) for i in range(len(self.__points) - 1)]

    def set_beizer_control_point(self, index: int, control_point: Vector2):
        self.__control_points[index] = control_point

    def get_point(self, index: int) -> PathPlanningPoint:
        return self.__points[index]

    def get_points_count(self) -> int:
        return len(self.__points)

    def add_point(self, point: PathPlanningPoint, control_point: Vector2 = None):
        self.__points.append(point)

        if len(self.__points) > 1:
            if control_point is None:
                control_point = self.__points[-2].position + (point.position - self.__points[-2].position) / 2
            self.__control_points.append(control_point)

    def get_state_at(self, time: float) -> Tuple[Vector2, float]:
        # If the time is less than 0, return the first point
        if time <= 0:
            first_point = self.__points[0]
            return first_point.position, first_point.heading

        # If the time is greater than the last point, return the last point
        if time >= self.__points[-1].time:
            last_point = self.__points[-1]
            return last_point.position, last_point.heading

        for i in range(0, len(self.__points) - 1):
            if self.__points[i].time < time <= self.__points[i + 1].time:
                start, end, control = self.get_bezier(i)

                relative_time = inverse_lerp(start.time, end.time, time)

                position = Vector2(*bezier(start.position, end.position, control, relative_time))
                heading = lerp_angle(start.heading, end.heading, relative_time)

                return position, heading

        return None
