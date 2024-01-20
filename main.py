import random
import pygame
pygame.init()
      
file = open('score.txt', 'r')
if len(file.read()) == 0:
    file.close()
    file = open('score.txt', 'w')
    file.write('0')
    highScore = 0
    file.close()

sc = WIDTH, HEIGHT = (600, 200)



class Ground:
    def __init__(self):
        self.image = pygame.image.load("photos/ground.png")
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()

        self.coordX2 = self.width
        self.y = 150
        self.coordX1 = 0

    def update(self, valueV):
        self.coordX2 -= valueV
        self.coordX1 -= valueV

        if not (self.coordX2 > -self.width):
            self.coordX2 = self.width

        if not (self.coordX1 > -self.width):
            self.coordX1 = self.width

    def draw(self, sc):
        sc.blit(self.image, (self.coordX2, self.y))
        sc.blit(self.image, (self.coordX1, self.y))


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super(Star, self).__init__()
        image = pygame.image.load(f"photos/stars.png")
        self.imageList = []
        for i in range(3):
            img = image.subsurface((0, 20 * (i), 18, 18))
            self.imageList.append(img)
        self.image = self.imageList[type - 1]
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def draw(self, sc):
        sc.blit(self.image, self.rect)

    def update(self, valueV, dino):
        if dino.alive:
            self.rect.x -= valueV
            if not (self.rect.right > 0):
                self.kill()


class Cactus(pygame.sprite.Sprite):
    def __init__(self, type):
        super(Cactus, self).__init__()

        self.imageList = []
        for i in range(5):
            scale = 0.65
            img = pygame.image.load(f"photos/Cactus/{i+1}.png")
            w1, h1 = img.get_size()
            img = pygame.transform.scale(img, (int(w1 * scale), int(h1 * scale)))
            self.imageList.append(img)

        self.image = self.imageList[type - 1]
        self.rect = self.image.get_rect()
        self.rect.bottom = 165
        self.rect.x = WIDTH + 10

    def update(self, valueV, dino):
        if dino.alive:
            self.rect.x -= valueV
            if not (self.rect.right > 0):
                self.kill()

            self.mask = pygame.mask.from_surface(self.image)

    def draw(self, sc):
        sc.blit(self.image, self.rect)


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bird, self).__init__()

        self.imageList = []
        for i in range(2):
            scale = 0.65
            img = pygame.image.load(f"photos/Bird/{i + 1}.png")
            w1, h1 = img.get_size()
            img = pygame.transform.scale(img, (int(w1 * scale), int(h1 * scale)))
            self.imageList.append(img)

        self.ind = 0
        self.image = self.imageList[self.ind]
        self.rect = self.image.get_rect(center=(x, y))

        self.counter = 0

    def draw(self, sc):
        sc.blit(self.image, self.rect)

    def update(self, valueV, dino):
        if dino.alive:
            self.rect.x -= valueV
            if not (self.rect.right > 0):
                self.kill()

            self.counter += 1
            if not (self.counter < 6):
                self.ind = (self.ind + 1) % len(self.imageList)
                self.image = self.imageList[self.ind]
                self.counter = 0

            self.mask = pygame.mask.from_surface(self.image)


