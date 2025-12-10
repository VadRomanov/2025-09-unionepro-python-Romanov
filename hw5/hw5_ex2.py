class Product:

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.discount_factor = 1

    def add(self, amount):
        if amount <= 0:
            print('Ошибка. Нельзя добавить неположительное кол-во товаров')
            return
        self.quantity += amount

    def take(self, amount):
        if self.quantity < amount:
            print('Ошибка. Недостаточно средств на счете')
            return
        if amount <= 0:
            print('Ошибка. Нельзя забрать неположительное кол-во товаров')
            return
        self.quantity -= amount

    def total_cost(self):
        return self.quantity * self.price * self.discount_factor

    def apply_discount(self, new_discount_factor):
        self.discount_factor = new_discount_factor


if __name__ == '__main__':
    apple = Product('apple', 100, 1)
    pear = Product('pear', 150, 2)
    print(apple.total_cost())
    apple.apply_discount(0.8)
    print(apple.total_cost())
    print(pear.total_cost())
