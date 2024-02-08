import sys


def start_path_planning():
    from frctools.frcmath import Vector2
    from frctools.controll.path_planning import PathPlanning, PathPlanningPoint
    from frctools.visualization.path_planning import PathPlanningVisualization

    planning = PathPlanning()
    planning.add_point(PathPlanningPoint(Vector2(5, 5), 0, 0))
    planning.add_point(PathPlanningPoint(Vector2(10, 5), 0, 5))
    planning.add_point(PathPlanningPoint(Vector2(15, 7), 0, 10))

    PathPlanningVisualization(planning, (17.960, 9.144), (0.686, 0.813)).run()


def start_cam_calibration():
    from frctools.visualization import CameraCalibratorVisualization

    calibrator = CameraCalibratorVisualization()
    calibrator.run()


ENTRYPOINTS = {
    'pathplanning': start_path_planning,
    'camcalibration': start_cam_calibration
}


if __name__ == '__main__':
    mode = sys.argv[1]

    if mode not in ENTRYPOINTS:
        print(f'Invalid mode: {mode}')
        sys.exit(1)

    ENTRYPOINTS[mode]()
