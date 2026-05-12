import pygame
import random

ENEMY_STATS = {
    "rat": {"hp": 5, "damage": 2},
    "bat": {"hp": 10, "damage": 4},
    "crab": {"hp": 7, "damage": 5}
}


class Enemy(pygame.sprite.Sprite):

    def __init__(self, image_path, x, y, enemy_type):

        super().__init__()

        self.type = enemy_type

        self.stats = ENEMY_STATS[enemy_type]

        self.hp = self.stats["hp"]
        self.damage = self.stats["damage"]

        self.shake_time = 0
        self.hit_flash_time = 0
        self.flash_duration = 120

        self.original_image = pygame.image.load(image_path).convert_alpha()

        
        if enemy_type == "rat":
            world_size = (48, 48)

        elif enemy_type in ["bat", "crab"]:
            world_size = (96, 96)

        else:
            world_size = (64, 64)

        self.image_world = pygame.transform.smoothscale(
            self.original_image,
            world_size
        )

        self.image = self.image_world
        self.rect = self.image.get_rect(center=(x, y))
