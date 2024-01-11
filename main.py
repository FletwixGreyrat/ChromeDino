import random
import pygame

from objects import Ground, Dino, Cactus, Cloud, Ptera, Star

pygame.init()

size = width, height = (600, 200)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
framesPerSecond = 60

# Создание переменных для трех основных цветов цветов
white = (225,225,225)
black = (0, 0, 0)
grey = (32, 33, 36)

# Добавление всех картинок

startImage = pygame.image.load('photos/startImage.png')
startImage = pygame.transform.scale(startImage, (60, 64))

gameOverImage = pygame.image.load('photos/game_over.png')
gameOverImage = pygame.transform.scale(gameOverImage, (200, 36))

numbers_img = pygame.image.load('photos/numbers.png')
numbers_img = pygame.transform.scale(numbers_img, (120, 12))

againImage = pygame.image.load('photos/again.png')
againImage = pygame.transform.scale(againImage, (40, 36))
againRect = againImage.get_rect()
againRect.y = 100
againRect.x = width // 2 - 20


# Загрузка музыки

jumpSound = pygame.mixer.Sound('Sounds/jump.wav')
dieSound = pygame.mixer.Sound('Sounds/die.wav')
every100MetersSound = pygame.mixer.Sound('Sounds/checkPoint.wav')

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
	global dinoSpeed
	global score
	global highScore

	if score and score > highScore:
		highScore = score

	counter = 0
	dinoSpeed = 5
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
# SPEEDUP -> Ускорение

console = []
PPPPPPP = False
TIMESET = False
AAAAAAA = False

# ! Важные переменные

counter = 0
cloud_time = 500
stars_time = 175
enemy_time = 100

dinoSpeed = 5
isjump = False
nagnulsya = False

start_page = True
mouse_pos = (-1, -1)

score = 0
highScore = 0

game = True

# ! Игровой цикл

while game:
	isjump = False
	if TIMESET:
		screen.fill(white)
	else:
		screen.fill(grey)

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
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

			if ''.join(console).upper() == 'TTTTTTT':
				score += 10000

			if ''.join(console).upper() == 'HISCORE':
				highScore = 99999

			if ''.join(console).upper() == 'AAAAAAA':
				AAAAAAA = not AAAAAAA


			if ''.join(console).upper() == 'PPPPPPP':
				PPPPPPP = not PPPPPPP

			if ''.join(console).upper() == 'SPEEDUP':
				dinoSpeed += 2
			
			if ''.join(console).upper() == 'TIMESET':
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
					bird = Ptera(width, y)
					birdSprite.add(bird)

			if counter % 100 == 0:
				dinoSpeed += 0.1
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
						dx = cactus.rect.x - chromeDino.rect.x
						if 0 <= dx <= (70 + (score//100)):
							isjump = True

					if pygame.sprite.collide_mask(chromeDino, cactus):
						dinoSpeed = 0
						chromeDino.alive = False
						dieSound.play()

				for cactus in birdSprite:
					if AAAAAAA:
						dx = bird.rect.x - chromeDino.rect.x
						if 0 <= dx <= 70:
							if chromeDino.rect.top <= bird.rect.top:
								isjump = True
							else:
								nagnulsya = True
						else:
							nagnulsya = False

					if pygame.sprite.collide_mask(chromeDino, bird):
						dinoSpeed = 0
						chromeDino.alive = False
						dieSound.play()
			if score and score % 100 == 0:
				every100MetersSound.play()

		birdSprite.update(dinoSpeed - 1, chromeDino)
		birdSprite.draw(screen)

		background.update(dinoSpeed)
		background.draw(screen)
		
		chromeDino.update(isjump, nagnulsya)
		chromeDino.draw(screen)

		starsSprite.update(dinoSpeed - 3, chromeDino)
		starsSprite.draw(screen)

		caktusSprite.update(dinoSpeed, chromeDino)
		caktusSprite.draw(screen)

		cloudSprite.update(dinoSpeed - 3, chromeDino)
		cloudSprite.draw(screen)
		
		string_score = str(score).zfill(5)
		for i, num in enumerate(string_score):
			intNum = int(num)
			screen.blit(numbers_img, (520 + 11 * i, 10), (intNum * 10, 0, 10, 12))

		if highScore:
			screen.blit(numbers_img, (425, 10), (100, 0, 20, 12))
			string_score = f'{highScore}'.zfill(5)
			for i, num in enumerate(string_score):
				intNum = int(num)
				screen.blit(numbers_img, (455 + 11 * i, 10), (intNum * 10, 0, 10, 12))

		if not chromeDino.alive:
			screen.blit(againImage, againRect)
			screen.blit(gameOverImage, (width // 2 - 100, 55))

			if againRect.collidepoint(mouse_pos):
				reset()

	elif start_page:
		screen.blit(startImage, (50, 100))

	pygame.draw.rect(screen, white, (0, 0, width, height), 4)
	clock.tick(framesPerSecond)
	pygame.display.update()

pygame.quit()