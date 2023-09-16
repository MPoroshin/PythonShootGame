import random # импорт модуля рандом
from sys import exit # импортфункции выхода из приложения

from pygame.locals import * # импорт вспомогательных методов из библиотеки pygame

from gameRole import * # импорт функционала из файла проекта

pygame.init() # инициализация pygame проекта
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # создание объекта окна с константами, определенными в другом файле
pygame.display.set_caption('ShootGame') # установка заголовка окна приложения


bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')  # создание объекта звука для пули
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav') # создание объекта звука для врагов
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav') # создание объекта звука для проигрыша
# устновка громкости для звуков, относительно общей громкости звуков
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0) # запуск звуков
pygame.mixer.music.set_volume(0.25) # утсновка общей громкости


background = pygame.image.load('resources/image/background.png').convert() # создание и объекта фона
game_over = pygame.image.load('resources/image/gameover.png') # создание объекта картинки для проигрыша

filename = 'resources/image/shoot.png' # путь до файла
plane_img = pygame.image.load(filename) # создание объекта выстрела


player_rect = [] # массив

# область игрока
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600] # позиция игрока в окне
player = Player(plane_img, player_rect, player_pos) # создание объекта игрок


bullet_rect = pygame.Rect(1004, 987, 9, 21) # область снаряда
bullet_img = plane_img.subsurface(bullet_rect) # настройка расположения изображения снаряда


enemy1_rect = pygame.Rect(534, 612, 57, 43) # область врага
enemy1_img = plane_img.subsurface(enemy1_rect) # настройка расположения изображения врага
enemy1_down_imgs = []
# добавление изображений врагов
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group() # создание группы слайдов для врагов


enemies_down = pygame.sprite.Group() # создание группы слайдов для врагов

shoot_frequency = 0 # частота выстрелов
enemy_frequency = 0 # частота врагов

player_down_index = 16 # значение падения игрока

score = 0 # очки

clock = pygame.time.Clock() # создание объекта часов

running = True # переменная цикла для осуществления бесконечного цикла

while running: # бесконечный цикл

    clock.tick(45) # задание частоты выполнения цикла


    if not player.is_hit: # условие, если игрок не задет
        # если частота выстрелов удовлетворяет условию, воспроиведение звука и осущесление выстрела
        if shoot_frequency % 15 == 0:
            bullet_sound.play()
            player.shoot(bullet_img)
        shoot_frequency += 1 # добавление частоты
        if shoot_frequency >= 15: # если частота выстрела больше 15
            shoot_frequency = 0 # обнуление частоты выстрела


    if enemy_frequency % 50 == 0: # частота врагов
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0] # случайное появление игроков
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos) # создание врага
        enemies1.add(enemy1) # добавление нового врага в группу спрайтов
    enemy_frequency += 1 # добавление частоты появления врагов
    if enemy_frequency >= 100: # обнуление частоты врагов, если частота превысила 100
        enemy_frequency = 0

    # движение снарядов, если зашли за край экрана - удаление из группы спрайтов
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)


    for enemy in enemies1: # движение врагов
        enemy.move()
        # столкновение игрока с врагом
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        # удаление врага, если зашел за край
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy)

    # проверка пересечения снарядов игрока и врагов
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)
        # поражение врага если снаряд попал


    screen.fill(0) # очищение окна
    screen.blit(background, (0, 0)) # заполнение фоном

    # если игрок не задет - добавление игрока в окно
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)


        player.img_index = shoot_frequency // 8 # частота выстрелов игрока
    else:
        # если задет остановка игры с поражение игркоа
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False

    # счетчик очков за задетых врагов
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1


    player.bullets.draw(screen) # отображение снарядов в окне
    enemies1.draw(screen) # отрисовка противников


    score_font = pygame.font.Font(None, 36) # шрифт
    score_text = score_font.render(str(score), True, (128, 128, 128)) # настройки шрифта
    text_rect = score_text.get_rect() # получение прямоугольника текста
    text_rect.topleft = [10, 10] # задание области
    screen.blit(score_text, text_rect) # размещение текста в окне


    pygame.display.update() # обновление окна

    # выход из приложения при нажатии кнопки закрытия окна
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            

    key_pressed = pygame.key.get_pressed() # получение объекта нажатия

    if not player.is_hit: # условие если игрок не задет
        # условия нажатия кнопок - осуществление перемещения игрока
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()


font = pygame.font.Font(None, 48) # создание объекта текста
text = font.render('Score: '+ str(score), True, (255, 0, 0)) # настрйока текста
text_rect = text.get_rect() # получение прямоугольника текста
text_rect.centerx = screen.get_rect().centerx # координаты прямоугольника
text_rect.centery = screen.get_rect().centery + 24 # координыты прямоугольника
screen.blit(game_over, (0, 0)) # размещение
screen.blit(text, text_rect) # размещение текста на дисплее

while 1: # бесконечный цикл
    for event in pygame.event.get(): # получение событий
        if event.type == pygame.QUIT: # условие выхода из приложения
            pygame.quit() # выход из программы
            exit() # закрытие приложения
    pygame.display.update() # обновление дисплея
