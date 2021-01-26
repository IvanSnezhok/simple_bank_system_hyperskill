import random
import sqlite3


def sql_insert(execute, info):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
    conn.commit()
    cur.execute(execute, info)
    conn.commit()
    conn.close()


def sql_fetch(execute, info):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
    conn.commit()
    cur.execute(execute, info)
    return print(cur.fetchall()), conn.commit(), conn.close()


def odd_multiply(numbers):
    for i in range(1, len(numbers) + 1, 2):
        numbers[i - 1] *= 2
    return numbers


def luhn_algorithm(card):
    str_15_digits = card
    numbers = [int(x) for x in str_15_digits]
    odd_by_two = odd_multiply(numbers)
    subtracted = map(lambda x: x - 9 if x > 9 else x, odd_by_two)
    checksum = sum(subtracted)
    control_n = 10 - (checksum % 10)
    return control_n if control_n < 10 else 0


def check_luhn(card):
    checksum = int(card[15])
    exp_checksum = luhn_algorithm(card[:15])
    if checksum == exp_checksum:
        return True
    return False


def check_card(check_number):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("SELECT number FROM card")
    info_card = [x[0] for x in cur.fetchall()]
    if check_number in info_card:
        cur.close()
        return True
    else:
        cur.close()
        return False


def check_pin(log_pin, check_number):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("SELECT pin FROM card WHERE number = ?", (check_number, ))
    conn.commit()
    info_pin = [x[0] for x in cur.fetchall()]
    if log_pin in info_pin:
        cur.close()
        return True
    else:
        cur.close()
        return False


def balance_card(card):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('SELECT balance From card WHERE number = ?', (card, ))
    balance = cur.fetchone()
    return balance[0]


class BankMenu:

    def __init__(self):
        self.number = None
        self.pin = None
        self.card = ()
        self.acc_num = None
        self.log_pin = None

    def card_gen(self):
        iin = str('400000')
        customer_number = random.randrange(100000000, 999999999)
        check_card_luhn = iin + str(customer_number)
        checksum = luhn_algorithm(check_card_luhn)
        self.number = iin + str(customer_number) + str(checksum)
        self.pin = random.randrange(1000, 9999)
        self.card = (self.number, self.pin)
        sql_insert("INSERT INTO card (number, pin) VALUES (?,?)", self.card)

    def sign_in(self):
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        choice = int(input())

        if choice == 1:
            BankMenu.card_gen(self)
            print('Your card has been created')
            print('Your card numbers:')
            print(self.number)
            print('Your card PIN:')
            print(self.pin)

        elif choice == 2:
            BankAccount.login(BankAccount())
        elif choice == 0:
            print('Bye!')
            exit()


class BankAccount(BankMenu):

    def login(self):
        print('Enter your card number:')
        log_card = input()
        self.acc_num = log_card
        print('Enter your PIN:')
        log_pin = input()
        if check_card(log_card) and check_pin(log_pin, log_card):
            print('You have successfully logged in!')
            self.account()
        else:
            print("Wrong card number or PIN!")
            BankMenu.sign_in(self)

    def account(self):
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')
        acc_choice = int(input())

        if acc_choice == 1:
            print(balance_card(self.acc_num))
            self.account()

        elif acc_choice == 2:
            print('Enter income:')
            income_money = int(input())
            conn = sqlite3.connect('card.s3db')
            cur = conn.cursor()
            cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (income_money, self.acc_num))
            conn.commit()
            conn.close()
            print('Income was added!')
            self.account()

        elif acc_choice == 3:
            print('Transfer')
            to_card = input('Enter card number: ')
            if self.acc_num == to_card:
                print("You can't transfer money to the same account!")
                self.account()
            elif not check_luhn(to_card):
                print("Probably you made a mistake in the card number. Please try again!")
                self.account()
            elif not check_card(to_card):
                print("Such a card does not exist.")
                self.account()
            print("Enter how much money you want to transfer:")
            money_to_card = int(input())
            if money_to_card > int(balance_card(self.acc_num)):
                print("Not enough money!")
                self.account()
            else:
                sql_insert('UPDATE card SET balance = balance + ? WHERE number = ?', (money_to_card, to_card,))
                sql_insert('UPDATE card SET balance = balance - ? WHERE number = ?', (money_to_card, self.acc_num,))
                print('Success!')
                self.account()

        elif acc_choice == 4:
            conn = sqlite3.connect('card.s3db')
            cur = conn.cursor()
            cur.execute('DELETE FROM card WHERE number = ?', (self.acc_num, ))
            conn.commit()
            cur.close()
            BankMenu.sign_in(self)
            
        elif acc_choice == 5:
            print('You have successfully logged out!')
            BankMenu.sign_in(self)

        elif acc_choice == 0:
            print('Bye!')
            exit()


while True:
    client = BankMenu()
    client.sign_in()
