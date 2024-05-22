from pathlib import Path
import re
from util import File
import bcrypt
import main

info_dir = Path("info")
users = Path("info/users.csv")
users_file = File("info/users.csv")
project_file = File("info/project.csv")
duty_file = File("info/duty.csv")


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
        if not users.exists():
            users_file.write(["email", "username", "password", "account"])

    def check_email(self):
        pattern = r"^[a-zA-Z0-9_. +-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, self.email):
            return True
        else:
            return False
    def check_username(self):
        pattern = r"[a-zA-Z0-9_.-]{4,16}$"
        if not re.match(pattern, self.username):
           return True
        else:
            return False
    def check_password(self):
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not re.match(pattern, self.password):
            return True
        else:
            return False

    def hash_password(self, password):
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def check_pass(self, entered_password, stored_password):
        return bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8'))

    def sign_up(self,email, password, username)->int:
        self.email = email
        self.username = username
        self.password = password
        self.make_dir_or_file()
        if  self.check_email():
            return 1
        
        elif  self.check_username():
            return 2
        
        elif  self.check_password():
            return 3
        else:
            self.make_dir_or_file()
            reader = users_file.read()
            for email, username, password, account in reader:
                if email == self.email:
                    return 4
                elif username == self.username:
                    return 5    
            users_file.append([self.email, self.username,
                            self.hash_password(self.password), self.account])
            return 0

    def log_in(self , username , password):
        self.username = username
        self.password = password
        self.make_dir_or_file()
        reader = users_file.read()
        for email, username, password, account in reader:
            if username == self.username and self.check_pass(self.password, password):
                if account == "active":
                    return 0
                else:
                    return 1
        else:
            return 2
        

    def get_leader_projects(self):
        leader_projects = []
        reader = project_file.read()
        for info in reader:
            if self.username == info[4]:
                leader_projects.append(info)
        return leader_projects

    def get_user_projects(self):
        user_projects = []
        reader = project_file.read()
        for info in reader:
            for member in info[5:]:
                if self.username == member:
                    user_projects.append(info)
        return user_projects
