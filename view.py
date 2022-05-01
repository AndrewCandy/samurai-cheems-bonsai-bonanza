"""
Creates the view of the Samurai Cheems: Bonsai Bananza game
"""
# Library imports
from abc import ABC, abstractmethod
import pygame
import pymunk.pygame_util

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
        self._board._draw_options = pymunk.pygame_util.DrawOptions(self._board._screen)

    def clear_screen(self):
        """
        Clears the screen.
        return: None
        """
        self._board._screen.fill(pygame.Color("white"))

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

    def draw_objects(self):
        """
        Draw the objects in default view.
        :return: None
        """
        self._board._space.debug_draw(self._board._draw_options)
