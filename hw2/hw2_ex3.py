from datetime import datetime
from pytz import timezone


def extract_clients_balance(clients, first_name, last_name):
    return clients.get(f'{first_name} {last_name}')

def update_clients_balance(clients, first_name, last_name, new_balance):
    clients[f'{first_name} {last_name}'] = new_balance


def greet_client(clients, first_name, last_name):
    balance = extract_clients_balance(clients, first_name, last_name)
    if balance is None:
        print(f'Ошибка: клиент {first_name} {last_name} не найден.')
        return

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


def deposit(clients, first_name, last_name, amount):
    balance = extract_clients_balance(clients, first_name, last_name)
    if balance is None:
        print(f'Ошибка: клиент {first_name} {last_name} не найден.')
        return None
    if amount > 0:
        balance += amount
        update_clients_balance(clients, first_name, last_name, balance)
        print(f'Счёт {first_name} {last_name} пополнен. Новый баланс: {balance}.')
    else:
        print('Ошибка: сумма пополнения должна быть положительной.')
    return balance


def withdraw(clients, first_name, last_name, amount):
    balance = extract_clients_balance(clients, first_name, last_name)
    if balance is None:
        print(f'Ошибка: клиент {first_name} {last_name} не найден.')
        return None
    if amount < 0:
        print('Ошибка: сумма снятия должна быть положительной.')
    elif balance < amount:
        print('Ошибка: недостаточно средств на счёте.')
    else:
        balance -= amount
        update_clients_balance(clients, first_name, last_name, balance)
        print(f'Со счёта {first_name} {last_name} снято {amount}. Новый баланс: {balance}.')

    return balance


if __name__ == '__main__':
    clients = {'Анна Петрова': 1000, 'Иван Сидоров': 500}

    greet_client(clients, 'Анна', 'Петрова')
    print(deposit(clients, 'Анна', 'Петрова', 200))
    print(withdraw(clients, 'Иван', 'Сидоров', 300))

    print(deposit(clients, 'Мария', 'Иванова', 100))
    print(withdraw(clients,'Анна', 'Петрова', -50))
    print(withdraw(clients, 'Иван', 'Сидоров', 1000))
