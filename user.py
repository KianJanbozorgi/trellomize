from pathlib import Path
import re
from util import File
import bcrypt

info_dir = Path("info")
users = Path("info/users.csv")
projects = Path("info/projects.csv")
manager = Path("manager.csv")
users_file = File(users)
projects_file = File(projects)
duty_file = File("info/duty.csv")
manager_file = File(manager)


invalid_email = """Invalid email address.
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
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return not re.match(pattern, self.email)

    def check_username(self):
        pattern = r"[a-zA-Z0-9_.-]{4,16}$"
        return not re.match(pattern, self.username)

    def check_password(self):
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        return not re.match(pattern, self.password)

    def hash_password(self, password):
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def check_pass(self, entered_password, stored_password):
        return bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8'))

    def sign_up(self, email, password, username):
        self.email = email
        self.username = username
        self.password = password
        self.make_dir_or_file()
        if self.check_email():
            raise ValueError(invalid_email)

        elif self.check_username():
            raise ValueError(invalid_username)

        elif self.check_password():
            raise ValueError(invalid_password)

        reader = users_file.read()
        for email, username, password, account in reader:
            if email == self.email:
                raise ValueError("This email is already in use.")
            elif username == self.username:
                raise ValueError("This username is already in use.")
        users_file.append([self.email, self.username,
                          self.hash_password(self.password), self.account])
        return "NO exception"

    def log_in(self, username, password):
        self.username = username
        self.password = password
        if self.is_manager():
            return
        self.make_dir_or_file()
        reader = users_file.read()
        for email, username, password, account in reader:
            if username == self.username and self.check_pass(self.password, password):
                if account == "active":
                    return "No exception"
                else:
                    raise PermissionError("Your account is deactive.")
        raise ValueError("Username or password is wrong.")

    def is_manager(self):
        if manager.exists():
            reader = manager_file.read()
            if reader[1][0] == self.username and self.check_pass(self.password, reader[1][1]):
                return True
        return False

    def deactive_account(self, username):
        reader = users_file.read()
        for index, info in enumerate(reader):
            if info[1] == username:
                if info[3] == "active":
                    info[3] = "deactive"
                    reader[index] = [*info]
                    break
                else:
                    raise ValueError("User account is currently deactive.")
        else:
            raise ValueError("There is no such username.")

        users_file.update(reader)

    def active_account(self, username):
        reader = users_file.read()
        for index, info in enumerate(reader):
            if info[1] == username:
                if info[3] == "deactive":
                    info[3] = "active"
                    reader[index] = [*info]
                    break
                else:
                    raise ValueError("User's account is currently active.")
        else:
            raise ValueError("There is no such username.")

        users_file.update(reader)

    def get_leader_projects(self):
        leader_projects = []
        reader = projects_file.read()
        for info in reader:
            if self.username == info[3]:
                leader_projects.append(info)
        return leader_projects

    def get_user_projects(self):
        user_projects = []
        reader = projects_file.read()
        for info in reader:
            if (len(info) > 4):
                for member in [username for username in info[4].split(",")]:
                    if self.username == member:
                        user_projects.append(info)
            else:
                continue
        return user_projects
