"""
Creates the view of the Samurai Cheems: Bonsai Bananza game
"""
# Library imports
from abc import ABC, abstractmethod
import math
import pygame
from pymunk import Vec2d
from sprite_sheet import SpriteSheet


class View(ABC):
    """
    Create an abstract class to hold view methods
    for Samurai Cheems: Bonsai Bonanza.

    Attributes:
        _board: An instance of the game model.
    """

    def __init__(self,board):
        """
        Initializes the View class
        """
        self._board=board

    @abstractmethod
    def clear_screen(self):
        """
        Clears the screen.
        return: None
        """

    @abstractmethod
    def draw_objects(self):
        """
        Creates an abstract method to draw objects
        """


class DefaultView(View):
    """
    The pymunk default view of representing objects.

    Attributes:
        _scaling_factor: A positive number used to alter the size of the final
        window.
        _screen: A temporary pygame surface to blit objects to before rescaling
        and updating the window.
        _window: The final scaled pygame surface to be shown on screen.
        _pip_image: A pygame surface containing the image for our pips.
        _background: A pygame surface containing the background image.
        _ball_images: A list of pygame surfaces each containing the image for
        a type of ball.
        _bonsai_images: A list of pygame surfaces each containing the image for
        a stage of bonsai tree growth.
    """

    def __init__(self, board):
        """
        Initializes the DefaultView class and the parent View class.
        """
        super().__init__(board)

        # Window Scaling
        scaling_factor = 1
        screen_size_x = 768
        screen_size_y = 672
        window_size_x = screen_size_x * scaling_factor
        window_size_y = screen_size_y * scaling_factor

        # Pygame
        self._screen = pygame.Surface((screen_size_x, screen_size_y))
        self._window = pygame.display.set_mode((window_size_x, window_size_y))

        # SpriteSheet setup
        ball_sprite_sheet = SpriteSheet("sprites/balls_sprite_sheet.png")
        pip_sprite_sheet = SpriteSheet("sprites/peg_sprite_sheet.png")
        bonsai_sprite_sheet = SpriteSheet\
            ("sprites/cherry_bonsai_sprite_sheet.png")

        # Single images
        self._pip_img = pip_sprite_sheet.image_at((8,0,8,8), -1)
        self._background = pygame.image.load("sprites/main_background.png")

        # Image lists
        self._ball_images = ball_sprite_sheet.load_strip((0,0,11,11), 3, -1)
        self._bonsai_images = bonsai_sprite_sheet.load_strip\
            ((0,0,264,336), 5, -1)

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

    def current_ball_image(self):
        """
        Gets the image for the current ball type.

        Returns:
            the pygame surface containing the image for the current ball.
        """
        return self._ball_images[self._board.current_ball_type]

    def draw_balls(self):
        """
        Draws all balls from _board to _screen.
        """
        for ball in self._board.balls:
            pos = ball.body.position
            #p = Vec2d(p.x, flipy(p.y))

            img = self.current_ball_image()
            ball_diam = ball.radius * 2

            rescaled_img = rescale(img, (ball_diam, ball_diam))
            # we need to rotate 180 degrees because of the y coordinate flip
            angle_degrees = math.degrees(-1*ball.body.angle)
            rotated_img = pygame.transform.rotate(rescaled_img, angle_degrees)

            pos = center_offset(rotated_img, pos)

            self._screen.blit(rotated_img, vec_to_tuple(pos))

    def draw_next_ball(self):
        """
        If there are no balls on screen, draw the next ball to be
        launched on _screen.
        """
        if len(self._board.balls) == 0:
            ball_daim = self._board.ball_radius * 2
            rescaled_img = rescale(self.current_ball_image(), \
                                        (ball_daim, ball_daim))
            position = Vec2d((240+768)/2, 20)
            position = center_offset(rescaled_img, position)
            self._screen.blit(rescaled_img, vec_to_tuple(position))

    def draw_pips(self):
        """
        Draws all pips from _board to _screen.
        """
        for pip in self._board.pips:
            offset = pip.offset

            img = self._pip_img
            ball_diam = pip.radius * 2
            rescaled_img = rescale(img, (ball_diam, ball_diam))

            offset = center_offset(rescaled_img, offset)
            #print(f"Pip pos: {p}")
            self._screen.blit(rescaled_img, vec_to_tuple(offset))

    def draw_static_lines(self):
        """
        Draws all lines from _board to _screen.
        """
        static_lines = self.get_static_lines()
        for line in static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            pos1 = round(pv1.x), round(pv1.y)
            pos2 = round(pv2.x), round(pv2.y)
            pygame.draw.lines(self._screen, pygame.Color("lightgray")\
                , False, [pos1, pos2], 2)

    def draw_bonsai(self):
        """
        Determines the stage of the game based on the score and blits the
        appropriate stage of the bonsai tree to _screen.
        """
        scores = self._board.get_scores()
        if 0 in scores:
            stage = 1
        elif 1 in scores:
            stage = 2
        else:
            stage = 3

        rescaled_img = rescale(self._bonsai_images[stage], (528, 672))
        self._screen.blit(rescaled_img, (240,0))

    def draw_pot(self):
        """
        Draws the front of the bonsai pot to _screen.
        """
        rescaled_img = rescale(self._bonsai_images[0], (528, 672))
        self._screen.blit(rescaled_img, (240,0))

    def draw_score(self):
        """
        Draws the score for each type of ball on _screen.
        """
        scores = self._board.get_scores()
        horz_offset = 103
        scoring_offset = 48
        for i in enumerate(scores):
            vert_offset = 151
            vert_offset = vert_offset + (scoring_offset * i[0])
            score = scores[i[0]]
            img = rescale(self._ball_images[i[0]], (36, 36))
            if score > 2:
                self._screen.blit(img, (horz_offset + (scoring_offset * 2)\
                    , vert_offset))
            if score > 1:
                self._screen.blit(img, (horz_offset + scoring_offset,\
                     vert_offset))
            if score > 0:
                self._screen.blit(img, (horz_offset, vert_offset))

    def clear_screen(self):
        """
        Clears the screen.
        return: None
        """
        background = rescale(self._background, (768, 672))
        self._screen.blit(background, (0,0))

    def draw_objects(self):
        """
        Draw all objects to pygame screen. Update window with screen.
        :return: None
        """
        self.draw_bonsai()
        self.draw_balls()

        # Called after draw_balls to make it look like balls are going into pot
        self.draw_pot()
        self.draw_pips()
        self.draw_next_ball()
        self.draw_score()
        #self.draw_static_lines()
        self._window.blit(rescale(self._screen, self._window.get_rect().size)\
            , (0, 0))
        pygame.display.update()

def center_offset(image, position):
    """
    Offest the position of an image so it is centered on the input position
    instead of being at the top left corner.

    Args:
        image: A pygame surface object.
        position: A Vec2d of the x and y position of the object.

    returns:
        A Vec2d of positions x and y modified to center the image to the
        input position.
    """
    offset = Vec2d(*image.get_size()) / 2
    return position - offset


def vec_to_tuple(vec):
    """
    Converts a Vec2d type into a tuple rounded to the nearest int for use
    in blitting.

     Args:
        vec: A Vec2d vector from pymunk.

    Returns:
        A Tuple of the rounded Vec2d values. Output format is (x, y).
    """
    return (round(vec.x), round(vec.y))


def rescale(image, dimensions):
    """
    rescales an image to the given dimensions.

     Args:
        image: A pygame surface object.
        dimensions: a tuple of the final width and height of the image.

    Returns:
        A pygame surface object of specified width and height.
    """
    return pygame.transform.scale(image, dimensions)
