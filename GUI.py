# https://metanit.com/python/tkinter/2.1.php

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json

SOURCE_RESOLUTION = 'resolution_data.json'  # имя файла для данных разрешения
ICON_PATH = 'world_of_tanks.ico'

# ---------------------------------------------------------
# события
def entered(text):
    """
    Изменяет текст указанных объектов при наведении на них мыши
    """
    exit_button['text'] = text


def leaved(text):
    """
    Изменяет текст при снятии и них курсора
    """
    exit_button['text'] = text
# ----------------------------------------------------------





# запись параметров экрана в файл
def json_writing(data: dict, source: str) -> None:
    """
    Функция записывает словарь данных
    data - что записывать
    source - куда записывать
    """
    with open(source, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def json_reading(source: str) -> dict:
    """
    Функция возвращает словарь данных
    source - откуда считывать
    """
    with open(source, 'r', encoding='utf-8') as file:
        return json.load(file)

def print_info(widget, depth=0) -> None:
    """
    Печатает информацию о виджетах (TODO в отдельном окне, вызывается по кнопке, и клику по виджету)
    """
    widget_class = widget.winfo_class() # получение информации класса виджета
    widget_width = widget.winfo_width()  # получение информации ширины виджета
    widget_height = widget.winfo_height()  # получение информации высоты виджета
    widget_x = widget.winfo_x()  # получение информаци координаты х верхнего левого угла виджета относительно родительского элемента
    widget_y = widget.winfo_y()  # получение информации координаты у верхнего левого угла виджета относительно родительского элемента
    widget_rootx = widget.winfo_rootx()  # получение информаци координаты х верхнего левого угла виджета относительно экрана
    widget_rooty = widget.winfo_rooty()  # получение информации координаты у верхнего левого угла виджета относительно экрана
    print(
        '\t' * depth + \
        f"{widget_class }\twight={widget_width}\theight={widget_height}\t"
        f"x_parent={widget_x}\t\ty_parent={widget_y}\t\t"
        f"x_screen={widget_rootx}\ty_screen={widget_rooty}"
    )
    # рекурсикная печать всех параметров вложенных виджетов
    for widget in widget.winfo_children():
        print_info(widget, depth + 1)

def resolution_settings():
    """
    Открывает окно настроек разрешения окна
    """
    window.title('Настройки окна')
    # создание места, где будут собраны все элементы интерфейса

    n = len(RESOLUTION_DICT)
    settings_label = [None] * n     # список для массива надписей
    settings_entry = [None] * n      # список для массива полей

    for i in range(n):
        window.rowconfigure(i, weight=1)
    window.rowconfigure(n + 1, weight=1)
    window.rowconfigure(n + 2, weight=1)

    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=7)
    window.columnconfigure(2, weight=1)
    count = 0
    row_count = 1
    column_count = 1

    # размещение элементов в окне
    for i, j in RESOLUTION_DICT.items():
        settings_label[count] = tk.Label(

            text=j['description']
        )

        settings_label[count].grid(
            row=row_count,
            column=column_count,
            sticky='w',
            padx=15
        )

        settings_entry[count] = tk.Entry(

        )
        settings_entry[count].grid(
            row=row_count,
            column=column_count + 1,
            sticky='ew'
        )
        row_count += 1
        count += 1

    # кнопка принятия настроек
    append_button = ttk.Button(

        text='Принять',
        state=['disabled'] # TODO дописать disabled enabled для отключения кнопки, если не было сделано изменений
    )     # TODO дописать код для записи данных в json
    append_button.grid(
        row=row_count,
        column=column_count + 1,
        sticky='ew',
        padx=10
    )

    # кнопка выхода из меню настроек
    exit_button = ttk.Button(

        text='Выход'
    )
    exit_button.grid(
        row=row_count,
        column=column_count,
        sticky='w',
        padx=15
    )
    exit_button.bind("<Enter>", entered('Меню'))
    exit_button.bind("<Leave>", entered('Выход'))




# создание окна приложения
window = tk.Tk()
# создание заголовка
window.title("Название окна")
# добавление ярлыка
window.iconbitmap(default=ICON_PATH)

RESOLUTION_DICT = json_reading(SOURCE_RESOLUTION)   # чтение параметров
window.attributes('-fullscreen', False) # полноэкранный режим (TODO добавить)
window.attributes('-toolwindow', False) # наличие верхней панели (TODO добавить)


# вычисление координат расположения окна
if RESOLUTION_DICT['ON_CENTER_X']['value']:
    X_COORDINATE = RESOLUTION_DICT['X_RESOLUTION']['value'] // 2 - \
                   RESOLUTION_DICT['WIGHT']['value'] // 2
else:
    if RESOLUTION_DICT['IS_LEFT']['value']:
        X_COORDINATE = \
            RESOLUTION_DICT['X_INDENT']['value']
    else:
        X_COORDINATE = \
            RESOLUTION_DICT['X_RESOLUTION']['value'] - \
            RESOLUTION_DICT['WIGHT']['value'] - \
            RESOLUTION_DICT['X_INDENT']['value']
if RESOLUTION_DICT['ON_CENTER_Y']['value']:
    Y_COORDINATE = \
        RESOLUTION_DICT['Y_RESOLUTION']['value'] // 2 - \
        RESOLUTION_DICT['HEIGHT']['value'] // 2
else:
    if RESOLUTION_DICT['IS_UP']['value']:
        Y_COORDINATE = \
            RESOLUTION_DICT['Y_INDENT']['value']
    else:
        Y_COORDINATE = \
            RESOLUTION_DICT['Y_RESOLUTION']['value'] - \
            RESOLUTION_DICT['HEIGHT']['value'] - \
            RESOLUTION_DICT['Y_INDENT']['value']
resolution = str(RESOLUTION_DICT['WIGHT']['value']) + 'x' + \
             str(RESOLUTION_DICT['HEIGHT']['value']) + '+' + \
             str(X_COORDINATE) + '+' + \
             str(Y_COORDINATE)
# задание размера окна
window.geometry(resolution)
window.resizable(
    RESOLUTION_DICT['RESIZABLE_Y']['value'],
    RESOLUTION_DICT['RESIZABLE_X']['value']
)


resolution_settings()

# name1_label = tk.Label(
#     frame,  # где расположена текстовая надпись
#     text="Текст надписи 1"
# )
# name1_label.grid(  # расположение во фрейме
#     row=3,
#     column=1
# )
#
# name1_tf = tk.Entry(  # поле ввода информации
#     frame
# )
# name1_tf.grid(
#     row=3,
#     column=2
# )
#
#
# def name1_button_pressed():
#     name1_data = name1_tf.get()  # полученине информации
#     # создание всплывающего окна
#     tk.messagebox.showinfo(title="Сообщение",
#                            message=f"Тут текст сообщения {name1_data}"
#                            )
#
#
# name1_button = tk.Button(
#     frame,
#     text="Что она делает",
#     command=name1_button_pressed

# )
# name1_button.grid(
#     row=4,
#     column=2
# )

# обновление информации о виджетах
window.update()
# создание цикла событий (всегда после методов параметров окна)
window.mainloop()
