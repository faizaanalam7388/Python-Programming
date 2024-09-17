import mysql.connector as a
import matplotlib.pyplot as plt
import pandas as pd

con = a.connect(host="localhost", user="root", passwd="root", database="library")

def addbook():
    bn = input("Enter BOOK Name: ")
    c = input("Enter BOOK Code: ")
    t = input("Total Books: ")
    s = input("Enter Subject: ")
    data = (bn, c, t, s)
    sql = 'INSERT INTO books VALUES (%s, %s, %s, %s)'
    c = con.cursor()
    c.execute(sql, data)
    con.commit()
    print(">_____________________________________________________<")
    print("Data Entered Successfully")
    main()

def issueb():
    n = input("Enter name:")
    r = input("Enter Reg No : ")
    co = input("Enter Book Code: ")
    d = input("Enter Date: ")
    a = "INSERT INTO issue VALUES (%s, %s, %s, %s)"
    data = (n, r, co, d)
    c = con.cursor()
    c.execute(a, data)
    con.commit()
    print(">_____________________________________________________<")
    print("Book issued to:", n)
    bookup(co, -1)

def submitb():
    n = input("Enter Name: ")
    r = input("Enter Reg No: ")
    co = input("Enter Book Code: ")
    d = input("Enter Date :")
    a = "INSERT INTO submit VALUES (%s, %s, %s, %s)"
    data = (n, r, co, d)
    c = con.cursor()
    c.execute(a, data)
    con.commit()
    print(">_____________________________________________________<")
    print("Book Submitted from:", n)
    bookup(co, 1)

def bookup(co, u):
    a = "SELECT TOTAL FROM books WHERE BCODE = %s"
    data = (co,)
    c = con.cursor()
    c.execute(a, data)
    myresult = c.fetchone()
    t = myresult[0] + u
    sql = "UPDATE books SET TOTAL = %s WHERE BCODE = %s"
    d = (t, co)
    c.execute(sql, d)
    con.commit()
    main()

def dbook():
    ac = input("Enter Book Code:")
    a = "DELETE FROM books WHERE BCODE = %s"
    data = (ac,)
    c = con.cursor()
    c.execute(a, data)
    con.commit()
    print(">_____________________________________________________<")
    print("Book with code", ac, "deleted successfully")
    main()

def dispbook():
    a = "SELECT * FROM books"
    c = con.cursor()
    c.execute(a)
    myresult = c.fetchall()
    for i in myresult:
        print('Book Name:', i[0])
        print('Book Code:', i[1])
        print('Total:', i[2])
        print('Subject:', i[3])
        print('>_________________________________________________<')
    main()

def check_availability():
    co = input("Enter Book Code: ")
    query = "SELECT TOTAL FROM books WHERE BCODE = %s"
    data = (co,)
    c = con.cursor()
    c.execute(query, data)
    result = c.fetchone()

    if result:
        if result[0] > 0:
            print("Book is available.")
        else:
            print("Book is not available.")
    else:
        print("Invalid Book Code.")

    main()

def plot_subjects():
    a = "SELECT SUBJECT, SUM(TOTAL) FROM books GROUP BY SUBJECT"
    c = con.cursor()
    c.execute(a)
    myresult = c.fetchall()

    subjects = [row[0] for row in myresult]
    total_books = [row[1] for row in myresult]

    plt.bar(subjects, total_books)
    plt.xlabel("Subjects")
    plt.ylabel("Total Books")
    plt.title("Total Books by Subject")
    plt.xticks(rotation=45)
    plt.show()
    main()

def view_issued_books():
    n = input("Enter Reg No: ")
    a = "SELECT * FROM issue WHERE RegNo = %s"
    data = (n,)
    c = con.cursor()
    c.execute(a, data)
    myresult = c.fetchall()
    if not myresult:
        print("No issued books found for Reg No:", n)
    else:
        print("Issued books for Reg No:", n)
        for i in myresult:
            print('Book Name:', i[0])
            print('Book Code:', i[1])
            print('Issue Date:', i[3])
            print('>_________________________________________________<')
    main()

def view_submitted_books():
    n = input("Enter Reg No: ")
    a = "SELECT * FROM submit WHERE RegNo = %s"
    data = (n,)
    c = con.cursor()
    c.execute(a, data)
    myresult = c.fetchall()
    if not myresult:
        print("No submitted books found for Reg No:", n)
    else:
        print("Submitted books for Reg No:", n)
        for i in myresult:
            print('Book Name:', i[0])
            print('Book Code:', i[1])
            print('Submit Date:', i[3])
            print('>_________________________________________________<')
    main()

def backup_books_to_csv():
    a = "SELECT * FROM books"
    c = con.cursor()
    c.execute(a)
    myresult = c.fetchall()

    df = pd.DataFrame(myresult, columns=['Book Name', 'Book Code', 'Total', 'Subject'])
    df.to_csv('library_books.csv', index=False)
    print("Books data backed up to 'library_books.csv'")
    main()

def main():

    print('''
_________________________________________________________________________________________________________________________________________________________

                                                        LIBRARY MANAGER
    1.ADD BOOKS
    2.ISSUE BOOKS
    3.SUBMIT BOOKS
    4.DELETE BOOKS
    5.DISPLAY BOOKS
    6.CHECK AVAILABILITY
    7.PLOT SUBJECTS
    8.MANAGER LOGIN
    9.CUSTOMER LOGIN
    10.BACKUP BOOKS TO CSV
_________________________________________________________________________________________________________________________________________________________
    ''')
    choice = input('Enter Task Number:')
    print('>______________________________________________________<')
    if choice == '1':
        addbook()
    elif(choice=='2'):
        issueb()
    elif(choice=='3'):
        submitb()
    elif(choice=='4'):
        dbook()
    elif(choice=='5'):
        dispbook()
    elif(choice=='6'):
        check_availability()
    elif(choice=='7'):
        plot_subjects()
    elif(choice=='8'):
        manager_login()
    elif(choice=='9'):
        customer_login()
    elif(choice=='10'):
        backup_books_to_csv()
    else:
        print('Wrong Choice')
        main()

def manager_login():
    ps = input("Enter Manager Password:")
    if ps == 'alam786':
        main()
    else:
        print("Wrong Password")
        manager_login()

def customer_login():
    print('''
_________________________________________________________________________________________________________________________________________________________

                                                        CUSTOMER MENU
    1. VIEW BOOKS
    2. CHECK AVAILABILITY
    3. VIEW ISSUED BOOKS
    4. VIEW SUBMITTED BOOKS
    5. LOGOUT
_________________________________________________________________________________________________________________________________________________________
    ''')
    choice = input('Enter Task Number:')
    print('>______________________________________________________<')
    if choice == '1':
        dispbook()
    elif choice == '2':
        check_availability()
    elif choice == '3':
        view_issued_books()
    elif choice == '4':
        view_submitted_books()
    elif choice == '5':
        main()
    else:
        print('Wrong Choice')
        customer_login()

def pswd():
    ps = input("Enter Password (Manager Login):")
    if ps == 'alam786':
        main()
    else:
        print("Wrong Password")
        pswd()

print('''
Welcome to the Library System!
1. Manager Login
2. Customer Login
''')

login_choice = input("Enter your choice: ")

if login_choice == '1':
    pswd()
elif login_choice == '2':
    customer_login()
else:
    print("Invalid choice.")