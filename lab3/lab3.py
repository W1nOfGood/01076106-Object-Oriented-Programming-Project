class User:
    def __init__(self, citizen_id: str, name: str):
        self.__citizen_id = citizen_id
        self.__name = name

    def get_citizen_id(self) -> str:
        return self.__citizen_id

    def get_name(self) -> str:
        return self.__name


class Transaction:
    def __init__(self, transaction_type: str, amount: float, atm_id: str, balance: float, transfer_account = None):
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__atm_id = atm_id
        self.__balance = balance
        self.__transfer_account = transfer_account

    def get_transaction_type(self) -> str:
        return self.__transaction_type

    def get_amount(self) -> float:
        return self.__amount

    def get_atm_id(self) -> str:
        return self.__atm_id

    def get_balance(self) -> float:
        return self.__balance

    def get_transfer_account(self):
        return self.__transfer_account

    def __str__(self) -> str:
        return f"{self.__transaction_type}-ATM:{self.__atm_id}-{int(self.__amount)}-{int(self.__balance)}"


class Account:
    def __init__(self, account_number: str, owner: User):
        self.__account_number = account_number
        self.__owner = owner
        self.__balance = 0.0
        self.__transactions = []

    def get_account_number(self) -> str:
        return self.__account_number

    def get_owner(self) -> User:
        return self.__owner

    def get_balance(self) -> float:
        return self.__balance

    def set_balance(self, amount: float):
        self.__balance = amount

    def deposit(self, amount: float, atm_id: str) -> str:
        if amount <= 0:
            return "error"
        self.__balance += amount
        transaction = Transaction("D", amount, atm_id, self.__balance)
        self.__transactions.append(transaction)
        return "success"

    def withdraw(self, amount: float, atm_id: str) -> str:
        if amount <= 0 or amount > self.__balance:
            return "error"
        self.__balance -= amount
        transaction = Transaction("W", amount, atm_id, self.__balance)
        self.__transactions.append(transaction)
        return "success"

    def transfer_out(self, amount: float, atm_id: str, to_account_number: str) -> str:
        if amount <= 0 or amount > self.__balance:
            return "error"
        self.__balance -= amount
        transaction = Transaction("TW", amount, atm_id, self.__balance, to_account_number)
        self.__transactions.append(transaction)
        return "success"

    def transfer_in(self, amount: float, atm_id: str, from_account_number: str) -> str:
        if amount <= 0:
            return "error"
        self.__balance += amount
        transaction = Transaction("TD", amount, atm_id, self.__balance, from_account_number)
        self.__transactions.append(transaction)
        return "success"

    def get_transactions(self) -> list:
        return self.__transactions


class ATMCard:
    def __init__(self, card_number: str, account: Account, pin: str):
        self.__card_number = card_number
        self.__account = account
        self.__pin = pin
        self.__annual_fee = 150
        self.__daily_withdrawal_limit = 40000

    def get_card_number(self) -> str:
        return self.__card_number

    def get_account(self) -> Account:
        return self.__account

    def verify_pin(self, pin: str) -> bool:
        return self.__pin == pin

    def get_daily_withdrawal_limit(self) -> float:
        return self.__daily_withdrawal_limit


class ATMMachine:
    def __init__(self, machine_id: str, initial_amount: float = 1000000):
        self.__machine_id = machine_id
        self.__balance = initial_amount
        self.__bank = None

    def get_machine_id(self) -> str:
        return self.__machine_id

    def get_balance(self) -> float:
        return self.__balance

    def set_bank(self, bank):
        self.__bank = bank

    def insert_card(self, card_number: str, pin = None):
        if self.__bank is None:
            return None
        card = self.__bank.get_card(card_number)
        if card:
            if pin and not card.verify_pin(pin):
                return "Invalid PIN"
            return card.get_account()
        return None

    def deposit(self, account: Account, amount: float) -> str:
        if amount <= 0:
            return "error"
        result = account.deposit(amount, self.__machine_id)
        if result == "success":
            self.__balance += amount
        return result

    def withdraw(self, account: Account, amount: float) -> str:
        if amount <= 0:
            return "error"
        if amount > self.__balance:
            return "ATM has insufficient funds"
        if amount > 40000:
            return "Exceeds daily withdrawal limit of 40,000 Baht"
        if amount > account.get_balance():
            return "error"
        result = account.withdraw(amount, self.__machine_id)
        if result == "success":
            self.__balance -= amount
        return result

    def transfer(self, from_account: Account, to_account: Account, amount: float) -> str:
        if amount <= 0 or amount > from_account.get_balance():
            return "error"

        result_out = from_account.transfer_out(amount, self.__machine_id, to_account.get_account_number())
        if result_out == "error":
            return "error"

        result_in = to_account.transfer_in(amount, self.__machine_id, from_account.get_account_number())
        if result_in == "error":
            return "error"

        return "success"


