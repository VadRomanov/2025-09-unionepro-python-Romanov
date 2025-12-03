import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def with_relatives_condition(row):
    return row['SibSp'] + row['Parch']


if __name__ == '__main__':
    df = pd.read_csv('train.csv')
    df['Relatives'] = df.apply(lambda row: with_relatives_condition(row), axis=1)
    sns.countplot(x='Relatives', data=df)

    plt.title('Кол-во родственников на борту')
    plt.xlabel('Количество родственников на борту')
    plt.ylabel('Количество пассажиров')

    print('Наибольшее кол-во (537) путешествовали без родственников, наибольшее кол-во родственников на борту - 10')
    plt.show()
