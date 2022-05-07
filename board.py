"""
Creates the model behind the Samurai Cheems: Bonsai Bananza game
"""

# Python imports
from typing import List

# Library imports
import pygame
import sound

# pymunk imports
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
from levels import LevelSetup


class Board():
    """
    Create a class to represent the game board
    for Samurai Cheems: Bonsai Bonanza.
    """

    def __init__(self):
        self.pot_lines = []
        self.tree_lines = []
        self.wall_lines = []
        self.pips = []
        self.pot_x_1 = 0
        self.pot_x_2 = 0

        self.setup = LevelSetup()

        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)

        # Physics
        # Time step
        self.dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self.physics_steps_per_frame = 1

        # pygame
        pygame.init()
        #self._screen = pygame.display.set_mode((600, 600))
        self._clock = pygame.time.Clock()

        # Balls that exist in the world
        self.balls = []

        # Ball types:
        self.ball_radius = 9
        # 0 = water, 1 = earth, 2 = sun
        self.current_ball_type = 0

        self._scores = [0,0,0]

    def draw_background(self):
        """
        Creates the walls around the game board
        """
        # Makes the physics body static
        static_body = self._space.static_body
        # Creates the locations of the wall lines
        self.wall_lines = [
            # Left Line
            pymunk.Segment(static_body, (240, 0), (240, 768), 0.0),
            pymunk.Segment(static_body, (768, 0), (768, 768), 0.0),
            pymunk.Segment(static_body, (240, 0), (768, 0), 0.0)
        ]
        # Adds physics parameters for the lines
        for line in self.wall_lines:
            line.elasticity = 0.5
            line.friction = 0.9
        # Adds the wall lines to the space.
        self._space.add(*self.wall_lines)

    def draw_level(self, level_num, level_state):
        """
        Creates the pegs, pot, and tree for each level and stage
        """
        # Clears the previous level
        self.empty_level()
        # Sets the physics type for the level objects
        static_body = self._space.static_body

        pip_radius = 8

        level_layout = self.setup.load_level(level_num, level_state)

        pip_layout = level_layout[0]
        for pip in pip_layout:
            self.pips.append(pymunk.Circle(static_body, pip_radius,
                                           pip))

        tree_layout = level_layout[1]
        for line in tree_layout:
            self.tree_lines.append(pymunk.Segment(
                static_body, line[0], line[1], 0.0))

        pot_layout = level_layout[2]
        for line in pot_layout:
            self.pot_lines.append(pymunk.Segment(
                static_body, line[0], line[1], 0.0))

        # Adds the physics for each object and
        # adds the object to the physics space
        for pip in self.pips:
            pip.elasticity = 0.95
            pip.friction = 0.9
        self._space.add(*self.pips)
        for line in self.tree_lines:
            line.elasticity = 0.5
            line.friction = 0.9
        self._space.add(*self.tree_lines)
        for line in self.pot_lines:
            line.elasticity = 0.5
            line.friction = 0.9
        self.pot_lines[0].collision_type = 2
        self._space.add(*self.pot_lines)

    def empty_level(self):
        """
        Clears the level of any previous pegs, pot lines, or tree lines
        """
        # Remove pips
        self._space.remove(*self.pips)
        self.pips = []

        # Remove the bonsai sprout
        self._space.remove(*self.tree_lines)
        self.tree_lines = []

        # Remove the pot
        self._space.remove(*self.pot_lines)
        self.pot_lines = []

    def next_ball(self):
        """
        
        """
        next_ball = self.current_ball_type + 1
        if next_ball > 2:
            next_ball = 0
        return next_ball

    def get_scores(self):
        """
        """
        return self._scores

    def check_if_scored(self):
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
        # Remove balls that fall into bonsai pot and increase score

        score_collision = self._space.add_collision_handler(1, 2)
        if len(self.balls) > 0:
            ball = self.balls[0]
            score_collision.begin = self.scores
            

        # Remove balls that fall out of bounds
        balls_to_remove = [
            ball for ball in self.balls if ball.body.position.y > 672-10]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self.balls.remove(ball)
            self.current_ball_type = self.next_ball()

    def scores(self, arbiter, space, data):
        self._space.remove(*self.balls)
        self.balls = []
        self._scores[self.current_ball_type] += 1
        self.current_ball_type = self.next_ball()
        sound.play_score()
        return True
