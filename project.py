from user import User, users_file, projects_file, manager_file, duty_file, projects, duty
from enum import Enum
from datetime import datetime, timedelta
import uuid
from typing import List, Any, Union, Tuple


class Project:
    """Class representing a project."""

    def create(self, id: Union[str, int], title: str, description: str, leader: str) -> None:
        """Create a new project."""
        self.Id = id
        if not self.check_id_unique():
            raise ValueError("The selected id is not unique.")

        self.title = title
        self.Description = description
        self.leader = leader
        self.write_to_file()

    def check_id_unique(self) -> bool:
        """Check if the project id is unique."""
        if not projects.exists():
            return True

        reader = projects_file.read()
        for info in reader:
            if info[0] == self.Id:
                return False

        return True

    def write_to_file(self) -> None:
        """Write project information to file."""
        if not projects.exists():
            projects_file.write(
                ["Id", "Title", "Description", "Leader", "Members"])

        if not duty.exists():
            duty_file.write(["Project_id", "Task_id", "Members", "Title", "Description",
                            "Priority", "Status", "Start", "End", "Comments", "History"])

        projects_file.append(
            [self.Id, self.title, self.Description, self.leader])

    def leader_projects(self, user: User) -> List[str]:
        """Get projects led by the user."""
        if not projects.exists():
            raise FileNotFoundError("You have not created any projects yet.")

        # Retrieve projects led by the user from the user object
        leader_projects = [f"(Id: {item[0]}, Title: {item[1]}, Description: {item[2]}, members: {"no body" if len(item) != 5 else item[4]})"
                           for item in user.get_leader_projects() if item[0] != "Name"]

        if not leader_projects:
            raise ValueError("You have not created any projects yet")

        return leader_projects

    def user_projects(self, user: User) -> List[str]:
        """Get projects where the user is a member."""
        if not projects.exists():
            raise FileNotFoundError("You are not a member of any projects.")

        # Retrieve projects where the user is a member from the user object
        user_projects = [f"(Id: {item[0]}, Title: {item[1]}, Description: {item[2]})"
                         for item in user.get_user_projects() if item[0] != "Id"]

        if not user_projects:
            raise ValueError("You are not a member of any projects.")

        return user_projects

    def find(self, id: Union[str, int]) -> Tuple[int, List[Any]]:
        """Find project by id."""
        projects = projects_file.read()
        for info in enumerate(projects):
            if id == info[1][0]:
                return info

    def add_member_func(self, input_username: str, id: Union[str, int]) -> None:
        """Add members to a project."""

        users = users_file.read()
        manager = manager_file.read()
        projects = projects_file.read()
        project_index, project = self.find(id)

        # Retrieve valid members from the users file and manager file
        valid_usernames = [info[1] for info in users if project[3] != info[1]]
        valid_members = [*valid_usernames, manager[1][0]]

        current_members = []
        if len(project) == 5:
            current_members = [member for member in project[4].split(",")]

        if input_username in current_members:
            raise ValueError("user is already a member of the project.")

        if input_username == project[3]:
            raise ValueError("You are the leader of project.")

        if input_username not in valid_members:
            raise ValueError("username not found.")

        all_members = [*current_members, input_username]

        if len(project) == 4:
            project.append(",".join(all_members))
        else:
            project[4] = ",".join(all_members)

        projects[project_index] = project
        projects_file.update(projects)

    def delete_member_func(self, input_username: str, id: Union[str, int]) -> None:
        """Delete members from a project."""

        projects = projects_file.read()
        project_index, project = self.find(id)

        current_members = []
        if len(project) == 5:
            current_members = [member for member in project[4].split(",")]

        if input_username not in current_members:
            raise ValueError("A user with such a username is not a member of the project.")

        current_members.remove(input_username)

        if not current_members:
            project.pop()
        else:
            project[4] = ",".join(current_members)

        projects[project_index] = project
        projects_file.update(projects)

    def delete_project(self, id: Union[str, int]) -> None:
        """Delete a project by id."""
        reader = projects_file.read()
        project_title = ""
        for project in reader:
            if str(project[0]) == id:
                project_title = project[1]
                reader.remove(project)
                break
        projects_file.update(reader)
        return project_title
    
    def check_id(self, id, projects_list):
        for project in projects_list:
            if str(id) in project:
                return
        raise ValueError("There is no project with this ID.")

class Priority(Enum):
    """Enumeration class for duty priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Status(Enum):
    """Enumeration class for duty status."""
    BACKLOG = 1
    TODO = 2
    DOING = 3
    DONE = 4
    ARCHIVED = 5


class Duty:
    """Class representing a duty."""

    def __init__(self, proj_id: Union[str, int] = None, members: List[str] = None, title: str = "no title", description: str = "no data", priority: int = 1,
                 history: List[str] = [], status: int = 1, start: str = str(datetime.now()), end: datetime = datetime.now() + timedelta(hours=24),
                 comments: List[str] = []) -> None:
        """Initialize a Duty instance."""
        self.task_id : uuid.UUID = self.check_id_unique()
        self.members = members
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.start = start
        self.end = end
        self.proj_id = proj_id
        self.comments = comments
        self.history = history

    def check_id_unique(self):
        """Generates a unique task ID not present in existing tasks."""
        tasks = duty_file.read()
        while True:
            self.task_id = uuid.uuid4()
            for task in tasks:
                if self.task_id == task[2]:
                    break
            else:
                return self.task_id

    def save(self) -> None:
        """Save duty information to file."""
        duty_file.append(
            [self.proj_id, self.task_id, self.members, self.title, self.description, self.priority, self.status, self.start, self.end, self.comments, self.history])
