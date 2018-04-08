#!/user/python3
import sqlite3
import os
import subprocess
import time


# Create a books table
def make_database_tables():
    print("Database created!")
    c.execute("""CREATE TABLE books (
                name TEXT,
                category TEXT,
                publishDate TEXT,
                available CHAR(3),
                delivered TEXT,
                writer TEXT,
                price INT);""")
    print("Table created")
    # 3 sec for see what happened
    time.sleep(3)


# Make insert to book table
def insert_book(name_, category, publish_date, available, delivered, writer, price):
    with conn:
        c.execute("INSERT INTO books VALUES(:name, :category, "
                  ":publishDate, :available, :delivered, :writer, :price)",
                  {'name': name_, 'category': category,
                   'publishDate': publish_date, 'available': available,
                   'delivered': delivered, 'writer': writer, 'price': price})


# Return name of books
def get_book_by_name(name):
    c.execute("SELECT * FROM books WHERE name=:name", {'name': name})
    return c.fetchall()


# Return entire book table
def show_table():
    c.execute("SELECT rowid,* FROM books;")
    return c.fetchall()


# Update book availability by name (is book in book shelf or not)
def update_available_with_name(name_, available):
    with conn:
        c.execute("""UPDATE books SET available=:available
                    WHERE name = :name""",
                  {'name': name_, 'available': available})


# Update book availability by id (is book in book shelf or not)
def update_available_with_id(id_, available):
    with conn:
        c.execute("""UPDATE books SET available=:available
                    WHERE rowid = :id""",
                  {'id': id_, 'available': available})


# Update the name of person that book delivered to
def update_deliver(name_, delivered):
    with conn:
        c.execute("""UPDATE books SET delivered=:delivered
                    WHERE name = :name""",
                  {'name': name_, 'delivered': delivered})


# Change book's name
def update_name(id_, name_):
    with conn:
        c.execute("""UPDATE books SET name=:name
                    WHERE rowid = :id""",
                  {'id': id_, 'name': name_})


# Vacuum the database
def reset_db():
    with conn:
        c.execute("VACUUM")


# Remove book from database
def remove_book(name_, writer):
    with conn:
        c.execute("DELETE FROM books WHERE name = :name AND writer = :writer",
                  {'name': name_, 'writer': writer})

    reset_db()


# Search methods(id, name, category, ...)
def search(method):
    def db_search(input_):
        if method == '1':
            c.execute("SELECT rowid,* FROM books WHERE rowid = :id", {'id': input_})
            return c.fetchall()
        elif method == '2':
            c.execute("SELECT rowid,* FROM books WHERE name = :name", {'name': input_})
            return c.fetchall()
        elif method == '3':
            c.execute("SELECT rowid,* FROM books WHERE category = :category", {'category': input_})
            return c.fetchall()
        elif method == '4':
            c.execute("SELECT rowid,* FROM books WHERE publishDate = :publishDate", {'publishDate': input_})
            return c.fetchall()
        elif method == '5':
            c.execute("SELECT rowid,* FROM books WHERE writer = :writer", {'writer': input_})
            return c.fetchall()
        elif method == '6':
            c.execute("SELECT rowid,* FROM books WHERE price = :price", {'price': input_})
            return c.fetchall()
        elif method == '7':
            c.execute("SELECT rowid,* FROM books WHERE available = :available", {'available': input_})
            return c.fetchall()
        elif method == '8':
            c.execute("SELECT rowid,* FROM books WHERE delivered = :delivered", {'delivered': input_})
            return c.fetchall()
    return db_search


# Design a table for showing data
def table(table_):
    print("_____________________________________________________________________"
          "____________________________________________________________________________")
    print("| ID", " " * 1, "|", "Name", " " * 36, "|", "Category", " " * 4, "|",
          "Publish date", "|", "Writer", " " * 14, "|", "Price", " " * 3, "|",
          "Available", "|",  "Delivered to|")
    print("|____" + "_" * 1, "|", "_____" + "_" * 36, "|", "_________" + "_" * 4,
          "|", "___________" + "_" * 1, "|", "_______" + "_" * 14, "|", "______" + "_" * 3,
          "|", "__________|", "____________|")

    for item in table_:
        print("|", str(item[0]), " " * (3 - len(str(item[0]))), "|",
              item[1], " " * (40 - len(item[1])), "|",
              item[2], " " * (12 - len(item[2])), "|",
              item[3], " " * (11 - len(item[3])), "|",
              item[6], " " * (20 - len(item[6])), "|",
              str("{:,}".format(item[7])), " " * (7 - len(str(item[7]))), "|",
              item[4], " " * (8 - len(item[4])), "|",
              item[5], " " * (10 - len(item[5])), "|")
        print("-" * 145)


