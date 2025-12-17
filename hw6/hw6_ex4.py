import unittest

class BankAccount:
    def __init__(self):
        self.balance = 0.0
        self.miles = 100

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount() # создаётся НОВЫЙ счёт для каждого теста

    def test_origin_balance(self):
        self.assertEqual(self.account.balance, 0)

    def test_deposit(self):
        self.account.deposit(100)
        self.assertEqual(self.account.balance, 100)

    def test_withdraw(self):
        self.account.deposit(200)
        self.account.withdraw(50)
        self.assertEqual(self.account.balance, 150)

    def test_independence(self):
        second_account = BankAccount()
        self.account.deposit(100)
        self.assertEqual(self.account.balance, 100)
        self.assertEqual(second_account.balance, 0)
