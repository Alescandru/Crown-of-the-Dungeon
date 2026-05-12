import pygame
import sys
from game import Game

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

game = Game(screen)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        game.handle_event(event)

    game.update()
    game.draw()

    pygame.display.update()
    clock.tick(60)