class Dino:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.runList = []
        self.nagnulsyaList = []

        for i in range(1, 4):
            img = pygame.image.load(f"photos/Dino/{i}.png")
            img = pygame.transform.scale(img, (52, 58))
            self.runList.append(img)

        for i in range(4, 6):
            img = pygame.image.load(f"photos/Dino/{i}.png")
            img = pygame.transform.scale(img, (70, 38))
            self.nagnulsyaList.append(img)

        self.deadImage = pygame.image.load(f"photos/Dino/8.png")
        self.deadImage = pygame.transform.scale(self.deadImage, (52, 58))

        self.reset()

        self.isJumping = False
        self.gravity = 1
        self.jumpHeight = 15
        self.vel = 0

    def draw(self, sc):
        sc.blit(self.image, self.rect)

    def update(self, jump, nagnulsya):
        if self.alive:
            if not self.isJumping and jump:
                self.vel = -self.jumpHeight
                self.isJumping = True

            self.vel += self.gravity
            if not (self.vel < self.jumpHeight):
                self.vel = self.jumpHeight

            self.rect.y += self.vel
            if self.rect.bottom > self.y:
                self.rect.bottom = self.y
                self.isJumping = False

            if nagnulsya:
                self.counter += 1
                if self.counter >= 6:
                    self.ind = (self.ind + 1) % len(self.nagnulsyaList)
                    self.image = self.nagnulsyaList[self.ind]
                    self.rect = self.image.get_rect()
                    self.rect.x = self.x
                    self.rect.bottom = self.y
                    self.counter = 0

            elif self.isJumping:
                self.ind = 0
                self.counter = 0
                self.image = self.runList[self.ind]
            else:
                self.counter += 1
                if self.counter >= 4:
                    self.ind = (self.ind + 1) % len(self.runList)
                    self.image = self.runList[self.ind]
                    self.rect = self.image.get_rect()
                    self.rect.x = self.x
                    self.rect.bottom = self.y
                    self.counter = 0

            self.mask = pygame.mask.from_surface(self.image)

        else:
            self.image = self.deadImage

    def reset(self):
        self.ind = 0
        self.image = self.runList[self.ind]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.bottom = self.y

        self.alive = True
        self.counter = 0


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Cloud, self).__init__()
        self.image = pygame.image.load(f"photos/cloud.png")
        self.image = pygame.transform.scale(self.image, (60, 18))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def update(self, valueV, dino):
        if dino.alive:
            self.rect.x -= valueV
            if not (self.rect.right > 0):
                self.kill()

    def draw(self, sc):
        sc.blit(self.image, self.rect)

size = width, height = (600, 200)
sc = pygame.display.set_mode(size)

clock = pygame.time.Clock()
framesPerSecond = 60

# Создание переменных для трех основных цветов цветов
white = (225, 225, 225)
black = (0, 0, 0)
grey = (32, 33, 36)

# Добавление всех картинок

startImage = pygame.image.load("photos/startImage.png")
startImage = pygame.transform.scale(startImage, (60, 64))

gameOverImage = pygame.image.load("photos/game_over.png")
gameOverImage = pygame.transform.scale(gameOverImage, (200, 36))

numbers_img = pygame.image.load("photos/numbers.png")
numbers_img = pygame.transform.scale(numbers_img, (120, 12))

againImage = pygame.image.load("photos/again.png")
againImage = pygame.transform.scale(againImage, (40, 36))
againRect = againImage.get_rect()
againRect.y = 100
againRect.x = width // 2 - 20

# Загрузка музыки

jumpSound = pygame.mixer.Sound("sound/jump.wav")
dieSound = pygame.mixer.Sound("sound/die.wav")
every100MetersSound = pygame.mixer.Sound("sound/checkPoint.wav")

# Создание нужных компонентов (окружение, динозавр, кактус, птица)

background = Ground()
chromeDino = Dino(50, 160)

caktusSprite = pygame.sprite.Group()
birdSprite = pygame.sprite.Group()
cloudSprite = pygame.sprite.Group()
starsSprite = pygame.sprite.Group()

# Функция сброса


def reset():
    global counter
    global dinovalueV
    global score
    global highScore

    if score and score > highScore:
        highScore = score

    counter = 0
    dinovalueV = 5
    score = 0

    starsSprite.empty()

    cloudSprite.empty()

    caktusSprite.empty()

    birdSprite.empty()

    chromeDino.reset()


# Читы для игрового цикла (С отсылками на различные игры)

# PPPPPPP - Неуязвимость
# !  Отсылка на ГТА. Чит выполняет аналогичную функцию с игрой от RockStar (PAINKILLER)
# TIMESET - Смена дня и ночи (отсылка на Майнкрафт)
# AAAAAAA - Имитация искуственного интеллекта (Динозавр совершает автопрыжок в самом выгодном месте)
# TTTTTTT -> добавляет десять тысяч очков к рекорду
# HISCORE -> Устанавливает лучший результат в 99999
# SSSSSSS -> Ускорение

console = []
PPPPPPP = False
TIMESET = False
AAAAAAA = False

# ! Важные переменные

counter = 0
cloud_time = 500
stars_time = 175
enemy_time = 100

dinovalueV = 5
isjump = False
nagnulsya = False

start_page = True
mouse_pos = (-1, -1)

score = 0

game = True

# ! Игровой цикл

