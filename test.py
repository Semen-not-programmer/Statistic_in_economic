# этот файл проверяет правильность функционирования программы
#
#

import os
FILENAME = os.path.basename(__file__)

class_name = "W:\Текстовые документы\Курс Методы анализа экономики\Литература\statistic.py"

from selection import Statistic


t = Statistic([10, 41, 485])
print(t)