class Bank:
    def __init__(self):
        self.__users = []
        self.__accounts = []
        self.__cards = []
        self.__atms = []

    def add_user(self, user: User):
        self.__users.append(user)

    def add_account(self, account: Account):
        self.__accounts.append(account)

    def add_card(self, card: ATMCard):
        self.__cards.append(card)

    def add_atm(self, atm: ATMMachine):
        self.__atms.append(atm)

    def get_card(self, card_number: str):
        for card in self.__cards:
            if card.get_card_number() == card_number:
                return card
        return None

    def get_atm(self, machine_id: str):
        for atm in self.__atms:
            if atm.get_machine_id() == machine_id:
                return atm
        return None

##################################################################################


## Define the format of the user as follows:
## {Citizen ID: [Name, Account Number, ATM Card Number, Account Balance]}

user ={'1-1101-12345-12-0':['Harry Potter','1234567890','12345',20000],
       '1-1101-12345-13-0':['Hermione Jean Granger','0987654321','12346',1000]}

atm ={'1001':1000000,'1002':200000}

## TODO 1: From the user data, create instances with the following details:
## TODO: key:value, where the key is the Citizen ID, and the value contains
## TODO: [Name, Account Number, ATM Card Number, Account Balance].
## TODO: Return the instance of the bank and create two ATM instances.

bank = Bank()

for citizen_id, data in user.items():
    name = data[0]
    account_number = data[1]
    card_number = data[2]
    initial_balance = data[3]

    user_obj = User(citizen_id, name)
    bank.add_user(user_obj)

    account_obj = Account(account_number, user_obj)
    bank.add_account(account_obj)

    account_obj.set_balance(initial_balance)

    card_obj = ATMCard(card_number, account_obj, "1234")
    bank.add_card(card_obj)

for atm_id, balance in atm.items():
    atm_obj = ATMMachine(atm_id, balance)
    atm_obj.set_bank(bank)
    bank.add_atm(atm_obj)



## TODO 2: Write a method to insert an ATM card into the machine. It should accept two parameters:
## TODO: 1) Bank instance 2) ATM card number.
## TODO: If the card is valid, return the account instance; if not, return None.
## TODO: This should be a method of the ATM machine.




## TODO 3: Write a method to deposit money. It should accept three parameters:
## TODO: 1) ATM machine instance, 2) Account instance, 3) Deposit amount.
## TODO: The method should increase the account balance and log the transaction in the account.
## TODO: Return "success" if the transaction is successful, otherwise return "error."
## TODO: Validate the input, e.g., the amount must be greater than 0.






## TODO 4: Write a method to withdraw money. It should accept three parameters:
## TODO: 1) ATM machine instance, 2) Account instance, 3) Withdrawal amount.
## TODO: The method should decrease the account balance and log the transaction in the account.
## TODO: Return "success" if the transaction is successful, otherwise return "error."
## TODO: Validate the input, e.g., the amount must be greater than 0 and not exceed the account balance.






## TODO 5: Write a method to transfer money. It should accept four parameters:
## TODO: 1) ATM machine instance, 2) Sender account instance, 3) Recipient account instance, 4) Transfer amount.
## TODO: The method should decrease the sender's balance, increase the recipient's balance, and log the transaction.
## TODO: Return "success" if the transaction is successful, otherwise return "error."
## TODO: Validate the input, e.g., the amount must be greater than 0 and not exceed the sender's balance.


print("--------------------------")
print("     Start Test Cases     ")
print("--------------------------")


# Test case #1: Test inserting Harry's ATM card into ATM machine #1
# and call the corresponding method.
# Expected result: Print Harry's account number and ATM card number correctly.
# Ans: 12345, 1234567890, Success
print("-------------------------")
atm_machine = bank.get_atm('1001')
harry_account = atm_machine.insert_card('12345', '1234')
if harry_account:
    print(f"{bank.get_card('12345').get_card_number()}, {harry_account.get_account_number()}, Success")
