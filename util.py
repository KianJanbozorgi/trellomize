import csv


class File:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, "r") as file:
            reader = csv.reader(file)
            return list(reader)

    def write(self, item):
        with open(self.path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(item)

    def append(self, item):
        with open(self.path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(item)
