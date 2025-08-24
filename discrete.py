# в этом файле считываются характеристики дискретной случайной величины

#
#
# python git_commit.py


from typing import Any, List, Union
from typing import Union
import math
import os

import numpy as np
FILENAME = os.path.basename(__file__)

#TODO добавить чтение через эксель

class Discrete_1D:
    """
    ДОБАВЛЕНИЕ
    добавить метод, который сортирует значения СВ

    ОТЛАДКА

    """
    flag = False # изменение флага на истинность остальных аттрибутов класса
    def __init__(self,
                meaning: list[Union[int, float]],
                probability: list[Union[int, float]]
                ) -> None:
        """
        meaning - значения случайной величины
        probability - вероятности появления значения случайной величины
        """
        self.meaning = meaning
        self._meaning = self.meaning

        self.probability = probability
        self._probability = self.probability

        self.n = len(self._meaning)
        self._miy = 0
        self._dispersion = 0
        self.execute()

    def execute(self) -> None:
        """
        Метод обновляет значения вычисляемых переменных, если изменены исходные данные
        """
        if not __class__.flag: #если изменены исходные данные
            self._is_equal_len()
            self.miy_execute()
            self.dispersion_execute()
            __class__.flag = True  # изменение флага на истинность остальных аттрибутов класса

    def miy_execute(self):
        """
        Метод вычисляет математическое ожидание одномерной дискретной случайной величины
        """
        for i in range(self.n):
            self._miy += self._probability[i] * self._meaning[i]

    def dispersion_execute(self):
        """
        Метод вычисляет дисперсию одномерной дискретной случайной величины
        """
        for i in range(self.n):
            self._dispersion += (self._meaning[i] - self._miy) ** 2 * self._probability[i]

    def _is_equal_len(self):
        """
        Проверяет, что длина списка значений равна длине списка вероятностей
        """
        if self._meaning and \
                self._probability and \
                len(self._meaning) != len(self._probability):
            raise ValueError(
                "Неодинаковые длины meaning и probability"
            )

    @property
    def meaning(self) -> list[Union[int, float]]:
        """
        Возвращает значение переменной
        """
        return self._meaning

    @meaning.setter
    def meaning(self, value: list[Union[int, float]]) -> None:
        """
        var - значение, которое необходимо присвоить
        """
        for i in value:
            if not isinstance(i, (int, float)):
                raise TypeError(
                    f"Значение элемента selection может быть только типа int, float, а не {type(i)}"
                )
        __class__.flag = False # изменение флага на истинность остальных аттрибутов класса
        self._meaning = value

    @property
    def probability(self) -> list[Union[int, float]]:
        """
        Возвращает значение переменной
        """
        return self._probability

    @probability.setter
    def probability(self, value: list[Union[int, float]]) -> None:
        """
        var - значение, которое необходимо присвоить
        """
        for i in value:
            if not isinstance(i, (int, float)):
                raise TypeError(
                    f"Значение элемента selection может быть только типа int, float, а не {type(i)}")
        summ = sum(value)
        if summ == 1:
            raise ValueError(
                f"Сумма вероятностей не равна 1, а равна {summ}"
            )
        self._probability = value
        __class__.flag = False # изменение флага на истинность остальных аттрибутов класса

    @property
    def miy(self):
        """
        Возвращает значение переменной
        """
        self.execute()
        return self._miy

    @property
    def dispersion(self):
        """
        Возвращает значение переменной
        """
        self.execute()
        return self._dispersion

    def __repr__(self) -> str:
        """

        """
        pass

    def __str__(self) -> str:
        """
        Описывает основные параметры при выводе экземпляра класса
        """
        self.execute()
        accuracy = 2 #количество знаков после заппятой
        dict_out = {
            'Значения СВ': [round(x, accuracy) for x in self._meaning],
            'Вероятности СВ': [round(x, accuracy) for x in self._probability],
            'Матожидание': round(self.miy, accuracy),
            'Дисперсия': round(self._dispersion, accuracy)
        } #подготовка словаря для вывода
        str_out = ''
        for key, value in dict_out.items():
            indent = (15 - len(key)) * ' ' #отступ
            str_out += key + indent + str(value) + '\n'
        return str_out








if __name__ == "__main__":
    m = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    p = [0.2, 0.1, 0.1, 0.05, 0.05, 0.07, 0.03, 0.01, 0.344444, 1]

    t = Discrete_1D(m, p)
    t.meaning = [1, 4, 3, 4, 5, 6, 7, 8, 9,1]
    print(t.dispersion)
    print(t)
    t.meaning = [1, 4, 3, 4, 5, 6, 7, 8, 9,10]
    print(t.dispersion)
    print(t)


