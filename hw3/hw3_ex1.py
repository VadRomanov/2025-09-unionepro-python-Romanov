import matplotlib.pyplot as plt

if __name__ == '__main__':
    minutes = [26, 42, 82]
    calories = [138, 229, 445]
    plt.plot()
    plt.plot(minutes,
             calories,
             color='g',
             marker='^',
             label='Затраченные калории',
             markerfacecolor='red',
             markeredgecolor='red')
    plt.title('Зависимость количество потраченных калорий\n от времени ходьбы в минутах', fontsize=15)
    plt.xlabel('Минуты', fontsize=12, color='blue')
    plt.ylabel('Калории', fontsize=12, color='blue')
    plt.legend()
    plt.grid(True)
    plt.show()