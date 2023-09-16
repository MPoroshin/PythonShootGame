import pygame # импорт модуля pygame


SCREEN_WIDTH = 480 # задаем константу ширины окна
SCREEN_HEIGHT = 800 # задаем константу высоты окна


# класс снаряд, наследуется от класса Sprite, который реализует возможности работы со спрайтами
class Bullet(pygame.sprite.Sprite):
	def __init__(self, bullet_img, init_pos): # конструктор класса
		pygame.sprite.Sprite.__init__(self) # конструктор родительского класса
		# заполнение полей объекта
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.midbottom = init_pos
		self.speed = 10


	def move(self): # метод объекта Bullet, реализующий передвижение объекта с заданной скоростью speed
		self.rect.top -= self.speed



# класс игрок, наследуется от класса Sprite, который реализует возможности работы со спрайтами
class Player(pygame.sprite.Sprite):
	def __init__(self, plane_img, player_rect, init_pos): # конструктор класса
		pygame.sprite.Sprite.__init__(self) # конструктор родительского класса

		# заполнение и инициализация полей класса
		self.image = []
		for i in range(len(player_rect)):
			self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
		self.rect = player_rect[0]
		self.rect.topleft = init_pos
		self.speed = 8
		self.bullets = pygame.sprite.Group()
		self.img_index = 0
		self.is_hit = False

	# реализация выстрела от игрока, с добавлением объекта класса Bullet в группу спрайтов bullets
	def shoot(self, bullet_img):
		bullet = Bullet(bullet_img, self.rect.midtop)
		self.bullets.add(bullet)

	# ряд функций реализующих передвижение игрока в четырех направлениях с заданной скоростью speed
	def moveUp(self):
		if self.rect.top <= 0:
			self.rect.top = 0
		else:
			self.rect.top -= self.speed

	def moveDown(self):
		if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
			self.rect.top = SCREEN_HEIGHT - self.rect.height
		else:
			self.rect.top += self.speed

	def moveLeft(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		else:
			self.rect.left -= self.speed

	def moveRight(self):
		if self.rect.left >= SCREEN_WIDTH - self.rect.width:
			self.rect.left = SCREEN_WIDTH - self.rect.width
		else:
			self.rect.left += self.speed

# класс враг, наследуется от класса Sprite, который реализует возможности работы со спрайтами
class Enemy(pygame.sprite.Sprite):
	def __init__(self, enemy_img, enemy_down_imgs, init_pos): # конструктор класса
		pygame.sprite.Sprite.__init__(self) # конструктор родительского класса
		# заполнение и инициализация полей класса
		self.image = enemy_img
		self.rect = self.image.get_rect()
		self.rect.topleft = init_pos
		self.down_imgs = enemy_down_imgs
		self.speed = 2
		self.down_index = 0

	# метод, реализующий передвижение врага с заданной скоростью speed
	def move(self):
		self.rect.top += self.speed