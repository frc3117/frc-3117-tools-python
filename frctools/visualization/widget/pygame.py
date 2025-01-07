try:
    from frctools.frcmath import clamp, Vector2

    import pygame


    class DragablePoint:
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

            self.dragging = False

        def draw(self, screen):
            if self.dragging:
                pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 5)
            else:
                pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 5)

        def update(self, screen, mouse_button_down, mouse_button_up, mouse_motion):
            if mouse_button_down:
                if mouse_button_down.button == 1:
                    event_pos_x, event_pos_y = mouse_button_down.pos
                    if (event_pos_x - self.x) ** 2 + (event_pos_y - self.y) ** 2 <= 25:
                        self.dragging = True
            elif mouse_button_up:
                if mouse_button_up.button == 1:
                    self.dragging = False

            if mouse_motion:
                if self.dragging:
                    event_pos_x, event_pos_y = mouse_motion.pos
                    self.x = clamp(event_pos_x, 5, screen.get_width() - 5)
                    self.y = clamp(event_pos_y, 5, screen.get_height() - 5)

            return self.x, self.y

        def tuple(self):
            return self.x, self.y


    class Text:
        def __init__(self, font: str = 'Arial', size: int = 20):
            self.font: pygame.font.SysFont = pygame.font.SysFont(font, size)

        def draw(self, screen, text, position, color=(0, 0, 0)):
            text_surface = self.font.render(text, True, color)
            screen.blit(text_surface, position)
except ImportError:
    class DragablePoint:
        def __init__(self, *args, **kwargs):
            raise ImportError("pygame is not installed")

    class Text:
        def __init__(self, *args, **kwargs):
            raise ImportError("pygame is not installed")
