import pygame
import cv2
from moviepy import VideoFileClip


class EndingSystem:

    def __init__(self, game):

        self.video = None
        self.current_frame = None

        self.game = game

        self.video_finished = False

        self.text_timer = 0

    # -------------------------
    # START ENDING
    # -------------------------

    def start(self):

        pygame.mixer.music.stop()
        self.video_finished = False
        self.current_frame = None

        if self.game.selected_class == 0:

            video_path = "video/fighter.mp4"

        elif self.game.selected_class == 1:

            video_path = "video/rogue.mp4"

        else:

            video_path = "video/wizard.mp4"

        self.video = cv2.VideoCapture(video_path)

        # EXTRAGE AUDIO AUTOMAT
        clip = VideoFileClip(video_path)

        clip.audio.write_audiofile(
            "temp_audio.mp3"
        )

        # PORNESTE SUNETUL
        pygame.mixer.music.load("temp_audio.mp3")
        pygame.mixer.music.play()

    # -------------------------
    # UPDATE
    # -------------------------

    def update(self):

        if self.video_finished:
            return

        success, frame = self.video.read()

        if not success:

            self.video_finished = True

            self.current_frame = None

            pygame.mixer.music.stop()

            if self.video:
                self.video.release()

            return

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame = cv2.resize(frame, (1280, 720))

        frame = frame.swapaxes(0, 1)

        self.current_frame = pygame.surfarray.make_surface(frame)

    # -------------------------
    # EVENTS
    # -------------------------

    def handle_event(self, event):

        if not self.video_finished:
            return

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                self.game.reset_game()
                self.game.state = "menu"

            elif event.key == pygame.K_RETURN:

                pygame.quit()
                exit()

    # -------------------------
    # DRAW
    # -------------------------

    def draw(self):

        screen = self.game.screen

        screen.fill((0, 0, 0))

        # VIDEO
        if not self.video_finished:

            if self.current_frame:
                screen.blit(self.current_frame, (0, 0))

        # FINAL SCREEN
        else:

            title = self.game.big_font.render(
                "VICTORY",
                True,
                (255, 215, 0)
            )

            screen.blit(title, (500, 180))

            text1 = self.game.font.render(
                "The adventurer reached the ancient crown.",
                True,
                (255, 255, 255)
            )

            text2 = self.game.font.render(
                "Peace returned to the realm.",
                True,
                (255, 255, 255)
            )

            replay = self.game.font.render(
                "SPACE - Replay",
                True,
                (255, 255, 255)
            )

            exit_text = self.game.font.render(
                "ENTER - Exit",
                True,
                (255, 255, 255)
            )

            screen.blit(text1, (350, 320))
            screen.blit(text2, (420, 370))

            screen.blit(replay, (500, 500))
            screen.blit(exit_text, (520, 550))