else:
    print("Failed to insert card")






# Test case #2: Test depositing 1000 Baht into Hermione's account using ATM machine #2.
# Call the deposit method.
# Expected result: Display Hermione's balance before and after the deposit, along with the transaction.
# Hermione's account before test: 1000
# Hermione's account after test: 2000
print("-------------------------")
atm_machine = bank.get_atm('1002')
hermione_account = atm_machine.insert_card('12346', '1234')
print(f"Hermione's account before test: {int(hermione_account.get_balance())}")
atm_machine.deposit(hermione_account, 1000)
print(f"Hermione's account after test: {int(hermione_account.get_balance())}")






# Test case #3: Test depositing -1 Baht into Hermione's account using ATM machine #2.
# Expected result: Display "Error."
print("-------------------------")
result = atm_machine.deposit(hermione_account, -1)
print(result)




# Test case #4: Test withdrawing 500 Baht from Hermione's account using ATM machine #2.
# Call the withdrawal method.
# Expected result: Display Hermione's balance before and after the withdrawal, along with the transaction.
# Hermione's account before test: 2000
# Hermione's account after test: 1500
print("-------------------------")
print(f"Hermione's account before test: {int(hermione_account.get_balance())}")
atm_machine.withdraw(hermione_account, 500)
print(f"Hermione's account after test: {int(hermione_account.get_balance())}")




# Test case #5: Test withdrawing 2000 Baht from Hermione's account using ATM machine #2.
# Expected result: Display "Error."
print("-------------------------")
result = atm_machine.withdraw(hermione_account, 2000)
print(result)





# Test case #6: Test transferring 10,000 Baht from Harry's account to Hermione's account using ATM machine #2.
# Call the transfer method.
# Expected result: Display Harry's balance before and after the transfer, Hermione's balance before and after the transfer, and the transaction log.
# Harry's account before test: 20000
# Harry's account after test: 10000
# Hermione's account before test: 1500
# Hermione's account after test: 11500
print("-------------------------")
print(f"Harry's account before test: {int(harry_account.get_balance())}")
print(f"Hermione's account before test: {int(hermione_account.get_balance())}")
atm_machine.transfer(harry_account, hermione_account, 10000)
print(f"Harry's account after test: {int(harry_account.get_balance())}")
print(f"Hermione's account after test: {int(hermione_account.get_balance())}")





# Test case #7: Display all of Hermione's transactions.
# Expected result:
# Hermione's transaction log:
# D-ATM:1002-1000-2000
# W-ATM:1002-500-1500
# TD-ATM:1002-10000-11500
print("-------------------------")
print("Hermione's transaction log:")
for transaction in hermione_account.get_transactions():
    print(transaction)



print("-------------------------")
# Test case #8: Test inserting an incorrect PIN.
# Call the method to insert the card and check the PIN.
atm_machine = bank.get_atm('1001')
test_result = atm_machine.insert_card('12345', '9999')  # Incorrect PIN
print(f"Actual result: {test_result}")
# Expected result: Invalid PIN
print("-------------------------")






# Test case #9: Test withdrawing more than the daily limit (40,000 Baht).
atm_machine = bank.get_atm('1001')
account = atm_machine.insert_card('12345', '1234')  # Correct PIN
harry_balance_before = account.get_balance()
print(f"Harry's account before test: {harry_balance_before}")
print("Attempting to withdraw 45,000 Baht...")
result = atm_machine.withdraw(account, 45000)
print(f"Expected result: Exceeds daily withdrawal limit of 40,000 Baht")
print(f"Actual result: {result}")
print(f"Harry's account after test: {account.get_balance()}")
print("-------------------------")






# Test case #10: Test withdrawing money when the ATM has insufficient funds.
atm_machine = bank.get_atm('1002')  # Assume machine #2 has 200,000 Baht left
account = atm_machine.insert_card('12345', '1234')
print("Test case #10: Test withdrawal when ATM has insufficient funds.")
print(f"ATM machine balance before: {atm_machine.get_balance()}")
print("Attempting to withdraw 250,000 Baht...")
result = atm_machine.withdraw(account, 250000)
print(f"Expected result: ATM has insufficient funds.")
print(f"Actual result: {result}")
print(f"ATM machine balance after: {atm_machine.get_balance()}")
print("-------------------------")

