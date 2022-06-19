from random import choice, uniform
import pygame


class Ball:
    def __init__(self, pong_game):
        self.screen = pong_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = pong_game.settings

        self.color = self.settings.object_color
        self.rect = pygame.Rect(
            0, 0, self.settings.ball_width, self.settings.ball_height)

        self.prepare_ball()

    def prepare_ball(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.dy = choice([-1, 1])
        self.dx = choice([-1, 1])
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed = self.settings.ball_speed
        self.moving = False
        self.done = False

    # Das Ball aendert die vertikale Richtung
    def bounce_dy(self):
        self.dy = -self.dy

    # Das Ball aendern die horizontale Richtung und beschleunigt
    def bounce_dx(self):
        self.dx = -self.dx
        self.speed *= 1.05

    # Prüfen, ob das Ball im Aus ist.
    def is_out_of_bounds(self):
        return self.x <= self.screen_rect.left or self.x >= self.screen_rect.right

    def hit_wall(self):
        return self.y <= self.screen_rect.top or self.y >= self.screen_rect.bottom

    def update(self):
        if self.moving:
            # Die Position des Ball anhand der Geschwindigkeit und Richtung aktualisieren
            self.x += self.dx*self.speed
            if self.dy < 0:
                self.y = max(0, self.y + self.dy*self.speed*uniform(0.2, 0.5))
            else:
                self.y = min(self.screen_rect.bottom, self.y +
                             self.dy*self.speed*uniform(0.2, 0.5))
            self.rect.x = self.x
            self.rect.y = self.y

            # Die aktuelle Runde beendet wenn das Ball im Aus ist.
            if self.is_out_of_bounds():
                self.done = True

    def draw_ball(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
