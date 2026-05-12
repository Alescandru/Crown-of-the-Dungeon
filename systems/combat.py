import pygame
import random
from .patterns import *
from .attacks import *

class CombatSystem:

    def handle_event(self, event):
            pass

    def __init__(self, game):

        self.attack_bar_x = 300
        self.attack_bar_dir = 1
        self.attack_bar_speed = 8
        self.attack_result = None
        self.attack_done = False

        self.game = game
        self.enemy = None

        self.attacks = []
        self.attack_left = 0
        self.attack_right = 0

        self.phase = "dodge"
        self.start_time = 0

        self.attack_bar_rect = pygame.Rect(300, 600, 600, 20)

        self.hit_zone = pygame.Rect(
            550,
            600,
            100,
            20
        )

        # ARENA
        self.arena = pygame.Rect(300, 300, 680, 400)

        # PLAYER BOX
        self.player_box = pygame.Rect(640, 500, 20, 20)

        self.attack_timer = 0

    # -------------------------
    # START COMBAT
    # -------------------------

    def start(self, enemy):

        self.enemy = enemy

        self.attacks = []

        self.phase = "dodge"
        self.start_time = pygame.time.get_ticks()

        self.player_box.center = (640, 500)

        self.attack_timer = pygame.time.get_ticks()

        self.attack_bar_x = 300
        self.attack_bar_dir = 1
        self.attack_done = False

    # -------------------------
    # UPDATE
    # -------------------------

    def update(self):

        player = self.game.player
        if player is None:
            return

        time_passed = (pygame.time.get_ticks() - self.start_time) / 1000

        if time_passed < 10:
            self.phase = "dodge"
            self.dodge_phase(player)
        else:
            self.phase = "attack"
            self.attack_phase(player)

    # -------------------------
    # DODGE PHASE
    # -------------------------

    def dodge_phase(self, player):

        keys = pygame.key.get_pressed()

        speed = player.speed + 2

        if keys[pygame.K_w]:
            self.player_box.y -= speed
        if keys[pygame.K_s]:
            self.player_box.y += speed
        if keys[pygame.K_a]:
            self.player_box.x -= speed
        if keys[pygame.K_d]:
            self.player_box.x += speed

        # LIMIT PLAYER IN ARENA
        self.player_box.x = max(self.arena.left, min(self.player_box.x, self.arena.right - self.player_box.width))
        self.player_box.y = max(self.arena.top, min(self.player_box.y, self.arena.bottom - self.player_box.height))

        # SPAWN PATTERNS
        self.spawn_patterns()

        # UPDATE ATTACKS
        for a in self.attacks[:]:

            a.update()

            # REMOVE IF OUTSIDE ARENA
            if a.outside(self.arena):
                self.attacks.remove(a)
                continue

            if a.collides(self.player_box):
                self.game.player.hp -= self.enemy.damage
                self.attacks.remove(a)

                if self.game.player.hp <= 0:
                    self.game.player.hp = 0
                    self.game.state = "game_over"


    # -------------------------
    # ATTACK PHASE
    # -------------------------

    def attack_phase(self, player):

        keys = pygame.key.get_pressed()

        # MOVE BAR
        self.attack_bar_x += self.attack_bar_dir * self.attack_bar_speed

        if self.attack_bar_x > 900:
            self.attack_bar_dir = -1
        if self.attack_bar_x < 300:
            self.attack_bar_dir = 1

        # SPACE = HIT
        if keys[pygame.K_SPACE] and not self.attack_done:

            self.attack_done = True

            damage = 0

            bar_rect = pygame.Rect(
                self.attack_bar_x,
                600,
                10,
                20
            )

            if bar_rect.colliderect(self.hit_zone):
                damage = player.damage
                self.enemy.hit_flash_time = pygame.time.get_ticks()
                self.enemy.shake_time = pygame.time.get_ticks()

            self.enemy.hp -= damage

            # CHECK DEATH
            if self.enemy.hp <= 0:
                self.game.enemy_group.remove(self.enemy)
                self.game.end_combat()
                return

            # IMPORTANT: revine la dodge
            self.phase = "dodge"
            self.start_time = pygame.time.get_ticks()
            self.attack_done = False

    # -------------------------
    # PATTERN SYSTEM
    # -------------------------
    def spawn_patterns(self):
        
        enemy_type = self.enemy.type
        now = pygame.time.get_ticks()

        if now - self.attack_timer < 1000:
            return

        self.attack_timer = now

        if enemy_type == "rat":
            side = random.choice(["left", "right"])
            if self.attack_left >= 2:
                side = "right"
                self.attack_left = 0
            elif self.attack_right >= 2:
                side = "left"
                self.attack_right = 0

            spawn_rat_scratch(self, side)
            if(side == "left"):
                self.attack_left += 1
            else:
                self.attack_right += 1


        elif enemy_type == "bat":
            spawn_bat_bite(self)

        elif enemy_type == "crab":
            side = random.choice(["left", "right"])
            if self.attack_left >= 2:
                side = "right"
                self.attack_left = 0
            elif self.attack_right >= 2:
                side = "left"
                self.attack_right = 0

            spawn_crab_claw(self, side)
            if(side == "left"):
                self.attack_left += 1
            else:
                self.attack_right += 1

    # -------------------------
    # DRAW
    # -------------------------

    def draw(self):

        screen = self.game.screen

        # ARENA
        pygame.draw.rect(screen, (0, 0, 0), self.arena)
        pygame.draw.rect(screen, (255, 255, 255), self.arena, 3)
       
        # ENEMY EFFECTS
        enemy_img = self.enemy.original_image.copy()

        now = pygame.time.get_ticks()

        # HIT FLASH
        if (
            self.enemy.hit_flash_time > 0
            and now - self.enemy.hit_flash_time < self.enemy.flash_duration
        ):

            flash = pygame.Surface(enemy_img.get_size(), pygame.SRCALPHA)
            flash.fill((255, 0, 0, 120))

            enemy_img.blit(flash, (0, 0))

        # SHAKE
        offset_x = 0

        if now - self.enemy.shake_time < 150:
            offset_x = random.randint(-6, 6)

        # DRAW ENEMY
        enemy_rect = enemy_img.get_rect(
            center=(640 + offset_x, 150)
        )

        screen.blit(enemy_img, enemy_rect)

        # DODGE ATTACKS
        if self.phase == "dodge":
            for attack in self.attacks:
                attack.draw(screen)


        # ATTACK MINI GAME
        elif self.phase == "attack":

            # BAR BACKGROUND
            pygame.draw.rect(
                screen,
                (50, 50, 50),
                self.attack_bar_rect
            )

            # PERFECT DE LOVIRE
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                self.hit_zone
            )

            # MOVING BAR
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (self.attack_bar_x, 600, 10, 20)
            )

        # PLAYER SOUL
        pygame.draw.rect(screen,
            (255, 255, 255),
            self.player_box)