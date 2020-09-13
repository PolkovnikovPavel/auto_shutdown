import pygame
import time, time, copy, random
import sqlite3


pygame.init()

WHITE = (255, 255, 255)  # установка цветов
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 0, 255)
LIGHT_GREEN = (27, 65, 16)
BROWN = (74, 47, 4)
GRAY = (128, 128, 128)


width, height = 0, 0


def install_size(size):  # инициализация
    global width, height
    width, height = size


def ps_height(percent):  # возрощает число процентов от высоты
    percent = percent / 100
    return int(height * percent)


def ps_width(percent):  # возрощает число процентов от ширены
    percent = percent / 100
    return int(width * percent)


class Object:  # любой граффический объект
    def __init__(self, canvas, image, x, y, width, height):
        self.canvas = canvas
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visibility = True

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def change_image(self, image):
        self.image = image

    def check_tip(self, x, y):  # проверка на принодлежность х и у в объекте
        if self.visibility:
            return (x >= self.x and x <= self.x + self.width and y >= self.y and
                    y <= self.y + self.height)

    def show(self):  # отобразить
        if self.visibility:
            self.canvas.blit(self.image, (self.x, self.y))


class Text(Object):  # объект текст
    def __init__(self, canvas, x, y, text, font, color=WHITE):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.text = str(text)
        self.font = font
        self.visibility = True
        self.color = color
        self.height = len(str(self.text).split('\n')) * ps_height(2)

    def change_text(self, new_text):
        self.text = str(new_text)

    def show(self):  # отобразить построчно
        if not self.visibility:
            return
        texts = str(self.text).split('\n')
        for i in range(len(texts)):
            text = self.font.render(texts[i], 1, self.color)
            self.canvas.blit(text, (self.x, int(self.y + i * ps_height(2))))


class Button(Object):  # кнопка
    def __init__(self, canvas, image, x, y, width, height, function=None, image_animation=None):
        self.canvas = canvas
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = [function]
        self.image_animation = image_animation
        self.visibility = True
        self.status = False

    def add_function(self, function):  # добовляет функцию
        if self.function == [None]:
            self.function = [function]
        else:
            self.function.append(function)

    def get_function(self, function):  # устонавливает одну функцию
        self.function = [function]

    def del_function(self):  # удоляет все функции
        self.function = [None]

    def get_image_animation(self, image):  # установка анимации при нажатии
        self.image_animation = image

    def show_animation(self):  # отобразить анимацию
        if self.image_animation is not None:
            self.canvas.blit(self.image_animation, (self.x, self.y))
        else:
            self.canvas.blit(self.image, (self.x, self.y))

    def click(self, *args):  # запустить все функции
        if self.function == [None] or not self.visibility:
            return False
        for function in self.function:
            try:
                return function(args)
            except:
                print('не удалось запустить функцию')
                return False

    def show(self):  # отобразить
        if self.visibility:
            if self.status:
                self.show_animation()
                return
            self.canvas.blit(self.image, (self.x, self.y))


class Group:  # группа
    def __init__(self):
        self.all_objects = []
        self.last_x, self.last_y = 0, 0
        self.visibility = True

    def add_objects(self, *objects):
        for object in objects:
            self.all_objects.append(object)

    def delete(self, *objects):
        if len(objects) == 0:
            self.all_objects = []
        for object in objects:
            del self.all_objects[self.all_objects.index(object)]

    def off_all(self):
        for object in self.all_objects:
            object.visibility = False

    def on_all(self):
        for object in self.all_objects:
            object.visibility = True

    def check(self, event):  # проверка событий
        if not self.visibility:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            self.last_x, self.last_y = x, y
            for object in self.all_objects:
                if isinstance(object, Button):
                    if object.check_tip(x, y):
                        object.status = True


        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            for object in self.all_objects:
                if isinstance(object, Button):
                    if object.status and object.check_tip(x, y):
                        object.click()
                    object.status = False


    def show(self):  # отображение
        for object in self.all_objects:
            object.show()
