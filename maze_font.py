
import pygame as pg


class TextFont:
    def __init__(self, size=18, font="Bauhaus 93"):
        self.set_font = pg.font.SysFont(font, size)

    def draw_text(self, win_screen, text_str, pos=(500, 500), color=(0, 0, 0)):
        color = color
        text = self.set_font.render(text_str, True, color)
        rect = text.get_rect()
        rect.topleft = pos
        win_screen.blit(text, rect)

    def draw_text_box(self, win_screen, rect, color, alpha=50, rounds=15):
        text_s = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
        pg.draw.rect(text_s, (color[0], color[1],
                     color[2], alpha), text_s.get_rect(), 0, rounds)
        win_screen.blit(text_s, rect)
