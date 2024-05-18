from pathlib import Path
import csv
from menu import Menu
import re

users_file = Path("info/users.csv")
info_dir = Path("info")
Invalid_email = """Invalid email address.
"""
invalid_username = """A valid username can include letters(uppercase and lowercase), numbers, '_', '.', '-'.
It should also have between 4 and 16 characters.
"""
invalid_password = """weak password.
A strong password includes at least one uppercase letter,one lowercase letter,one number
and one special character. It should also contain at least 8 characters.
"""


class User:
    def __init__(self):
        self.email = ""
        self.username = ""
        self.password = ""
        self.account = "active"

    def make_dir_or_file(self):
        if not info_dir.exists():
            info_dir.mkdir()
        if not users_file.exists():
            with open('info/users.csv', 'w', newline="") as user_info:
                writer = csv.writer(user_info)
                writer.writerow(["email", "username", "password", "account"])

    def check_email(self):
        pattern = r"^[a-zA-Z0-9_. +-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, self.email):
            raise ValueError(f"\n{Invalid_email}")

    def check_username(self):
        pattern = r"[a-zA-Z0-9_.-]{4,16}$"
        if not re.match(pattern, self.username):
            raise ValueError(f"\n{invalid_username}")

    def check_password(self):
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not re.match(pattern, self.password):
            raise ValueError(f"\n{invalid_password}")

    def sign_up(self):
        self.email = input("-Please enter a valid email address: ")
        self.check_email()
        self.username = input("-Please enter a valid username: ")
        self.check_username()
        self.password = input("-Please enter a strong password: ")
        self.check_password()
        self.make_dir_or_file()
        with open("info/users.csv", "r") as users_info:
            reader = csv.reader(users_info)
            for email, username, password, account in reader:
                if email == self.email:
                    raise Exception("Duplicate email")
                if username == self.username:
                    raise Exception("Duplicate username")
        self.write_info()

    def write_info(self):
        with open("info/users.csv", "a", newline="") as users_info:
            writer = csv.writer(users_info)
            writer.writerow([self.email, self.username,
                            self.password, self.account])

    def log_in(self):
        self.username = input("-Username: ")
        self.password = input("-Password: ")
        self.make_dir_or_file()
        with open("info/users.csv", "r") as users_info:
            reader = csv.reader(users_info)
            for email, username, password, account in reader:
                if username == self.username and password == self.password:
                    if account == "active":
                        break
                    else:
                        raise Exception("Your account is deactive.")
            else:
                raise Exception("Wrong username or password.")
