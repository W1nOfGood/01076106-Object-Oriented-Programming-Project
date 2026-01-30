class Bank:

    def __init__(self):
        self.__user_list = []
        self.__atm_list = []
        self.__seller_list = []

    def add_user(self, user):
        self.__user_list.append(user)

    def search_user_from_id(self, citizen_id):
        for user in self.__user_list:
            if user.citizen_id == citizen_id:
                return user
        return None

    def add_atm_machine(self, atm):
        self.__atm_list.append(atm)

    def search_atm_machine(self, atm_no):
        for atm in self.__atm_list:
            if atm.atm_no == atm_no:
                return atm
        return None

    def add_seller(self, seller):
        self.__seller_list.append(seller)

    def search_seller(self, name):
        for seller in self.__seller_list:
            if seller.name == name:
                return seller
        return None

    def search_account_from_card(self, card_no):
        for user in self.__user_list:
            for account in user.account_list:
                if hasattr(account, 'get_card') and account.get_card() is not None:
                    if account.get_card().card_no == card_no:
                        return account
        return None

    def search_account_from_account_no(self, account_no):
        for user in self.__user_list:
            for account in user.account_list:
                if account.account_no == account_no:
                    return account
        return None

class User:
    def __init__(self, citizen_id, name):
        self.__citizen_id = citizen_id
        self.__name = name
        self.__account_list = []

    @property
    def citizen_id(self):
        return self.__citizen_id

    @property
    def name(self):
        return self.__name

    @property
    def account_list(self):
        return self.__account_list

    def add_account(self, account):
        self.__account_list.append(account)

    def search_account(self, account_no):
        for account in self.__account_list:
            if account.account_no == account_no:
                return account
        return None

class Account:
    def __init__(self, account_no, amount):
        self.__account_no = account_no
        self.__amount = amount
        self.__transaction = []

    @property
    def account_no(self):
        return self.__account_no

    @property
    def amount(self):
        return self.__amount

    def __add__(self, amount):
        if amount > 0:
            self.__amount += amount
            self.__transaction.append(Transaction('D', amount, self.__amount, None))
        return self

    def __sub__(self, amount):
        if amount > 0 and amount <= self.__amount:
            self.__amount -= amount
            self.__transaction.append(Transaction('W', amount, self.__amount, None))
        return self

    def transfer(self, amount, target_account):
        if amount > 0 and amount <= self.__amount and amount <= 100000:
            self.__amount -= amount
            self.__transaction.append(Transaction('T', amount, self.__amount, target_account.account_no))
            target_account + amount
        return self

    def paid(self, amount, target_account):
        if amount > 0 and amount <= self.__amount:
            self.__amount -= amount
            self.__transaction.append(Transaction('P', amount, self.__amount, target_account.account_no))
            target_account + amount
        return self

    def __iter__(self):
        return iter(self.__transaction)

class SavingAccount(Account):

    def __init__(self, account_no, amount):
        Account.__init__(self, account_no, amount)
        self.__card = None

    def add_card(self, card):
        self.__card = card

    def get_card(self):
        return self.__card

class FixDepositAccount(Account):
    pass

class Transaction:
    def __init__(self, transaction_type, amount, total, target_account):
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__total = total
        self.__target_account = target_account

    def __str__(self):
        if self.__target_account:
            return f"Type: {self.__transaction_type}, Amount: {self.__amount}, Balance: {self.__total}, Target: {self.__target_account}"
        return f"Type: {self.__transaction_type}, Amount: {self.__amount}, Balance: {self.__total}"

class Card:
    def __init__(self,card_no, account, pin):
        self.__card_no = card_no
        self.__account = account
        self.__pin = pin

    @property
    def card_no(self):
        return self.__card_no

    @property
    def account(self):
        return self.__account

    @property
    def pin(self):
        return self.__pin

class ATM_Card(Card):
    pass

class Debit_Card(Card):
    pass

class ATM_machine:

    withdraw_limit = 20000
    transfer_limit = 100000

    def __init__(self,atm_no,money):
        self.__atm_no = atm_no
        self.__money = money

    @property
    def atm_no(self):
        return self.__atm_no

    def insert_card(self, card, pin):
        if card.pin == pin:
            return "Success"
        return None

    def deposit(self, account, amount):
        if amount > 0:
            self.__money += amount
            account + amount
        return self

    def withdraw(self, account, amount):
        if amount > 0 and amount <= self.withdraw_limit and amount <= self.__money and amount <= account.amount:
            self.__money -= amount
            account - amount
        return self

    def transfer(self, account, amount, target_account):
        if amount > 0 and amount <= self.transfer_limit and amount <= account.amount:
            account.transfer(amount, target_account)
        return self

