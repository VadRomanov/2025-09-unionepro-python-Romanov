import re

def is_inn(value):
    return bool(re.match(r'^\d{12}$', value))

if __name__ == '__main__':
    print(is_inn('123456789012'))
    print(is_inn('12 3456789012'))
    print(is_inn('123456789012g'))
    print(is_inn('q123456789012'))
    print(is_inn(' 123456789012'))
    print(is_inn('123456789012 '))
    print(is_inn('1234'))
