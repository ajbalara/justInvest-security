# Anand Balaram SYSC 4810 Assignment


# Imports
import os

from hashlib import blake2b

import subprocess

import sys

import random

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

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

PASSWORD_FILE_STRUCTURE = ["username", "hash", "salt", "role"]

USERNAME_POSITION_IN_FILE = PASSWORD_FILE_STRUCTURE.index("username")

HASH_POSITION_IN_FILE = PASSWORD_FILE_STRUCTURE.index("hash")

SALT_POSITION_IN_FILE = PASSWORD_FILE_STRUCTURE.index("salt")

ROLE_POSITION_IN_FILE = PASSWORD_FILE_STRUCTURE.index("role")

INVALID_INPUT = "Invalid input!\n"

SPECIAL_INPUT = 0


# Functions

def set_time()->bool:
    """ Has the user set the time to a value between 0-24. Returns whether or not teller has access"""
    while True:
        try:
            time = int(input("Please enter the hour of the day (use 24 hour notation): "))
            if time < 0 or time > 24:
                print(INVALID_INPUT)
                continue
            return accessible_to_teller(time)
        except:
            print(INVALID_INPUT)
            continue

def accessible_to_teller(time: int)->bool:
    """ Returns whether or not teller has access based on the given time"""
    return time >= BUSINESS_DAY_START_HOUR and time <=BUSINESS_DAY_CLOSE_HOUR

def startup():
    """ Prints the startup menu for the user to see"""
    print("justInvestSystem")
    print("----------------------------------")

def print_operations():
    print("Operations available on the system:")
    print("1. View account balance")
    print("2. View investment portfolio")
    print("3. Modify investment portfolio")
    print("4. View Financial Advisor contact info")
    print("5. View Financial Planner contact info")
    print("6. View money market instruments")
    print("7. View private consumer instruments")
    print("0. Quit")
    print()

def user_sign_in(teller_access: bool)->str:
    """ Signs the user in or registers them. Will not let tellers access the system if the time set is not between 9am and 7pm"""
    signed_in = False
    
    while(not signed_in):
        print()
        username = input("Enter username to sign in or enter 0 to register: ")
        print()
        signup = False
        try:
            signup = int(username) == SPECIAL_INPUT
        except:
            signup = False
        if signup:
            return launch_signup()
        elif valid_username(username):
            if (USERS[username] == "Teller" and not teller_access):
                print("Teller can't access the system outside of business hours!")
                continue
            correct_pwd = False
            while(not correct_pwd):
                correct_pwd = authenticate_user(username)
            return USERS[username]
        print("Invalid username, please try again")
    
def launch_signup()->str:
    """ Signs up user"""
    username = input("Please enter your desired username: ")
    password = input_password()
    role = input_role()
    add_user(username, password, role)
    print("Signup was successful!")
    return username

def input_password()->str:
    """ Returns the password that the user enters"""
    prompt="Enter password: "
    print(prompt, end='', flush=True)
    password = ""
    while True:
        key = keyboard.read_event(suppress=True)
        if key.event_type == "down":
            if key.name == "enter":
                print()
                break
            elif key.name == "backspace":
                if password:
                    password = password[:-1]
                    print("\b \b", end='', flush=True)
            elif len(key.name) == 1:
                password += key.name
                print("*", end='', flush=True)
    return password

def input_role()->str:
    """ Returns the inputted role of the new user"""
    print_roles()
    while True:
        try:
            user_select = int(input("Which role would you like to signup as?\n"))
            if user_select < 1 or user_select > 5:
                print(INVALID_INPUT)
            else:
                return ACCESS_CONTROL_POLICY[user_select]
        except:
            print(INVALID_INPUT)


def print_roles():
    """ Prints out roles for the system"""
    print("Roles available on the system:")
    print("1. Client")
    print("2. Premium Client")
    print("3. Financial Advisor")
    print("4. Financial Planner")
    print("5. Teller")
    print()

def valid_username(username: str)->bool:
    """ Returns whether username is in password file"""
    reserved_keyword = False
    try:
        reserved_keyword = int(username) == SPECIAL_INPUT
    except:
        reserved_keyword = False

    return not reserved_keyword and username in USERS

def authenticate_user(username: str)->bool:
    """ Returns whether user gives the correct password"""

    pwd = input("Please enter your password: ")
    print("ACCESS GRANTED!")
    print("Your authorized operations are: ", ACCESS_CONTROL_POLICY[USERS[username]])
    return True

def add_user(username, password, role):
    """ Adds user to the passwd file"""
    return

def write_user_to_file(username: str, hash: str, salt: str, role: str):
    """ Writes a user to file"""
    file = open(PASSWORD_FILE_PATH, "a")   

    string_to_write = "\n" + username + ", " + hash + ", " + salt + ", " + role
    file.write(string_to_write)

    file.close()

def check_file_for_user(entered_username: str)-> tuple[str, str, str]:
    """ Checks if the user is in the file and if so, returns a tuple containing it's hash value and the salt. Otherwise returns None"""

    file = open(PASSWORD_FILE_PATH, "r")

    for line in file:
        entry = line.strip()
        values = entry.split(',')
        username = values[USERNAME_POSITION_IN_FILE]
        
        if username == entered_username:
            return (values[HASH_POSITION_IN_FILE], values[SALT_POSITION_IN_FILE], values[ROLE_POSITION_IN_FILE])
    return None


def user_selection()->int:
    """ Returns the user selection of the options"""
    print()
    while True:
        try:
            user_select = int(input("Which operation would you like to perform?\n"))
            if user_select < SPECIAL_INPUT or user_select > 7:
                print(INVALID_INPUT)
            else:
                return user_select
        except:
            print(INVALID_INPUT)

def quit(user_select: int)->bool:
    """ Returns whether the user has chosen to quit the program"""
    return user_select == SPECIAL_INPUT

def access_control(user_select: str, user_role: str):
    """ Prints if user has access to a service"""
    if (user_select in ACCESS_CONTROL_POLICY[user_role]):
        print("Access Granted!")
        return
    print("Access Denied!")

def main():
    """ Main program that runs"""
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