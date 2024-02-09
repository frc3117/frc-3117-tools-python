try:
    from frctools.frcmath import clamp, angle_normalize, Vector2, repeat, bezier
    from frctools.controll import PathPlanning
    from frctools.visualization.widget.pygame import DragablePoint, Text
    from frctools.visualization.resources import ResourcesLoader

    import math
    import pygame


    class PixelUnitConverter:
        def __init__(self, img_resolution: tuple, img_size: tuple):
            if img_resolution[0] > img_resolution[1]:
                self.__pixel_to_unit_ratio = img_size[0] / img_resolution[0]
                self.__unit_to_pixel_ratio = img_resolution[0] / img_size[0]
            else:
                self.__pixel_to_unit_ratio = img_size[1] / img_resolution[1]
                self.__unit_to_pixel_ratio = img_resolution[1] / img_size[1]

        def to_pixel(self, unit: float):
            return unit * self.__unit_to_pixel_ratio

        def to_unit(self, pixel: float):
            return pixel * self.__pixel_to_unit_ratio

        def to_pixel_point(self, point: tuple):
            return int(point[0] * self.__unit_to_pixel_ratio), int(point[1] * self.__unit_to_pixel_ratio)

        def to_unit_point(self, point: tuple):
            return point[0] * self.__pixel_to_unit_ratio, point[1] * self.__pixel_to_unit_ratio


    class BezierSegment:
        def __init__(self, start: DragablePoint, end: DragablePoint, control: DragablePoint):
            self.start = start
            self.end = end
            self.control = control

        def get_point(self, t: float):
            x = (1 - t) ** 2 * self.start.x + 2 * (1 - t) * t * self.control.x + t ** 2 * self.end.x
            y = (1 - t) ** 2 * self.start.y + 2 * (1 - t) * t * self.control.y + t ** 2 * self.end.y

            return x, y

        def draw(self, screen):
            pygame.draw.line(screen, (0, 0, 0), self.start.tuple(), self.control.tuple())
            pygame.draw.line(screen, (0, 0, 0), self.control.tuple(), self.end.tuple())

            for i in range(0, 1000):
                t = i / 1000

                x, y = bezier(self.start.tuple(), self.end.tuple(), self.control.tuple(), t)
                #x, y = self.get_point(t)
                pygame.draw.circle(screen, (0, 100, 0, 100), (int(x), int(y)), 1)

    class Robot:
        def __init__(self, size, position=(0, 0), angle=0.0):
            self.size = size

            self.position = position
            self.angle = angle

        def set_position(self, position):
            self.position = position

        def set_angle(self, angle):
            self.angle = angle

        def rotate(self, angle):
            self.angle = angle_normalize(self.angle + angle)

        def draw(self, screen):
            x, y = self.position

            forward = (x, y - self.size[0] / 2)
            forward_x = (forward[0] - x) * math.cos(self.angle) - (forward[1] - y) * math.sin(self.angle) + x
            forward_y = (forward[0] - x) * math.sin(self.angle) + (forward[1] - y) * math.cos(self.angle) + y

            vertices = [
                (x + self.size[0] / 2, y + self.size[1] / 2),
                (x - self.size[0] / 2, y + self.size[1] / 2),
                (x - self.size[0] / 2, y - self.size[1] / 2),
                (x + self.size[0] / 2, y - self.size[1] / 2)
            ]

            for i in range(len(vertices)):
                x_rotated = (vertices[i][0] - x) * math.cos(self.angle) - (vertices[i][1] - y) * math.sin(self.angle) + x
                y_rotated = (vertices[i][0] - x) * math.sin(self.angle) + (vertices[i][1] - y) * math.cos(self.angle) + y
                vertices[i] = (x_rotated, y_rotated)

            pygame.draw.polygon(screen, (0, 0, 0), vertices, width=3)
            pygame.draw.line(screen, (0, 255, 0), (x, y), (forward_x, forward_y), width=3)


    class PathPlanningVisualization:
        def __init__(self, path_planning: PathPlanning, field_size, robot_size, max_resolution: tuple = (1500, 1500)):
            self.path_planning = path_planning

            self.__bg = pygame.image.load(ResourcesLoader.get_resource_path('TopViewField.png'))

            max_size = max(self.__bg.get_width(), self.__bg.get_height())
            width_ratio = self.__bg.get_width() / max_size
            height_ratio = self.__bg.get_height() / max_size

            self.__bg = pygame.transform.scale(self.__bg, (int(width_ratio * max_resolution[0]), int(height_ratio * max_resolution[1])))

            self.__field_unit_converter = PixelUnitConverter((self.__bg.get_width(), self.__bg.get_height()), field_size)

            self.screen = pygame.display.set_mode((self.__bg.get_width(), self.__bg.get_height()))
            self.clock = pygame.time.Clock()

            self.__generate__()

            self.running = False

            pygame.font.init()
            self.__mouse_pos_text = Text()

            self.robot = Robot(self.__field_unit_converter.to_pixel_point(robot_size))

        def __generate__(self):
            self.points = {}
            self.control_points = []

            self.segments = []

            for i in range(self.path_planning.get_points_count()):
                path_planning_point = self.path_planning.get_point(i)
                dragable_point = DragablePoint(*self.__field_unit_converter.to_pixel_point(path_planning_point.position.to_tuple()))

                self.points[path_planning_point] = dragable_point

            for bezier in self.path_planning.get_all_bezier():
                start_point, end_point, control_vector = bezier

                start = self.points[start_point]
                end = self.points[end_point]

                control = DragablePoint(*self.__field_unit_converter.to_pixel_point(bezier[2].to_tuple()))
                self.control_points.append(control)

                self.segments.append(BezierSegment(start, end, control))

        def run(self):
            self.running = True
            while True:
                events = {}
                for event in pygame.event.get():
                    events[event.type] = event

                if pygame.QUIT in events:
                    self.running = False
                    break

                self.screen.fill((255, 255, 255))
                self.screen.blit(self.__bg, (0, 0))

                mouse_button_down = events.get(pygame.MOUSEBUTTONDOWN, None)
                mouse_button_up = events.get(pygame.MOUSEBUTTONUP, None)
                mouse_motion = events.get(pygame.MOUSEMOTION, None)

                selected = None
                for point in self.points:
                    dragable_point = self.points[point]

                    dragable_point.update(self.screen, mouse_button_down, mouse_button_up, mouse_motion)
                    dragable_point.draw(self.screen)

                    point.position = Vector2(*self.__field_unit_converter.to_unit_point(dragable_point.tuple()))

                    if dragable_point.dragging:
                        selected = point

                for i, control in enumerate(self.control_points):
                    control.update(self.screen, mouse_button_down, mouse_button_up, mouse_motion)
                    control.draw(self.screen)

                    self.path_planning.set_beizer_control_point(i, Vector2(*self.__field_unit_converter.to_unit_point(control.tuple())))

                for segment in self.segments:
                    segment.draw(self.screen)
                    if selected == segment.control:
                        selected = None

                if selected is not None:
                    mouse_scroll = events.get(pygame.MOUSEWHEEL)
                    if mouse_scroll:
                        selected.heading = angle_normalize(selected.heading + mouse_scroll.y * 0.15)
                        self.robot.rotate(mouse_scroll.y * -0.15)

                    self.robot.set_angle(selected.heading)
                    self.robot.set_position(self.__field_unit_converter.to_pixel_point(selected.position.to_tuple()))
                else:
                    time = repeat(pygame.time.get_ticks() / 1000, self.path_planning.get_time())
                    position, heading = self.path_planning.get_state_at(time)

                    self.robot.set_angle(heading)
                    self.robot.set_position(self.__field_unit_converter.to_pixel_point(position.to_tuple()))

                self.robot.draw(self.screen)

                mouse_unit_x, mouse_unit_y = self.__field_unit_converter.to_unit_point(pygame.mouse.get_pos())
                self.__mouse_pos_text.draw(self.screen,
                                           text=f'Mouse Position: X={mouse_unit_x:.2f} Y={mouse_unit_y:.2f}',
                                           position=(10, 10),
                                           color=(255, 255, 255))

                pygame.display.flip()
                self.clock.tick(60)

            pygame.quit()

except ImportError as e:
    class DragablePoint:
        def __init__(self):
            raise ImportError('Pygame is not installed')

    class BezierSegment:
        def __init__(self):
            raise ImportError('Pygame is not installed')

    class PathPlanningVisualization:
        def __init__(self):
            raise ImportError('Pygame is not installed')
