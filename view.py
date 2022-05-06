"""
Creates the view of the Samurai Cheems: Bonsai Bananza game
"""
# Library imports
from abc import ABC, abstractmethod
import math
import pygame
from sprite_sheet import SpriteSheet
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
        self._screen_size_x = 768
        self._screen_size_y = 672
        self._window_size_x = self._screen_size_x * self._scaling_factor
        self._window_size_y = self._screen_size_y * self._scaling_factor

        # pygame
        self._screen = pygame.Surface((self._screen_size_x, self._screen_size_y))
        self._window = pygame.display.set_mode((self._window_size_x, self._window_size_y))

        #sprite setup
        self._ball_sprite_sheet = SpriteSheet("sprites/balls_sprite_sheet.png")
        self._pip_sprite_sheet = SpriteSheet("sprites/peg_sprite_sheet.png")
        self._bonsai_sprite_sheet = SpriteSheet("sprites/cherry_bonsai_sprite_sheet.png")

        self._ball_images = self._ball_sprite_sheet.load_strip((0,0,9,9), 3, -1)
        self._pip_img = self._pip_sprite_sheet.image_at((8,0,8,8), -1)
        self._bonsai_images = self._bonsai_sprite_sheet.load_strip((0,0,264,336), 4, -1)

        self._background = pygame.image.load("sprites/temp_background.png")

    def clear_screen(self):
        """
        Clears the screen.
        return: None
        """
        background = pygame.transform.scale(self._background, (self._screen_size_x, self._screen_size_y))
        self._screen.blit(background, (0,0))

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
        """
        Combines all lines from _board into one list.

        Returns:
            A list of static line objects from _board.
        """
        static_lines = []
        static_lines.extend(self._board.pot_lines)
        static_lines.extend(self._board.tree_lines)
        static_lines.extend(self._board.wall_lines)
        return static_lines

    def draw_balls(self):
        """
        Draws all balls from _board to _screen.
        """
        for ball in self._board.balls:
            p = ball.body.position
            p = Vec2d(p.x, flipy(p.y))

            img = self._ball_images[self._board.current_ball_type]
            ball_diam = ball.radius * 2

            rescaled_img = pygame.transform.scale(img, (ball_diam, ball_diam))
            # we need to rotate 180 degrees because of the y coordinate flip
            angle_degrees = math.degrees(ball.body.angle)
            rotated_img = pygame.transform.rotate(rescaled_img, angle_degrees)

            offset = Vec2d(*rotated_img.get_size()) / 2
            p = p - offset

            self._screen.blit(rotated_img, (round(p.x), round(p.y)))

    def draw_pips(self):
        """
        Draws all pips from _board to _screen.
        """
        for pip in self._board.pips:
            p = pip.offset
            p = Vec2d(p[0], flipy(p[1]))

            img = self._pip_img
            ball_diam = pip.radius * 2
            rescaled_img = pygame.transform.scale(img, (ball_diam, ball_diam))


            offset = Vec2d(*rescaled_img.get_size()) / 2
            p = p - offset
            #print(f"Pip pos: {p}")
            self._screen.blit(rescaled_img, (round(p.x), round(p.y)))

    def draw_static_lines(self):
        """
        Draws all lines from _board to _screen.
        """
        static_lines = self.get_static_lines()
        for line in static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = round(pv1.x), round(flipy(pv1.y))
            p2 = round(pv2.x), round(flipy(pv2.y))
            pygame.draw.lines(self._screen, pygame.Color("lightgray"), False, [p1, p2], 2)

    def draw_bonsai(self):
        """
        
        """
        scores = self._board.get_scores()
        if 0 in scores:
            stage = 1
        elif 1 in scores:
            stage = 2
        else:
            stage = 3
        
        rescaled_img = pygame.transform.scale(self._bonsai_images[stage], (528, 672))
        self._screen.blit(rescaled_img, (240,0))

    def draw_pot(self):
        """
        """
        rescaled_img = pygame.transform.scale(self._bonsai_images[0], (528, 672))
        self._screen.blit(rescaled_img, (240,0))

    def draw_objects(self):
        """
        Draw all objects to pygame screen. Update window with screen.
        :return: None
        """
        self.draw_bonsai()
        self.draw_balls()
        self.draw_pot()
        self.draw_pips()
        self.draw_static_lines()
        self._window.blit(pygame.transform.scale(self._screen, self._window.get_rect().size), (0, 0))
        pygame.display.update()
