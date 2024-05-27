from pathlib import Path
import re
from util import File
import bcrypt
from typing import List

# Define file paths
info_dir = Path("info")
users = Path("info/users.csv")
projects = Path("info/projects.csv")
duty = Path("info/duty.csv")
manager = Path("manager.csv")

# Initialize file objects
users_file = File(users)
projects_file = File(projects)
duty_file = File(duty)
manager_file = File(manager)

# Error messages for invalid email, username, and password formats
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
    """Class to handle user operations such as signup, login, and account management."""

    def __init__(self) -> None:
        """Initialize User attributes."""
        self.email: str = ""
        self.username: str = ""
        self.password: str = ""
        self.account: str = "active"

    def make_dir_or_file(self) -> None:
        """Create necessary directories and files if they don't exist."""
        if not info_dir.exists():
            info_dir.mkdir()
        if not users.exists():
            users_file.write(["email", "username", "password", "account"])

    def check_email(self) -> bool:
        """Check if the email format is valid."""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return not re.match(pattern, self.email)

    def check_username(self) -> bool:
        """Check if the username format is valid."""
        pattern = r"[a-zA-Z0-9_.-]{4,16}$"
        return not re.match(pattern, self.username)

    def check_password(self) -> bool:
        """Check if the password format is valid."""
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        return not re.match(pattern, self.password)

    def hash_password(self, password: str) -> str:
        """Hash the given password."""
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def check_pass(self, entered_password: str, stored_password: str) -> bool:
        """Check if the entered password matches the stored hashed password."""
        return bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8'))

    def sign_up(self, email: str, password: str, username: str) -> str:
        """Sign up a new user."""
        self.email = email
        self.username = username
        self.password = password
        self.make_dir_or_file()
        if self.check_email():
            raise ValueError("Invalid email address.")

        elif self.check_username():
            raise ValueError("Invalid username.")

        elif self.check_password():
            raise ValueError("Weak password.")

        reader = users_file.read()
        for email, username, password, account in reader:
            if email == self.email:
                raise ValueError("This email is already in use.")
            elif username == self.username:
                raise ValueError("This username is already in use.")
        users_file.append([self.email, self.username,
                          self.hash_password(self.password), self.account])
        return "NO exception"

    def log_in(self, username: str, password: str) -> str:
        """Log in the user."""
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
                    raise PermissionError("Your account is deactivated.")
        raise ValueError("Username or password is wrong.")

    def is_manager(self) -> bool:
        """Check if the user is a manager."""
        if manager.exists():
            reader = manager_file.read()
            if reader[1][0] == self.username and self.check_pass(self.password, reader[1][1]):
                return True
        return False

    def deactive_account(self, username: str) -> None:
        """Deactivate a user's account."""
        reader = users_file.read()
        for index, info in enumerate(reader):
            if info[1] == username:
                if info[3] == "active":
                    info[3] = "deactive"
                    reader[index] = [*info]
                    break
                else:
                    raise ValueError("User account is currently deactivated.")
        else:
            raise ValueError("There is no such username.")

        users_file.update(reader)

    def active_account(self, username: str) -> None:
        """Activate a user's account."""
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

    def get_leader_projects(self) -> List[List[str]]:
        """Get projects led by the user."""
        leader_projects = []
        reader = projects_file.read()
        for info in reader:
            if self.username == info[3]:
                leader_projects.append(info)
        return leader_projects

    def get_user_projects(self) -> List[List[str]]:
        """Get projects where the user is a member."""
        user_projects = []
        reader = projects_file.read()
        for info in reader:
            if len(info) > 4:
                for member in [username for username in info[4].split(",")]:
                    if self.username == member:
                        user_projects.append(info)
            else:
                continue
        return user_projects
