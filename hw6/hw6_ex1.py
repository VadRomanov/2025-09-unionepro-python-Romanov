import re

text = """
В 1910 году Генри Норрис Расселл изучал звёзды.
В 1926 году Фаулер опубликовал статью.
Юнона пролетела мимо Европы в 2022 году.
А в 2031 году ожидается прибытие JUICE.
"""

def find_years_in_text(text):
    return re.findall(r'\b([1-2]\d{3})\b', text)

if __name__ == '__main__':
    result = find_years_in_text(text)
    print(result)