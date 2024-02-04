from frctools.frcmath import Vector3, Quaternion
from .camera import CameraThread
from typing import List


class AprilTag:
    def __init__(self, id: int, size: float, position: Vector3, rotation: Quaternion):
        self.__id = id
        self.__size = size
        self.__position = position
        self.__rotation = rotation

    @property
    def id(self):
        return self.__id

    @property
    def size(self):
        return self.__size

    @property
    def position(self):
        return self.__position

    @property
    def rotation(self):
        return self.rotation


CRESCENDO_2024_APRIL_TAGS = {
    1: AprilTag(1, 165.1, Vector3(15.079472, 0.245872, 1.355852), Quaternion(0., 0., 0.8660254037844386, 0.5)),
    2: AprilTag(2, 165.1, Vector3(16.185134, 0.883666, 1.355852), Quaternion(0., 0., 0.8660254037844386, 0.5)),
    3: AprilTag(3, 165.1, Vector3(16.579342, 4.982718, 1.451102), Quaternion(0., 0., 1., 0.)),
    4: AprilTag(4, 165.1, Vector3(16.579342, 5.547868, 1.451102), Quaternion(0., 0., 1., 0.)),
    5: AprilTag(5, 165.1, Vector3(14.700758, 8.2042, 1.355852), Quaternion(0., 0., 0.7071067811865476, -0.7071067811865475)),
    6: AprilTag(6, 165.1, Vector3(1.8415, 8.2042, 1.355852), Quaternion(0., 0., 0.7071067811865476, -0.7071067811865475)),
    7: AprilTag(7, 165.1, Vector3(-0.0381, 5.547868, 1.451102), Quaternion(0., 0., 0., 1.)),
    8: AprilTag(8, 165.1, Vector3(-0.0381, 4.982718, 1.451102), Quaternion(0., 0., 0., 1.)),
    9: AprilTag(9, 165.1, Vector3(0.356108, 0.883666, 1.355852), Quaternion(0., 0., 0.5, 0.8660254037844387)),
    10: AprilTag(10, 165.1, Vector3(1.461516, 0.245872, 1.355852), Quaternion(0., 0., 0.5, 0.8660254037844387)),
    11: AprilTag(11, 165.1, Vector3(11.904726, 3.713226, 1.3208), Quaternion(0., 0., 0.5, -0.8660254037844387)),
    12: AprilTag(12, 165.1, Vector3(11.904726, 4.49834, 1.3208), Quaternion(0., 0., 0.5, 0.8660254037844387)),
    13: AprilTag(13, 165.1, Vector3(11.220196, 4.105148, 1.3208), Quaternion(0., 0., 1., 0.)),
    14: AprilTag(14, 165.1, Vector3(5.320792, 4.105148, 1.3208), Quaternion(0., 0., 0., 1.)),
    15: AprilTag(15, 165.1, Vector3(4.641342, 4.49834, 1.3208), Quaternion(0., 0., 0.8660254037844386, 0.5)),
    16: AprilTag(16, 165.1, Vector3(4.641342, 3.713226, 1.3208), Quaternion(0., 0., 0.8660254037844386, -0.5)),
}

try:
    import cv2 as cv
    import numpy as np
    import pupil_apriltags as apriltag

    class AprilTagCamera:
        def __init__(self, tag_size: float, focal_length: float, camera_matrix: np.ndarray):
            self.__detector = apriltag.Detector(families='tag36h11')

            self.__tag_size = tag_size
            self.__focal_length = focal_length
            self.__camera_matrix = camera_matrix

        def look_for_tags(self, frame) -> List[apriltag.Detection]:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            results = self.__detector.detect(gray)

            return results

        @staticmethod
        def draw_tags(frame, tags: List[apriltag.Detection]):
            out_img = frame.copy()
            for tag in tags:
                cv.polylines(out_img, [np.array(tag.corners, np.int32)], True, (0, 255, 0), 2)
                cv.putText(out_img, str(tag.tag_id), (int(tag.corners[0][0]), int(tag.corners[0][1])), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)

            return out_img



except ImportError:
    class AprilTagCamera:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("OpenCV, Numpy, Apriltags3 need to be installed installed.")
