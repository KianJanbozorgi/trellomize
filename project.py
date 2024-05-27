from pathlib import Path
from user import users_file, projects_file, duty_file, projects
from enum import Enum
import datetime
import uuid


class Project:
    def __init__(self):
        self.duties = []

    def create(self, id, title, description, leader):
        self.Id = id
        if not self.check_id_unique():
            raise ValueError("The selected id is not unique")
        self.title = title
        self.Description = description
        self.leader = leader
        self.write_to_file()

    def check_id_unique(self):
        if not projects.exists():
            return True
        reader = projects_file.read()
        for info in reader:
            if info[0] == self.Id:
                return False
        return True

    def write_to_file(self):
        if not projects.exists():
            projects_file.write(
                ["Id", "Title", "Description", "Leader", "Members"])
        projects_file.append(
            [self.Id, self.title, self.Description, self.leader])

    def leader_projects(self, user):
        if not projects.exists():
            raise FileNotFoundError("Project file not found.")
        projects = [f"(Id: {item[0]}, Title: {item[1]}, Description: {item[2]}, members: {"no body" if len(item) != 5 else item[4]})"
                    for item in user.get_leader_projects() if item[0] != "Name"]
        if not projects:
            raise ValueError("You have not created any projects yet")
        return projects

    def user_projects(self, user):
        if not projects.exists():
            raise FileNotFoundError("Project file not found.")
        projects = [f"(Id: {item[0]}, Title: {item[1]}, Description: {item[2]})"
                    for item in user.get_user_projects() if item[0] != "Id"]
        if not projects:
            raise ValueError("You are not a member of any projects.")
        return projects

    def find(self, id):
        projects = projects_file.read()
        for info in enumerate(projects):
            if id == info[1][0]:
                return info

    def input_members_func(self, input_username):
        return [name for name in input_username.split(",")]

    def add_member_func(self, input_username, id):
        input_members = self.input_members_func(input_username)

        reader = users_file.read()
        valid_members = [info[1] for info in reader]

        add_member = [
            username for username in input_members if username in valid_members]

        projects = projects_file.read()
        project_index, project = self.find(id)

        current_members = []
        if len(project) > 4:
            current_members = [member for member in project[4].split(",")]

        new_members = [
            username for username in add_member if username not in current_members]

        all_members = current_members + new_members

        if len(project) == 4:
            project.append(",".join(all_members))

        else:
            project[4] = ",".join(all_members)

        projects[project_index] = project
        projects_file.update(projects)

    def delete_member_func(self, input_username, id):
        input_members = self.input_members_func(input_username)

        projects = projects_file.read()
        project_index, project = self.find(id)

        current_members = []
        if len(project) > 4:
            current_members = [member for member in project[4].split(",")]

        delete_members = [
            member for member in input_members if member in current_members]

        new_current_members = [
            member for member in current_members if member not in delete_members]
        project[4] = ",".join(new_current_members)
        projects[project_index] = project
        projects_file.update(projects)

    def delete_project(self, id):
        reader = projects_file.read()
        for project in reader:
            if str(project[0]) == id:
                reader.remove(project)
        projects_file.update(reader)

    def add_duties(self, duty):
        self.duties.append(duty)


class Priority(Enum):

    LOW = 1

    MEDIUM = 2

    HIGH = 3

    CRITICAL = 4


class Status(Enum):

    BACKLOG = 1

    TODO = 2

    DOING = 3

    DONE = 4

    ARCHIVED = 5


class Duty:
    def __init__(self, proj_id=None, members=None, title="no title", description="no data", priority=1,
                 history=[], status=1, start=str(datetime.datetime.now()), end=datetime.datetime.now() + datetime.timedelta(hours=24),
                 comments=[],  ID=uuid.uuid4()):
        self.Id = ID
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

    def save(self):
        duty_file.append(
            [self.proj_id, self.Id, self.members, self.title, self.description, self.priority, self.status, self.start, self.end, self.comments, self.history])
