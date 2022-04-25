import pygame
import os

class Item:
    def __init__(self, image_file, x, y):
        self.surface = pygame.image.load(os.path.join("assets", image_file))
        self.x = x
        self.y = y
