class Person:  
    def __init__(self, name):  
        self.name = name # приватный атрибут
        self._name = self.name
    @property  
    def name(self):  
        return self._name  
    @name.setter  
    def name(self, value):  
        if not isinstance(value, str):  
            raise TypeError('Name must be a string')  
        self._name = value

    def dk(self):
        w = self._name * 2

person = Person("sgdrfhjk")
# Использование геттера:  
print(person.name)  
# Использование сеттера:  
person.name = 'Sam'
person.dk()