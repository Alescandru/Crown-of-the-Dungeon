import pygame


class Attack:

    def __init__(self, rect, vx=0, vy=0, color=(255, 0, 0)):

        self.rect = rect
        self.vx = vx
        self.vy = vy
        self.color = color

    def update(self):

        self.rect.x += self.vx
        self.rect.y += self.vy

    def draw(self, screen):

        pygame.draw.rect(screen, self.color, self.rect)

    def collides(self, player_rect):

        return self.rect.colliderect(player_rect)

    def outside(self, arena):

        return not arena.colliderect(self.rect)


class ShapeAttack:

    def __init__(self, blocks, vx=0, vy=0, color=(255, 0, 0)):
        self.blocks = blocks
        self.vx = vx
        self.vy = vy
        self.color = color

        # IMPORTANT: compatibilitate
        self.rect = self.blocks[0]

    def update(self):
        for r in self.blocks:
            r.x += self.vx
            r.y += self.vy

        # update rect pentru coliziuni globale
        self.rect = self.blocks[0]

    def draw(self, screen):
        for b in self.blocks:
            pygame.draw.rect(screen, self.color, b)

    def collides(self, player_rect):
        return any(b.colliderect(player_rect) for b in self.blocks)

    def outside(self, arena):
        return all(not arena.colliderect(b) for b in self.blocks)