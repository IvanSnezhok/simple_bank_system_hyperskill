import random


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
    custom_card = []
    custom_pin = []

    def __init__(self):
        self.card = None
        self.pin = None

    def card_gen(self):
        iin = 400000
        customer_number = random.randint(0000000000, 999999999)
        checksum = luhn_algorithm(iin, customer_number)
        self.card = int(f'{iin}{customer_number}{checksum}')
        self.pin = int(random.randint(1111, 9999))
        Bank.custom_card.append(self.card)
        Bank.custom_pin.append(self.pin)

    def account(self):
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
        log_card = int(input())
        print('Enter your PIN:')
        log_pin = int(input())
        if log_card in self.custom_card and log_pin in self.custom_pin:
            print('You successfully logged in!')
            self.account()
        else:
            print('Wrong card number or PIN!')
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
            print(self.card)
            print('Your card PIN:')
            print(self.pin)
        elif choice == 2:
            self.login()
        elif choice == 0:
            exit()


while True:
    customer = Bank()
    customer.sign_in()
