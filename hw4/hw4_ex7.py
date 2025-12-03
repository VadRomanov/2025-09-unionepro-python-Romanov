import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv('train.csv')
    survivors_count = df.groupby('Pclass')['Survived'].sum().reset_index()
    sns.barplot(x='Pclass', y='Survived', data=survivors_count, palette='viridis')

    plt.title('Общее количество выживших в каждом классе обслуживания')
    plt.xlabel('Класс обслуживания')
    plt.ylabel('Количество выживших пассажиров')

    print('Наибольшее кол-во выживших пассажиров было в 1 классе')
    plt.show()
