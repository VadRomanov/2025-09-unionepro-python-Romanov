import re

text = """
Температура поверхности Сириуса B — 25000 K, а Сириуса A — 10000 К.
Плотность белого карлика — 10^6 г/см3.
"""

def find_temperatures_in_text(text):
    return re.findall(r'\b\d+\s[KК]\b', text)

if __name__ == '__main__':
    result = find_temperatures_in_text(text)
    print(result)