while game:
    isjump = False
    if TIMESET:
        sc.fill(white)
    else:
        sc.fill(grey)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            file = open('score.txt', 'w')
            file.write(highScore)
            file.close()
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                isjump = True
                jumpSound.play()

            if event.key == pygame.K_DOWN:
                nagnulsya = True

            if event.key == pygame.K_SPACE:
                if start_page:
                    start_page = False
                elif chromeDino.alive:
                    jumpSound.play()
                    isjump = True
                else:
                    reset()

            if event.key == pygame.K_ESCAPE:
                exit()

            key = pygame.key.name(event.key)
            console.append(key)
            console = console[-7:]

            if "".join(console).upper() == "TTTTTTT":
                score += 10000

            if "".join(console).upper() == "HISCORE":
                highScore = 99999

            if "".join(console).upper() == "AAAAAAA":
                AAAAAAA = not AAAAAAA

            if "".join(console).upper() == "PPPPPPP":
                PPPPPPP = not PPPPPPP

            if "".join(console).upper() == "SSSSSSS":
                dinovalueV += 2

            if "".join(console).upper() == "TIMESET":
                TIMESET = not TIMESET

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_DOWN:
                nagnulsya = False

            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                isjump = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = (-1, -1)

    if not start_page:
        if chromeDino.alive:
            counter += 1

            if counter % cloud_time == 0:
                y = random.randint(40, 100)
                cloud = Cloud(width, y)
                cloudSprite.add(cloud)

            if counter % int(enemy_time) == 0:

                if not (random.randint(1, 10) == 5):
                    type = random.randint(1, 4)
                    cactus = Cactus(type)
                    caktusSprite.add(cactus)

                elif random.randint(1, 10) == 5:
                    y = random.choice([85, 130])
                    bird = Bird(width, y)
                    birdSprite.add(bird)

            if counter % 100 == 0:
                dinovalueV += 0.1
                enemy_time -= 0.5

            if counter % 5 == 0:
                score += 1

            if counter % stars_time == 0:
                type = random.randint(1, 3)
                y = random.randint(40, 100)
                star = Star(width, y, type)
                starsSprite.add(star)

            if not PPPPPPP:
                for cactus in caktusSprite:
                    if AAAAAAA:
                        deltaX = cactus.rect.x - chromeDino.rect.x
                        if 0 <= deltaX <= (70 + (score // 100)):
                            isjump = True

                    if pygame.sprite.collide_mask(chromeDino, cactus):
                        dinovalueV = 0
                        chromeDino.alive = False
                        dieSound.play()

                for cactus in birdSprite:
                    if AAAAAAA:
                        deltaX = bird.rect.x - chromeDino.rect.x
                        if 0 <= deltaX <= 70:
                            if chromeDino.rect.top <= bird.rect.top:
                                isjump = True
                            else:
                                nagnulsya = True
                        else:
                            nagnulsya = False

                    if pygame.sprite.collide_mask(chromeDino, bird):
                        dinovalueV = 0
                        chromeDino.alive = False
                        dieSound.play()
            if score and score % 100 == 0:
                every100MetersSound.play()

        birdSprite.update(dinovalueV - 1, chromeDino)
        birdSprite.draw(sc)

        background.update(dinovalueV)
        background.draw(sc)

        chromeDino.update(isjump, nagnulsya)
        chromeDino.draw(sc)

        starsSprite.update(dinovalueV - 3, chromeDino)
        starsSprite.draw(sc)

        caktusSprite.update(dinovalueV, chromeDino)
        caktusSprite.draw(sc)

        cloudSprite.update(dinovalueV - 3, chromeDino)
        cloudSprite.draw(sc)

        string_score = str(score).zfill(5)
        for i, num in enumerate(string_score):
            intNum = int(num)
            sc.blit(numbers_img, (520 + 11 * i, 10), (intNum * 10, 0, 10, 12))

        if highScore:
            sc.blit(numbers_img, (425, 10), (100, 0, 20, 12))
            string_score = f"{highScore}".zfill(5)
            for i, num in enumerate(string_score):
                intNum = int(num)
                sc.blit(numbers_img, (455 + 11 * i, 10), (intNum * 10, 0, 10, 12))

        if not chromeDino.alive:
            sc.blit(againImage, againRect)
            sc.blit(gameOverImage, (width // 2 - 100, 55))

            if againRect.collidepoint(mouse_pos):
                reset()

    elif start_page:
        sc.blit(startImage, (50, 100))

    pygame.draw.rect(sc, white, (0, 0, width, height), 4)
    clock.tick(framesPerSecond)
    pygame.display.update()

pygame.quit()