class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        print(f'{self.name} ест.')

    def make_sound(self):
        print(f'{self.name} издает звук.')


class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def make_sound(self):
        print('Гав!')

    def fetch(self):
        print(f'{self.name} принес(ла) палку.')


class Cat(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)

    def make_sound(self):
        print('Мяу!')

    def purr(self):
        print(f'{self.name} мурлычет.')


class Bird(Animal):
    def fly(self):
        print(f'{self.name} летит.')


class Parrot(Bird):
    def make_sound(self):
        print('Кар! Я хороший!')


if __name__ == '__main__':
    dog = Dog('Beethoven', 10, 'Saint Bernard')
    cat = Cat('Garfield', 5)
    parrot = Parrot('Iago', 3)

    zoo_animals = [dog, cat, parrot]

    for animal in zoo_animals:
        animal.make_sound()
    print()
    for animal in zoo_animals:
        if isinstance(animal, Dog):
            animal.fetch()
        if isinstance(animal, Cat):
            animal.purr()
        if isinstance(animal, Parrot):
            animal.fly()
        animal.eat()
        print()
