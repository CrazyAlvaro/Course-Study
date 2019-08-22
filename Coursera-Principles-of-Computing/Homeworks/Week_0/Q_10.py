class BankAccount:
    def __init__(self, initial_balance):
        """ Creates an account with the given balance.  """
        self._balance_ = initial_balance
        self._fee_ = 0

    def deposit(self, amount):
        """Deposits the amount into the account."""
        self._balance_ += amount

    def withdraw(self, amount):
        """
        Withdraws the amount from the account.  Each withdrawal resulting in a
        negative balance also deducts a penalty fee of 5 dollars from the balance.
        """
        self._balance_ -= amount
        if self._balance_ < 0:
            self._balance_ -= 5
            self._fee_ += 5

    def get_balance(self):
        """Returns the current balance in the account."""
        return self._balance_

    def get_fees(self):
        """Returns the total fees ever deducted from the account."""
        return self._fee_


if __name__ == "__main__":
    """ unit test """
    my_account = BankAccount(10)
    my_account.withdraw(5)
    my_account.deposit(10)
    my_account.withdraw(5)
    my_account.withdraw(15)
    my_account.deposit(20)
    my_account.withdraw(5) 
    my_account.deposit(10)
    my_account.deposit(20)
    my_account.withdraw(15)
    my_account.deposit(30)
    my_account.withdraw(10)
    my_account.withdraw(15)
    my_account.deposit(10)
    my_account.withdraw(50) 
    my_account.deposit(30)
    my_account.withdraw(15)
    my_account.deposit(10)
    my_account.withdraw(5) 
    my_account.deposit(20)
    my_account.withdraw(15)
    my_account.deposit(10)
    my_account.deposit(30)
    my_account.withdraw(25) 
    my_account.withdraw(5)
    my_account.deposit(10)
    my_account.withdraw(15)
    my_account.deposit(10)
    my_account.withdraw(10) 
    my_account.withdraw(15)
    my_account.deposit(10)
    my_account.deposit(30)
    my_account.withdraw(25) 
    my_account.withdraw(10)
    my_account.deposit(20)
    my_account.deposit(10)
    my_account.withdraw(5) 
    my_account.withdraw(15)
    my_account.deposit(10)
    my_account.withdraw(5) 
    my_account.withdraw(15)
    my_account.deposit(10)
    my_account.withdraw(5) 
    print my_account.get_balance(), my_account.get_fees()
