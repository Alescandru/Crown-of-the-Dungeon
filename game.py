import pygame

from player import Player
from enemy import Enemy
from systems.combat import CombatSystem
from systems.ui import UISystem
from systems.overworld import OverworldSystem
from systems.ending import EndingSystem


class Game:

    def __init__(self, screen):

        self.screen = screen
        self.state = "menu"

        self.player = None

        self.overworld = OverworldSystem(self)
        self.combat = CombatSystem(self)

        self.hud_surface = pygame.Surface((260, 80), pygame.SRCALPHA)
        self.hp_font = pygame.font.Font(None, 50)
        self.hud_surface.fill((0, 0, 0))

        self.selected_class = 0

        self.enemy_group = pygame.sprite.Group()

        self.create_enemies()

        self.ui = UISystem(self)

        self.menu_bg = pygame.image.load("img/Background/ColidorAlbastru.jpg").convert()
        self.menu_bg = pygame.transform.scale(self.menu_bg, (1280,720))

        self.story_bg = self.menu_bg

        self.font = pygame.font.Font(None, 40)
        self.big_font = pygame.font.Font(None, 70)

        self.fighter_img = pygame.image.load("img/Class/fighter.png").convert_alpha()
        self.rogue_img = pygame.image.load("img/Class/rogue.png").convert_alpha()
        self.wizard_img = pygame.image.load("img/Class/wizard.png").convert_alpha()

        # CROWN
        self.ending = EndingSystem(self)

        self.crown_image = pygame.image.load(
            "img/crown.png"
        ).convert_alpha()

        self.crown_image = pygame.transform.scale(
            self.crown_image,
            (32, 32)
        )

        self.crown_rect = self.crown_image.get_rect(
            topleft=(190, 300)
        )

        pygame.mixer.init()

        pygame.mixer.music.load("sound/music/menu.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    # -------------------
    # EVENTS
    # -------------------

    def handle_event(self, event):

        self.ui.handle_event(event)

        if self.state == "overworld":
            self.overworld.handle_event(event)

        elif self.state == "combat":
            self.combat.handle_event(event)

        elif self.state == "ending":
            self.ending.handle_event(event)

        elif self.state == "game_over":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.state = "menu"

                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    exit()

    # -------------------
    # UPDATE
    # -------------------

    def update(self):

        if self.state == "overworld":
            self.overworld.update()

        elif self.state == "combat":
            self.combat.update()

        elif self.state == "ending":
            self.ending.update()

    # -------------------
    # DRAW
    # -------------------

    def draw(self):

        self.ui.draw()

        if self.state == "overworld":
            self.overworld.draw()

        elif self.state == "combat":
            self.combat.draw()

        elif self.state == "ending":
            self.ending.draw()

        elif self.state == "game_over":

            self.screen.fill((0, 0, 0))

            title = self.big_font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(title, (500, 250))

            restart = self.font.render("Press SPACE to return to menu", True, (255, 255, 255))
            exit_text = self.font.render("Press ENTER to exit", True, (255, 255, 255))

            self.screen.blit(restart, (430, 400))
            self.screen.blit(exit_text, (450, 450))

        self.draw_hud()

    def draw_hud(self):

        if self.player is None:
            return

        self.hud_surface.fill((0, 0, 0, 160))

        hp_text = self.hp_font.render(
            f"HP: {self.player.hp}",
            True,
            (255, 80, 80)
        )

        self.hud_surface.blit(hp_text, (15, 15))

        pygame.draw.rect(
            self.hud_surface,
            (255, 255, 255),
            self.hud_surface.get_rect(),
            2
        )

        self.screen.blit(self.hud_surface, (20, 20))

    # -------------------
    # ENEMY MANAGEMENT
    # -------------------

    def create_enemies(self):

        self.enemy_group.add(
            Enemy("img/Enemy/rat.png", 900, 310, "rat"),
            Enemy("img/Enemy/rat.png", 1070, 1300, "rat"),
            Enemy("img/Enemy/rat.png", 900, 1050, "rat"),
            Enemy("img/Enemy/rat.png", 1120, 1050, "rat"),
            Enemy("img/Enemy/rat.png", 240, 920, "rat"),
            Enemy("img/Enemy/rat.png", 800, 1600, "rat"),
            Enemy("img/Enemy/rat.png", 900, 1550, "rat"),
            Enemy("img/Enemy/bat.png", 370, 720, "bat"),
            Enemy("img/Enemy/bat.png", 250, 1770, "bat"),
            Enemy("img/Enemy/bat.png", 230, 250, "bat"),
            Enemy("img/Enemy/bat.png", 230, 380, "bat"),
            Enemy("img/Enemy/bat.png", 900, 800, "bat"),
            Enemy("img/Enemy/crab.png", 1220, 490, "crab"),
            Enemy("img/Enemy/crab.png", 1430, 850, "crab"),
            Enemy("img/Enemy/crab.png", 1420, 1770, "crab")
        )

    def start_combat(self, enemy):
        self.state = "combat"
        self.combat.start(enemy)

    def end_combat(self):
        self.state = "overworld"

    # -------------------
    # RESET GAME
    # -------------------

    def reset_game(self):

        self.player = None

        self.enemy_group.empty()
        self.create_enemies()

        self.combat.enemy = None
        self.combat.attacks = []
        self.combat.phase = "dodge"

        self.state = "menu"

        self.ending.video_finished = False
        self.ending.current_frame = None

        if self.ending.video:
            self.ending.video.release()

        pygame.mixer.music.load("sound/music/menu.mp3")
        pygame.mixer.music.play(-1)