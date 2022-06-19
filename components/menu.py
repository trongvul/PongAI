import pygame


class Menu:
    def __init__(self, pong_game):
        self.screen = pong_game.screen
        self.screen_rect = self.screen.get_rect()
        self.color = (250, 250, 250)
        self.font = pygame.font.Font('./font/AtariClassicChunky-PxXP.ttf', 20)

        self._prep_two_players_mode()
        self._prep_easy_mode()
        self._prep_difficult_mode()

    def _prep_two_players_mode(self):
        two_players_str = "Press 2: 2 Players"
        self.two_players_img = self.font.render(
            two_players_str, True, self.color)
        self.two_players_rect = self.two_players_img.get_rect()
        self.two_players_rect.center = self.screen_rect.center
        self.two_players_rect.y -= 50

    def _prep_easy_mode(self):
        easy_mode_str = "Press 3: 1 Players (Easy)"
        self.easy_mode_img = self.font.render(easy_mode_str, True, self.color)
        self.easy_mode_rect = self.easy_mode_img.get_rect()
        self.easy_mode_rect.center = self.screen_rect.center

    def _prep_difficult_mode(self):
        difficult_mode_str = "Press 4: 1 Players (Difficult)"
        self.difficult_mode_img = self.font.render(
            difficult_mode_str, True, self.color)
        self.difficult_mode_rect = self.difficult_mode_img.get_rect()
        self.difficult_mode_rect.center = self.screen_rect.center
        self.difficult_mode_rect.y += 50

    def blit_menu(self):
        self.screen.blit(self.two_players_img, self.two_players_rect)
        self.screen.blit(self.easy_mode_img, self.easy_mode_rect)
        self.screen.blit(self.difficult_mode_img, self.difficult_mode_rect)
