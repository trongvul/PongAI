import pygame


class Scoreboard:
    def __init__(self, pong_game):
        self.screen = pong_game.screen
        self.screen_rect = self.screen.get_rect()
        self.color = (250, 250, 250)

        self.player1_score = 0
        self.player2_score = 0
        self.winner = None
        self.max_score = 11

        self.font = pygame.font.Font('./font/AtariClassicChunky-PxXP.ttf', 25)
        self.prep_score()
        self.msg_image = None

    # Bereistellung der Punkte
    def prep_score(self):
        score_str = str(self.player1_score) + ":" + str(self.player2_score)
        self.score_image = self.font.render(
            score_str, True, self.color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.midtop = self.screen_rect.midtop
        self.score_rect.y += 10

    def increment_player1_score(self):
        self.player1_score += 1

    def increment_player2_score(self):
        self.player2_score += 1

    def reset_scoreboard(self):
        self.player1_score = 0
        self.player2_score = 0
        self.winner = None

    def _render_msg(self, s):
        self.msg_image = self.font.render(s, True, self.color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.midtop = self.screen_rect.midtop
        self.msg_rect.y += 50

    def blit_score(self):
        # Punkte werden ständig aktualisiert
        score_str = f"{self.player1_score} : {self.player2_score}"
        self.score_image = self.font.render(
            score_str, True, self.color)
        self.screen.blit(self.score_image, self.score_rect)

    def blit_start_msg(self):
        start_str = "Press SPACE to serve or M to return to the menu"
        self._render_msg(start_str)
        self.screen.blit(self.msg_image, self.msg_rect)

    def blit_end_msg(self):
        endgame_str = f"Player {self.winner} has won! Press SPACE to start again"
        self._render_msg(endgame_str)
        self.screen.blit(self.msg_image, self.msg_rect)
