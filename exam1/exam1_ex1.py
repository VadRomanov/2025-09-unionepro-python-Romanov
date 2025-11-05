import datetime


def validate_date(day, month, year):
    datetime.date(year, month, day)

def prepare_str_date(date):
    if not isinstance(date, str):
        raise ValueError
    return date.replace(' ', '')


def is_magic(date: str) -> bool:
    try:
        prepared_str_date = prepare_str_date(date)
        day, month, year = map(int, prepared_str_date.split('.'))
        validate_date(day, month, year)
        control_value = year % 100
        value = day * month
        return value == control_value
    except ValueError:
        print('Ошибка: на входе должна быть строка с правильной датой в формате дд.мм.гггг')
        return False


if __name__ == '__main__':
    print(is_magic('10.06.1960'))
    print(is_magic('11.06.1960'))
    print(is_magic('15.03.1945'))
    print(is_magic('15 . 03.1 94 5'))
    print(is_magic('31.02.2025'))
    print(is_magic(123))
