import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    cars = ['A1', 'A8', 'A3', 'A4', 'A5', 'A6']
    prices = [1500000, 2500000, 1400000, 2200000, 1300000, 1450000]

    original_prices = np.array(prices)
    prices_after_increase = original_prices * 1.05

    index = np.arange(len(cars))
    bw = 0.3
    plt.title('Влияние утильсбора на цены машин', fontsize=15)
    plt.bar(index, original_prices, bw, color='b', label='Оригинальная цена')
    plt.bar(index + bw, prices_after_increase, bw, color='orange', label='С утильсбором')
    plt.xticks(index + bw / 2, cars)
    plt.xlabel('Машины', fontsize=12)
    plt.ylabel('Цена, ₽', fontsize=12)
    plt.legend()
    plt.show()