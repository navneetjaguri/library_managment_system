import json
import os
import uuid 
from datetime import datetime, timedelta

class Book:
    def __init__(self, book_id, title, author, name, status="Available", due_date=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.name = name
        self.status = status
        self.due_date = due_date

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "name": self.name,
            "status": self.status,
            "due_date": self.due_date
        }

    @staticmethod
    def from_dict(data):
        return Book(
            data["book_id"],
            data["title"],
            data["author"],
            data["name"],
            data.get("status", "Available"),
            data.get("due_date")
        )

class Library:
    def __init__(self, filename="library_data.json"):
        self.filename = filename
        self.books = []
        self.history = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(b) for b in data.get("books", [])]
                    self.history = data.get("history", [])
            except (json.JSONDecodeError, KeyError):
                self.books = []
                self.history = []
        else:
            self.books = []
            self.history = []

    def save_data(self):
        data = {
            "books": [b.to_dict() for b in self.books],
            "history": self.history
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def add_book(self):
        print("\n--- Add New Book ---")
        book_id = str(uuid.uuid4().int)[:4]

        title = input("Enter Title: ")
        author = input("Enter Author: ")
        name = input("Enter Book Name: ")
        
        new_book = Book(book_id, title, author, name)
        self.books.append(new_book)
        self.save_data()
        print("Book added successfully!")

    def show_all_books(self):
        print("\n--- All Books ---")
        if not self.books:
            print("Not Available .")
            return

        header = f"{'ID':<10} {'Title':<20} {'Author':<20} {'Name':<20} {'Status':<15} {'Due Date':<15}"
        print(header)
        print("-" * len(header))
        for b in self.books:
            due = b.due_date if b.due_date else "N/A"
            print(f"{b.book_id:<10} {b.title:<20} {b.author:<20} {b.name:<20} {b.status:<15} {due:<15}")

    def search_book(self):
        print("\n--- Search Book ---")
        query = input("Enter Book Name or ID to search: ").lower()
        results = [b for b in self.books if query in b.name.lower() or query == b.book_id.lower()]
        
        if not results:
            print("No books found matching your search.")
        else:
            for b in results:
                print(f"ID: {b.book_id} | Title: {b.title} | Author: {b.author} | Name: {b.name} | Status: {b.status}")

    def issue_book(self):
        print("\n--- Issue Book ---")
        book_id = input("Enter Book ID to issue: ")
        book = next((b for b in self.books if b.book_id == book_id), None)

        if not book:
            print("Error: Not Found.")
        elif book.status == "Issued":
            print(f"Error: this book because it is Already Issued. Due date: {book.due_date}")
        else:
            user_name = input("Enter Issuer Name: ")
            days = int(input("Enter number of days for issue (default 14): ") or 14)
            
            due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            book.status = "Issued"
            book.due_date = due_date
            
            log = {
                "book_id": book_id,
                "book_name": book.name,
                "issuer": user_name,
                "issue_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "due_date": due_date,
                "type": "Issue"
            }
            self.history.append(log)
            self.save_data()
            print(f"Book issued to {user_name} successfully! Due date: {due_date}")

    def return_book(self):
        print("\n--- Return Book ---")
        book_id = input("Enter Book ID to return: ")
        book = next((b for b in self.books if b.book_id == book_id), None)

        if not book:
            print("Error: Not Found.")
        elif book.status == "Available":
            print("Error: Already Available.")
        else:
            book.status = "Available"
            book.due_date = None
            
            log = {
                "book_id": book_id,
                "book_name": book.name,
                "return_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "Return"
            }
            self.history.append(log)
            self.save_data()
            print("Book returned successfully!")

    def remove_book(self):
        print("\n--- Remove Book ---")
        book_id = input("Enter Book ID to remove: ")
        book = next((b for b in self.books if b.book_id == book_id), None)

        if not book:
            print("Error: Not Found.")
        elif book.status == "Issued":
            print(f"Error: can`t remove this book because it is Already Issued. Due date: {book.due_date}")
        else:
            self.books.remove(book)
            self.save_data()
            print("Book removed from records.")

    def show_history(self):
        print("\n--- Issue History ---")
        if not self.history:
            print("No history logs found.")
            return

        for log in self.history:
            if log["type"] == "Issue":
                print(f"[{log['issue_date']}] ISSUE: '{log['book_name']}' (ID: {log['book_id']}) issued to {log['issuer']}. Due: {log['due_date']}")
            else:
                print(f"[{log['return_date']}] RETURN: '{log['book_name']}' (ID: {log['book_id']}) returned.")

    def show_count(self):
        total = len(self.books)
        available = sum(1 for b in self.books if b.status == "Available")
        issued = total - available
        print("\n--- Book Count ---")
        print(f"Total Books:     {total}")
        print(f"Available Books: {available}")
        print(f"Issued Books:    {issued}")
