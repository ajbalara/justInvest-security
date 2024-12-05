# Anand Balaram SYSC 4810 Assignment

# System Functions
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def getch():
    """Get a single character from the user."""
    if os.name == 'nt':  # Windows
        return msvcrt.getch().decode('utf-8')
    else:  # Linux/Unix
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# Imports
import os

import subprocess

import sys

print("Setting up and installing libaries...")
print()

if os.name == 'nt':  # Windows
    import msvcrt
else:  # Linux/Unix
    import tty
    import termios

try:
    from argon2 import PasswordHasher
    print("argon2 library already installed!")
except ImportError:
    print("argon2 library not found. Installing...")
    install("argon2-cffi")
    from argon2 import PasswordHasher  # Retry importing after installation
print()


# Constants

ACCESS_CONTROL_POLICY = {
    "Client": [1, 2, 4],
    "Premium Client": [1, 2, 3, 4, 5],
    "Financial Advisor": [1, 2, 3, 7],
    "Financial Planner": [1, 2, 3, 6, 7],
    "Teller": [1, 2]
}

USER_ROLES = ["Client", "Premium Client", "Financial Advisor", "Financial Planner", "Teller"]

BUSINESS_DAY_START_HOUR = 9

BUSINESS_DAY_CLOSE_HOUR = 17

FILENAME = "passwd.txt"

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

PASSWORD_FILE_PATH = os.path.join(SCRIPT_PATH, FILENAME)

PASSWORD_FILE_STRUCTURE = ["username", "hash", "role"]

USERNAME_POSITION_IN_FILE = PASSWORD_FILE_STRUCTURE.index("username")

HASH_POSITION_IN_FILE = PASSWORD_FILE_STRUCTURE.index("hash")

ROLE_POSITION_IN_FILE = PASSWORD_FILE_STRUCTURE.index("role")

INVALID_INPUT = "Invalid input!\n"

SPECIAL_INPUT = 0

TOP_20_MOST_COMMON_PASSWORDS = [
    "123456",
    "123456789",
    "12345",
    "qwerty",
    "password",
    "12345678",
    "111111",
    "123123",
    "1234567890",
    "1234567",
    "qwerty123",
    "000000",
    "1q2w3e",
    "aa12345678",
    "abc123",
    "password1",
    "1234",
    "qwertyuiop",
    "123321",
    "password123"
]

# Classes
class User:
    def __init__(self, username: str, role: str):
        self.username = username
        self.role = role

# Functions

# Setup Functions
def set_time()->bool:
    """ Has the user set the time to a value between 0-23. Returns whether or not teller has access"""
    while True:
        try:
            time = int(input("Please enter the hour of the day (use 24 hour notation). Note that 0 is 12am and 23 is 11pm: "))
            if time < 0 or time > 23:
                print(INVALID_INPUT)
                continue
            return accessible_to_teller(time)
        except:
            print(INVALID_INPUT)
            continue

def accessible_to_teller(time: int)->bool:
    """ Returns true if teller has access based on the given time"""
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

# Login Functions
def user_sign_in(teller_access: bool)->User:
    """ Signs the user in. Returns the user. Will not let tellers access the system if the time set is not between 9am and 7pm"""
    signed_in = False
    while(not signed_in):
        username = input("Enter username to sign in or enter 0 to register: ")
        if check_user_input_is_zero(username):
            launch_signup()
        else:
            user = authenticate_user(username)
            if user is None or not check_teller_logic(user, teller_access):
                continue
            return user

def check_teller_logic(user: User, teller_access: bool)->bool:
    """ Returns true if the user should be allowed to access the system based on the time of day and whether or not they are a teller"""
    if user.role == "Teller" and not teller_access:
        print("A Teller cannot access the system outside of business hours!")
        return False
    return True


def check_user_input_is_zero(username: str)->bool:
    """ Returns if the user wants to signup or if they attempted to login"""
    try_to_sign_up = False
    try:
        try_to_sign_up = int(username) == SPECIAL_INPUT
    except:
        try_to_sign_up = False
    return try_to_sign_up


def launch_signup()->bool:
    """ Signs up user. Returns if successful for testing purposes"""
    username = input("Please enter your desired username: ")
    if get_user_from_file(PASSWORD_FILE_PATH, username) is not None:
        print("This username already exists!")
        return False
    password = input_password("Choose a password (minimum 8 characters, at least 1 number): ")
    if not proactive_password_checker(username, password):
        return False
    role = input_role()
    add_user(username, password, role)
    print("Signup was successful!")
    return True


