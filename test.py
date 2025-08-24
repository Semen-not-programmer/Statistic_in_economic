# https://metanit.com/python/tkinter/2.1.php

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
from typing import Union, Any


class Behaviour(tk.Tk):
    def __init__(self):
        super().__init__()

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

    def set_settings(self,
                   source: str):
        """
        Применение настроек к классу окна, откуда метод был вызван
        """
        DICT = Behaviour.json_reading(source)  # чтение параметров
        self.attributes('-fullscreen',
                        DICT['FULLSCREEN']['value'])  # полноэкранный режим
        self.attributes('-toolwindow',
                        DICT['TOOLWINDOW']['value'])  # наличие верхней панели

        # вычисление координат расположения окна
        if DICT['ON_CENTER_X']['value']:
            X_COORDINATE = DICT['X_RESOLUTION']['value'] // 2 - \
                           DICT['WIGHT']['value'] // 2
        else:
            if DICT['IS_LEFT']['value']:
                X_COORDINATE = \
                    DICT['X_INDENT']['value']
            else:
                X_COORDINATE = \
                    DICT['X_RESOLUTION']['value'] - \
                    DICT['WIGHT']['value'] - \
                    DICT['X_INDENT']['value']
        if DICT['ON_CENTER_Y']['value']:
            Y_COORDINATE = \
                DICT['Y_RESOLUTION']['value'] // 2 - \
                DICT['HEIGHT']['value'] // 2
        else:
            if DICT['IS_UP']['value']:
                Y_COORDINATE = \
                    DICT['Y_INDENT']['value']
            else:
                Y_COORDINATE = \
                    DICT['Y_RESOLUTION']['value'] - \
                    DICT['HEIGHT']['value'] - \
                    DICT['Y_INDENT']['value']
        resolution = str(DICT['WIGHT']['value']) + 'x' + \
                     str(DICT['HEIGHT']['value']) + '+' + \
                     str(X_COORDINATE) + '+' + \
                     str(Y_COORDINATE)
        # задание размера окна
        self.geometry(resolution)
        self.resizable(
            DICT['RESIZABLE_Y']['value'],
            DICT['RESIZABLE_X']['value']
        )
        # создание заголовка
        self.title(DICT['TITLE']['value'])

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

    @staticmethod
    def check_type(value: Any,
                   name: str,
                   type_check: Union[type, tuple[type]]) -> None:
        """
        Метод проверяет соответствие входных типов данных требуемым значениям
        value - входное значение
        name - имя переменной (для оформления)
        type_check - требуемый тип или кортеж требуемых типов
        """
        if not isinstance(value, type_check):
            raise TypeError(
                f'Переменная {name} может принимать только '
                f'значения типа {type_check}')

    @staticmethod
    def check_value_positive(value: Union[int, float],
                             name: str) -> None:
        """
        Метод проверяет, положительны ли значения входных данных
        value - входное значение
        name - имя переменной (для оформления)
        """
        if value < 0:
            raise TypeError(f'Переменная {name} может принимать только '
                            f'положительные значения')

    @staticmethod
    def check_str_list(value: str,
                       name: str,
                       str_list: list[str]) -> None:
        """
        Метод проверяет, есть ли данная строка в разрешённых значениях, которые
        она может принимать
        value - входное значение
        name - имя переменной (для оформления)
        str_list - список возможных комбинаций
        """
        if value not in str_list:
            raise ValueError(f"Значение переменной {name} может принимать одно из значений {str_list}, а не {value}")



class Main_Window(Behaviour):
    SOURCE_RESOLUTION = 'resolution_data.json'  # имя файла для данных разрешения
    ICON_PATH = 'world_of_tanks.ico'

    def __init__(self):
        super().__init__()

        # добавление ярлыка
        self.iconbitmap(default=__class__.ICON_PATH)
        Behaviour.set_settings(self, __class__.SOURCE_RESOLUTION)
        self.building()
        self.update()


    def building(self):
        """
        Открывает окно настроек разрешения окна
        Настраивает все параметры
        """
        DICT = Behaviour.json_reading(__class__.SOURCE_RESOLUTION)
        # создание места, где будут собраны все элементы интерфейса
        self.n = len(DICT)
        self.label = [None] * self.n  # список для массива надписей
        self.entry = [None] * self.n  # список для массива полей


        for i in range(self.n):
            self.rowconfigure(i, weight=1)
        self.rowconfigure(self.n + 1, weight=1)
        self.rowconfigure(self.n + 2, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=7)
        self.columnconfigure(2, weight=1)
        self.row_count = 1
        self.column_count = 1
        self.count = 0  # индекс необходимиго элемента



        # размещение элементов в окне
        for key, value in DICT.items():
            self.label[self.count]  = Label_Field(
                row=self.row_count,
                colunn=self.column_count,
                sticky='w',
                insert_value=str(value['description']),
                class_name=__class__
            )

            self.entry[self.count] = Entry_Field(
                row=self.row_count,
                colunn=self.column_count + 1,
                validate='none',
                sticky='w',
                insert_value=str(value['value']),
                class_name=__class__
            )

            self.row_count += 1
            self.count += 1

        self.error_lable_create()
        self.append_button_create()
        self.exit_button_create()






    def error_lable_create(self):
        # поле сообщения об ошибке при введении параметров
        ...

    def append_button_create(self):
        # кнопка принятия настроек
        self.append_button = ttk.Button(

            text='Принять',
            state=['disabled']
            # TODO дописать disabled enabled для отключения кнопки, если не было сделано изменений
        )  # TODO дописать код для записи данных в json
        self.append_button.grid(
            row=self.row_count,
            column=self.column_count + 1,
            sticky='ew',
            padx=10
        )

    def exit_button_create(self):
        # кнопка выхода из меню настроек
        self.exit_button = ttk.Button(
            command=self.exit_button_clicked,
            text='Выход'
        )
        self.exit_button.grid(
            row=self.row_count,
            column=self.column_count,
            sticky='w',
            padx=15
        )
        self.exit_button.bind("<Enter>", self.exit_button_enter)
        self.exit_button.bind("<Leave>", self.exit_button_leave)

    def exit_button_enter(self, event):
        """
        Изменяет текст кнопки выхода при наведении мыши
        """
        self.exit_button["text"] = 'Меню'

    def exit_button_leave(self, event):
        """
        Изменяет текст кнопки выхода при снятии мыши
        """
        self.exit_button["text"] = 'Выход'
    def exit_button_clicked(self):
        self.destroy()



