import argparse
import csv
from pathlib import Path
import shutil
from menu import console, Menu
from util import File

manager_file = File("manager.csv")
info_dir = Path("info")


class Manager:
    def __init__(self):
        self.args = self.get_info()

    def get_info(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("command", choices=["create-admin", "purge-data"])
        parser.add_argument("--username", type=str)
        parser.add_argument("--password", type=str)
        return parser.parse_args()

    def exist(self):
        try:
            reader = manager_file.read()
            if len(reader) == 2:
                return True
        except FileNotFoundError:
            pass
        return False

    def sign_up(self):
        console.clear()
        if not self.exist():
            manager_file.append(["username", "password"])
            manager_file.append([self.args.username, self.args.password])
            print("signed up successfully")
        else:
            print("System manager is already built.")

    def purge_data(self):
        if self.exist():
            menu = Menu(
                ["Are you sure you want to purge all data?", "Yes", "No"])
            menu.display()
            console.clear()
            if menu.selected_option == "Yes":
                if info_dir.exists():
                    shutil.rmtree(info_dir)
                    print("All data has been purged.")
                else:
                    print("No data to purge.")
            elif menu.selected_option == "No":
                print("purge data operation cancelled.")
        else:
            console.clear()
            print("data purging failed")


if __name__ == "__main__":
    manager = Manager()
    if manager.args.command == "create-admin":
        manager.sign_up()

    elif manager.args.command == "purge-data":
        manager.purge_data()
