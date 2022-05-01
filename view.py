"""
Creates the view of the Samurai Cheems: Bonsai Bananza game
"""
# Library imports
from abc import ABC, abstractmethod
import math
import pygame
import pymunk.pygame_util
from pymunk import Vec2d

def flipy(y):
    return y

class View(ABC):
    """
    Create an abstract class to hold view methods
    for Samurai Cheems: Bonsai Bonanza.
    """
    # Define your methods here.

    def __init__(self,board):
        """
        Initializes the View class
        """
        self._board=board
        #self._board._draw_options = pymunk.pygame_util.DrawOptions(self._board._screen)

        # Window Scaling
        self._scaling_factor = 1
        self._screen_size = 600
        self._window_size = self._screen_size * self._scaling_factor

        # pygame
        self._screen = pygame.Surface((self._screen_size, self._screen_size))
        self._window = pygame.display.set_mode((self._window_size, self._window_size))

        self._ball_img = pygame.image.load("test.png")
        self._pip_img = pygame.image.load("test.png")

    def clear_screen(self):
        """
        Clears the screen.
        return: None
        """
        self._screen.fill(pygame.Color("white"))

    @abstractmethod
    def draw_objects(self):
        """
        Creates an abstract method to draw objects
        """


class DefaultView(View):
    """
    The pymunk default view of representing objects.

    Attributes:
        None
    """

    def get_static_lines(self):
        static_lines = []
        static_lines.extend(self._board.pot_lines)
        static_lines.extend(self._board.tree_lines)
        static_lines.extend(self._board.wall_lines)
        return static_lines

    def draw_objects(self):
        """
        Draw the objects in default view.
        :return: None
        """
        for ball in self._board.balls:
            # image draw
            p = ball.body.position
            p = Vec2d(p.x, flipy(p.y))

            # we need to rotate 180 degrees because of the y coordinate flip
            angle_degrees = math.degrees(ball.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self._ball_img, angle_degrees)

            offset = Vec2d(*rotated_logo_img.get_size()) / 2
            p = p - offset

            self._screen.blit(rotated_logo_img, (round(p.x), round(p.y)))

        for pip in self._board.pips:
            p = pip.offset
            p = Vec2d(p[0], flipy(p[1]))

            offset = Vec2d(*self._pip_img.get_size()) / 2
            p = p - offset
            #print(f"Pip pos: {p}")
            self._screen.blit(self._pip_img, (round(p.x), round(p.y)))

        static_lines = self.get_static_lines()
        for line in static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = round(pv1.x), round(flipy(pv1.y))
            p2 = round(pv2.x), round(flipy(pv2.y))
            pygame.draw.lines(self._screen, pygame.Color("lightgray"), False, [p1, p2], 2)

        self._window.blit(pygame.transform.scale(self._screen, self._window.get_rect().size), (0, 0))
        pygame.display.update()
