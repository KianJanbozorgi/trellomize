from pathlib import Path
import csv
from menu import Menu
import re

users_file = Path("info/users.csv")
info_dir = Path("info")


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

    def sign_up(self):
        self.email = input("-Email: ")
        self.username = input("-Username: ")
        self.password = input("-Password: ")
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
