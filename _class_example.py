class Name:
    """

    """
    def __int__(self,
                ) -> None:
        """

        """
        pass

    def __repr__(self) -> str:
        """

        """
        return f'{self.__class__.__name__}(id_={self.id_}, name=' \
               f'{self.name!r}, pages={self.pages!r})'

    def __str__(self) -> None:
        """

        """
        accuracy = 2  # количество знаков после запятой
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

    @property
    def name(self):
        """
        Возвращает значение переменной
        """
        return self._name

    @name.setter
    def selection(self, var: list[Union[int, float]]) -> None:
        """
        var - значение, которое необходимо присвоить
        """
        for i in var:
            if not isinstance(i, (int, float)):
                raise TypeError(
                    f"Значение элемента selection может быть только типа int, float, а не {type(i)}")
        self._name = self.sort(var)
