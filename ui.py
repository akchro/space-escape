import pygame
import text

class ShipMenu:
    def __init__(self):
        self.image = pygame.image.load('data/shipmenumed.png')
        self.image_rect = self.image.get_rect()
        self.font = text.Font('data/large_font.png')

    def render(self, surface, location):
        self.font.render(self.image, "test", (30, 10))
        surface.blit(self.image, (location[0], location[1] - self.image.get_height()))

    def menu(self, hp, guns, shields, energy, surface, location): # TODO add shields/hull
        self.font.render(self.image, hp, (60, 20))
        self.font.render(self.image, guns, (40, 45))
        self.font.render(self.image, shields, (20, 70))
        self.font.render(self.image, energy, (20, 95))
        surface.blit(self.image, (location[0], location[1] - self.image.get_height()))


class ProgressBar:
    def __init__(self):
        self.pb1 = pygame.image.load('data/bigprogressbar1.png')
        self.pb2 = pygame.image.load('data/bigprogressbar2.png')
        self.pb3 = pygame.image.load('data/bigprogressbar3.png')
        self.pb4 = pygame.image.load('data/bigprogressbar4.png')
        self.pb5 = pygame.image.load('data/bigprogressbar5.png')

    def render(self, surface, location):
        seconds = pygame.time.get_ticks()/1000
        if seconds >= 20:
            surface.blit(self.pb5, (location[0], location[1]))
        elif seconds >= 15:
            surface.blit(self.pb4, (location[0], location[1]))
        elif seconds >= 10:
            surface.blit(self.pb3, (location[0], location[1]))
        elif seconds >= 5:
            surface.blit(self.pb2, (location[0], location[1]))
        elif seconds >= 0:
            surface.blit(self.pb1, (location[0], location[1]))