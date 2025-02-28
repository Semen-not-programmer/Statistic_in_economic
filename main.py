from typing import Any, List, Union
from typing import Union
import math


class Statistic:
    """

    """

    def __init__(self,
                 selection: list[Union[int, float]]) -> None:
        """
        selection - исходная выборка

        n - размер выборки
        miy - математическое ожидание
        dispersion - дисперсия
        dispersion_1 - дисперсия несмещённая
        median - медиана
        mode - мода
        """
        self.selection = selection
        self.n = len(self._selection)
        self.miy = self.math_expect()
        self.dispersion = self.dispersion()
        self.median = self.median()
        self.mode = self.mode()

    def index(self,
              percentile: Union[int, float]) -> Union[int, float]:
        """
        Метод возвращает элемент из вариационного ряда по заданому значению процентиля percentile
        """
        i = percentile * self.n / 100
        if i % 1 != 0:
            out = self._selection[math.floor(i)]
        else:
            out = (self._selection[int(i) - 1] + self._selection[int(i)]) / 2
        return out

    def percentile(self,
                   value: Union[int, float]) -> float:
        """
        Метод расчитывает процент значений элементов, которые меньше заданного value
        """
        n_p = 0
        for i in self._selection:
            if i < value:
                n_p += 1
            else:
                break
        out = (n_p + 0.5) / self.n * 100
        # крайние условия: без элементов и максимум 100%
        if out > 100:
            out = 100
        elif n_p == 0:
            out = 0
        return out

    def box_plot(self) -> tuple[Union[int, float]]:
        """
        q_1 - квантиль уровня 25%
        q_2 - квантиль уровня 50%
        q_3 - квантиль уровня 75%
        i_qr - межквартильный размах
        """
        q_1 = self.index(25)
        q_3 = self.index(75)
        i_qr = q_3 - q_1
        return tuple((q_1 - i_qr, q_3 + i_qr))

    def blowout(self) -> list[Union[int, float]]:
        """
        Метод проверяет данные на наличие выбросов
        """
        low, up = self.box_plot()
        out_list = []
        i_low = 0
        i_up = len(self._selection) - 1
        for i in range(len(self._selection)):
            if self._selection[i] < low:
                out_list.append(self._selection[i])
            else:
                i_low = i
                break
        for i in range(len(self._selection) -1, 0, -1):
            if self._selection[i] > up:
                out_list.append(self._selection[i])
            else:
                i_up = i
                break
        self._selection = self._selection[i_low: i_up + 1]
        return out_list

    def math_expect(self) -> float:
        """

        """
        summ = 0
        for x_i in self._selection:
            summ += x_i
        return summ / self.n

    def dispersion(self) -> float:
        """
        Метод возвращает квадрат среднего квадратичного отклонения
        """
        summ = 0
        for x_i in self._selection:
            summ += (x_i - self.miy) ** 2
        return summ / self.n

    def dispersion_1(self) -> float:
        """
        Метод возвращает квадрат среднего квадратичного отклонения
        несмещённую величину дисперсии
        """
        summ = 0
        for x_i in self._selection:
            summ += (x_i - self.miy) ** 2
        return summ / (self.n - 1)

    def median(self) -> float:
        """
        Метод находит центральное значение в вариационном ряде
        """
        if self.n % 2 == 0:
            return (self._selection[self.n // 2] + self._selection[self.n // 2 - 1]) / 2
        else:
            return self._selection[(self.n - 1) // 2]

    def mode(self) -> Union[int, float, None]:
        """
        Метод возвращает значение элемента, который повторяется наибольшее число раз, если таких элементов несколько, то возвращает список
        """
        var_dict = dict()
        for i in self._selection:
            if i not in var_dict.keys():
                var_dict[i] = 1
            else:
                var_dict[i] += 1
        # Нахождение элемента с максимальной частотой
        maxx = 0
        answer = None
        for key, value in var_dict.items():
            if value > maxx:
                maxx = value
                answer = key
            elif value == maxx:
                if isinstance(answer, list):
                    answer += [key]
                else:
                    answer = list([answer, key])
        try:
            if len(answer) == len(var_dict.keys()):
                answer = None
        finally:
            return answer

    @staticmethod
    def sort(var: list[Union[int, float]]) -> list[Union[int, float]]:
        """
        var - список, который необходимо отсортировать
        """
        for i in range(1, len(var)):
            temp = var[i]
            j = i - 1
            while j >= 0 and temp < var[j]:
                var[j + 1] = var[j]
                j -= 1
            var[j + 1] = temp
        return var

    def weight_average(self,
                       weight_list: list[Union[int, float]]) -> float:
        """
        Метод возвращает среднее взвешенное -
        """
        summ = 0
        for i in range(len(self._selection)):
            summ += self._selection[i] * weight_list[i]
        summ_weight = 0
        for var in weight_list:
            summ_weight += var
        return summ / summ_weight

    @property
    def selection(self):
        return self._selection

    @selection.setter
    def selection(self, var: list[Union[int, float]]) -> None:
        """
        var - список, который необходимо проверить и назначить
        """
        for i in var:
            if not isinstance(i, (int, float)):
                raise TypeError(f"Значение элемента selection может быть только типа int, float, а не {type(i)}")
        self._selection = self.sort(var)

    def __str__(self):
        accuracy = 2    # количество знаков после запятой
        box_tuple = self.box_plot()
        dict_out = {'Вариационный ряд': self._selection,
                    'Математическое ожидание': round(self.miy, accuracy),
                    'Дисперсия': round(self.dispersion, accuracy),
                    'Медиана': self.median,
                    'Мода': self.mode,
                    "Межквартильный размах": box_tuple}
        str_out = ''
        for key, value in dict_out.items():
            indent = (30 - len(key)) * ' '
            str_out += key + indent + str(value) + '\n'
        return str_out

if __name__ == "__main__":
    t = Statistic([74, 60, 82, 90, 55, 98])
    print(t.percentile(82))

for i in range(3):
    i += 1
