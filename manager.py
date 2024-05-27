from user import User, manager_file, info_dir
import argparse
import shutil
from menu import console, Menu


class Manager:
    """A class to manage system administrators and data purging operations.

    Attributes:
        args (argparse.Namespace): Command-line arguments parsed by argparse.
        user (User): An instance of the User class.
    """

    def __init__(self) -> None:
        """Initialize the Manager class."""
        self.args: argparse.Namespace = self.get_info()  # Parse command-line arguments
        self.user: User = User()  # Initialize User object

    def get_info(self) -> argparse.Namespace:
        """Parse command-line arguments."""
        parser: argparse.ArgumentParser = argparse.ArgumentParser()
        parser.add_argument("command", choices=["create-admin", "purge-data"])
        parser.add_argument("--username", type=str)
        parser.add_argument("--password", type=str)
        return parser.parse_args()

    def exist(self) -> bool:
        """Check if the manager file exists."""
        try:
            reader = manager_file.read()
            if len(reader) == 2:
                return True
        except FileNotFoundError:
            pass
        return False

    def sign_up(self) -> None:
        """Sign up a new system manager."""
        console.clear()  # Clear console screen
        if not self.exist():
            # Add headers to manager file
            manager_file.append(["username", "password"])
            manager_file.append(
                [self.args.username, self.user.hash_password(self.args.password)])
            print("Signed up successfully")
        else:
            print("System manager is already built.")

    def purge_data(self) -> None:
        """Purge all data if the manager exists."""
        if self.exist():
            # Create a confirmation menu
            menu = Menu(
                ["Are you sure you want to purge all data?", "Yes", "No"])
            menu.display()
            console.clear()  # Clear console screen
            if menu.selected_option == "Yes":
                if info_dir.exists():  # Check if data directory exists
                    # Delete the entire directory and its contents
                    shutil.rmtree(info_dir)
                    print("All data has been purged.")
                else:
                    print("No data to purge.")
            elif menu.selected_option == "No":
                print("Purge data operation cancelled.")
        else:
            console.clear()  # Clear console screen
            print("Data purging failed")


if __name__ == "__main__":
    manager = Manager()

    if manager.args.command == "create-admin":
        manager.sign_up()  # Call sign_up method

    elif manager.args.command == "purge-data":
        manager.purge_data()  # Call purge_data method
