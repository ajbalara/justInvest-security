# Anand Balaram SYSC 4810 Assignment


# Imports
import os

from hashlib import blake2b

import subprocess

import sys


# Constants

USERS = {
    "Sasha Kim": "Client",
    "Emery Blake": "Client",
    "Noor Abbasi": "Premium Client",
    "Zuri Adebayo": "Premium Client",
    "Mikael Chen": "Financial Advisor",
    "Jordan Riley": "Financial Advisor",
    "Ellis Nakamura": "Financial Planner",
    "Harper Diaz": "Financial Planner",
    "Alex Hayes": "Teller",
    "Adair Patel": "Teller"
}

ACCESS_CONTROL_POLICY = {
    "Client": [1, 2, 4],
    "Premium Client": [1, 2, 3, 4, 5],
    "Financial Advisor": [1, 2, 3, 7],
    "Financial Planner": [1, 2, 3, 6, 7],
    "Teller": [1, 2]
}

BUSINESS_DAY_START_HOUR = 9

BUSINESS_DAY_CLOSE_HOUR = 17

FILENAME = "passwd.txt"

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

PASSWORD_FILE_PATH = os.path.join(SCRIPT_PATH, FILENAME)

PASSWORD_FILE_STRUCTURE = ["username", "hash", "salt"]

USERNAME_POSITION_IN_FILE = PASSWORD_FILE_STRUCTURE.index("username")

HASH_POSITION_IN_FILE = PASSWORD_FILE_STRUCTURE.index("hash")

SALT_POSITION_IN_FILE = PASSWORD_FILE_STRUCTURE.index("salt")


# Functions

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def setup_libraries():
    print("Setting up and installing libaries...")
    print()
    try:
        import keyboard
        print("All dependencies already installed!")
    except ImportError:
        print("keyboard library not found. Installing...")
        install("keyboard")
        import keyboard  # Retry importing after installation
    print()

def set_time():
    time = int(input("Please enter the hour of the day (use 24 hour notation): "))
    return accessible_to_teller(time)

def accessible_to_teller(time):
    return time >= 9 and time <=17

def startup():
    print("justInvestSystem")
    print("----------------------------------")

def print_operations():
    print("Operations avaiable on the system:")
    print("1. View account balance")
    print("2. View investment portfolio")
    print("3. Modify investment portfolio")
    print("4. View Financial Advisor contact info")
    print("5. View Financial Planner contact info")
    print("6. View money market instruments")
    print("7. View private consumer instruments")
    print()

def user_sign_in(teller_access):
    signed_in = False
    
    while(not signed_in):
        print()
        username = input("Enter username to sign in or enter 0 to register: ")
        print()
        quit = False
        try:
            quit = int(username) == 0
        except:
            quit = False
        if quit:
            launch_signup()
        elif valid_username(username):
            if (USERS[username] == "Teller" and not teller_access):
                print("Teller can't access the system outside of business hours!")
                continue
            correct_pwd = False
            while(not correct_pwd):
                correct_pwd = authenticate_user(username)
            return USERS[username]
        print("Invalid username, please try again")
    
def launch_signup():
    username = input("Please enter your desired username: ")
    password = input("Please enter your desired password: ")

def valid_username(username):
    return username in USERS

def authenticate_user(username):
    pwd = input("Please enter your password: ")
    print("ACCESS GRANTED!")
    print("Your authorized operations are: ", ACCESS_CONTROL_POLICY[USERS[username]])

def add_user():
    return

def write_user_to_file(username, hash, salt):
    file = open(PASSWORD_FILE_PATH, "a")   

    string_to_write = "\n" + username + ", " + hash + ", " + str(salt)
    file.write(string_to_write)

    file.close()

def check_file_for_user(entered_username):
    file = open(PASSWORD_FILE_PATH, "r")

    for line in file:
        entry = line.strip()
        values = entry.split(',')
        username = values[USERNAME_POSITION_IN_FILE]
        
        if username == entered_username:
            return (values[HASH_POSITION_IN_FILE], values[SALT_POSITION_IN_FILE])
    return None


def user_selection():
    print()
    user_select = input("Which operation would you like to perform?\n")
    return int(user_select)

def quit(user_select):
    return int(user_select) == 0

def access_control(user_select, user_role):
    if (user_select in ACCESS_CONTROL_POLICY[user_role]):
        print("Access Granted!")
        return
    print("Access Denied!")

def main():
    setup_libraries()
    teller_access = set_time()
    print_operations()
    user_role = user_sign_in(teller_access)

    while(True):
        user_select = user_selection()
        if quit(user_select):
            break
        access_control(user_select, user_role)

# Main program

if __name__ == '__main__':
    main()