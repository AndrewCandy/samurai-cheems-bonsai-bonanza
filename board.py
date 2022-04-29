# Python imports
import random
from typing import List

# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d


class Board(object):

    def __init__(self):

        self.level_num = 1
        self.level_state = 1
        self.pot_lines = []
        self.tree_lines = []
        self.pips = []
        self.pot_x_1 = 0
        self.pot_x_2 = 0

        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((600, 600))
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Balls that exist in the world
        self._balls: List[pymunk.Circle] = []

        # Execution control and time until the next ball spawns
        #self._running = True

        self.score = 0  

    def draw_background(self):
        static_body = self._space.static_body
        wall_lines = [
            pymunk.Segment(static_body, (0, 0), (0, 600), 0.0),
            pymunk.Segment(static_body, (600, 0), (600, 600), 0.0),
            pymunk.Segment(static_body, (0, 0), (600, 0), 0.0)
        ]
        for line in wall_lines:
            line.elasticity = 0.5
            line.friction = 0.9
        self._space.add(*wall_lines)

    def draw_level(self,level_num, level_state):
        self.empty_level()
        static_body = self._space.static_body
        pip_radius=5

        pips_1_1 = []
        for row in range(6):
            for col in range(10):
                pips_1_1.append(pymunk.Circle(static_body,pip_radius,(col*70+35*(row % 2),row*70+100)))
        
        pot_lines_1_1 = [
            pymunk.Segment(static_body, (200, 600 - 10), (400, 600 - 10), 0.0),
            pymunk.Segment(static_body, (200.0, 600 - 10), (150.0, 600 - 60), 0.0),
            pymunk.Segment(static_body, (400.0, 600 - 10), (450.0, 600 - 60), 0.0),
        ]
        tree_lines_1_1 = []

        pips_1_2 = []
        for row in range(4):
            for col in range(10):
                pips_1_2.append(pymunk.Circle(static_body,pip_radius,(col*70+35*(row % 2),row*120+100)))

        if level_num == 1:
            if level_state == 1:
                self.pips = pips_1_1
                self.tree_lines = tree_lines_1_1
                self.pot_lines = pot_lines_1_1
                self.pot_x_1 = 200
                self.pot_x_2 = 400
            if level_state == 2:
                self.pips = pips_1_2
                self.tree_lines = tree_lines_1_1
                self.pot_lines = pot_lines_1_1
                self.pot_x_1 = 200
                self.pot_x_2 = 400


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
        self._space.add(*self.pot_lines)

    def empty_level(self):
        self._space.remove(*self.pips)
        self.pips = []
        
        self._space.remove(*self.tree_lines)
        self.tree_lines = []
        
        self._space.remove(*self.pot_lines)
        self.pot_lines = []
    
    def check_if_scored(self):
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
        # Remove balls that fall into bonsai pot and increase score
        balls_to_remove = [ball for ball in self._balls if ball.body.position.y > 550 and self.pot_x_1 < ball.body.position.x < self.pot_x_2]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self._balls.remove(ball)
            self.score += 1

        # Remove balls that fall out of bounds
        balls_to_remove = [ball for ball in self._balls if ball.body.position.y > 590]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self._balls.remove(ball)