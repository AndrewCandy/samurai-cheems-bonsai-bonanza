"""
This module handles all of the sounds in our python file
"""
import pygame


def initialize_mixer():
    """
    This method loads the music and initializes the mixer for pygame

    Inputs:
        none
    Returns:
        the music object
    """
    # Test Sound?
    pygame.mixer.init()
    music = pygame.mixer.music.load("Sounds/Background Track.mp3")

    return music


def loop_music():
    """
    This function loops the music. No inputs or arguments
    """
    pygame.mixer.music.play(-1)


def play_score():
    """
    This function loads and plays the score sound no inputs or arguments
    """
    score = pygame.mixer.Sound("Sounds/Chime.mp3")
    score.play()
