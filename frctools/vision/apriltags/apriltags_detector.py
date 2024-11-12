from threading import Thread
from typing import Tuple, Callable, List

import json


try:
    from picamera2 import Picamera2
    from ..mjpegstreamer import MjpegStreamer


    import cv2 as cv
    import numpy as np
    import pupil_apriltags as april_tags


    def __draw_frustum__(img, translation, rotation, camera_params, tag_size, outline_color):
        camera_params = np.array(camera_params)
        dist_coeffs = np.zeros((4, 1))

        # 3D points of the bottom of the frustum
        bottom = np.array([
            [-tag_size / 2, tag_size / 2, 0],
            [tag_size / 2, tag_size / 2, 0],
            [tag_size / 2, -tag_size / 2, 0],
            [-tag_size / 2, -tag_size / 2, 0]
        ], dtype=np.float32)

        # 3D points of the top of the frustum
        top = np.array([
            [-tag_size / 2, tag_size / 2, -tag_size],
            [tag_size / 2, tag_size / 2, -tag_size],
            [tag_size / 2, -tag_size / 2, -tag_size],
            [-tag_size / 2, -tag_size / 2, -tag_size]
        ], dtype=np.float32)

        rotation = np.array(rotation)
        translation = np.array(translation)

        image_points_bottom, _ = cv.projectPoints(bottom, rotation, translation, camera_params, dist_coeffs)
        image_points_top, _ = cv.projectPoints(top, rotation, translation, camera_params, dist_coeffs)

        top_corner_points = []

        # Draw pillars from bottom points to top points
        for i in range(4):
            x1, y1 = image_points_bottom[i][0]
            x2, y2 = image_points_top[i][0]

            top_corner_points.append((x2, y2))

            cv.line(img, (int(x1), int(y1)), (int(x2), int(y2)), outline_color, 2)

        # Create a polyline for the top corners
        top_corners_temp = np.array(top_corner_points, dtype=np.int32)
        return cv.polylines(img, [top_corners_temp], isClosed=True, color=outline_color, thickness=2)


    class AprilTagsDetector:
        def __init__(self,
                     cam_num: int = 0,
                     resolution: Tuple[int, int] = (1456, 1088),
                     fps: int = 30, is_gray: bool = True,
                     calibration_file: str = 'calibration.json',
                     mjpeg_streamer: MjpegStreamer = None,
                     mjpeg_stream_prefix: str = 'apriltags',
                     tag_families: str = 'tag36h11',
                     tag_size: float = 0.165,
                     frame_callback: Callable[[List[april_tags.Detection]], None] = None):
            self.__cam_num = cam_num
            self.__resolution = resolution
            self.__fps = fps
            self.__is_gray = is_gray
            self.__calibration_file = calibration_file
            self.__tag_families = tag_families
            self.__tag_size = tag_size
            self.__frame_callback = frame_callback

            self.__is_running = False
            self.__should_run = False
            self.__thread = None

            if mjpeg_streamer is not None:
                self.__raw_stream = mjpeg_streamer.create_stream(f'{mjpeg_stream_prefix}/raw', fps, resolution)
                self.__detection_stream = mjpeg_streamer.create_stream(f'{mjpeg_stream_prefix}/detection', fps, resolution)
            else:
                self.__raw_stream = None
                self.__detection_stream = None

        def start(self):
            if self.__is_running:
                return

            self.__thread = Thread(target=self.__target__, daemon=False)
            self.__thread.start()

        def stop(self):
            if not self.__is_running:
                return

            self.__should_run = False

        def __target__(self):
            self.__should_run = True
            self.__is_running = True

            try:
                # Load camera calibration
                with open(self.__calibration_file, 'r') as f:
                    camera_calibration = json.load(f)

                    # Load distortion coeficients
                    dist_json = camera_calibration['distortion']

                    dist = np.array([
                        dist_json['k1'],
                        dist_json['k2'],
                        dist_json['p1'],
                        dist_json['p2'],
                        dist_json['k3']
                    ], dtype=np.float32)

                    # Load camera matrix
                    mtx_json = camera_calibration['matrix']

                    #   April Tags format
                    april_tags_camera_params = (
                        mtx_json['fx'],
                        mtx_json['fy'],
                        mtx_json['cx'],
                        mtx_json['cy']
                    )
                    #   OpenCV format
                    camera_matrix = np.array([
                        [mtx_json['fx'], 0, mtx_json['cx']],
                        [0, mtx_json['fy'], mtx_json['cy']],
                        [0, 0, 1]
                    ], dtype=np.float32)

                # Initialize the camera
                cap = Picamera2(self.__cam_num)
                video_config = cap.create_video_configuration({'size': self.__resolution, 'format': 'RGB888'})
                cap.configure(video_config)
                cap.set_controls({"FrameRate": self.__fps})

                cap.start()

                # Initialize the April Tags detector
                apri_tags_detector = april_tags.Detector(families=self.__tag_families)

                while self.__should_run:
                    # Read img from camera
                    img = cap.capture_array()
                    detection_img = img.copy()

                    # Convert img to grayscale
                    if self.__is_gray:
                        gray_img = img[..., 2]
                    else:
                        gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

                    # Detect tags
                    detection_list = apri_tags_detector.detect(gray_img, estimate_tag_pose=True,
                                                               camera_params=april_tags_camera_params,
                                                               tag_size=self.__tag_size)

                    if self.__frame_callback:
                        self.__frame_callback(detection_list)

                    # Only draw tags on the image if anyone is looking at the stream
                    if self.__detection_stream is not None and self.__detection_stream.has_demand():
                        tags_outline = []
                        tags_center = []
                        for detection in detection_list:
                            # Get vertices for the outline of the tag
                            points = np.array([[int(corners[0]), int(corners[1])] for corners in detection.corners],
                                              np.int32)
                            points = points.reshape((-1, 1, 2))
                            tags_outline.append(points)

                            # Get center point of the tag
                            center = np.array([[int(detection.center[0]), int(detection.center[1])]], np.int32)
                            center = center.reshape((-1, 1, 2))
                            tags_center.append(center)

                            # Get the pose of the tag
                            position = (detection.pose_t[0][0], detection.pose_t[1][0], detection.pose_t[2][0])
                            rotation = detection.pose_R

                            # Draw the bounding box of the tag
                            detection_img = __draw_frustum__(img, position, rotation, camera_matrix, self.__tag_size,
                                                             (0, 255, 0))

                        # Draw outline of tags
                        detection_img = cv.polylines(detection_img, tags_outline, True, (0, 255, 0), 3)
                        # Draw center of tags
                        detection_img = cv.polylines(detection_img, tags_center, True, (0, 0, 255), 5)

                    # Set the frame for the MJPEG stream
                    if self.__raw_stream is not None:
                        self.__raw_stream.set_frame(img)
                    if self.__detection_stream is not None:
                        self.__detection_stream.set_frame(detection_img)
            except Exception as e:
                print(e)

            cap.stop()

            self.__should_run = False
            self.__is_running = False

        def join(self):
            if self.__is_running:
                self.__thread.join()
except ImportError:
    class AprilTagsDetector:
        def __init__(self, *args, **kwargs):
            raise ImportError('picamera2, mjpeg_streamer, cv2, numpy, pupil_apriltags are not installed')
