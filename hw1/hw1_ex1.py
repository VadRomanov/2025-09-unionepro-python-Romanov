import random
from xmlrpc.client import MAXINT, MININT


def copy_array_without_first_and_last_elements(origin_array):
    copy_array = origin_array[:]
    copy_array.pop(0)
    copy_array.pop(-1)
    return copy_array


def check_array_contains_elements(array_to_check, *elements):
    intersection = set(array_to_check) & set(elements)
    return len(intersection) == len(elements)


if __name__ == '__main__':
    try:
        list_size = input('Введите размер массива:')
        if list_size.isalpha():
            raise Exception('Должно быть целое положительное число')
        list_size = int(list_size)
        if list_size < 0:
            raise Exception('Число должно быть положительным')
    except ValueError:
        print('Число должно быть целым')
    except Exception as e:
        print(e)
    else:
        array = [random.randint(MININT, MAXINT) for _ in range(1, list_size + 1)]

        print(f'Длина массива: {len(array)}')
        print(f'Последний элемент массива: {array[-1]}')
        print(f'Массив в обратном порядке: {array[::-1]}')
        print('Да' if check_array_contains_elements(array, 5, 17) else 'Нет')
        print(
            f'Копия массива после удаления первого и последнего элементов: {copy_array_without_first_and_last_elements(array)}')
