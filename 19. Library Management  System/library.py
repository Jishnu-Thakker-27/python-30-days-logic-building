books = []

def add_book():
    name = input("Enter book name: ")
    author = input("Enter author name: ")
    
    book = {
        "name": name,
        "author": author,
        "issued": False
    }
    
    books.append(book)
    print("Book added successfully!")

def view_books():
    if not books:
        print("No books available.")
        return
    
    for i, book in enumerate(books):
        status = "Available" if not book["issued"] else "Issued"
        print(f"{i}. {book['name']} by {book['author']} - {status}")

def issue_book():
    view_books()
    
    try:
        index = int(input("Enter book index to issue: "))
        
        if books[index]["issued"]:
            print("Book already issued!")
        else:
            books[index]["issued"] = True
            print("Book issued successfully!")
    
    except:
        print("Invalid input!")

def return_book():
    view_books()
    
    try:
        index = int(input("Enter book index to return: "))
        
        if not books[index]["issued"]:
            print("Book was not issued!")
        else:
            books[index]["issued"] = False
            print("Book returned successfully!")
    
    except:
        print("Invalid input!")

while True:
    print("Library Management System")
    print("1. Add Book")
    print("2. View Books")
    print("3. Issue Book")
    print("4. Return Book")
    print("5. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_book()
    elif choice == "2":
        view_books()
    elif choice == "3":
        issue_book()
    elif choice == "4":
        return_book()
    elif choice == "5":
        print("Exiting... ")
        break
    else:
        print("Invalid choice!")
