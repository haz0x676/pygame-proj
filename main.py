import pygame
import random

import sys

v = 10
FPS = 60
lost = 0
score = 0
clock = pygame.time.Clock()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
img_hero = "data/spaceship.png"
img_bullet = "data/bullet.png"
img_enemy = "data/asteroid.png"


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
    for i in range(400):
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
        self.txt_surface = pygame.font.Font(
            None, 32).render(text, True, self.color)

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
            self.txt_surface = pygame.font.Font(
                None, 32).render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class GameSprite(pygame.sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        pygame.sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, отрисовывающий героя на окне
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys[pygame.K_d] and self.rect.x < 700:
            self.rect.x += self.speed

    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -10)
        bullets.add(bullet)


class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()


class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > height:
            self.rect.x = random.randint(80, width - 80)
            self.rect.y = 0
            lost = lost + 1


if __name__ == '__main__':
    pygame.display.set_caption("Игра Space Шутер")
    pygame.init()
    bullets = pygame.sprite.Group()
    size = width, height = 800, 700
    screen = pygame.display.set_mode(size)
    monsters = pygame.sprite.Group()
    for i in range(1, 6):
        monster = Enemy(img_enemy, random.randint(80, width - 80), -40, 80, 50, random.randint(1, 5))
        monsters.add(monster)
    input_box = InputBox((width // 2 - 70) - 22, 160, 140, 32)
    flag_level = False
    level = 0

    menu_flag = True
    while menu_flag:
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if x_pos in range(325, 486) and y_pos in range(339, 382):
                        menu_flag = False
            if flag_level:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if x_pos in range(309, 409) and y_pos in range(190, 232):
                        level = 1
                        flag_level = False
                    elif x_pos in range(309, 409) and y_pos in range(270, 310):
                        level = 2
                        flag_level = False
                    elif x_pos in range(309, 409) and y_pos in range(350, 390):
                        level = 3
                        flag_level = False
                    elif x_pos in range(309, 409) and y_pos in range(430, 470):
                        level = 4
                        flag_level = False
                    elif x_pos in range(309, 409) and y_pos in range(510, 550):
                        level = 5
                        flag_level = False

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
            change_level(screen, "Level 2", 280)
            change_level(screen, "Level 3", 360)
            change_level(screen, "Level 4", 440)
            change_level(screen, "Level 5", 520)
        clock.tick(FPS)
        pygame.display.flip()

    all_sprites = pygame.sprite.Group()
    ship = Player(img_hero, 300, 550, 200, 200, 5)
    run = True
    while run:
        screen.fill("black")
        draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ship.fire()

        bullets.draw(screen)
        bullets.update()
        monsters.draw(screen)
        monsters.update()
        collides = pygame.sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, random.randint(80, width - 80), -40, 80, 50, random.randint(1, 5))
            monsters.add(monster)
        ship.reset()
        ship.update()
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()
