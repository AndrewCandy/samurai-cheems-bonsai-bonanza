# Library imports
import pygame
from abc import ABC, abstractmethod


class View(ABC):
    """
    Create an abstract class to hold view methods for tic tac toe.
    """
    # Define your methods here.

    def __init__(self,board):
        self._board=board
    
    def clear_screen(self) -> None:
        """
        Clears the screen.
        :return: None
        """
        self._board._screen.fill(pygame.Color("white"))

    @abstractmethod
    def draw_objects(self):
        """
        Creates an abstract draw method
        """


class DefaultView(View):
    """
    A text based Tic-tac-toe view method to represent the state of the
    tic-tac-toe board as a string.

    Attributes:
        None
    """

    def draw_objects(self) -> None:
        """
        Draw the objects.
        :return: None
        """
        self._board._space.debug_draw(self._board._draw_options)
