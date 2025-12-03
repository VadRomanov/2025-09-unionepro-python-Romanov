import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv('train.csv')
    sns.histplot(x=df['Age'])

    plt.title('Распределение пассажиров по возрасту')
    plt.xlabel('Возраст пассажирв')
    plt.ylabel('Количество пассажиров')

    print('Основная часть пассажиров была от 18 до 35 лет - взрослых')
    plt.show()
