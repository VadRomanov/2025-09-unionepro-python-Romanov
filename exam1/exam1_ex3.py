def validate_quantity(quantity):
    if not isinstance(quantity, int):
        raise ValueError(f'Ошибка: число доставок должно быть целочисленным числом')
    if quantity <= 0:
        raise ValueError(f'Ошибка: число доставок не может быть меньше или равно 0, число доставок = {quantity}')


def get_shipping_cost(quantity: int) -> int:
    validate_quantity(quantity)
    return 1000 + (quantity - 1) * 120


if __name__ == '__main__':
    print(get_shipping_cost(1))
    print(get_shipping_cost(60))
    print(get_shipping_cost(3))
