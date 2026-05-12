import pygame


class OverworldSystem:

    def __init__(self, game):

        self.game = game

        
        # MAP SIZE     
        self.map_width = 2000
        self.map_height = 2000

        
        # VISUAL MAP
        self.map_image = pygame.image.load("img/Map/dungeon1.jpg").convert()

        self.map_image = pygame.transform.scale(
            self.map_image,
            (self.map_width, self.map_height)
        )        
        # COLLISION MAP
        self.collision_map = pygame.image.load("img/Map/dungeon1Collision3.png").convert()

        self.collision_map = pygame.transform.scale(
            self.collision_map,
            (self.map_width, self.map_height)
        )   
        # CAMERA
        
        self.camera_x = 0
        self.camera_y = 0

    # -------------------------
    # EVENTS
    # -------------------------
    def handle_event(self, event):
        pass

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self):

        player = self.game.player

        if player is None:
            return

        
        # SAVE OLD POSITION
        old_x = player.rect.x
        old_y = player.rect.y

        
        # PLAYER MOVEMENT        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            player.rect.y -= player.speed

        if keys[pygame.K_s]:
            player.rect.y += player.speed

        if keys[pygame.K_a]:
            player.rect.x -= player.speed

        if keys[pygame.K_d]:
            player.rect.x += player.speed

        
        # MAP LIMITS        
        if player.rect.left < 0:
            player.rect.left = 0

        if player.rect.right > self.map_width:
            player.rect.right = self.map_width

        if player.rect.top < 0:
            player.rect.top = 0

        if player.rect.bottom > self.map_height:
            player.rect.bottom = self.map_height

        
        # COLLISION CHECK
        # BLACK PIXELS = WALL
        check_points = [

            (player.rect.left, player.rect.top),
            (player.rect.right - 1, player.rect.top),

            (player.rect.left, player.rect.bottom - 1),
            (player.rect.right - 1, player.rect.bottom - 1),

            (player.rect.centerx, player.rect.centery)
        ]

        collided = False

        for point in check_points:

            color = self.collision_map.get_at(point)

            if color[:3] == (0, 0, 0):

                collided = True
                break

        # RESET POSITION IF COLLISION
        if collided:

            player.rect.x = old_x
            player.rect.y = old_y

        
        # CAMERA FOLLOW
        self.camera_x = player.rect.centerx - 500
        self.camera_y = player.rect.centery - 300

        # LIMIT CAMERA
        self.camera_x = max(
            0,
            min(
                self.camera_x,
                self.map_width - self.game.screen.get_width()
            )
        )

        self.camera_y = max(
            0,
            min(
                self.camera_y,
                self.map_height - self.game.screen.get_height()
            )
        )

        
        # ENEMY COLLISION
        hit_enemy = pygame.sprite.spritecollideany(
            player,
            self.game.enemy_group
        )

        if hit_enemy:
            self.game.start_combat(hit_enemy)

        # CROWN COLLISION
        if player.rect.colliderect(
            self.game.crown_rect
        ):
            self.game.state = "ending"
            self.game.ending.start()

    # -------------------------
    # DRAW
    # -------------------------
    def draw(self):

        screen = self.game.screen

        
        # DRAW MAP
        screen.blit(
            self.map_image,
            (-self.camera_x, -self.camera_y)
        )

        # DRAW ENEMIES
        for enemy in self.game.enemy_group:

            screen.blit(
                enemy.image,
                (
                    enemy.rect.x - self.camera_x,
                    enemy.rect.y - self.camera_y
                )
            )

        # DRAW PLAYER
        if self.game.player:

            screen.blit(
                self.game.player.image,
                (
                    self.game.player.rect.x - self.camera_x,
                    self.game.player.rect.y - self.camera_y
                )
            )

        # DRAW CROWN
        screen.blit(
            self.game.crown_image,
            (
                self.game.crown_rect.x - self.camera_x,
                self.game.crown_rect.y - self.camera_y
            )
        )