from json.tool import main
import os
import json
from colorama import init 



init(autoreset=True)

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"


FILENAME = "transactions.json"

def load_transactions():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    return []

def save_transactions(transactions):
    with open(FILENAME, "w") as file:
        json.dump(transactions, file, indent=4)


def add_transaction(transactions):
    trans_type = input("Enter (Income/Expense): ").strip().lower()
    if trans_type not in ("income", "expense"):
        print(f"{RED}Invalid type! Must be 'income' or 'expense'.{RESET}")
        return

    try:
        amount = float(input("Amount: "))
    except ValueError:
        print(f"{RED}Invalid amount! Please enter a number.{RESET}")
        return

    category = input("Category: ").strip()
    description = input("Description: ").strip()

    transactions.append({
        "type": trans_type,
        "amount": amount,
        "category": category,
        "description": description
    })
    save_transactions(transactions) 
    print(f"{GREEN}Transaction added!{RESET}")


def view_transactions(transactions):
    if not transactions:
        print(f"{BLUE}No transactions found.{RESET}")
        return
    for i, t in enumerate(transactions, 1):
        print(f"{YELLOW}\n{i}. {t['type'].title()} - ${t['amount']} - {t['category']} - {t['description']}{RESET}")


def show_balance(transactions):
    income = sum(t["amount"] for t in transactions if t["type"] == "income")
    expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = income - expense
    print("\n -----------------------")
    print(f"{YELLOW}Total Income: ${income:.2f}{RESET}")
    print(f"{YELLOW}Total Expenses: ${expense:.2f}{RESET}")
    print(f"{YELLOW}Balance: ${balance:.2f}{RESET}")


def delete_transaction(transactions):
    if not transactions:
        print(f"{RED}No transactions available to delete.{RESET}")
        return

    view_transactions(transactions)
    try:
        index = int(input(f"{GREEN}Enter the number of the transaction to delete: {RESET}")) - 1
        if 0 <= index < len(transactions):
            deleted = transactions.pop(index)
            save_transactions(transactions)
            print(f"{GREEN}Deleted: {deleted['type'].title()} - ${deleted['amount']} - {deleted['category']}{RESET}")
        else:
            print(f"{RED}Invalid transaction number.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input! Please enter a number.{RESET}")


def edit_transaction(transactions):
    if not transactions:
        print(f"{RED}No transactions available to edit.{RESET}")
        return

    view_transactions(transactions)

    try:
        index = int(input(f"{GREEN}Enter the number of the transaction to edit: {RESET}")) - 1
        if 0 <= index < len(transactions):
            original = transactions[index]

            print(f"{YELLOW}Leave a field blank to keep the current value.{RESET}")

            new_type = input(f"Type (income/expense) [{original['type']}]: ").strip().lower()
            if new_type and new_type not in ("income", "expense"):
                   print(f"{RED}Invalid type! Must be 'income' or 'expense'.{RESET}")
            elif not new_type:
                new_type = original['type']
                
            new_amount = input(f"Amount [{original['amount']}]: ").strip()
            new_category = input(f"Category [{original['category']}]: ").strip()
            new_description = input(f"Description [{original['description']}]: ").strip()

            if new_type in ("income", "expense"):
                original["type"] = new_type
                
            if new_amount:
                try:
                    original["amount"] = float(new_amount)
                except ValueError:
                    print(f"{RED}Invalid amount. Keeping previous value.{RESET}")
            if new_category:
                original["category"] = new_category
            if new_description:
                original["description"] = new_description

            save_transactions(transactions)
            print(f"{GREEN}Transaction updated successfully!{RESET}")
        else:
            print(f"{RED}Invalid transaction number.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input! Please enter a number.{RESET}")


'''def filter_by_type(transactions):
    trans_type = input("Enter transaction type to filter (income/expense):").strip().lower()

    if trans_type not in ("income","expense"):

     print(f"{RED}Invalid type! Must be 'income' or 'expense'.{RESET}")
    
     retry = input(f"{YELLOW}Would you like to try again? (y/n): {RESET}").strip().lower()
     if retry =='y':
        trans_type = input("Enter transaction type to filter (income/expense):").strip().lower()
        

    filtered = [t for t in transactions if t["type"] == trans_type]
    
    if not filtered:
        print(f"{YELLOW}No {trans_type} transactions found.{RESET}")
        return
    print(f"\n{BLUE}--- {trans_type.title()} Transactions ---{RESET}")
    for i, t in enumerate(filtered, 1):
        print(f"{YELLOW}{i}. ${t['amount']} - {t['category']} - {t['description']}{RESET}")'''
        
def filter_by_type(transactions):
    def is_valid_type(value):
        return value in ("income", "expense")

    trans_type = retry_input(
        "Enter transaction type to filter (income/expense): ",
        validator=is_valid_type,
        error_msg="Must be 'income' or 'expense'."
    )

    if not trans_type:
        return  

    filtered = [t for t in transactions if t["type"] == trans_type]
    if not filtered:
        print(f"{YELLOW}No {trans_type} transactions found.{RESET}")
        return

    print(f"\n{BLUE}--- {trans_type.title()} Transactions ---{RESET}")
    for i, t in enumerate(filtered, 1):
        print(f"{YELLOW}{i}. ${t['amount']} - {t['category']} - {t['description']}{RESET}")
        
        
def retry_input(prompt, validator=None, max_retries=3, error_msg="Invalid input!"):
    for attempt in range(max_retries):
        value = input(prompt).strip()
        if not validator or validator(value):
            return value
        print(f"{RED}{error_msg} Attempt {attempt + 1} of {max_retries}.{RESET}")
    print(f"{RED}Maximum retries reached.{RESET}")
    return None
        

def main():
    transactions = load_transactions()

    while True:
        print("\n--- Budget Tracker ---")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Show Balance")
        print("4. Delete")
        print("5. Edit")
        print("6. Filter")
        choice = input("\n Choose an option: ")

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            show_balance(transactions)
        elif choice == "4":
            delete_transaction(transactions)
        elif choice =="5":
            edit_transaction(transactions)
        elif choice =="6":
            filter_by_type(transactions)    

        else:
            print(f"{RED}Invalid choice! Please try again.{RESET}")

if __name__ == "__main__":
    main()
