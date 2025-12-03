import pandas as pd


def get_age_group(age):
    if age < 18:
        return 'child'
    elif age > 60:
        return 'senior'
    elif 18 <= age <= 60:
        return 'adult'
    else:
        return None


if __name__ == '__main__':
    df = pd.read_csv('train.csv')
    print('Exercise 1.')
    print('====================================================================================================')
    print('\nHead:')
    print('----------------------------------------------------------------------------------------------------')
    print(df.head())
    print('\nInfo:')
    print('----------------------------------------------------------------------------------------------------')
    print(df.info())
    print('\nExercise 2.')
    print('====================================================================================================')
    print(df.isnull().sum() * 100 / len(df))
    print('\nExercise 3.')
    print('====================================================================================================')
    surviving_female = len(df[(df['Survived'] == 1) & (df['Sex'] == 'female')])
    men_over_50 = len(df[(df['Sex'] == 'male') & (df['Age'] > 50)])
    first_class_passengers_paid_over_100 = len(df[(df['Pclass'] == 1) & (df['Fare'] > 100)])
    print(f'Number of surviving female passengers: {surviving_female}')
    print(f'Number of male passengers over 50 years of age: {men_over_50}')
    print(f'Number of first-class passengers who paid more than 100: {first_class_passengers_paid_over_100}')
    print('\nExercise 4.')
    print('====================================================================================================')
    df['Age_group'] = df['Age'].apply(get_age_group)
    print(df.head())
