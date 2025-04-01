import unittest
from math_utils.functions import add, subtract

class TestMathUtils(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 5), 4)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(10, -2), 12)

if __name__ == "__main__":
    unittest.main()