class Button_Field:
    def __init__(self):
        pass
    # TODO сделать

class Label_Field:
    """
    Класс создаёт текстовую надпись
    """
    def __init__(self,
                 row: int,
                 colunn: int,
                 padx: Union[int, list[int]] = 0,
                 pady: Union[int, list[int]] = 0,
                 sticky: str = 'none',
                 insert_value: Union[int, float, str] = '',
                 class_name=Main_Window) -> None:
        """
        row - номер ряда
        column - номер столбца
        padx - отступ по горизонтали
        pady - отступ по вертикали
        sticky - тип растяжения по пространству
        insert_value - что записано в пустом поле изначально
        class_name - в каком классе создавать поле
        """
        self.row = row
        self.column = colunn
        self.padx = padx
        self.pady = pady
        self.sticky = sticky
        self.insert_value = insert_value

        self.create_var(class_name)
        self.create_field(class_name)

    def create_field(self, class_name):
        """
        Создание поля надписи, в которой текст является переменной
        """
        class_name.label = ttk.Label(
            text=class_name.label_var.get()
        )
        if self.sticky != 'none':
            class_name.label.grid(
                row=self.row,
                column=self.column,
                sticky=self.sticky,
                padx=self.padx,
                pady=self.pady
            )
        else:
            class_name.label.grid(
                row=self.row,
                column=self.column,
                padx=self.padx,
                pady=self.pady
            )


    def create_var(self, class_name):
        """
        Создание переменной, указвающей на текст
        """
        class_name.label_var = tk.StringVar()
        class_name.label_var.set(self.insert_value)


    def change_var(self, class_name, insert_value):
        """
        Изменяет значение переменной, указывающей на текст
        """
        class_name.label_var.set(insert_value + '\t' * 10)
        self.create_field(class_name)


class Entry_Field:
    """
    Класс создаёт поле ввода
    TODO добавить валидацию
    """
    def __init__(self,
                 row: int,
                 colunn: int,
                 validate: str='none',
                 sticky: str='none',
                 insert_value: Union[int, float, str]='',
                 class_name=Main_Window) -> None:
        """
        row - номер ряда
        column - номер столбца
        validate - тип проверки
        sticky - тип растяжения по пространству
        insert_value - что записано в пустом поле изначально
        class_name - в каком классе создавать поле
        """
        self.row = row
        self.column = colunn
        self.validate = validate
        self.sticky = sticky
        self.insert_value = insert_value


        self.create_var(class_name)
        self.create_field(class_name)


    def create_field(self, class_name):
        """
        Метод создаёт поле с необходимыми параметрами,
        где текст является переменной
        """
        class_name.entry = tk.Entry(
            validate=self._validate,
            validatecommand=self.check_function
        )
        if self.sticky != 'none':
            class_name.entry.insert(0, class_name.entry_var.get())
            class_name.entry.grid(
                row=self._row,
                column=self._column,
                sticky=self._sticky
            )
        else:
            class_name.entry.insert(0, class_name.entry_var.get())
            class_name.entry.grid(
                row=self._row,
                column=self._column
            )


    def create_var(self, class_name):
        """
        Создание переменной, указвающей на текст
        """
        class_name.entry_var = tk.StringVar()
        class_name.entry_var.set(self.insert_value)

    def change_var(self, class_name, insert_value):
        """
        Изменяет значение переменной, указывающей на текст
        """
        class_name.entry_var.set(insert_value)
        self.create_field(class_name)

    def check_function(self):
        ...

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value: int):
        Behaviour.check_type(value, 'row', int)
        Behaviour.check_value_positive(value, 'row')
        self._row = value

    @property
    def column(self):
        return self._row

    @column.setter
    def column(self, value: int):
        Behaviour.check_type(value, 'column', int)
        Behaviour.check_value_positive(value, 'column')
        self._column = value

    @property
    def validate(self):
        return self._validate

    @validate.setter
    def validate(self, value: str):
        Behaviour.check_type(value, 'validate', str)
        Behaviour.check_str_list(value, 'validate',
                                 ['none', 'focus', 'focusin', 'focusout', 'key', 'all'])
        self._validate = value

    @property
    def sticky(self):
        return self._sticky

    @sticky.setter
    def sticky(self, value: str):
        Behaviour.check_type(value, 'sticky', str)
        Behaviour.check_str_list(value, 'sticky',
                                 ['n', 'e', 's', 'w',
                                  'ne', 'nw', 'se', 'sw', 'ns', 'we', 'none'])
        self._sticky = value

    @property
    def insert_value(self):
        return self._insert_value

    @insert_value.setter
    def insert_value(self, value: Any):
        self._insert_value= value




swwwwww = Main_Window()
swwwwww.mainloop()

