import sys
import numpy as np
import pygame
from pygame import mixer
from components.paddle import Paddle
from components.ball import Ball
from components.scoreboard import Scoreboard
from components.menu import Menu
from status.game_mode import GameMode
from status.game_state import GameState
from settings import Settings
from nn_model.model import build_model


class PongGame:
    """
    Attribute:
        settings - Alle Einstellungen des Spiels
        screen - Der Hauptbildschirm
        current_mode - Der aktuelle Spielmodus
        current_state - Der aktuelle Spielzustand
        paddle1 - das linke Paddel
        paddle2 - das rechte Paddel
        scoreboard - Die Anzeigertafel, die zeigt die Punkte und Benachrichtigung
        ball - Das Ball
        menu - Das Menü, in dem die Modi dargestellt werden
        model - das neuronale Netzmodell
        paddle_prev_y - die letzte y-Position des zweiten Paddel. Es wird verwendet, um die Bewegungsrichtung zu bestimmen, die als Label der Daten gesammelt wird.
    """

    def __init__(self):
        pygame.init()

        # Einstellung des Bildschirms
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.screen_caption)

        # Spielmodus und Spielstatus initialisieren
        self.current_mode = None
        self.current_state = GameState.MENU

        self.model = None
        self.paddle_prev_y = None

        # Sound im Spiel bereitstellen
        self._prepare_sounds()

        # das Menü, das Ball, den Paddel initialisieren
        self._prepare_components()

    def _prepare_sounds(self):
        mixer.init()
        self.paddle_hit = mixer.Sound('./sounds/paddle_hit.wav')
        self.paddle_hit.set_volume(0.5)
        self.score_sound = mixer.Sound('./sounds/score.wav')
        self.score_sound.set_volume(0.1)
        self.wall_hit = mixer.Sound('./sounds/wall_hit.wav')
        self.wall_hit.set_volume(0.5)

    def _prepare_components(self):
        self.paddle1 = Paddle(
            self, self.settings.paddle1_x, self.settings.paddle1_y)
        self.paddle2 = Paddle(
            self, self.settings.paddle2_x, self.settings.paddle2_y)
        self.ball = Ball(self)
        self.scoreboard = Scoreboard(self)
        self.menu = Menu(self)

    def run_game(self):
        while True:
            self._check_events()
            if self.current_state == GameState.PLAY:
                if self.current_mode == GameMode.ONE_PLAYER_DIFFCULT:
                    self._update_diff_mode()
                    # Wenn Daten im Diffcult-Modus gesammelt wird
                    # self._save_data()
                elif self.current_mode == GameMode.ONE_PLAYER_EASY:
                    self._update_easy_mode()
                self.paddle1.update()
                self.paddle2.update()
                self._update_ball()
                self._update_score()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Wähle einen Spielmodus aus dem Menü
        if self.current_state == GameState.MENU:
            if event.key == pygame.K_2:
                self.current_mode = GameMode.TWO_PLAYERS
                self.current_state = GameState.SERVE
            elif event.key == pygame.K_3:
                self.current_mode = GameMode.ONE_PLAYER_EASY
                self.current_state = GameState.SERVE
            elif event.key == pygame.K_4:
                self.current_mode = GameMode.ONE_PLAYER_DIFFCULT
                self.current_state = GameState.SERVE

        # Steuere das linke Paddel
        if event.key == pygame.K_s:
            self.paddle1.moving_down = True
        elif event.key == pygame.K_w:
            self.paddle1.moving_up = True

        # Steuere das rechte Paddel, wenn der 2-Spieler-Modus aktiviert ist.
        if self.current_mode == GameMode.TWO_PLAYERS:
            if event.key == pygame.K_DOWN:
                self.paddle2.moving_down = True
            elif event.key == pygame.K_UP:
                self.paddle2.moving_up = True

        # Beginne mit dem Aufschlag
        # die Anzeigetafel wird bei Spielende zurückgesetzt
        if event.key == pygame.K_SPACE:
            if self.current_state != GameState.MENU:
                if self.current_state == GameState.END:
                    self.scoreboard.reset_scoreboard()
                self.current_state = GameState.PLAY
                self.ball.moving = True

        # Komme zum Menü
        if event.key == pygame.K_m:
            self._reset_round()
            self.scoreboard.reset_scoreboard()
            self.model = None
            self.current_mode = None
            self.current_state = GameState.MENU

        # Das Spiel verlassen
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        #  Das linke Paddel stoppt, wenn die entsprechende Taste losgelassen wird
        if event.key == pygame.K_s:
            self.paddle1.moving_down = False
        elif event.key == pygame.K_w:
            self.paddle1.moving_up = False

       #  Das rechte Paddel stoppt, wenn die entsprechende Taste losgelassen wird
        if self.current_mode == GameMode.TWO_PLAYERS:
            if event.key == pygame.K_DOWN:
                self.paddle2.moving_down = False
            elif event.key == pygame.K_UP:
                self.paddle2.moving_up = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        if self.current_state == GameState.MENU:
            self.menu.blit_menu()
        else:
            self.paddle1.draw_paddle()
            self.paddle2.draw_paddle()
            self.ball.draw_ball()
            self.scoreboard.blit_score()
            if self.current_state == GameState.SERVE:
                self.scoreboard.blit_start_msg()
            elif self.current_state == GameState.END:
                self.scoreboard.blit_end_msg()
        pygame.display.flip()

    # Steuere das Verhalten des Balls
    def _update_ball(self):
        collision = self._check_ball_paddle_collision()
        # Das Ball kollidiert mit einem der Paddel
        if collision:
            self.paddle_hit.play()
            self.ball.bounce_dx()
        # Das Ball trifft den obere/ untere Rand
        if self.ball.hit_wall():
            self.wall_hit.play()
            self.ball.bounce_dy()
        # Die aktuelle Runde beendet wenn das Ball im Aus ist.
        if self.ball.is_out_of_bounds():
            self.ball.done = True
        self.ball.update()

    def _update_score(self):
        # Wenn der Ball zu irgendeinem Zeitpunkt in horizontaler Richtung im Außenbereich ist, beendet die Runde und wird der Punkt berechnet
        if self.ball.done:
            if self.ball.x < 0:
                self.scoreboard.increment_player2_score()
            elif self.ball.x > self.screen.get_rect().right:
                self.scoreboard.increment_player1_score()
            self.score_sound.play()
            self._reset_round()
            # Solange einer der beiden Spieler zuerst 11 Punkte erreicht, gewinnt er den Spiel und wird im Anzeiger dargestellt
            if self.scoreboard.player1_score >= self.scoreboard.max_score or self.scoreboard.player2_score >= self.scoreboard.max_score:
                self.current_state = GameState.END
                if self.scoreboard.player1_score == 10:
                    self.scoreboard.winner = 1
                else:
                    self.scoreboard.winner = 2

    # Im Difficult-Modus bewegt sich das rechte Paddel relativ zur y-Richtung des Balls
    def _update_diff_mode(self):
        self.paddle2.rect.centery = self.ball.y
        self.paddle2.y = self.paddle2.rect.y

    # Im Easy-Modus produziert der AI-Agent 6 Q-Werte anhand des Eingabebildschirms in Pixel. Der höchste Wert bestimmt die Bewegung des Paddels
    def _update_easy_mode(self):
        # Bereitstellung des Modells
        if self.model is None:
            self.model = build_model()
            self.model.load_weights('./nn_model/weights/model_weights.h5')
        ball_x, ball_y, velocity_x, velocity_y, paddle_y = self._collect_input_data()
        input = np.array([ball_x, ball_y, velocity_x, velocity_y, paddle_y])
        prediction = self.model.predict(input[np.newaxis])
        self.paddle2.speed = 3
        if prediction >= 0.5:
            self.paddle2.moving_up = False
            self.paddle2.moving_down = True
        else:
            self.paddle2.moving_up = True
            self.paddle2.moving_down = False

    def _reset_round(self):
        self.current_state = GameState.SERVE
        self.paddle_prev_y = None
        self.ball.prepare_ball()
        self.paddle1.reset()
        self.paddle2.reset()

    def _check_ball_paddle_collision(self):
        collision = pygame.Rect.colliderect(
            self.ball.rect, self.paddle1.rect) or pygame.Rect.colliderect(self.ball.rect, self.paddle2.rect)
        return collision

    # Sammeln der Daten für das neuronale Netz
    def _save_data(self):
        ball_x, ball_y, velocity_x, velocity_y, paddle_y = self._collect_input_data()
        input_data = str(ball_x) + " " + str(ball_y) + " " + \
            str(velocity_x) + " " + str(velocity_y) + " " + str(paddle_y)+"\n"

        label = self._collect_labels(paddle_y)

        if label is not None:
            label = str(label)+"\n"
            with open('nn_model/data/input_data.txt', 'a') as file:
                file.writelines(input_data)
            with open('nn_model/data/label.txt', 'a') as file:
                file.writelines(label)

        self.paddle_prev_y = paddle_y

    def _collect_input_data(self):
        ball_x = self.ball.rect.x
        ball_y = self.ball.rect.y
        speed = self.ball.speed
        dx = self.ball.dx
        dy = self.ball.dy
        velocity_x = dx*speed
        velocity_y = dy*speed
        paddle_y = self.paddle2.rect.y
        return ball_x, ball_y, velocity_x, velocity_y, paddle_y

    def _collect_labels(self, paddle_y):
        if self.paddle_prev_y is None:
            self.paddle_prev_y = self.settings.paddle2_y + 1
        label = None
        # Nach oben bewegen
        if paddle_y - self.paddle_prev_y <= 0:
            label = 0
        # Nach unten bewegen
        elif paddle_y - self.paddle_prev_y > 0:
            label = 1
        return label


if __name__ == '__main__':
    pong = PongGame()
    pong.run_game()
