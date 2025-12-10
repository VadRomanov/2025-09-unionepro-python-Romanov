class BankAccount:

    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def add(self, amount):
        if amount <= 0:
            print('Ошибка. Нельзя зачислить неположительную сумму')
            return
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            print('Ошибка. Недостаточно средств на счете')
            return
        if amount <= 0:
            print('Ошибка. Нельзя снять неположительную сумму')
            return
        self.balance -= amount


if __name__ == '__main__':
    account = BankAccount(777, 1000)
    account.withdraw(1100)
    account.add(100)
    account.withdraw(101)

    print(account.balance)
