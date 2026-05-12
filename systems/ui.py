import pygame
from player import Player


class UISystem:

    def __init__(self, game):

        self.game = game

        self.selected_class = 0

        self.story_text = [
            "You were hired by the king",
            "to recover the lost crown.",
            "",
            "But the dungeon is filled",
            "with dangerous creatures.",
            "",
            "Good luck adventurer..."
        ]

        self.classes = ["fighter", "rogue", "wizard"]

    # -------------------
    # UPDATE EVENTS
    # -------------------

    def handle_event(self, event):

        if self.game.state == "menu":

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.state = "class_select"

        elif self.game.state == "class_select":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_a:
                    self.selected_class -= 1

                if event.key == pygame.K_d:
                    self.selected_class += 1

                self.selected_class %= len(self.classes)

                if event.key == pygame.K_RETURN:

                    self.game.selected_class = self.selected_class

                    self.game.player = Player(
                        f"img/Class/{self.classes[self.selected_class]}.png",
                        1270, 1320,
                        self.classes[self.selected_class]
                    )

                    self.game.state = "story"

        elif self.game.state == "story":

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.state = "overworld"

    # -------------------
    # DRAW MENU
    # -------------------

    def draw(self):

        screen = self.game.screen

        if self.game.state == "menu":
            self.draw_menu(screen)

        elif self.game.state == "class_select":
            self.draw_class_select(screen)

        elif self.game.state == "story":
            self.draw_story(screen)

    # -------------------
    # MENU
    # -------------------

    def draw_menu(self, screen):

        screen.blit(self.game.menu_bg, (0, 0))

        title = self.game.big_font.render("Dungeon Adventure", True, (255,255,255))
        play = self.game.font.render("Press ENTER to Play", True, (255,255,255))

        screen.blit(title, (390, 200))
        screen.blit(play, (470, 500))

    # -------------------
    # CLASS SELECT
    # -------------------

    def draw_class_select(self, screen):

        screen.fill((20,20,20))

        title = self.game.big_font.render("Choose Your Class", True, (255,255,255))
        screen.blit(title, (390, 50))

        class_data = [
            {"name": "fighter", "x": 140, "img": self.game.fighter_img},
            {"name": "rogue", "x": 520, "img": self.game.rogue_img},
            {"name": "wizard", "x": 900, "img": self.game.wizard_img},
        ]

        for i, data in enumerate(class_data):

            temp = Player(
                f"img/Class/{data['name']}.png",
                0, 0,
                data["name"]
            )

            image_rect = data["img"].get_rect(center=(data["x"] + 110, 280))
            screen.blit(data["img"], image_rect)

            if self.selected_class == i:

                pygame.draw.rect(
                    screen,
                    (255,0,0),
                    (
                        image_rect.x - 10,
                        image_rect.y - 10,
                        image_rect.width + 20,
                        image_rect.height + 20
                    ),
                    4
                )

            screen.blit(
                self.game.font.render(temp.player_class, True, (255,255,255)),
                (data["x"], 470)
            )

            screen.blit(
                self.game.font.render(f"HP: {temp.hp}", True, (255,255,255)),
                (data["x"], 510)
            )

            screen.blit(
                self.game.font.render(f"Speed: {temp.speed}", True, (255,255,255)),
                (data["x"], 550)
            )

            screen.blit(
                self.game.font.render(f"Damage: {temp.damage}", True, (255,255,255)),
                (data["x"], 590)
            )

        controls = self.game.font.render(
            "A/D = Select   ENTER = Confirm",
            True,
            (200,200,200)
        )

        screen.blit(controls, (390, 660))

    # -------------------
    # STORY (FIX COMPLET)
    # -------------------

    def draw_story(self, screen):

        screen.blit(self.game.story_bg, (0,0))

        y = 120

        for line in self.story_text:

            text = self.game.font.render(line, True, (255,255,255))
            screen.blit(text, (350, y))
            y += 45

        cont = self.game.font.render(
            "Press SPACE to continue",
            True,
            (255,0,0)
        )

        screen.blit(cont, (430, 620))