def input_password(prompt):
    """Prompt for password input, showing '*' instead of characters."""
    print(prompt, end="", flush=True)
    password = []

    while True:
        ch = getch()
        if ch == '\r' or ch == '\n':  # Enter key (End input)
            break
        elif ch == '\x08' or ch == '\x7f':  # Backspace key
            if password:
                password.pop()
                # Handle removing the last '*' on the screen
                print("\b \b", end="", flush=True)
        else:  # Normal character
            password.append(ch)
            print("*", end="", flush=True)

    print()  # Print a newline after input
    return ''.join(password)

def proactive_password_checker(username: str, password: str)->bool:
    """ Returns True if the password meets the requirements"""
    if len(password) < 8:
        print("Password not long enough!")
        return False
    elif len(password) > 12:
        print("Password too long!")
        return False
    elif password in TOP_20_MOST_COMMON_PASSWORDS:
        print("Weak password!")
        return False
    elif not any(char.isdigit() for char in password):
        print("Password does not contain a digit!")
        return False
    elif not any(char.islower() for char in password):
        print("Password does not contain a lower-case letter!")
        return False
    elif not any(char.isupper() for char in password):
        print("Password does not contain a upper-case letter!")
        return False
    elif password == username:
        print("Password cannot be the same as username!")
        return False
    return True

def input_role()->str:
    """ Returns the inputted role of the new user"""
    print_roles()
    while True:
        try:
            user_input = input("Which role would you like to signup as?\n")
            user_select = int(user_input)
            if user_select < 1 or user_select > 5:
                print(INVALID_INPUT)
            else:
                return USER_ROLES[user_select-1]
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

def authenticate_user(username: str)->User:
    """ Returns whether user gives the correct password"""

    user_data = get_user_from_file(PASSWORD_FILE_PATH, username)

    if user_data is None:
        print("Username does not exist!")
        return None

    file_hash, role = user_data

    password = input_password("Enter your password: ")

    ph = PasswordHasher()

    try:
        ph.verify(file_hash, password)
    except:
        print("Wrong Password!")
        return None
    
    print("ACCESS GRANTED!")
    return User(username, role)

def add_user(username, password, role):
    """ Adds user to the passwd file"""
    ph = PasswordHasher()
    hash = ph.hash(password)
    write_user_to_file(PASSWORD_FILE_PATH, username, hash, role)
    return

def write_user_to_file(password_file_path: str, username: str, hash: str, role: str):
    """ Writes a user to file"""
    file = open(password_file_path, "a")   

    string_to_write = username + ", " + hash + ", " + role + "\n"
    file.write(string_to_write)

    file.close()

def get_user_from_file(password_file_path: str, entered_username: str)-> tuple[str, str]:
    """ Checks if the user is in the file and if so, returns a tuple containing their hash value and the role. Otherwise returns None"""

    file = open(password_file_path, "r")

    for line in file:
        entry = line.strip()
        values = entry.split(', ')
        username = values[USERNAME_POSITION_IN_FILE]
        
        if username == entered_username:
            file.close()
            return (values[HASH_POSITION_IN_FILE], values[ROLE_POSITION_IN_FILE])
    file.close()
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

# Access Control Functions
def access_control(user_select: str, user_role: str)->bool:
    """ Prints if user has access to a service. Returns whether or not they have access"""
    if (user_select in ACCESS_CONTROL_POLICY[user_role]):
        return True
    return False

def display_access(user: User)->str:
    """ Prints the operations the user has access to. Returns the string for testing purposes"""
    string_to_print = "Welcome " + user.username + "! You are a " + user.role + ". You can access operations: " + str(ACCESS_CONTROL_POLICY[user.role])
    print(string_to_print)
    return string_to_print

def main():
    """ Main program that runs"""
    teller_access = set_time()
    print_operations()
    user = user_sign_in(teller_access)
    display_access(user)
    while(True):
        print_operations()
        user_select = user_selection()
        if quit(user_select):
            break
        if access_control(user_select, user.role):
            print("Access Granted!")
        else:
            print("Access Denied!")

# Main program

if __name__ == '__main__':
    main()