# Exit
def exit_():
    os.system("exit")


# Clear screen
def clear():
    os.system("clear")


# Sum of all book's prices
def price_counter(table_):
    tot_price = 0
    for item in table_:
        tot_price = int(item[7]) + tot_price
    return tot_price


def main():
    clear()
    try:
        # Choose an option
        option = input("""USAGE:
                            1. Show Database
                            2. Insert new book
                            3. Edit book availability
                            4. Edit book deliverer
                            5. Edit book's name
                            6. Removing book
                            7. Search
                            8. Total price
                            9. Exit enter 8 or [Ctl + C]
                            
        
                            [$] Please insert option's number: """)
        # Every number is for one of the above options for example:
        # '2' is insert new book
        if '2' in option:
            clear()
            print("========(INSERT NEW BOOK)========")
            print("[!] You can use (ctl + c) to going back to menu." )
            try:
                while True:
                    clear()
                    # Show the table
                    table_ = show_table()
                    table(table_)

                    name_ = input("Name: ")
                    category = input("Category: ")
                    publish_date = input("Publish date: ")
                    writer = input("Writer: ")
                    price = int(input("Price: "))
                    available = input("Book is available (Y/N): ").upper()

                    # Book is available or not
                    if available == 'N':
                        delivered = input("Delivered to: ")
                        insert_book(name_, category, publish_date, available,
                                    delivered, writer, price)

                    elif available == 'Y':
                        delivered = "None"
                        insert_book(name_, category, publish_date, available,
                                    delivered, writer, price)
                    table_ = show_table()
                    table(table_)
                    print("[!] Don't want enter more book in DB ?, Then press (Ctl+C)"
                          " to going back to the menu.")
            # If keyboard interrupt then back to menu
            except KeyboardInterrupt:
                clear()
                main()
            except Exception as e:
                print("[-] There is an Error: {}".format(e))

        elif '1' in option:
            clear()
            print("========(SHOW TABLE)========")
            try:
                table_ = show_table()
                table(table_)
                cmd = input("[!] Use (Ctl + C) to going back to menu.")
                conn.close()
                if cmd:
                    main()
            except KeyboardInterrupt:
                clear()
                main()
            except Exception as e:
                print("[-] There is an Error: {}".format(e))

        elif '3' in option:
            clear()
            print("========(EDIT AVAILABILITY)========")
            print("[!] You can use (ctl + c) to going back to menu.")
            try:
                while True:
                    clear()
                    print("[!] You can use (ctl + c) to going back to menu.")
                    table_ = show_table()
                    table(table_)
                    q = input("Find and edit with ID or NAME?")

                    # Edit by id or name
                    if 'id' or 'ID' in q:
                        id_ = input("Please insert book id that you want to edit: ")
                        available = input("Book is available (Y/N): ")
                        update_available_with_id(id_, available.upper())

                    elif 'name' or 'NAME' in q:
                        name_ = input("Please insert book's name that you want to edit: ")
                        available = input("Book is available (Y/N): ")
                        update_available_with_name(name_, available.upper())
            except KeyboardInterrupt:
                clear()
                main()
            except Exception as e:
                print("[-] There is an Error: {}".format(e))

        elif '4' in option:
            clear()
            print("========(EDIT DELIVERY)========")
            print("[!] You can use (ctl + c) to going back to menu.")
            try:
                while True:
                    table_ = show_table()
                    table(table_)
                    name_ = input("Name of book that you delivered to: ")
                    delivered_ = input("Name of person: ")
                    # Update delivered to
                    update_deliver(name_, delivered_)
            except KeyboardInterrupt:
                clear()
                main()
            except Exception as e:
                print("[-] There is an Error: {}".format(e))

        elif '5' in option:
            clear()
            print("========(EDIT BOOK'S NAME)========")
            print("[!] You can use (ctl + c) to going back to menu.")
            try:
                while True:
                    clear()
                    print("[!] You can use (ctl + c) to going back to menu.")
                    table_ = show_table()
                    table(table_)
                    id_ = int(input("Input book's ID: "))
                    name_ = input("Input books name: ")
                    # Update book's name
                    update_name(id_, name_)
            except KeyboardInterrupt:
                clear()
                main()
            except Exception as e:
                print("[-] There is an Error: {}".format(e))

        elif '6' in option:
            clear()
            print("========(REMOVING BOOK)========")
            print("[!] You can use (ctl + c) to going back to menu.")
            try:
                while True:
                    table_ = show_table()
                    table(table_)
                    name_ = input("Input Book's name: ")
                    writer = input("Input writer's name: ")
                    # Removing book with name of the book and the writer
                    remove_book(name_, writer)
                    clear()
            except KeyboardInterrupt:
                clear()
                main()
            except Exception as e:
                print("[-] There is an Error: {}".format(e))

        elif '7' in option:
            clear()
            print("========(SEARCH)========")
            print("[!] You can use (ctl + c) to going back to menu.")
            try:
                input_method = input("""You can search by this methods:
                1. ID
                2. Name
                3. Category
                4. Publish date
                5. Writer
                6. Price
                7. Available
                8. Delivered to

                Please insert by number: """)

                clear()
                print("==================(SEARCH)==================")

                # Search based on one of above options
                if input_method == '1':
                    ans_by = input("Please insert ID number: ")
                    method_return = search(input_method)
                    s = method_return(ans_by)

                elif input_method == '2':
                    ans_by = input("Please insert Name of the book:")
                    method_return = search(input_method)
                    s = method_return(ans_by)

                elif input_method == '3':
                    ans_by = input("Please insert category:")
                    method_return = search(input_method)
                    s = method_return(ans_by)

                elif input_method == '4':
                    ans_by = input("Please insert publish date:")
                    method_return = search(input_method)
                    s = method_return(ans_by)

                elif input_method == '5':
                    ans_by = input("Please insert writer:")
                    method_return = search(input_method)
                    s = method_return(ans_by)

                elif input_method == '6':
                    ans_by = input("Please insert price:")
                    method_return = search(input_method)
                    s = method_return(ans_by)

                elif input_method == '7':
                    ans_by = input("Please insert availability:")
                    method_return = search(input_method)
                    s = method_return(ans_by)

                elif input_method == '8':
                    ans_by = input("Please insert Name of person that delivered:")
                    method_return = search(input_method)
                    s = method_return(ans_by)

                data_list = []
                clear()
                print("==================(SEARCH)==================")
                # Print the result
                for tuple_ in s:
                    for item in tuple_:
                        data_list.append(item)
                    print("""
                    [+]ID: {}
                    [+]Name of the book: {}
                    [+]Category: {}
                    [+]Publish date: {}
                    [+]Writer: {}
                    [+]Price: {}
                    [+]Available: {}
                    [+]Delivered to: {}
                    """.format(data_list[0], data_list[1], data_list[2], data_list[3], data_list[6],
                               data_list[7], data_list[4], data_list[5]))
                    data_list = []
                cmd = input("[!] Use (Ctl + C) to going back to menu.")
                if cmd:
                    main()
            except KeyboardInterrupt:
                clear()
                main()
            except:
                print('[-] Found nothing, check what you insert!')

        elif '8' in option:
            clear()
            print("========(TOTAL PRICE)========")
            try:
                table_ = show_table()
                # Total price of all book's that recorded
                total = price_counter(table_)
                sep_total = "{:,}".format(total)
                print("Total price of all books: {} $".format(sep_total))
                cmd = input("[!] Use (Ctl + C) to going back to menu.")
                if cmd:
                    main()
            except KeyboardInterrupt:
                clear()
                main()
            except Exception as e:
                print("[-] There is an Error: {}".format(e))

        elif '9' in option:
            clear()
            exit_()
    except KeyboardInterrupt:
        os.system("clear")
        exit_()


if __name__ == '__main__':
    # Make an ls on terminal
    ls = str(subprocess.check_output(['ls']))
    find = ls.find("book.db")
    # If find book.db then just connect otherwise
    # after making DB create books table
    if find == -1:
        conn = sqlite3.connect('book.db')
        c = conn.cursor()
        make_database_tables()
    else:
        conn = sqlite3.connect('book.db')
        c = conn.cursor()

    main()
    conn.close()