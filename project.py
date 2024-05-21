import random
from menu import *
from pathlib import Path
from user import users_file, project_file ,duty_file

project = Path("info/project.csv")
username = ""


class Project:
    def __init__(self):
        self.duties = []
        self.add_member = []
        self.delete_member = []
        self.delete_project = False

    def create(self,id,title,description,leader,members):
        self.Id = id
        try:
            self.check_id_unique()
        except Exception as ex:
            print(ex)
        else:
            self.title = title
            self.Description = description
            self.leader = leader
            self.members = members
            self.write_to_file()

    def check_id_unique(self):
        try:
            reader = project_file.read()
            for info in reader:
                if info[1] == self.Id:
                    raise Exception("The selected ID is not unique")
        except FileNotFoundError:
            pass

    def project_menu(self, user):
        menu = Menu(["Choose one of the following: ", "Create project", "View created projects(leader)",
                     "View created projects(user)", "Back"])
        menu.display()
        if menu.selected_option == "Create project":
            self.creat()
        elif menu.selected_option == "View created projects(leader)":
            project = self.leader_projects(user)
            self.change_leader_projects(project)
        elif menu.selected_option == "View created projects(user)":
            project = self.user_projects(user)

    def write_to_file(self):
        if not project.exists():
            project_file.write(
                [ "Id", "Title", "Description", "Leader" ,"Members"])
        project_file.append(
            [self.Id, self.title, self.Description, self.leader ,self.members])

    def leader_projects(self, user):
        if not project.exists():
            raise Exception("You have not created any projects yet")
        projects = [f"{item[0]} (Id: {item[1]}, Title: {item[2]}, Description: {item[3]})"
                    for item in user.get_leader_projects() if item[0] != "Name"]
        if not projects:
            raise Exception("You have not created any projects yet")
        menu = Menu(["projects:", *projects])
        menu.display()
        return menu.selected_option

    def user_projects(self, user):
        if not project.exists():
            raise Exception("You have not created any projects yet")
        projects = [item[0]
                    for item in user.get_user_projects() if item[0] != "Name"]
        if not projects:
            raise Exception("You have not created any projects yet")
        menu = Menu(["projects:", *projects])
        menu.display()
        return menu.selected_option

    def leader_projects_menu(self):
        menu = Menu(["what do you want to do?", "Add member", "Delete member",
                     "Delete project", "Back"])
        menu.display()
        console.clear()
        reader = users_file.read()
        if menu.selected_option == "Add member":
            members_username = input(
                "Enter the username of members that you want to add to the project: ").split()
            for username in members_username:
                for info in reader:
                    if info[1] == username:
                        self.add_member.append(username)
                        break
        elif menu.selected_option == "Delete member":
            members_username = input(
                "Enter the username of members that you want to delete from the project: ").split()
            for username in members_username:
                for info in reader:
                    if info[1] == username:
                        self.delete_member.append(username)
                        break
        elif menu.selected_option == "Delete project":
            self.delete = True

    def change_leader_projects(self, choice):
        reader = project_file.read()
        console.clear()
        self.leader_projects_menu()
        counter = 1
        for info in enumerate(reader):
            if choice[choice.find(":") + 2: choice.find(",")] == info[1][1] and self.add_member:
                for username in self.add_member:
                    if username not in [username for username in info[1][4:]]:
                        info[1].append(username)
                        reader[0].append(f"Member{counter}")
                        counter += 1
                index, new_info = info
                reader[index] = [*new_info]
            elif choice[choice.find(":") + 2: choice.find(",")] == info[1][1] and self.delete_member:
                for username in self.delete_member:
                    if username in info[1][5:]:
                        info[1].remove(username)
                index, new_info = info
                reader[index] = [*new_info]
            elif choice[choice.find(":") + 2: choice.find(",")] == info[1][1] and self.delete:
                reader.remove(info[1])
            project_file.update(reader)

    def add_duties(self, duty):
        self.duties.append(duty)


class Duty:
    def __init__(self,proj_id=None , members=None, title=None, description=None, priority=None,
                 history=[] ,status=None, start=None, end=None, comments=[],  ID=random.randint(1,7000)):
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
        # duty_file.write(
        #     ["Proj_Id" , "ID", "Members","Title", "Description", "Priority" ,"Status" , "Start" , "End" , "Comments" , "History"])
        duty_file.append(
            [self.proj_id,self.Id,self.members, self.title, self.description, self.priority ,self.status , self.start , self.end , self.comments , self.history])
        
        # def add_history(username, n):
        #     if n == 1:
        #         comments.append((username, "changed the status"))
        #     if n == 2:
        #         comments.append((username, "changed the priority"))
        #     if n == 3:
        #         comments.append((username, "changed the start"))
        #     if n == 4:
        #         comments.append((username, "changed the end"))

        # def change_status(a, username):
        #     a = input("new status : ")
        #     status = a
        #     add_history(username, 1)

        # def change_priority(a, username):
        #     a = input("new priority : ")
        #     priority = a
        #     add_history(username, 2)

        # def change_start(a, username):
        #     a = input("new start : ")
        #     start = a
        #     add_history(username, 3)

        # def change_end(a, username):
        #     a = input("new start : ")
        #     start = a
        #     add_history(username, 4)

        # def add_comment(a, username):
        #     a = input("new comment : ")
        #     comments.append((username, a))
