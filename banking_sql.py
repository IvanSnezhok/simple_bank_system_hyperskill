import random
import sqlite3


def sql_connect_insert(execute, info):
    conn = sqlite3.connect('card.s3db')

# DATABASE card (
# id INTEGER
# number TEXT
# pin TEXT
# balance INTEGER DEFAULT 0)

    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
    conn.commit()
    cur.execute(execute, info)
    conn.commit()
    conn.close()


def sql_connect_exist(execute, card_pin):
    conn = sqlite3.connect('card.s3db')

    # DATABASE card (
    # id INTEGER
    # number TEXT
    # pin TEXT
    # balance INTEGER DEFAULT 0)

    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
    conn.commit()
    return cur.execute(execute, card_pin), cur.fetchone(), conn.commit(), conn.close()


def check_login(check_number, check_pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("SELECT number FROM card")
    info_card = [x[0] for x in cur.fetchall()]
    if check_number in info_card:
        cur.execute("SELECT pin FROM card WHERE number = ?", [check_number])
        info_pin = [x[0] for x in cur.fetchall()]
        if check_pin in info_pin:
            return True
        else:
            return False
    else:
        return False


def odd_multiply(numbers):
    for i in range(1, len(numbers) + 1):
        if i % 2 != 0:
            numbers[i - 1] *= 2
    return numbers


def luhn_algorithm(iin, can):
    str_15_digits = f'{iin}{can}'
    numbers = list(map(lambda x: int(x), str_15_digits))
    odd_by_two = odd_multiply(numbers)
    subtracted = map(lambda x: x - 9 if x > 9 else x, odd_by_two)
    checksum = sum(subtracted)
    control_n = 10 - (checksum % 10)
    return control_n if control_n < 10 else 0


class Bank:

    def __init__(self):
        self.number = None
        self.pin = None
        self.card = ()

    def card_gen(self):
        iin = str('400000')
        customer_number = random.randrange(100000000, 999999999)
        checksum = luhn_algorithm(iin, customer_number)
        self.number = iin + str(customer_number) + str(checksum)
        self.pin = random.randrange(1000, 9999)
        self.card = (self.number, self.pin)
        sql_connect_insert("INSERT INTO card (number, pin) VALUES (?,?)", self.card)

    def account(self):
        print('you have successfully logged in!')
        print('1. Balance')
        print('2. Log out')
        print('0. Exit')
        acc_choice = int(input())
        if acc_choice == 1:
            print('Balance = 0')
            self.account()
        elif acc_choice == 2:
            print('You have successfully logged out!')
            self.sign_in()
        elif acc_choice == 0:
            print('Bye!')
            exit()

    def login(self):
        print('Enter your card number:')
        log_card = input()
        print('Enter your PIN:')
        log_pin = input()
        if check_login(log_card, log_pin):
            self.account()
        else:
            print("Wrong card number or PIN!")
            self.sign_in()

    def sign_in(self):
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        choice = int(input())
        if choice == 1:
            Bank.card_gen(self)
            print('Your card has been created')
            print('Your card numbers:')
            print(self.number)
            print('Your card PIN:')
            print(self.pin)
        elif choice == 2:
            self.login()
        elif choice == 0:
            print('Bye!')
            exit()


while True:
    customer = Bank()
    customer.sign_in()
