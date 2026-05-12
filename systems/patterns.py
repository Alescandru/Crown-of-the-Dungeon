import pygame
import random

from .attacks import *

    # -------------------------
    # RAT SCRATCH
    # -------------------------
def spawn_rat_scratch(combat_system,side):

    arena = combat_system.arena

    vx=5

    start_x = arena.left - 100

    if side == "right":
        start_x = arena.right + 100
        vx=-8

    base_y = arena.top + 20
    y_offset = random.randint(0, 250)

    y = base_y + y_offset

    block_size = 8

    pattern = [
        "00000000000000000011111100000000000",
        "00000000000000000000011111110000000",
        "00000000000000000000000000000000000",
        "00000000000000000000000000000000000",
        "00000000000000000000000000000000000",
        "00000000000000000000000000000000000",
        "00000000000000000000000000000000000",
        "00000111111000000000000000000000000",
        "00111111000000000000000011111000000",
        "00000000000000000000000000011111000",
        "00000000000000000000000000000000000",
        "00000000000000000000000000000000000",
        "00000000000000000000000000000000000",
        "00000000000000000000000000000000000",
        "00000000000000000000000000000000000",
        "00000000000000000000000000000000000",
        "00000001111110000000000000000000000",
        "00000000011111100000000000000000000",
        "00000000000000000000000000111111000",
    ]

    blocks = []

    for row_index, row in enumerate(pattern):

        for col_index, cell in enumerate(row):

            if cell == "1":

                x = start_x + col_index * block_size

                if side == "right":
                    x = start_x - col_index * block_size

                rect = pygame.Rect(
                    x,
                    y + row_index * block_size,
                    block_size,
                    block_size
                )

                blocks.append(rect)

    combat_system.attacks.append(
        ShapeAttack(blocks, vx, 0)
    )
    # -------------------------
    # BAT BITE
    # -------------------------
def spawn_bat_bite(combat_system):

    arena = combat_system.arena

    base_x = arena.width / 2
    x_offset = random.randint(-100, 100)

    vy=7
    start_x = base_x + x_offset

    y = arena.top - 30

    block_size = 13

    pattern = [
        "000111111111111111100001111111111111111000",
        "000111111111111000000000000111111111111000",
        "000011111111110000000000000011111111110000",
        "000001111111100000000000000001111111100000",
        "000000111111000000000000000000111111000000",
        "000000011110000000000000000000011110000000",
        "000000001100000000000000000000001100000000",
        "000000000100000000000000000000001000000000",
    ]

    blocks = []

    for row_index, row in enumerate(pattern):

        for col_index, cell in enumerate(row):

            if cell == "1":

                x = start_x + col_index * block_size

                rect = pygame.Rect(
                    x,
                    y + row_index * block_size,
                    block_size,
                    block_size
                )

                blocks.append(rect)

    combat_system.attacks.append(
        ShapeAttack(blocks, 0, vy)
    )
    # -------------------------
    # CRAB CLAW
    # -------------------------
def spawn_crab_claw(combat_system, side="left"):

    arena = combat_system.arena

    start_x = arena.left
    vy = 8

    if side == "right":
        start_x = arena.right

    y = arena.top - 30

    block_size = 17

    pattern = [
        "00000011111111100000",
        "00000111111111111000",
        "00001110000000111110",
        "11111000000000000111",
        "11111000000000000000",
        "11011111000001110000",
        "00000011111111100000",
    ]

    blocks = []

    for row_index, row in enumerate(pattern):

        for col_index, cell in enumerate(row):

            if cell == "1":

                x = start_x + col_index * block_size

                if side == "right":
                    x = start_x - col_index * block_size

                rect = pygame.Rect(
                    x,
                    y + row_index * block_size,
                    block_size,
                    block_size
                )

                blocks.append(rect)

    combat_system.attacks.append(
        ShapeAttack(blocks, 0, vy)
    )
