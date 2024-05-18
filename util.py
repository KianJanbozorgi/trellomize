import csv
from typing import List


class File:
    def __init__(self, path: str):
        """Initialize with the given file path."""
        self.path = path

    def read(self) -> List[List[str]]:
        """Read and return the contents of the CSV file."""
        with open(self.path, "r", newline="") as file:
            return list(csv.reader(file))

    def write(self, item: List[str]) -> None:
        """Write a single row to the CSV file."""
        with open(self.path, "w", newline="") as file:
            csv.writer(file).writerow(item)

    def append(self, item: List[str]) -> None:
        """Append a single row to the CSV file."""
        with open(self.path, "a", newline="") as file:
            csv.writer(file).writerow(item)
