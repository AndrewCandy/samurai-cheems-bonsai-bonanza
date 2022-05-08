"""
Creates the controller behind the Samurai Cheems: Bonsai Bananza game
"""
from abc import ABC, abstractmethod
import random

# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util


class Controller(ABC):
    """
    Create an abstract class to hold view methods for tic tac toe.
    """
    # Define your methods here.

    def __init__(self,board):
        self._board=board
        self.running = True

    def process_events(self) -> None:
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            #Quits if the close button is pressed
            if event.type == pygame.QUIT:
                self.running = False
            #Quits if the escape button is pressed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            #Clears level for debugging purposes
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._board.space.remove(*self._board.pips)
                self._board.pips = []
            #Launches a new ball when clicked
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_xy = event.pos[0], event.pos[1]
                #Makes sure only one ball is on the screen at a time.
                if len(self._board.balls) == 0:
                    self.create_ball(mouse_xy)


    @abstractmethod
    def create_ball(self,mouse_pos):
        """
        Creates an abstract draw method
        """

class MouseController(Controller):
    """
    A text based Tic-tac-toe view method to represent the state of the
    tic-tac-toe board as a string.

    Attributes:
        None
    """

    def create_ball(self,mouse_pos) -> None:
        """
        Create a ball.
        :return:
        """
        #Physical Parameters of the ball
        mass = 10
        radius = self._board.ball_radius
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))

        #Sends the momentum parameters to the body
        body = pymunk.Body(mass, inertia)

        #Set launch position
        _pos = (240+768)/2, 20
        body.position = _pos

        #Finds the distance from the mouse to the launch position when clicked
        mouse_dist = ((mouse_pos[0] - _pos[0])**2+\
            (mouse_pos[1] - _pos[1])**2) ** 0.5

        #Creates starting speed with some randomness to prevent the exact same
        #launch having the same trajectory
        vel_mag = 500 + random.randint(0,50)

        #Sets initial velocity in the direction of the mouse click
        vel = vel_mag/mouse_dist*(mouse_pos[0] - _pos[0]),\
             vel_mag/mouse_dist*(mouse_pos[1] - _pos[1])

        #Sends the velocity to the body
        body.velocity = vel

        #Creates shape and collision parameters for the body
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        shape.collision_type = 1

        #Adds the ball to the space and to the list of balls
        self._board.space.add(body,shape)
        self._board.balls.append(shape)
