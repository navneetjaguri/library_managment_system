from features import Library

class ManagementSystem:
    
    def main():
        library = Library()
    
        while True:
            print("\nLibrary Management System\n")
            print("1. Add Book")
            print("2. Show All Books")
            print("3. Search Book")
            print("4. Issue Book")
            print("5. Return Book")
            print("6. Remove Book")
            print("7. Issue History")
            print("8. Book Count")
            print("9. Exit")
            
            choice = input("\nEnter your choice (1-9): ")
            
            if choice == '1':
                library.add_book()
            elif choice == '2':
                library.show_all_books()
            elif choice == '3':
                library.search_book()
            elif choice == '4':
                library.issue_book()
            elif choice == '5':
                library.return_book()
            elif choice == '6':
                library.remove_book()
            elif choice == '7':
                library.show_history()
            elif choice == '8':
                library.show_count()
            elif choice == '9':
                print("Exiting system.")
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 9.")

    if __name__ == "__main__":
        main()
