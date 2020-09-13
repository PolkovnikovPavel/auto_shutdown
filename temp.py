import os, time
from System import *


def exit(*args):  # завершает программу
    global running
    save()
    running = False


def save():  # сохраняет текущии данные
    pass


def create_all_objects():  # определяет все объекты
    font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 40)
    text = Text(screen, ps_width(6.5), ps_height(50), 'Чтоб отменить нажмите', font, BLACK)
    objects_main.add_objects(text)

    font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 25)
    text = Text(screen, ps_width(10), ps_height(30), 'Выключение через:', font, BLACK)
    objects_main.add_objects(text)


FPS = 100
ratio = 3 / 5  # отношение сторон окна приложения

type_window = 'main_window'  # опредиление типа окна

size = 500
size = width, height = int(size), int(size * ratio)
print(size)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 30)
screen = pygame.display.set_mode(size)
install_size(size)  # инсталяция итоговых размеров окна для дальнейшей работы

objects_main = Group()
create_all_objects()


running = True
is_press = False
is_close = False
font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 25)
text = Text(screen, ps_width(58), ps_height(30), '5 мин. 00 сек.', font, BLACK)
timer = time.time()
time_disconnection = 300
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)  # поддержка фпс
    screen.fill(WHITE)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            is_press = True

        if event.type == pygame.MOUSEBUTTONUP:
            if is_press:
                exit()

        if event.type == pygame.MOUSEMOTION:
            pass
    now = time.time() - timer

    if type_window == 'main_window':
        objects_main.show()
        min = int(time_disconnection - now) // 60
        sec = int(time_disconnection - now) - min * 60
        text.change_text(f'{min} мин. {sec} сек.')
        text.show()

    pygame.display.flip()  # обновление экрана

    if now >= time_disconnection:
        running = False
        is_close = True



pygame.quit()

if is_close:
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

