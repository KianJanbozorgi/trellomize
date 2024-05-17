import argparse
import csv
from pathlib import Path
import shutil
from menu import console, Menu

manager_file = Path("manager.csv")
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

    def write_info(self):
        with open("manager.csv", "a", newline="") as manger_info:
            writer = csv.writer(manger_info)
            writer.writerow(["username", "password"])
            writer.writerow([self.args.username, self.args.password])

    def exist(self):
        try:
            with open("manager.csv", "r") as manger_info:
                reader = csv.reader(manger_info)
                if len([*reader]) == 2:
                    return True
        except FileNotFoundError:
            pass
        return False

    def sign_up(self):
        console.clear()
        if not self.exist():
            manager.write_info()
            print("Signed up successfully")
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
