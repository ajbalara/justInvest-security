# Anand Balaram SYSC 4810 Assignment Tests

import unittest
from assignment import access_control, ACCESS_CONTROL_POLICY

#from assignment import access_control


class Access_Control_TestCase(unittest.TestCase):
    """Test access_control (Problem 1c)"""

    def test_1(self):
        """ Expect all True"""
        for role in ACCESS_CONTROL_POLICY:
            for access in ACCESS_CONTROL_POLICY[role]:
                self.assertTrue(access_control(access, role))

    def test_2(self):
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

if __name__ == '__main__':
    unittest.main(verbosity=2)
