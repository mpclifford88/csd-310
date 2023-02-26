'''
    Title: what_a_book_.py
    Author: Matthew Clifford
    Date: 02/26/2023
'''

# cspell: disable
# pylint: disable=consider-using-f-string;
# pylint: disable=c0103

import sys
import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "whatabook_user",
    "password": "fR%oA!dB5*nLwW",
    "host": "194.156.136.38",
    "db": "whatabook",
    "raise_on_warnings": True
}

def show_menu():
    '''This is to show the main menu'''
    print("\n  -- Main Menu --")

    print("    1. View Books\n    2. View Store Locations\n    3. My Account\n    4. Exit Program")

    try:
        choice = int(input('      <Example enter: 1 for book listing>: '))

        return choice
    except ValueError:
        print("\n  Invalid number, program terminated...\n")

        sys.exit(0)

def show_books(_cursor):
    '''This is the inner join'''
    _cursor.execute("SELECT book_id, book_name, author, details from book")
    books = _cursor.fetchall()

    print("\n  -- DISPLAYING BOOK LISTING --")
    for book in books:
        print("  Book Name: {}\n  Author: {}\n  Details: {}\n".format(book[0], book[1], book[2]))

def show_locations(_cursor):
    '''Inner join'''
    _cursor.execute("SELECT store_id,S locale from store")

    locations = _cursor.fetchall()

    print("\n  -- DISPLAYING STORE LOCATIONS --")

    for location in locations:
        print("  Locale: {}\n".format(location[1]))

def validate_user():
    '''validate the ID of users'''
    try:
        user_id = int(input('\n      Enter a customer id <Example 1 for user_id 1>: '))

        if user_id < 0 or user_id > 3:
            print("\n  Invalid customer number, program terminated...\n")
            sys.exit(0)

        return user_id
    except ValueError:
        print("\n  Invalid number, program terminated...\n")

        sys.exit(0)

def show_account_menu():
    '''This is the account menu of the user'''
    try:
        print("\n      -- Customer Menu --")
        print("        1. Wishlist\n        2. Add Book\n        3. Main Menu")
        account_option1 = int(input('        <Example enter: 1 for wishlist>: '))

        return account_option1
    except ValueError:
        print("\n  Invalid number, program terminated...\n")

        sys.exit(0)

def show_wishlist(_cursor, _user_id):
    '''This is where we query the DB for a list of books added to the user's wishlist'''
    _cursor.execute("SELECT user.user_id, user.first_name, user.last_name" +
                    "book.book_id, book.book_name, book.author " +
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(_user_id))  
    wishlist = _cursor.fetchall()

    print("\n        -- DISPLAYING WISHLIST ITEMS --")

    for book in wishlist:
        print("        Book Name: {}\n        Author: {}\n".format(book[4], book[5]))

def show_books_to_add(_cursor, _user_id):
    """ query the database for a list of books not in the users wishlist """

    query = ("SELECT book_id, book_name, author, details "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})"
            .format(_user_id))

    print(query)

    _cursor.execute(query)

    books_to_add = _cursor.fetchall()

    print("\n        -- DISPLAYING AVAILABLE BOOKS --")

    for book in books_to_add:
        print("        Book Id: {}\n        Book Name: {}\n".format(book[0], book[1]))

def add_book_to_wishlist(_cursor, _user_id, _book_id):
    '''defining the command to add a book to the wishlist'''
    _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})"
                    .format(_user_id, _book_id))

try:

    db = mysql.connector.connect(config) # connect to the WhatABook database

    cursor = db.cursor() # cursor for MySQL queries

    print("\n  Welcome to the WhatABook Application! ")

    user_selection = show_menu() # show the main menu

    while user_selection != 4:

        if user_selection == 1:
            show_books(cursor)

        if user_selection == 2:
            show_locations(cursor)

        if user_selection == 3:
            my_user_id = validate_user()
            account_option = show_account_menu()

            while account_option != 3:

                if account_option == 1:
                    show_wishlist(cursor, my_user_id)

                if account_option == 2:

                    show_books_to_add(cursor, my_user_id)

                    book_id = int(input("\n        Enter the id of the book you want to add: "))
                    add_book_to_wishlist(cursor, my_user_id, book_id)

                    db.commit()

                    print("\n        Book id: {} was added to your wishlist!".format(book_id))

                if account_option < 0 or account_option > 3:
                    print("\n      Invalid option, please retry...")

                account_option = show_account_menu()
        if user_selection < 0 or user_selection > 4:
            print("\n      Invalid option, please retry...")
            user_selection = show_menu()

    print("\n\n  Program terminated...")

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:

    db.close()
