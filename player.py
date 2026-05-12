import pygame


CLASS_STATS = {
    "fighter": {"hp": 24, "speed": 2, "damage": 6},
    "rogue": {"hp": 20, "speed": 3, "damage": 7},
    "wizard": {"hp": 18, "speed": 2, "damage": 10}
}


class Player(pygame.sprite.Sprite):

    def __init__(self, image, x, y, player_class):

        super().__init__()

        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))

        self.rect = self.image.get_rect(center=(x, y))

        stats = CLASS_STATS[player_class]

        self.player_class = player_class
        self.hp = stats["hp"]
        self.speed = stats["speed"]
        self.damage = stats["damage"]

    def move(self, collision_map):

        keys = pygame.key.get_pressed()

        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed

        next_rect = self.rect.move(dx, dy)

        try:
            if collision_map.get_at(next_rect.center)[:3] != (0, 0, 0):
                self.rect = next_rect
        except:
            pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)