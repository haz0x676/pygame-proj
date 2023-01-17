import pygame
import random
import json
import sys

pygame.font.init()
font1 = pygame.font.SysFont('Arial', 80)
v = 13
finish_lose = False
finish_win = False

FPS = 45
lost = 0
font2 = pygame.font.SysFont('Arial', 36)
lose = font1.render('ВЫ ПРОИГРАЛИ!', True, (180, 0, 0))
win = font1.render('ВЫ ВЫИГРАЛИ', True, (0, 255, 0))
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
    for i in range(200):
        screen.fill(pygame.Color('white'),
                    (random.random() * width,
                     random.random() * height, 1, 1))


def terminate():
    pygame.quit()
    sys.exit()


def create_button(screen, info, x, y):
    font = pygame.font.Font(None, 35)
    text = font.render(info, True, (30, 144, 255))
    text_x = x
    text_y = y
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 255), (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 1)


def read_json(file_name):
    with open(file_name) as input_file:
        data = json.load(input_file)
    return data


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
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, hp=1):
        # Вызываем конструктор класса (Sprite):
        pygame.sprite.Sprite.__init__(self)
        self.hp = hp
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

        if keys[pygame.K_d] and self.rect.x < 620:
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
            lost += 1


if __name__ == '__main__':
    pygame.display.set_caption("Игра Space Шутер")
    pygame.init()
    size = width, height = 800, 700
    screen = pygame.display.set_mode(size)
    input_box = InputBox((width // 2 - 70) - 22, 160, 140, 32)
    flag_level = False
    level = 1
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
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
                        if x_pos in range(310, 499) and y_pos in range(241, 278):
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
                create_button(screen, "Level 1", width // 2 - 82, 200)
                create_button(screen, "Level 2", width // 2 - 82, 280)
                create_button(screen, "Level 3", width // 2 - 82, 360)
                create_button(screen, "Level 4", width // 2 - 82, 440)
                create_button(screen, "Level 5", width // 2 - 82, 520)
            clock.tick(FPS)
            pygame.display.flip()
        game_running = True
        while game_running:
            all_sprites = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            monsters = pygame.sprite.Group()
            ship = Player(img_hero, 300, 550, 200, 200, 5)
            run = True
            score = 0

            min_speed, goal_score, max_speed, limit, hp, bullets_cnt = map(int, read_json("levels.json")[
                f"level_{level}"].values())

            for i in range(1, 3):
                monster = Enemy(img_enemy, random.randint(80, width - 80), -40, 80, 50,
                                random.randint(min_speed, max_speed), hp)
                monsters.add(monster)

            while run:
                screen.fill("black")
                draw(screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if bullets_cnt > 0:
                                ship.fire()
                                bullets_cnt -= 1
                text = font2.render("Счет: " + str(score), True, (255, 255, 255))
                screen.blit(text, (10, 20))

                text_lose = font2.render("Пропущено: " + str(lost), True, (255, 255, 255))
                screen.blit(text_lose, (10, 50))

                text_bullets = font2.render("Количество пуль: " + str(bullets_cnt), True, (255, 255, 255))
                screen.blit(text_bullets, (10, 80))

                bullets.draw(screen)
                bullets.update()
                monsters.draw(screen)
                monsters.update()
                collides = pygame.sprite.groupcollide(monsters, bullets, False, True)
                # этот цикл повторится столько раз, сколько монстров подбито
                for c in collides:
                    c.hp -= 1
                    if c.hp == 0:
                        c.kill()
                        score += 1
                        monster = Enemy(img_enemy, random.randint(80, width - 80), -40, 80, 50, random.randint(1, 5),
                                        hp)
                        monsters.add(monster)
                if pygame.sprite.spritecollide(ship, monsters, False) or lost >= limit:
                    run = False
                    finish_lose = True
                if goal_score == score:
                    run = False
                    finish_win = True
                ship.reset()
                ship.update()
                clock.tick(FPS)
                pygame.display.flip()

            screen.blit(lose, (100, 200))
            while finish_lose:
                draw(screen)
                screen.blit(lose, (80, 200))
                create_button(screen, 'Выйти в главное меню', 80, 550)
                create_button(screen, "Попробовать заново", 450, 550)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x_pos, y_pos = event.pos
                        if x_pos in range(71, 360) and y_pos in range(540, 579):
                            finish_lose = False
                            game_running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x_pos, y_pos = event.pos
                        if x_pos in range(442, 709) and y_pos in range(542, 581):
                            finish_lose = False
                            game_running = True
                pygame.display.flip()
            while finish_win:
                draw(screen)
                screen.blit(win, (80, 200))
                create_button(screen, 'Выйти в главное меню', 80, 550)
                create_button(screen, "Попробовать заново", 450, 550)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x_pos, y_pos = event.pos
                        if x_pos in range(71, 360) and y_pos in range(540, 579):
                            finish_win = False
                            game_running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x_pos, y_pos = event.pos
                        if x_pos in range(442, 709) and y_pos in range(542, 581):
                            finish_win = False
                            game_running = True

                pygame.display.flip()