class Seller:
    def __init__(self,name):
        self.__name = name
        self.__edc_list = []

    @property
    def name(self):
        return self.__name

    def add_edc(self, edc):
        self.__edc_list.append(edc)

    def search_edc_from_no(self, edc_no):
        for edc in self.__edc_list:
            if edc.edc_no == edc_no:
                return edc
        return None

    def paid(self, account, amount, target_account):
        account.paid(amount, target_account)

class EDC_machine:
    def __init__(self,edc_no):
        self.__edc_no = edc_no

    @property
    def edc_no(self):
        return self.__edc_no

    def paid(self, debit_card, amount, target_account):
        debit_card.account.paid(amount, target_account)



##################################################################################

# Reference data format: {Citizen ID: [Name, Account Type, Account Number, Account Balance, Card Type, Card Number]}


# TODO 1: Create an instance of the Bank and create instances of User, Account, and Card
# TODO   : Use the data in the `user` dictionary freely in any format.
# TODO   : The Account class is divided into two subclasses: Savings and FixedDeposit.
# TODO   : The Card class is divided into two subclasses: ATM and Debit.


scb = Bank()
scb.add_user(User('1-1101-12345-12-0','Harry Potter'))
scb.add_user(User('1-1101-12345-13-0','Hermione Jean Granger'))
scb.add_user(User('9-0000-00000-01-0','KFC'))
scb.add_user(User('9-0000-00000-02-0','Tops'))
harry = scb.search_user_from_id('1-1101-12345-12-0')
harry.add_account(SavingAccount('1234567890', 20000))
harry_account = harry.search_account('1234567890')
harry_account.add_card(ATM_Card('12345', harry_account, '1234'))
hermione = scb.search_user_from_id('1-1101-12345-13-0')
hermione.add_account(SavingAccount('0987654321', 2000))
hermione_account1 = hermione.search_account('0987654321')
hermione_account1.add_card(Debit_Card('12346', hermione_account1, '1234'))
hermione.add_account(FixDepositAccount('0987654322', 1000))
kfc = scb.search_user_from_id('9-0000-00000-01-0')
kfc.add_account(SavingAccount('0000000321', 0))
tops = scb.search_user_from_id('9-0000-00000-02-0')
tops.add_account(SavingAccount('0000000322', 0))

# TODO 2: Create an instance of the ATM machine

scb.add_atm_machine(ATM_machine('1001',1000000))
scb.add_atm_machine(ATM_machine('1002',200000))

# TODO 3: Create an instance of Seller and add EDC machines to the Seller

temp = Seller('KFC')
temp.add_edc(EDC_machine('2101'))
scb.add_seller(temp)
temp = Seller('Tops')
temp.add_edc(EDC_machine('2201'))
scb.add_seller(temp)

# TODO 4: Create a method for deposit using `__add__` and withdrawal using `__sub__`.
# TODO   : Test deposit, withdrawal, and transfer using `+` and `-` with each account type.





# TODO 5: Create methods `insert_card`, `deposit`, `withdraw`, and `transfer` in the ATM machine and call them through the account.
# TODO   : Test money transfers between each account type.




# TODO 6: Create a method paid on the EDC machine and call it through the account.





# TODO 7: Create the itermethod in the Account class to return transactions for use in afor loop.






# Test case #1: Test deposit from an ATM using Harry's ATM card.
# The card must be inserted first. Locate ATM machine 1 and Harry's ATM card.
# Then call the function or method `deposit` from the ATM machine and use `+` from the account.
# Expected outcome:
# Test Case #1
# Harry's ATM No :  12345
# Harry's Account No :  1234567890
# Success
# Harry account before deposit :  20000
# Deposit 1000
# Harry account after deposit :  21000

atm_machine = scb.search_atm_machine('1001')
harry_account = scb.search_account_from_card('12345')
atm_card = harry_account.get_card()
print("Test Case #1")
print("Harry's ATM No : ",atm_card.card_no)
print("Harry's Account No : ",harry_account.account_no)
print(atm_machine.insert_card(atm_card, "1234"))
print("Harry account before deposit : ",harry_account.amount)
print("Deposit 1000")
atm_machine.deposit(harry_account,1000)
print("Harry account after deposit : ",harry_account.amount)
print("")



