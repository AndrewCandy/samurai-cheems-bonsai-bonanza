"""
Creates the model behind the Samurai Cheems: Bonsai Bananza game
"""

# Library imports
import pygame
import sound

# pymunk imports
import pymunk
from levels import LevelSetup


class Board():
    """
    Create a class to represent the game board
    for Samurai Cheems: Bonsai Bonanza.

    Public Attributes:
        pot_lines: A list of all pymunk line objects that make up the bonsai
        pot.
        tree_lines: A list of all pymunk line objects that make up the bonsai
        tree leaf walls currently in the physics space.
        wall_lines: A list of all pymunk line objects that make up the border
        of the physics space.
        pips: A list of pymunk static circle objects for all pegs currently in
        the physics space.
        setup: An instance of the LevelSetup class that contains position
        information for game elements in each level and stage.
        ball_radius: An int representing the radius of the ball.
        balls: A list containing all dynamic circle objects currently in the
        physics space.
        current_ball_type: An int representing which type of ball is currently
        in use for scoring purposes.

    Private Attributes:
        _space: The 2d pymunk physics environment where all our physics objects
        exist and our simulation occurs.
        _scores: The total score of each ball type. Saved as a list of three
        integers.


    """

    def __init__(self):
        self.pot_lines = []
        self.tree_lines = []
        self.wall_lines = []
        self.pips = []

        self.setup = LevelSetup()

        # Space
        self._space = pymunk.Space()
        # Set gravity in space
        self._space.gravity = (0.0, 900.0)

        # pygame
        pygame.init()

        # Ball info
        self.ball_radius = 11

        # Balls that exist in the world
        self.balls = []

        # Ball type:
        # 0 = water, 1 = earth, 2 = sun
        self.current_ball_type = 0

        # Scoring
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
        Returns the int type of the next ball to be generated.
        """
        next_ball = self.current_ball_type + 1
        if next_ball > 2:
            next_ball = 0
        return next_ball

    def get_scores(self):
        """
        returns the list of scores for use outside this class.
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
