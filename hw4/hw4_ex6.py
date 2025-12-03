import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv('train.csv')
    class_counts = df['Pclass'].value_counts()
    sns.barplot(x=class_counts.index, y=class_counts.values)

    plt.title('Распределение пассажиров по классам обслуживания')
    plt.xlabel('Класс обслуживания')
    plt.ylabel('Количество пассажиров')

    print('Наибольшее кол-во пассажиров было в 3 классе')
    plt.show()
