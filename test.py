# https://metanit.com/python/tkinter/2.1.php

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json








class Behaviour(tk.Tk):
    SOURCE_RESOLUTION = 'resolution_data.json'  # имя файла для данных разрешения
    ICON_PATH = 'world_of_tanks.ico'

    def __init__(self):
        """

        """
        super().__init__()
        self.RESOLUTION_DICT = self.json_reading(__class__.SOURCE_RESOLUTION)  # чтение параметров

    @staticmethod
    def print_info(widget, depth=0) -> None:
        """
        Печатает информацию о виджетах (TODO в отдельном окне, вызывается по кнопке, и клику по виджету)
        """
        widget_class = widget.winfo_class()  # получение информации класса виджета
        widget_width = widget.winfo_width()  # получение информации ширины виджета
        widget_height = widget.winfo_height()  # получение информации высоты виджета
        widget_x = widget.winfo_x()  # получение информаци координаты х верхнего левого угла виджета относительно родительского элемента
        widget_y = widget.winfo_y()  # получение информации координаты у верхнего левого угла виджета относительно родительского элемента
        widget_rootx = widget.winfo_rootx()  # получение информаци координаты х верхнего левого угла виджета относительно экрана
        widget_rooty = widget.winfo_rooty()  # получение информации координаты у верхнего левого угла виджета относительно экрана
        print(
            '\t' * depth + \
            f"{widget_class}\twight={widget_width}\theight={widget_height}\t"
            f"x_parent={widget_x}\t\ty_parent={widget_y}\t\t"
            f"x_screen={widget_rootx}\ty_screen={widget_rooty}"
        )
        # рекурсикная печать всех параметров вложенных виджетов
        for widget in widget.winfo_children():
            __class__.print_info(widget, depth + 1)

    def set_settings(self):
        self.attributes('-fullscreen',
                          False)  # полноэкранный режим (TODO добавить)
        self.attributes('-toolwindow',
                          False)  # наличие верхней панели (TODO добавить)

        # вычисление координат расположения окна
        if self.RESOLUTION_DICT['ON_CENTER_X']['value']:
            X_COORDINATE = self.RESOLUTION_DICT['X_RESOLUTION']['value'] // 2 - \
                           self.RESOLUTION_DICT['WIGHT']['value'] // 2
        else:
            if self.RESOLUTION_DICT['IS_LEFT']['value']:
                X_COORDINATE = \
                    self.RESOLUTION_DICT['X_INDENT']['value']
            else:
                X_COORDINATE = \
                    self.RESOLUTION_DICT['X_RESOLUTION']['value'] - \
                    self.RESOLUTION_DICT['WIGHT']['value'] - \
                    self.RESOLUTION_DICT['X_INDENT']['value']
        if self.RESOLUTION_DICT['ON_CENTER_Y']['value']:
            Y_COORDINATE = \
                self.RESOLUTION_DICT['Y_RESOLUTION']['value'] // 2 - \
                self.RESOLUTION_DICT['HEIGHT']['value'] // 2
        else:
            if self.RESOLUTION_DICT['IS_UP']['value']:
                Y_COORDINATE = \
                    self.RESOLUTION_DICT['Y_INDENT']['value']
            else:
                Y_COORDINATE = \
                    self.RESOLUTION_DICT['Y_RESOLUTION']['value'] - \
                    self.RESOLUTION_DICT['HEIGHT']['value'] - \
                    self.RESOLUTION_DICT['Y_INDENT']['value']
        resolution = str(self.RESOLUTION_DICT['WIGHT']['value']) + 'x' + \
                     str(self.RESOLUTION_DICT['HEIGHT']['value']) + '+' + \
                     str(X_COORDINATE) + '+' + \
                     str(Y_COORDINATE)
        # задание размера окна
        self.geometry(resolution)
        self.resizable(
            self.RESOLUTION_DICT['RESIZABLE_Y']['value'],
            self.RESOLUTION_DICT['RESIZABLE_X']['value']
        )

    # запись параметров экрана в файл
    @staticmethod
    def json_writing(data: dict, source: str) -> None:
        """
        Функция записывает словарь данных
        data - что записывать
        source - куда записывать
        """
        with open(source, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def json_reading(source: str) -> dict:
        """
        Функция возвращает словарь данных
        source - откуда считывать
        """
        with open(source, 'r', encoding='utf-8') as file:
            return json.load(file)


class Main_Window(tk.Tk):
    ...
    pass




class Window_Resolution_Settings(tk.Tk, Behaviour):
    """
    Открывает окно настроек разрешения окна
    """
    def __init__(self):
        super().__init__()
        # создание окна приложения
        self    = tk.Tk()
        # создание заголовка
        self.title("Название окна")
        # добавление ярлыка
        self.iconbitmap(default=Behaviour.ICON_PATH)
        # создание места, где будут собраны все элементы интерфейса
        self.configurate()

    def configurate(self):
        n = len()
        self.settings_label = [None] * n     # список для массива надписей
        self.settings_entry = [None] * n      # список для массива полей

        for i in range(n):
            self.rowconfigure(i, weight=1)
        self.rowconfigure(n + 1, weight=1)
        self.rowconfigure(n + 2, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=7)
        self.columnconfigure(2, weight=1)
        count = 0
        row_count = 1
        column_count = 1

        # размещение элементов в окне
        for i, j in RESOLUTION_DICT.items():
            self.settings_label[count] = tk.Label(
                text=j['description']
            )

            self.settings_label[count].grid(
                row=row_count,
                column=column_count,
                sticky='w',
                padx=15
            )

            self.settings_entry[count] = tk.Entry(
                ...
            )
            self.settings_entry[count].grid(
                row=row_count,
                column=column_count + 1,
                sticky='ew'
            )
            row_count += 1
            count += 1

        # кнопка принятия настроек
        self.append_button = ttk.Button(
            text='Принять',
            state=['disabled'] # TODO дописать disabled enabled для отключения кнопки, если не было сделано изменений
        )     # TODO дописать код для записи данных в json
        self.append_button.grid(
            row=row_count,
            column=column_count + 1,
            sticky='ew',
            padx=10
        )

        # кнопка выхода из меню настроек
        self.exit_button = ttk.Button(
            text='Выход'
        )
        self.exit_button.grid(
            row=row_count,
            column=column_count,
            sticky='w',
            padx=15
        )
        # задание поведения кнопки выхода
        self.exit_button.bind("<Enter>", self.entered('Меню'))
        self.exit_button.bind("<Leave>", self.leaved('Выход'))

    def entered(self, text):
        """
        Изменяет текст указанных объектов при наведении на них мыши
        """
        self.exit_button['text'] = text

    def leaved(self, text):
        """
        Изменяет текст при снятии и них курсора
        """
        self.exit_button['text'] = text









window.update()
# создание цикла событий (всегда после методов параметров окна)
window.mainloop()
