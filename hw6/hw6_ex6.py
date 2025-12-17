import re

def is_rgb(value) -> bool:
    return bool(re.match(r'^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$', value))

if __name__ == '__main__':
    print(is_rgb('#00ffff'))
    print(is_rgb('#00ffft'))
    print(is_rgb('#5d8aa8'))
    print(is_rgb('#0ff'))
    print(is_rgb('#0ff43g54'))
