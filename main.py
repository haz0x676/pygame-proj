import pygame
import random

import sys

v = 10
FPS = 10
clock = pygame.time.Clock()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')



def main_text(screen):
    font = pygame.font.Font(None, 40)
    text = font.render("Добро пожаловать в Space Шутер!", True, (65, 105, 225))
    screen.blit(text, (170, 40))
    pygame.draw.line(screen, (0, 255, 255), (170, 69), (650, 69), width=2)


def nickname_button(screen):
    font = pygame.font.Font(None, 35)
    text = font.render("Введите имя", True, (30, 144, 255))
    text_x = width // 2 - 70
    text_y = 115
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 255), (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 1)


def level_button(screen):
    font = pygame.font.Font(None, 35)
    text = font.render("Выбор уровня", True, (30, 144, 255))
    text_x = width // 2 - 82
    text_y = 250
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 255), (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 1)


def game_button(screen):
    font = pygame.font.Font(None, 35)
    text = font.render("Начать игру", True, (30, 144, 255))
    text_x = width // 2 - 64
    text_y = 350
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 255), (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 1)


def draw(screen):
    screen.fill(pygame.Color('black'))
    for i in range(350):
        screen.fill(pygame.Color('white'),
                    (random.random() * width,
                     random.random() * height, 1, 1))


def terminate():
    pygame.quit()
    sys.exit()




def change_level(screen, info, y):
        font = pygame.font.Font(None, 35)
        text = font.render(info, True, (30, 144, 255))
        text_x = width // 2 - 82
        text_y = y
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 255), (text_x - 10, text_y - 10,
                                                text_w + 20, text_h + 20), 1)
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.color = COLOR_ACTIVE
            if event.key == pygame.K_RETURN:
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
    


if __name__ == '__main__':
    pygame.display.set_caption("Игра Space Шутер")
    pygame.init()
    size = width, height = 800, 700
    screen = pygame.display.set_mode(size)
    input_box = InputBox((width // 2 - 70) - 22, 160, 140, 32)
    flag_level = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if not flag_level:
                if event.type == pygame.KEYDOWN:
                    input_box.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if x_pos in range(306, 501) and y_pos in range(238, 284):
                        flag_level = True
            if flag_level:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    print(x_pos, y_pos)


        draw(screen)       
        if not flag_level:
            input_box.update()
            input_box.draw(screen)
            main_text(screen)
            level_button(screen)
            nickname_button(screen)
            game_button(screen)
        if flag_level:
            change_level(screen, "Level 1", 200)
            change_level(screen, "Level 2", 250)
            change_level(screen, "Level 3", 300)
            change_level(screen, "Level 4", 350)
            change_level(screen, "Level 5", 400)
        clock.tick(FPS)
        pygame.display.flip()
