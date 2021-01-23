import pygame
import sys
import os
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()


class MainPers:
    def __init__(self):
        self.moving_right = False
        self.moving_left = False

    def collision_test(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, rect, movement, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        rect.x += movement[0]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types

    def change_action(self, action, frame, new):
        if action != new:
            action = new
            frame = 0
        return action, frame


def load_animation(path, frame_durations):
    global anim_frames
    anim_name = path.split('/')[-1]
    anim_frame_data = []
    n = 0
    for frame in frame_durations:
        anim_frame_id = anim_name + '_' + str(n + 1)
        image_location = path + '/' + anim_frame_id + '.png'
        animation_image = pygame.image.load(image_location).convert()
        animation_image.set_colorkey((0, 0, 0))
        anim_frames[anim_frame_id] = animation_image.copy()
        for i in range(frame):
            anim_frame_data.append(anim_frame_id)
        n += 1
    return anim_frame_data


def load_image(name):
    # если файл не существует, то выходим
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image


def map_add(filename):
    file = open(filename, 'r')
    data = file.read().split('\n')
    file.close()
    map = list()
    for i in data:
        map.append(list(i))
    return map


def load_image(name):
    # если файл не существует, то выходим
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image


def what_level():
    with open("level.txt", "r+") as f:
        level = f.read()
        return level


def reset_game():
    with open("level.txt", "r+") as f:
        f.seek(0)
        f.write('0')


# starting new level
def next_level(window_size):
    with open("level.txt", "r+") as f:
        prev_level = f.read()
        level = int(prev_level) + 1
        f.seek(0)
        f.write(str(level))
    game(window_size, level)


def draw_pause(window_size, lose, game_win=False):
    pygame.display.set_caption('My game')
    WINDOW_SIZE = window_size
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    while True:
        screen.fill((127, 36, 163))

        # font selecting
        font = pygame.font.Font('fonts/FrakturOmniv1.otf', 90)
        # checking if player losed or won
        if lose:
            text = font.render("YOU LOSE", True, (0, 0, 0))
            nex = font.render("Again", True, (0, 0, 0))
        elif not lose and game_win:
            text = font.render("THE END", True, (0, 0, 0))
            nex = font.render("More", True, (0, 0, 0))
        elif not lose and not game_win:
            text = font.render("YOU WIN", True, (0, 0, 0))
            nex = font.render("NeXt", True, (0, 0, 0))

        # for centring everything
        menu = font.render("Menu", True, (0, 0, 0))
        text_x = screen.get_width() // 2 - text.get_width() // 2
        text_y = screen.get_height() // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()

        pygame.draw.rect(screen, (255, 255, 255), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20))
        pygame.draw.rect(screen, (0, 0, 0), (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 8)

        fir_rect = [text_x // 2, text_y * 1.5]

        pygame.draw.rect(screen, (255, 255, 255), (fir_rect[0], fir_rect[1], text_w, text_h))
        pygame.draw.rect(screen, (0, 0, 0), (fir_rect[0], fir_rect[1], text_w, text_h), 8)

        sec_rect = [text_x // 2 * 3, text_y * 1.5]

        pygame.draw.rect(screen, (255, 255, 255), (sec_rect[0], sec_rect[1], text_w, text_h))
        pygame.draw.rect(screen, (0, 0, 0), (sec_rect[0], sec_rect[1], text_w, text_h), 8)

        screen.blit(menu, (sec_rect[0] + text_w // 3, sec_rect[1]))
        screen.blit(nex, (fir_rect[0] + text_w // 3, fir_rect[1]))
        screen.blit(text, (text_x, text_y))

        # events

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if fir_rect[0] + text_w > mouse[0] > fir_rect[0] and fir_rect[1] + text_h > mouse[1] > fir_rect[1] \
                        and not lose and game_win:
                    reset_game()
                    next_level(window_size)
                if fir_rect[0] + text_w > mouse[0] > fir_rect[0] and fir_rect[1] + text_h > mouse[1] > fir_rect[1] \
                        and not lose:
                    next_level(WINDOW_SIZE)
                if fir_rect[0] + text_w > mouse[0] > fir_rect[0] and fir_rect[1] + text_h > mouse[1] > fir_rect[1] \
                        and lose:
                    game(window_size, what_level())
                if sec_rect[0] + text_w > mouse[0] > sec_rect[0] and sec_rect[1] + text_h > mouse[1] > sec_rect[1]:
                    main_menu(WINDOW_SIZE)

            if event.type == KEYDOWN:
                if event.key == K_q:
                    break
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        surf = pygame.transform.scale(screen, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(60)


def game(window_size=(1280, 720), level=1):
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

    timer = 11
    dt = 0

    font5 = pygame.font.Font(None, 40)

    pygame.display.set_caption('My game')
    WINDOW_SIZE = window_size
    LEVEL = level
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    display = pygame.Surface((WINDOW_SIZE[0] // 2.5, WINDOW_SIZE[1] // 2.5))
    zoom_mode = 0

    lower_wall = load_image('environment/6.png')
    TILE_SIZE = lower_wall.get_width()
    upper_wall = pygame.image.load('environment/5.png')
    right_wall = pygame.image.load('environment/8.png')
    left_wall = pygame.image.load('environment/7.png')
    platform = load_image('environment/1.png')
    door = load_image('environment/2.png')

    global anim_frames
    anim_frames = {}

    try:
        game_map = map_add('maps/map_' + str(LEVEL) + '.txt')
    except:
        draw_pause(WINDOW_SIZE, False, True)

    # animations loading
    anim_database = dict()
    anim_database['run'] = load_animation('person/run', [7, 7, 7, 7, 7, 7])
    anim_database['idle'] = load_animation('person/idle', [30, 30])
    anim_database['jump'] = load_animation('person/jump', [12, 12, 12, 12, 12])
    anim_database['falling'] = load_animation('person/falling', [20, 20, 20, 20, 20])

    player_action = 'idle'
    player_frame = 0
    player_flip = False

    moving_right = False
    moving_left = False
    man = MainPers()
    player_y_momentum = 0
    air_timer = 0
    scroll = [0, 0]

    player_rect = pygame.Rect(150, 1000, 17, 30)

    while True:
        display.fill((127, 36, 163))

        # for camera

        scroll[0] += int((player_rect.x - scroll[0] - WINDOW_SIZE[0] // 6.74) / 15)
        scroll[1] += int((player_rect.y - scroll[1] - WINDOW_SIZE[1] // 4.8) / 15)

        tile_rects = []
        y = 0

        # timer for level
        timer -= dt
        if timer <= 0:
            draw_pause(WINDOW_SIZE, lose=True)
        txt = font5.render(str(round(timer, 2)), True, 'white')
        display.blit(txt, (70, 70))

        # map painting
        for row in game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    display.blit(platform, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '2':
                    display.blit(door, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    door_x = x * TILE_SIZE
                    door_y = y * TILE_SIZE
                if tile == '5':
                    display.blit(upper_wall, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '6':
                    display.blit(lower_wall, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '7':
                    display.blit(left_wall, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '8':
                    display.blit(right_wall, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                x += 1
            y += 1

        # player movement

        player_movement = [0, 0]
        if moving_right:
            player_movement[0] += 3
        if moving_left:
            player_movement[0] -= 3
        player_movement[1] += player_y_momentum
        player_y_momentum += 0.2
        if player_y_momentum > 3:
            player_y_momentum = 3

        # player animations

        if player_movement[0] < 0 and player_movement[1] > 1:
            player_action, player_frame = man.change_action(player_action, player_frame, 'falling')
            player_flip = True
        elif player_movement[0] == 0 and player_movement[1] > 1:
            player_action, player_frame = man.change_action(player_action, player_frame, 'falling')
            player_flip = False
        elif player_movement[0] < 0 and player_movement[1] < -0.5:
            player_action, player_frame = man.change_action(player_action, player_frame, 'jump')
            player_flip = True
        elif player_movement[0] > 0 and player_movement[1] < -0.5:
            player_action, player_frame = man.change_action(player_action, player_frame, 'jump')
            player_flip = False
        elif player_movement[0] == 0 and player_movement[1] < -0.5:
            player_action, player_frame = man.change_action(player_action, player_frame, 'jump')
            player_flip = True
        elif player_movement[0] > 0 and player_movement[1] > 1:
            player_action, player_frame = man.change_action(player_action, player_frame, 'falling')
            player_flip = False
        elif player_movement[0] > 0 and player_movement[1] > 1:
            player_action, player_frame = man.change_action(player_action, player_frame, 'jump')
            player_flip = False
        elif player_movement[0] > 0:
            player_action, player_frame = man.change_action(player_action, player_frame, 'run')
            player_flip = False
        elif player_movement[0] == 0:
            player_action, player_frame = man.change_action(player_action, player_frame, 'idle')
            player_flip = True
        elif player_movement[0] < 0:
            player_action, player_frame = man.change_action(player_action, player_frame, 'run')
            player_flip = True

        player_rect, collisions = man.move(player_rect, player_movement, tile_rects)

        if collisions['bottom']:
            player_y_momentum = 0
            air_timer = 0
        else:
            air_timer += 1

        # animations

        player_frame += 1
        if player_frame >= len(anim_database[player_action]):
            player_frame = 0
        player_image_id = anim_database[player_action][player_frame]
        player_image = anim_frames[player_image_id]

        display.blit(pygame.transform.flip(player_image, player_flip, False),
                     (player_rect.x - scroll[0], player_rect.y - scroll[1]))

        # checking for ending the game

        if player_rect.x >= door_x - 10 and player_rect.x <= door_x + 41 \
                and player_rect.y + 12.5 == door_y + 43.5:
            draw_pause(WINDOW_SIZE, lose=False)

        # game events

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_z:
                    zoom_mode += 1
                    if zoom_mode % 2 == 1:
                        player_rect = pygame.Rect(150, 400, player_image.get_width(), player_image.get_height() - 1)
                        display = pygame.Surface((WINDOW_SIZE[0] // 0.9, WINDOW_SIZE[1] // 0.85))
                    else:
                        player_rect = pygame.Rect(150, 1000, player_image.get_width(), player_image.get_height() - 1)
                        display = pygame.Surface((WINDOW_SIZE[0] // 2.56, WINDOW_SIZE[1] // 2.56))
                if event.key == K_s:
                    player_rect = pygame.Rect(150, 1000, player_image.get_width(), player_image.get_height() - 1)
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_UP:
                    if air_timer < 6:
                        player_y_momentum = -5
                if event.key == K_0:
                    main_menu(WINDOW_SIZE)
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        if zoom_mode % 2 == 1:
            dt = 0
        else:
            dt = clock.tick(60) / 1000


def options_menu(window_size=(1280, 720)):
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('My game')
    WINDOW_SIZE = window_size

    # music
    pygame.mixer.music.load('sounds/menu_music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

    # first font
    f1 = pygame.font.Font('fonts/FrakturOmniv1.otf', 300)

    # third font
    f3 = pygame.font.Font('fonts/FrakturOmniv1.otf', 100)

    # second font
    f2 = pygame.font.Font('fonts/ariblk.ttf', 48)

    fullhd = f2.render('1920x1080', True, (0, 0, 0))
    hd = f2.render('1280x720', True, (0, 0, 0))
    back = f3.render('Back', True, (0, 0, 0))
    name = f1.render('Insanire', True, (255, 255, 255))
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    while True:
        screen.fill((23, 0, 46))
        screen.blit(name, (230, 0))

        # first button
        pygame.draw.rect(screen, (255, 255, 255), (200, 400, 300, 100))
        pygame.draw.rect(screen, (0, 0, 0), (200, 400, 300, 100), 8)

        # second button
        pygame.draw.rect(screen, (255, 255, 255), (450, 550, 300, 100))
        pygame.draw.rect(screen, (0, 0, 0), (450, 550, 300, 100), 8)

        # back button
        pygame.draw.rect(screen, (255, 255, 255), (700, 400, 300, 100))
        pygame.draw.rect(screen, (0, 0, 0), (700, 400, 300, 100), 8)
        screen.blit(hd, (210, 400))
        screen.blit(fullhd, (710, 400))
        screen.blit(back, (500, 555))

        # events
        events = pygame.event.get()

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 200 < mouse[0] < 500 and 400 < mouse[1] < 500:
                    # first button checking
                    screen = pygame.display.set_mode((1280, 720), 0, 32)
                    WINDOW_SIZE = (1280, 720)
                if 700 < mouse[0] < 1000 and 400 < mouse[1] < 500:
                    # second button checking
                    screen = pygame.display.set_mode((1920, 780), 0, 32)
                    WINDOW_SIZE = (1920, 1080)
                if 450 < mouse[0] < 750 and 550 < mouse[1] < 650:
                    # back button checking
                    main_menu(WINDOW_SIZE)

        surf = pygame.transform.scale(screen, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(60)


def main_menu(window_size=(1280, 720)):
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('My game')
    WINDOW_SIZE = window_size

    # music
    pygame.mixer.music.load('sounds/menu_music.mp3')
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play()

    # first font
    f1 = pygame.font.Font('fonts/FrakturOmniv1.otf', 300)

    # rendering name of the game
    name = f1.render('Insanire', True, (255, 255, 255))

    # second font
    f2 = pygame.font.Font('fonts/FrakturOmniv1.otf', 85)

    # rendering start button
    start = f2.render('Start', True, (0, 0, 0))

    # rendering options button
    options = f2.render('Options', True, (0, 0, 0))
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    while True:
        # game name writing
        screen.fill((23, 0, 46))
        screen.blit(name, (230, 0))

        # start button
        pygame.draw.rect(screen, (255, 255, 255), (200, 400, 300, 100))
        pygame.draw.rect(screen, (0, 0, 0), (200, 400, 300, 100), 8)

        # options button
        pygame.draw.rect(screen, (255, 255, 255), (700, 400, 300, 100))
        pygame.draw.rect(screen, (0, 0, 0), (700, 400, 300, 100), 8)
        screen.blit(start, (270, 400))
        screen.blit(options, (760, 400))

        events = pygame.event.get()

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 200 < mouse[0] < 500 and 400 < mouse[1] < 500:
                    pygame.mixer.music.load('sounds/music.mp3')
                    game(WINDOW_SIZE, what_level())
                if 700 < mouse[0] < 1000 and 400 < mouse[1] < 500:
                    options_menu(WINDOW_SIZE)

        surf = pygame.transform.scale(screen, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main_menu()
