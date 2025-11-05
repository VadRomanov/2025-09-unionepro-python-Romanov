from datetime import datetime
from pytz import timezone

def greet_client(first_name, last_name):
    current_time_with_zone = timezone('Europe/Moscow').localize(datetime.now()).time()
    current_hour = current_time_with_zone.hour
    if current_hour < 6:
        greeting = 'Доброй ночи'
    elif current_hour < 12:
        greeting = 'Доброе утро'
    elif current_hour < 18:
        greeting = 'Добрый день'
    else:
        greeting = 'Добрый вечер'

    print(f'{greeting}, {first_name} {last_name}!')

def deposit(balance, amount):
    if amount > 0:
        balance += amount
    else:
        print('Ошибка: сумма пополнения должна быть положительной.')
    return balance

def withdraw(balance, amount):
    if amount < 0:
        print('Ошибка: сумма снятия должна быть положительной.')
    elif balance < amount:
        print('Ошибка: недостаточно средств на счёте.')
    else:
        balance -= amount
    return balance


if __name__ == '__main__':

    greet_client('Vadim', 'Romanov')
    print(deposit(1000, 500))
    print(deposit(1000, -200))
    print(withdraw(1000, 300))
    print(withdraw(1000, 1500))
    print(withdraw(1000, -100))
