import unittest
from app import getResponse


class TestApp(unittest.TestCase):
    def test_getResponse(self):
        # Test case 1: Empty user input
        user_input = ""
        expected_output = ""
        self.assertEqual(getResponse(user_input), expected_output)

        # Test case 2: User input with a sentence
        user_input = "How are you?"
        expected_output = "Hello! How can I assist you?"
        self.assertEqual(getResponse(user_input), expected_output)

        # Test case 3: User input with a question
        user_input = "What is the weather like today?"
        expected_output = "I'm sorry, I don't have that information."
        self.assertEqual(getResponse(user_input), expected_output)


if __name__ == "__main__":
    unittest.main()
