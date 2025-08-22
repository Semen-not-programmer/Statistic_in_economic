# скрипт отправляет всю папку в git без изменения gitignore и ветки
#
#
# python git_commit.py

import os
import time
print("Введите текст коммита")
text = input()


def commit(text: str) -> None:
    os.system("git add .")
    time.sleep(5)
    os.system("git commit -m \"" + text + "\"")
    time.sleep(10)
    os.system("git push")
