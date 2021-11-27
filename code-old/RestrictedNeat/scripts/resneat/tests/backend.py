import unittest

from backend.overseer import Overseer


class TestOverseerWithPyneat(unittest.TestCase):

    def test_environment_initialization(self):
        o = Overseer('Walker-v3')


if __name__ == '__main__':
    unittest.main()
