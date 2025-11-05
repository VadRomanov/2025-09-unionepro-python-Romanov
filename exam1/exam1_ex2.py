import random


def validate_numbers(*numbers):
    for number in numbers:
        if not isinstance(number, int):
            raise ValueError('Ошибка: должно быть целочисленное число')
        if number <= 0:
            raise ValueError(f'Ошибка: число не может быть меньше 0, число = {number}')

def validate_range(number_of_tickets, start_of_number_range, end_of_number_range, number_of_digits_in_ticket_number):
    range_capacity = end_of_number_range - start_of_number_range
    if range_capacity < number_of_tickets:
        raise ValueError(f'Ошибка: неверые значения на входе. '
                         f'Количество уникальных номеров билетов {number_of_tickets} '
                         f'невозможно расположить в диапазоне от {start_of_number_range} до {end_of_number_range}, '
                         f'который соответствует числу цифр в номере билета {number_of_digits_in_ticket_number}'
                         f' (максимум {range_capacity} уникальных номеров)')


def print_tickets(tickets_to_print):
    for ticket in tickets_to_print:
        print(ticket)

def generate_ticket_numbers(number_of_tickets=100, number_of_digits_in_ticket_number=7):
    validate_numbers(number_of_tickets, number_of_digits_in_ticket_number)
    start_of_number_range = 10 ** (number_of_digits_in_ticket_number - 1)
    end_of_number_range = 10 ** number_of_digits_in_ticket_number - 1
    validate_range(number_of_tickets, start_of_number_range, end_of_number_range, number_of_digits_in_ticket_number)
    new_tickets = set()
    while len(new_tickets) < number_of_tickets:
        ticket = random.randint(start_of_number_range, end_of_number_range)
        new_tickets.add(ticket)
    return new_tickets

if __name__ == '__main__':
    tickets = generate_ticket_numbers()
    print_tickets(tickets)