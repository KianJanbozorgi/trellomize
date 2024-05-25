import unittest
from main import SayHello  # Replace with your actual class name

class TestSayHelloApp(unittest.TestCase):

    def setUp(self):
        self.app = SayHello()
        
    def test_app_opens(self):
        self.assertIsNotNone(self.app.window)  # Check if window is created

    def test_sign_up_success(self):
        # Simulate successful sign-up (replace with actual sign-up logic)
        self.app.user_name.text = "new_user"
        self.app.user_email.text = "new_user@example.com"
        self.app.user_password.text = "secure_password"
        self.app.sign_in_button_fun("")
        # Ideally, you'd check data persistence or user object creation here

    def test_sign_up_duplicate_user(self):
        # Simulate duplicate username sign-up (replace with actual logic)
        username = "existing_user"
        email = "existing@example.com"
        password = "user_password"
        self.app.sign_up(username, email, password)  # Sign-up first
        with self.assertRaises(Exception):  # Expect an exception on duplicate
            self.app.sign_up(username, "another@example.com", password)

    def test_login_success(self):
        # Simulate successful sign-up beforehand (replace with actual logic)
        username = "created_user"
        password = "created_user_password"
        self.app.log_in(username, password)
        # Ideally, you'd check if the project page is displayed

    def test_login_incorrect_username(self):
        username = "wrong_username"
        password = "correct_password"  # Assuming a user exists with this password
        with self.assertRaises(Exception):  # Expect an exception for wrong username
            self.app.log_in(username, password)

    # Add more test cases here for other functionalities (UI elements, project management buttons)

if __name__ == "__main__":
    unittest.main()