# Test case #2: Test withdrawal from an ATM using Hermione's ATM card.
# The card must be inserted first. Locate ATM machine 2 and Hermione's ATM card.
# Then call the function or method `withdraw` from the ATM machine and use `-` from the account.
# Expected outcome:
# Test Case #2
# Hermione's ATM No :  12346
# Hermione's Account No :  0987654321
# Success
# Hermione account before withdraw :  2000
# withdraw 1000
# Hermione account after withdraw :  1000

atm_machine = scb.search_atm_machine('1002')
hermione_account = scb.search_account_from_card('12346')
atm_card = hermione_account.get_card()
print("Test Case #2")
print("Hermione's ATM No : ", atm_card.card_no)
print("Hermione's Account No : ", hermione_account.account_no)
print(atm_machine.insert_card(atm_card, "1234"))
print("Hermione account before withdraw : ",hermione_account.amount)
print("withdraw 1000")
atm_machine.withdraw(hermione_account,1000)
print("Hermione account after withdraw : ",hermione_account.amount)
print("")



# Test case #3: Test transferring 10,000 THB from Harry's account to Hermione's account at the counter.
# Call the method for performing the money transfer.
# Expected outcome:
# Test Case #3
# Harry's Account No :  1234567890
# Hermione's Account No :  0987654321
# Harry account before transfer :  21000
# Hermione account before transfer :  1000
# Harry account after transfer :  11000
# Hermione account after transfer :  11000

harry_account = scb.search_account_from_card('12345')
hermione_account = scb.search_account_from_card('12346')
print("Test Case #3")
print("Harry's Account No : ",harry_account.account_no)
print("Hermione's Account No : ", hermione_account.account_no)
print("Harry account before transfer : ",harry_account.amount)
print("Hermione account before transfer : ",hermione_account.amount)
harry_account.transfer(10000, hermione_account)
print("Harry account after transfer : ",harry_account.amount)
print("Hermione account after transfer : ",hermione_account.amount)
print("")


# Test case #4: Test payment using a card reader. Call the `paid` method from the card reader.
# Hermione makes a payment of 500 THB to KFC using her own card.
# Expected outcome:
# Hermione's Debit Card No :  12346
# Hermione's Account No :  0987654321
# Seller :  KFC
# KFC's Account No :  0000000321
# KFC account before paid :  0
# Hermione account before paid :  11000
# KFC account after paid :  500
# Hermione account after paid :  10500

hermione_account = scb.search_account_from_account_no('0987654321')
debit_card = hermione_account.get_card()
kfc_account = scb.search_account_from_account_no('0000000321')
kfc = scb.search_seller('KFC')
edc = kfc.search_edc_from_no('2101')

print("Test Case #4")
print("Hermione's Debit Card No : ", debit_card.card_no)
print("Hermione's Account No : ",hermione_account.account_no)
print("Seller : ", kfc.name)
print("KFC's Account No : ", kfc_account.account_no)
print("KFC account before paid : ",kfc_account.amount)
print("Hermione account before paid : ",hermione_account.amount)
edc.paid(debit_card, 500, kfc_account)
print("KFC account after paid : ",kfc_account.amount)
print("Hermione account after paid : ",hermione_account.amount)
print("")


# Test case #5: Test electronic payment by calling the `paid` method from KFC.
# Hermione makes a payment of 500 THB to Tops.
# Expected outcome:
# Test Case #5
# Hermione's Account No :  0987654321
# Tops's Account No :  0000000322
# Tops account before paid :  0
# Hermione account before paid :  10500
# Tops account after paid :  500
# Hermione account after paid :  10000

hermione_account = scb.search_account_from_account_no('0987654321')
tops_account = scb.search_account_from_account_no('0000000322')
tops = scb.search_seller('Tops')
print("Test Case #5")
print("Hermione's Account No : ",hermione_account.account_no)
print("Tops's Account No : ", tops_account.account_no)
print("Tops account before paid : ",tops_account.amount)
print("Hermione account before paid : ",hermione_account.amount)
tops.paid(hermione_account,500,tops_account)
print("Tops account after paid : ",tops_account.amount)
print("Hermione account after paid : ",hermione_account.amount)
print("")


# Test case #6: Display all transactions of Hermione using a `for` loop.
# Expected outcome:
# Test Case #6
# Hermione's transactions:
# Type: W, Amount: 1000, Balance: 1000
# Type: D, Amount: 10000, Balance: 11000
# Type: P, Amount: 500, Balance: 10500
# Type: P, Amount: 500, Balance: 10000

hermione_account = scb.search_account_from_account_no('0987654321')
print("Test Case #6")
print("Hermione's transactions:")
for transaction in hermione_account:
    print(transaction)
