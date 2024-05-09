import random

class Project:
    def __init__(self,name=None,Description=None,Id=None,duties=None):
        self.Id = random.randint(1,1000) 
        self.name = input("Project Name: ")
        self.Description = input("Description: ")
        self.duties = []
    def add_duties(a,b):
        a.duties.append(b)        
class Duty:
    def __init__(self,members=None,title=None,description=None,priority=None,
             status=None,start=None,end=None,comments=None,history=None,id=None):
        self.id = random.randint(1,50) 
        self.members = input("Members: ").split(',')
        self.title = input("Title: ")
        self.description = input("Description: ")
        self.priority = input("Priority: ")
        self.status = input("Status: ")
        self.start = input("Start: ")
        self.end = input("End: ")
        self.comments = []
        self.history = []
        def add_history(username , n):
            if n == 1:
                comments.append((username,"changed the status"))
            if n == 2:
                comments.append((username,"changed the priority"))
            if n == 3:
                comments.append((username,"changed the start"))
            if n == 4:
                comments.append((username,"changed the end"))
        def change_status(a,username):
            a = input("new status : ")
            status = a
            add_history(username,1)
        def change_priority(a ,username):
            a = input("new priority : ")
            priority = a
            add_history(username,2)
        def change_start(a , username):
            a = input("new start : ")
            start = a
            add_history(username,3)    
        def change_end(a , username):
            a = input("new start : ")
            start = a
            add_history(username,4)    
        def add_comment(a ,username):
            a = input("new comment : ")
            comments.append((username , a))