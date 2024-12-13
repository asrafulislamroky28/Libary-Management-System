import json
from datetime import datetime, timedelta

LEND_FILE = "lend_data.json"

def lend_book(all_books):
    try:
        try:
            with open(LEND_FILE, "r") as file:
                lend_data = json.load(file)
        except FileNotFoundError:
            lend_data = []

        borrower_name = input("Enter borrower's name: ")
        borrower_phone = input("Enter borrower's phone number: ")
        book_title = input("Enter the title of the book to lend: ")

        for book in all_books:
            if book["title"].lower() == book_title.lower():
                if book["quantity"] > 0:
                    book["quantity"] -= 1
                    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

                    lend_entry = {
                        "borrower_name": borrower_name,
                        "borrower_phone": borrower_phone,
                        "book_title": book_title,
                        "lend_date": datetime.now().strftime("%Y-%m-%d"),
                        "due_date": due_date
                    }
                    lend_data.append(lend_entry)

                    with open(LEND_FILE, "w") as file:
                        json.dump(lend_data, file, indent=4)

                    with open("all_books.json", "w") as file:
                        json.dump(all_books, file, indent=4)

                    print(f"Book '{book_title}' lent to {borrower_name}, due by {due_date}.")
                    return
                else:
                    print("Not enough books available to lend.")
                    return
        print("Book not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def return_book(all_books):
    try:
        with open(LEND_FILE, "r") as file:
            lend_data = json.load(file)

        book_title = input("Enter the title of the book to return: ")
        borrower_name = input("Enter the borrower's name: ")

        for lend_entry in lend_data:
            if lend_entry["book_title"].lower() == book_title.lower() and lend_entry["borrower_name"].lower() == borrower_name.lower():
                lend_data.remove(lend_entry)

                for book in all_books:
                    if book["title"].lower() == book_title.lower():
                        book["quantity"] += 1
                        break

                with open(LEND_FILE, "w") as file:
                    json.dump(lend_data, file, indent=4)

                with open("all_books.json", "w") as file:
                    json.dump(all_books, file, indent=4)

                print(f"Book '{book_title}' returned by {borrower_name}.")
                return
        print("No matching lend record found.")
    except FileNotFoundError:
        print("No lending records found.")
    except Exception as e:
        print(f"An error occurred: {e}")
