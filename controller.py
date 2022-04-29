
from abc import ABC, abstractmethod

# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
from board import Board

class Controller(ABC):
    """
    Create an abstract class to hold view methods for tic tac toe.
    """
    # Define your methods here.

    def __init__(self,board):
        self._board=board
        self._running = True

    def _process_events(self) -> None:
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                p = event.pos[0], event.pos[1]
                
                if len(self._board._balls) == 0:
                    self.create_ball(p)


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
        mass = 10
        radius = 15
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        _pos = 300, 20
        body.position = _pos
        mouse_dist = ((mouse_pos[0] - _pos[0])**2+(mouse_pos[1] - _pos[1])**2) ** 0.5
        vel_mag = 500
        vel = vel_mag*(mouse_pos[0] - _pos[0])/mouse_dist, vel_mag*(mouse_pos[1] - _pos[1])/mouse_dist
        body.velocity = vel
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        self._board._space.add(body, shape)
        self._board._balls.append(shape)
    
    
