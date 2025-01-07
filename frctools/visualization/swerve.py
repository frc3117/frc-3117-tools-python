try:
    from ntcore import NetworkTable, NetworkTableInstance
    from frctools.frcmath import Vector2
    from typing import List

    import pygame


    class SwerveModuleData:
        def __init__(self, index: int, position: Vector2, nt: NetworkTableInstance):
            base_key = f'/SmartDashboard/SwerveDrive/{index}'

            self.steering_entry = nt.getEntry(f'{base_key}/SteerAngle')
            self.steering_target_entry = nt.getDoubleTopic(f'{base_key}/SteerTargetAngle').subscribe(0.)
            self.drive_entry = nt.getEntry(f'{base_key}/DriveSpeed')

            self.position = position

        def draw(self, screen):
            vertices = [
                Vector2(30, 14),
                Vector2(30, -14),
                Vector2(-30, -14),
                Vector2(-30, 14)
            ]

            angle = self.steering_entry.getDouble(0.)
            velocity = self.drive_entry.getDouble(0.)

            vertices = [(v.rotate(angle) + self.position).to_tuple() for v in vertices]
            pygame.draw.polygon(screen, (0, 0, 0), vertices, 4)

            velocity_vec = Vector2(50, 0).rotate(angle) * velocity + self.position
            pygame.draw.line(screen, (0, 255, 0), self.position.to_tuple(), velocity_vec.to_tuple(), 4)

            forward_dot = (Vector2(20, 0).rotate(angle) + self.position).to_tuple()
            pygame.draw.circle(screen, (255, 0, 0), forward_dot, 4)


    class SwerveDriveData:
        def __init__(self, position):
            self.position = position


    class SwerveVisualization:
        def __init__(self, wheel_positions: List[Vector2]):
            self.nt = NetworkTableInstance.getDefault()
            self.nt.setServerTeam(3117)
            self.nt.startClient4('SwerveVisualizer')

            self.screen = pygame.display.set_mode((800, 800))
            self.clock = pygame.time.Clock()

            max_magn = max([v.magnitude for v in wheel_positions])

            center = Vector2(400, 400)
            wheel_positions = [(v / max_magn * 300.) + center for v in wheel_positions]

            self.swerves: List[SwerveModuleData] = []
            for i in range(4):
                self.swerves.append(SwerveModuleData(i, wheel_positions[i], self.nt))

            self.running = False

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

                for module in self.swerves:
                    module.draw(self.screen)

                pygame.display.flip()
                self.clock.tick(60)

            pygame.quit()
except ImportError:
    class SwerveModuleData:
        def __init__(self, *args, **kwargs):
            raise ImportError("pygame is not installed")


    class SwerveDriveData:
        def __init__(self, *args, **kwargs):
            raise ImportError("pygame is not installed")


    class SwerveVisualization:
        def __init__(self, *args, **kwargs):
            raise ImportError("pygame is not installed")