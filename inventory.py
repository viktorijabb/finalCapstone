"""
Inventory program for shoes, that reads from inventory.txt
Functionality:
d - display all shoe data
s - search for shoe
a - add shoes to database
r - re-stock
c - check which shoes are for sale
v - show value of each position of stock
x - exit

"""

from tabulate import tabulate

#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return int(self.cost)

    def get_quantity(self):
        return int(self.quantity)

    def __str__(self):
        return f"{str(self.country)},{str(self.code)},{str(self.product)},{str(self.cost)},{str(self.quantity)}"


#=============Shoe list===========

shoe_list = []  # DO NOT CHANGE # CONTAINS DATA FROM inventory.txt
                # list of objects

#==========Functions outside the class - menu options ==============

def read_shoes_data():
    # reads inventory.txt and appends to shoe_list - upon start up of program
    lines = get_lines()

    for index, line in enumerate(lines, 1):  # starts count from 1 for ux
        country, code, product, cost, quantity = split_lines(index, line)
        shoes = Shoe(country, code, product, cost, quantity)  # shoe object
        shoe_list.append(shoes)


def capture_shoes():  # option a
    # allows user to add new shoe data
    country = input("Enter the country: ")
    code = input("Enter the product code: ")
    product = input("Enter the product name: ")
    while True:
        try:
            cost = int(input("Enter the cost: "))
            break
        except ValueError:
            print("The cost should be a whole number!")
    while True:
        try:
            quantity = int(input("Enter the quantity: "))
            break
        except ValueError:
            print("The quantity should be a whole number!")
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)  # appends to shoe list

    with open("inventory.txt", "a") as file:
        file.write(f"\n{str(new_shoe)}")  # appends to inventory.txt


def view_all():  # option d
    # displays all data from file
    table = []
    try:
        with open("inventory.txt", "r") as inventory_file:
            for i, line in enumerate(inventory_file):
                new_line = f"{str(i)}," + (line.replace("\n", ""))
                table.append(new_line.split(","))
    except FileNotFoundError:
        print("Inventory file not found!")
    print(tabulate(table[1:]))


def re_stock():  # option r
    # allows user to re-stock item with lowest stock
    stock_list = get_stock_l()
    min = get_min(stock_list)
    print(f"Lowest stock:\n{find_by_stock(min)}")  # finds and prints shoe w lowest stock level

    usr_inp = input("Would you like to update this stock?(y/n) ").lower()
    if usr_inp == "y":
        while True:
            try:
                usr_inp_stock = int(input("Enter stock to add: "))
                break
            except ValueError:
                print("Error: Enter a whole number! ")

        lines = get_lines()

        for index, line in enumerate(lines, 1):  # starts count from 1 for ux
            country, code, product, cost, quantity = split_lines(index, line)

            if int(min) == int(quantity):
                new_stock = int(min) + int(usr_inp_stock)
                quantity.replace(str(quantity), str(new_stock))  # replaces stock level in txt file
                print(f"{code} stock updated from {min} to {new_stock}")

    elif usr_inp != "n":
        print("Input not valid! ")


def search_shoe():  # option s
    # finds shoe by SKU code
    usr_inp_sku = (input("Enter the code of the product you are"
                           " looking for:\n").lower()).replace("sku", "")

    for item in shoe_list:
        if item.code.replace("SKU", "") == usr_inp_sku:
            print("Product: \n")
            print(tabulate([[item.country, item.code, item.product, item.cost,  item.quantity]]))


def value_per_item():  # option v
    # prints cost * quantity for all shoes
    print("Code     Value")  # 'header' for result display

    for item in shoe_list:
        value = int(item.cost) * int(item.quantity)
        print(item.code, value)


def highest_qty():  # option c
    # prints item with highest stock level
    stock_list = get_stock_l()
    max = get_max(stock_list)
    print(f"Shoes for sale:\n{find_by_stock(max)}")

# ---- secondary functions ------

def get_min(l):
    # calculate the minimum value
    min = l[0]
    for i in l:
        if i < min:
            min = i
    return min

def get_max(l):
    # calculate the max value
    max = l[0]
    for i in l:
        if i > max:
            max = i
    return max


def get_lines():
    # retrieves data from database txt file
    with open("inventory.txt", "r+", encoding='utf-8-sig') as inv_f:  # encoding to eliminate special chars
        return inv_f.readlines()[1:]  # skips header row


def split_lines(index, line):
    # splits line of text file shoe database and returns 5 values or relevant error with pointer
    try:
        country, code, product, cost, quantity = line.strip("\n").split(",")
        return country, code, product, cost, quantity
    except ValueError:
        print(f"There is an error in line {index} of the shoe database")


def get_stock_l():
    # generate list of stock levels from list of objects
    return [int(item.quantity) for item in shoe_list]


def find_by_stock(search_value):
    # searches for a product with certain quantity, returns info of item
    for item in shoe_list:
        if int(search_value) == int(item.quantity):
            return (tabulate([[item.country, item.code, item.product, item.cost, item.quantity]]))
#==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''
#view_all()


while True:
    read_shoes_data()  # UPON START UP OF PROGRAM AND AFTER EVERY MENU OPTION
    print("""Welcome to INVENTORY.py, home of shoes data!  
d - display all shoe data
s - search for shoe
a - add shoes to database
r - re-stock 
c - check which shoes are for sale
v - show value of each position of stock
x - exit """)
    menu = input(" ").lower()
    if menu == "d":
        view_all()
    elif menu == "s":
        search_shoe()
    elif menu == "a":
        capture_shoes()
    elif menu == "r":
        re_stock()
    elif menu == "c":
        highest_qty()
    elif menu == "v":
        value_per_item()
    elif menu == "x":
        print("Goodbye! ")
        break
    else:
        print("Input not valid!")