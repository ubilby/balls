# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random

WIDTH = 1024  # ширина
HEIGHT = 512  # высота окна
FPS = 60  # частота кадров в секунду


# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
# создаем экземпляр часов, для регуляции частоты кадров
clock = pygame.time.Clock()


# создаем класс врагов
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        # инициализируем спрайт, задаем его параметры
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


# наследуемся от pygame.sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # запускаем инициализатор встроенных классов
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))  # задаем форму и размер
        self.image.fill(GREEN)  # заполняем цветом
        # get_rect() оценивает изображение image и обрисовывает его
        self.rect = self.image.get_rect()
        # отрисовываем изображение по центру
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

# для каждого спрайта определена фунция update, она описывает поведение спрайта в каждом кадре
# pygame.key.get_pressed() возвращает словарь нажата кнопка или нет - для всех кнопок
    def update(self):
        self.speedx = 0
        # проверяем какая нажата кнопка
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        # проверка не уходит ли герой с экрана
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        """Метод создает пулю, и в качестве места старта задает верхгюю часть
        спрайта игрока"""
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# спрайт пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


# нужно создать группу спрайтов
all_sprites = pygame.sprite.Group()
# создаем спрайт игрока
player = Player()
# добавляем спрайт в группу
all_sprites.add(player)
# добавляем группу для пуль
bullets = pygame.sprite.Group()
# тоже самое с мобами
mobs = pygame.sprite.Group()
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление
    all_sprites.update()
    # проверим, не не попал ли игрок по врагам
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    # Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    # Рендеринг (Отрисовка)
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()


pygame.quit()
