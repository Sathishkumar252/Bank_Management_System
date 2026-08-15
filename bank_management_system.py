"""
BANK MANAGEMENT SYSTEM
-----------------------
A menu-driven CLI application to manage bank accounts.

Features:
- Create Account (auto-generated account number + PIN protected)
- Deposit / Withdraw money
- Check Balance
- Transfer money between accounts
- View mini statement (transaction history)
- Delete Account
- Data is saved to 'bank_data.json' so it persists between runs
"""

import json
import os
from datetime import datetime

DATA_FILE = "bank_data.json"


# ---------------------------------------------------------
# ACCOUNT CLASS
# ---------------------------------------------------------
class Account:
    def __init__(self, acc_number, name, pin, balance=0, transactions=None):
        self.acc_number = acc_number
        self.name = name
        self.pin = pin
        self.balance = balance
        self.transactions = transactions if transactions else []

    def deposit(self, amount):
        self.balance += amount
        self._log(f"Deposited ₹{amount}")

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance!")
        self.balance -= amount
        self._log(f"Withdrew ₹{amount}")

    def _log(self, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append(f"[{timestamp}] {action} | Balance: ₹{self.balance}")

    def to_dict(self):
        return {
            "acc_number": self.acc_number,
            "name": self.name,
            "pin": self.pin,
            "balance": self.balance,
            "transactions": self.transactions,
        }


# ---------------------------------------------------------
# BANK CLASS (manages all accounts)
# ---------------------------------------------------------
class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_data()

    # ---------- Persistence ----------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                for acc_num, details in data.items():
                    self.accounts[int(acc_num)] = Account(
                        details["acc_number"],
                        details["name"],
                        details["pin"],
                        details["balance"],
                        details["transactions"],
                    )

    def save_data(self):
        data = {acc_num: acc.to_dict() for acc_num, acc in self.accounts.items()}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    # ---------- Core operations ----------
    def create_account(self, name, pin, initial_deposit=0):
        acc_number = 1001 + len(self.accounts)
        while acc_number in self.accounts:
            acc_number += 1
        account = Account(acc_number, name, pin, initial_deposit)
        if initial_deposit > 0:
            account._log(f"Initial deposit ₹{initial_deposit}")
        self.accounts[acc_number] = account
        self.save_data()
        return account

    def authenticate(self, acc_number, pin):
        account = self.accounts.get(acc_number)
        if account and account.pin == pin:
            return account
        return None

    def transfer(self, from_acc, to_acc, amount):
        if to_acc not in self.accounts:
            raise ValueError("Destination account does not exist!")
        from_acc.withdraw(amount)
        dest = self.accounts[to_acc] if isinstance(to_acc, int) else to_acc
        dest.deposit(amount)
        self.save_data()

    def delete_account(self, acc_number):
        if acc_number in self.accounts:
            del self.accounts[acc_number]
            self.save_data()
            return True
        return False


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def get_positive_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("⚠️  Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("⚠️  Please enter a valid number.")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("⚠️  Please enter a valid number.")


def pause():
    input("\nPress Enter to continue...")


# ---------------------------------------------------------
# MAIN MENU / CLI
# ---------------------------------------------------------
def main():
    bank = Bank()

    while True:
        print("\n" + "=" * 40)
        print("        🏦  BANK MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Transfer Money")
        print("6. Mini Statement")
        print("7. Delete Account")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ").strip()

        # ---------------- CREATE ACCOUNT ----------------
        if choice == "1":
            name = input("Enter your name: ").strip()
            pin = get_int("Set a 4-digit PIN: ")
            deposit = get_positive_amount("Initial deposit amount (0 if none): ") \
                if input("Deposit initial amount? (y/n): ").lower() == "y" else 0
            account = bank.create_account(name, pin, deposit)
            print(f"\n✅ Account created successfully!")
            print(f"   Account Number: {account.acc_number}")
            print(f"   Keep this number and PIN safe.")
            pause()

        # ---------------- DEPOSIT ----------------
        elif choice == "2":
            acc_num = get_int("Enter account number: ")
            pin = get_int("Enter PIN: ")
            account = bank.authenticate(acc_num, pin)
            if account:
                amount = get_positive_amount("Enter amount to deposit: ")
                account.deposit(amount)
                bank.save_data()
                print(f"✅ Deposited ₹{amount}. New balance: ₹{account.balance}")
            else:
                print("❌ Invalid account number or PIN.")
            pause()

        # ---------------- WITHDRAW ----------------
        elif choice == "3":
            acc_num = get_int("Enter account number: ")
            pin = get_int("Enter PIN: ")
            account = bank.authenticate(acc_num, pin)
            if account:
                amount = get_positive_amount("Enter amount to withdraw: ")
                try:
                    account.withdraw(amount)
                    bank.save_data()
                    print(f"✅ Withdrew ₹{amount}. New balance: ₹{account.balance}")
                except ValueError as e:
                    print(f"❌ {e}")
            else:
                print("❌ Invalid account number or PIN.")
            pause()

        # ---------------- CHECK BALANCE ----------------
        elif choice == "4":
            acc_num = get_int("Enter account number: ")
            pin = get_int("Enter PIN: ")
            account = bank.authenticate(acc_num, pin)
            if account:
                print(f"💰 Current Balance: ₹{account.balance}")
            else:
                print("❌ Invalid account number or PIN.")
            pause()

        # ---------------- TRANSFER ----------------
        elif choice == "5":
            acc_num = get_int("Enter your account number: ")
            pin = get_int("Enter PIN: ")
            account = bank.authenticate(acc_num, pin)
            if account:
                to_acc = get_int("Enter destination account number: ")
                amount = get_positive_amount("Enter amount to transfer: ")
                try:
                    bank.transfer(account, to_acc, amount)
                    print(f"✅ Transferred ₹{amount} to account {to_acc}.")
                except ValueError as e:
                    print(f"❌ {e}")
            else:
                print("❌ Invalid account number or PIN.")
            pause()

        # ---------------- MINI STATEMENT ----------------
        elif choice == "6":
            acc_num = get_int("Enter account number: ")
            pin = get_int("Enter PIN: ")
            account = bank.authenticate(acc_num, pin)
            if account:
                print(f"\n--- Last 5 Transactions for {account.name} ---")
                if account.transactions:
                    for t in account.transactions[-5:]:
                        print(t)
                else:
                    print("No transactions yet.")
            else:
                print("❌ Invalid account number or PIN.")
            pause()

        # ---------------- DELETE ACCOUNT ----------------
        elif choice == "7":
            acc_num = get_int("Enter account number: ")
            pin = get_int("Enter PIN: ")
            account = bank.authenticate(acc_num, pin)
            if account:
                confirm = input("Are you sure? This cannot be undone (y/n): ").lower()
                if confirm == "y":
                    bank.delete_account(acc_num)
                    print("✅ Account deleted successfully.")
                else:
                    print("Cancelled.")
            else:
                print("❌ Invalid account number or PIN.")
            pause()

        # ---------------- EXIT ----------------
        elif choice == "8":
            print("\n👋 Thank you for using Bank Management System. Goodbye!")
            break

        else:
            print("⚠️  Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    main()
