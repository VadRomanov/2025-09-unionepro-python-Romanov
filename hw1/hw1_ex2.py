def get_fibonacci(n):
    fib_list = [0, 1]
    if n == 0:
        return []
    elif n == 1:
        return [0]
    else:
        while len(fib_list) < n:
            next_fib = fib_list[-1] + fib_list[-2]
            fib_list.append(next_fib)
        return fib_list


def get_sum_of_even(set_n):
    sum_of_even = 0
    for i in set_n:
        if i % 2 == 0:
            sum_of_even += i
    return sum_of_even


if __name__ == '__main__':
    try:
        n = input('Введите целое положительное число:')
        if n.isalpha():
            raise Exception('Должно быть целое положительное число')
        n = int(n)
        if n < 0:
            raise Exception('Число должно быть положительным')
    except ValueError:
        print('Число должно быть целым')
    except Exception as e:
        print(e)
    else:
        fibonacci = get_fibonacci(n)
        sum_of_even = get_sum_of_even(fibonacci)
        print(f'Вывод: {sum_of_even}')
