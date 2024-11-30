# Anand Balaram SYSC 4810 Assignment Tests

# Imports
import unittest
from assignment import access_control, ACCESS_CONTROL_POLICY, write_user_to_file, get_user_from_file, install
import os

try:
    from argon2 import PasswordHasher
    print("argon2 library already installed!")
except ImportError:
    print("argon2 library not found. Installing...")
    install("argon2-cffi")
    from argon2 import PasswordHasher  # Retry importing after installation
print()

# Constants
FILENAME = "test_passwd.txt"

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

PASSWORD_FILE_PATH = os.path.join(SCRIPT_PATH, FILENAME)

# Tests
class Access_Control_TestCase(unittest.TestCase):
    """Test access_control (Problem 1c)"""

    def test_access_granted(self):
        """ Expect all True"""
        for role in ACCESS_CONTROL_POLICY:
            for access in ACCESS_CONTROL_POLICY[role]:
                self.assertTrue(access_control(access, role))

    def test_access_denied(self):
        """ Expect all False"""
        deny_list = dict()

        for role in ACCESS_CONTROL_POLICY:
            deny_list[role] = []
            for i in range(1, 8):
                if i not in ACCESS_CONTROL_POLICY[role]:
                    deny_list[role].append(i)

        for role in deny_list:
            for access in deny_list[role]:
                self.assertFalse(access_control(access, role))

class Write_and_Get_File_TestCase(unittest.TestCase):
    """ Test write_user_to_file and get_user_from_file (Problem 2d)"""

    def test_writing_and_getting(self):
        username = "Test"
        password = "verysecurepassword123"
        
        ph = PasswordHasher()
        hash = ph.hash(password)

        role = "Client"

        write_user_to_file(PASSWORD_FILE_PATH, username, hash, role)

        read_data = get_user_from_file(PASSWORD_FILE_PATH, username)
        self.assertIsNotNone(read_data)
        read_hash, read_role = read_data

        self.assertEqual(read_hash, hash)
        self.assertEqual(read_role, role)

        # Clear the file to ensure that there are no duplicate usernames in the file
        # Checking for this is outside of the scope for these functions and is handled elsewhere in the code
        with open(PASSWORD_FILE_PATH, "w") as file:
            pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
