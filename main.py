import pandas as pd
import random
import project
import csv
import os
from menu import *
from user import *
from kivy.app import App
import datetime
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
import logging
from kivy.config import Config




logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO)



class SayHello(App):
    def build(self):
        #returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

  

        # label widget
        self.greeting = Label(
                        text= f"""Hi,sign in please!
                                  If you already have an account login, please!""",
                        font_size= 18,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.greeting)
        # button widget
        self.button_sign = Button(
                      text= "Sign in",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.button_log = Button(
                      text= "Log in",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.button_log.bind(on_press=self.log_in)
        self.button_sign.bind(on_press=self.sign_in)
        self.window.add_widget(self.button_log)
        self.window.add_widget(self.button_sign)

        return self.window
    
    def sign_in(self, instance):
        # change label text to "Hello + user name!"
        self.window.clear_widgets()  # Clear sign-in window
        

    # Project name input
        self.user_name = TextInput(hint_text="UserName")
        self.window.add_widget(self.user_name)

    # Project description input
        self.user_password = TextInput(hint_text="Password", multiline=True)
        self.window.add_widget(self.user_password)
        
        self.user_email = TextInput(hint_text="Email", multiline=True)
        self.window.add_widget(self.user_email)

        
        self.submit = Button(text= "submit",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        
        self.window.add_widget(self.submit)
        self.submit.bind(on_press=self.sign_in_button_fun)
        
    def sign_in_button_fun(self,instance):
        user = User()
        if user.sign_up(email=self.user_email.text , password=self.user_password.text , username=self.user_name.text) == 0:
            self.project_page(self.user_name.text)
            logging.info(f"""signed in""")
        if user.sign_up(email=self.user_email.text , password=self.user_password.text , username=self.user_name.text) == 1:
            self.window.add_widget(Label(text=Invalid_email))
        if user.sign_up(email=self.user_email.text , password=self.user_password.text , username=self.user_name.text) == 2:
            self.window.add_widget(Label(text=invalid_username))
        if user.sign_up(email=self.user_email.text , password=self.user_password.text , username=self.user_name.text) == 3:
            self.window.add_widget(Label(text=invalid_password))
        if user.sign_up(email=self.user_email.text , password=self.user_password.text , username=self.user_name.text) == 4:
            self.window.add_widget(Label(text="this email is already in use"))
        if user.sign_up(email=self.user_email.text , password=self.user_password.text , username=self.user_name.text) == 5:
            self.window.add_widget(Label(text="this username is already in use"))
        
    def log_in(self, instance):
        self.window.clear_widgets()  # Clear sign-in window
        

    # Project name input
        self.user_name = TextInput(hint_text="UserName")
        self.window.add_widget(self.user_name)

    # Project description input
        self.user_password = TextInput(hint_text="Password", multiline=True)
        self.window.add_widget(self.user_password)
        self.submit = Button(text= "submit",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        
        self.window.add_widget(self.submit)
        self.submit.bind(on_press=self.log_in_button_fun)
        
    def log_in_button_fun(self,instance):
        user = User()
        if user.log_in(username=self.user_name.text , password=self.user_password.text) == 0:
            self.project_page(self.user_name.text)
            logging.info(f"""logged in""")
        elif user.log_in(username=self.user_name.text , password=self.user_password.text) == 1:
            self.window.add_widget(Label(text="your account is deactive"))
        elif user.log_in(username=self.user_name.text , password=self.user_password.text) == 2:
            self.window.add_widget(Label(text="username or password is wrong"))
    def project_page(self , user_name):
        self.window.clear_widgets()
        self.greeting = Label(
                        text= f"""Hi,{user_name}""",
                        font_size= 18,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.greeting)
        self.make_proj_button = Button(text= "make a project",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        self.see_proj_button = Button(text= "see projects",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        self.edit_proj_button = Button(text= "edit projects",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        
        self.window.add_widget(self.make_proj_button)
        self.window.add_widget(self.see_proj_button)
        self.window.add_widget(self.edit_proj_button)
        self.make_proj_button.bind(on_press=self.make_proj_fun_link)
        self.see_proj_button.bind(on_press=self.see_proj_fun_link)
        self.edit_proj_button.bind(on_press=self.edit_proj_fun_link)
        self.back = Button(
                      text= "back",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.back.bind(on_press=self.back_fun2)
        
        self.window.add_widget(self.back)
        
    def back_fun2(self,instance):
        self.log_in("salam")
    def edit_proj_fun_link(self,instance):
        self.window.clear_widgets()
        reader = project_file.read()
        for Id , title , des , leader , member in reader:
            if leader == self.user_name.text:
                self.show = Label(
                        text= f"""{Id , title , des ,member}""",
                        font_size= 18,
                        color= '#00FFCE'
                        )
                self.window.add_widget(self.show)
        self.proj_id_conf = TextInput(hint_text="ID")
        self.window.add_widget(self.proj_id_conf)
        self.edit_members = Button(text= "edit members",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        self.delete_project = Button(text= "delete",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        
        
        self.window.add_widget(self.edit_members)
        self.window.add_widget(self.delete_project)
        self.edit_members.bind(on_press=self.edit_members_fun)
        self.delete_project.bind(on_press=self.delete_project_fun)
        self.back = Button(
                      text= "back",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.back.bind(on_press=self.back_fun3)
        
        self.window.add_widget(self.back)
        
    def back_fun3(self,instance):
        self.project_page(self.user_name.text)
    def delete_project_fun(self,instance):
        reader = project_file.read()
        l = []
        for row in reader:
            if str(row[0]) != self.proj_id_conf.text:
                l.append(row)
        with open("info/project.csv","w",newline="") as f:
            Writer=csv.writer(f)
            Writer.writerows(l)
        logging.info(f"""deleted project""")
        self.edit_proj_fun_link("salam")
    def edit_members_fun(self,instance):
        self.new_member = TextInput(hint_text="new members")
        self.window.add_widget(self.new_member)
        self.new_members_button = Button(text= "submit",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        
        
        self.window.add_widget(self.new_members_button)
        self.new_members_button.bind(on_press=self.new_members_fun)
    def new_members_fun(self,instance):
        reader = project_file.read()
        l = []
        for row in reader:
            if str(row[0]) == self.proj_id_conf.text:
                save_list = list(row)
            if str(row[0]) != self.proj_id_conf.text:
                l.append(row)
        with open("info/project.csv","w",newline="") as f:
            Writer=csv.writer(f)
            Writer.writerows(l)
        prj = project.Project()
        prj.create(id=save_list[0] , title=save_list[1],description=save_list[2],leader=save_list[3], members=self.new_member.text)
        self.edit_proj_fun_link("salam")
        logging.info(f"""edited project members""")
    def see_proj_fun_link(self,instance):
        self.see_proj_fun(self.user_name)
    def see_proj_fun(self,user_name):
        self.window.clear_widgets()
        self.see_leader_button = Button(text= "Leader",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        self.window.add_widget(self.see_leader_button)
        self.see_member_button = Button(text= "member",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        
        
        self.window.add_widget(self.see_member_button)
        self.see_leader_button.bind(on_press=self.see_leader_fun_link)
        self.see_member_button.bind(on_press=self.see_member_fun_link)
        self.back = Button(
                      text= "back",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.back.bind(on_press=self.back_fun3)
        
        self.window.add_widget(self.back)
        
    def back_fun3(self,instance):
        self.project_page(self.user_name.text)
    def see_leader_fun_link(self,instance):
        self.see_leader_fun(self.user_name.text)
    def see_leader_fun(self,user_name):
        self.window.clear_widgets()
        self.window.cols = 1
        reader = project_file.read()
        for Id , title , des , leader , member in reader:
            if leader == user_name:
                self.show = Label(
                        text= f"""{Id , title , des }""",
                        font_size= 18,
                        color= '#00FFCE'
                        )
                self.window.add_widget(self.show)
        self.proj_id_conf = TextInput(hint_text="ID")
        self.window.add_widget(self.proj_id_conf)
        self.submit = Button(text= "submit",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        
        
        self.window.add_widget(self.submit)
        self.submit.bind(on_press=self.duty_page_link)
        self.back = Button(
                      text= "back",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.back.bind(on_press=self.back_fun8)
        
        self.window.add_widget(self.back)
        
    def back_fun8(self,instance):
        self.see_proj_fun("salam")
    def duty_page_link(self , instance):
        self.duty_page(self.proj_id_conf.text)
    def duty_page(self,proj_id):
        self.window.clear_widgets()
        self.window.cols = 10
        # root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        # self.window.add_widget(root)
        self.duty_name = TextInput(text=" no name")
        self.duty_des = TextInput(text="no data")
        self.duty_start = TextInput(text=f"""{datetime.datetime.now()}""")
        self.duty_end = TextInput(text=f"""{datetime.datetime.now() + datetime.timedelta(hours=24)}""")
        self.duty_members = TextInput(text="")
        self.duty_priority = TextInput(text="1")
        self.duty_status = TextInput(text="1")
        self.window.add_widget(self.duty_name)
        self.window.add_widget(self.duty_des)
        self.window.add_widget(self.duty_start)
        self.window.add_widget(self.duty_end)
        self.window.add_widget(self.duty_members)
        self.window.add_widget(self.duty_priority)
        self.window.add_widget(self.duty_status)
        self.window.add_widget(Label(text=f"""form\n 1 to 4\n low\n medium\n high\n critical\n""",font_size=12))
        self.window.add_widget(Label(text=f"""from\n 1 to 5\n \nbacklog \ntodo \nready \ndone \narchived""",font_size=12))

        self.make_duty_button = Button(text= "make",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        
        
        self.window.add_widget(self.make_duty_button)
        self.make_duty_button.bind(on_press=self.make_duty_link)
        df = pd.read_csv("info/duty.csv")
        df.sort_values(by=['Priority'] , inplace=True)
        print(df['Proj_Id'])
        self.window.add_widget(Label(text=f"""BackLog"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))

        for i,proj in zip(list(df.index),list(df['Proj_Id'])):
            print(proj , self.proj_id_conf.text)
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 1: 
                    self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))
                    
        self.window.add_widget(Label(text=f"""TODO"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))

        for i,proj in zip(list(df.index),list(df['Proj_Id'])):
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 2: 
                    self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))


                
        self.window.add_widget(Label(text=f"""DOING"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))


        for i,proj in zip(list(df.index),list(df['Proj_Id'])):
            
                if int(self.proj_id_conf.text) == int(proj):
                    if int(df["Status"][i]) == 3: 
                        self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                        self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                        self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                        self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                        self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                        self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                        self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                        self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                        self.window.add_widget(self.edit_duty_name)
                        self.window.add_widget(self.edit_duty_id)
                        self.window.add_widget(self.edit_duty_des)
                        self.window.add_widget(self.edit_duty_start)
                        self.window.add_widget(self.edit_duty_end)
                        self.window.add_widget(self.edit_duty_members)
                        self.window.add_widget(self.edit_duty_priority)
                        self.window.add_widget(self.edit_duty_status)
                        self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                        self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))


                    
        self.window.add_widget(Label(text=f"""DONE"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))


        for i,proj in zip(list(df.index),list(df['Proj_Id'])):
            
                if int(self.proj_id_conf.text) == int(proj):
                    if int(df["Status"][i]) == 4: 
                        self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                        self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                        self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                        self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                        self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                        self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                        self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                        self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                        self.window.add_widget(self.edit_duty_name)
                        self.window.add_widget(self.edit_duty_id)
                        self.window.add_widget(self.edit_duty_des)
                        self.window.add_widget(self.edit_duty_start)
                        self.window.add_widget(self.edit_duty_end)
                        self.window.add_widget(self.edit_duty_members)
                        self.window.add_widget(self.edit_duty_priority)
                        self.window.add_widget(self.edit_duty_status)
                        self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                        self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))


        self.window.add_widget(Label(text=f"""Archived"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))


        for i,proj in zip(list(df.index),list(df['Proj_Id'])):
                if int(self.proj_id_conf.text) == int(proj):
                    if int(df["Status"][i]) == 5: 
                        self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                        self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                        self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                        self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                        self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                        self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                        self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                        self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                        self.window.add_widget(self.edit_duty_name)
                        self.window.add_widget(self.edit_duty_id)
                        self.window.add_widget(self.edit_duty_des)
                        self.window.add_widget(self.edit_duty_start)
                        self.window.add_widget(self.edit_duty_end)
                        self.window.add_widget(self.edit_duty_members)
                        self.window.add_widget(self.edit_duty_priority)
                        self.window.add_widget(self.edit_duty_status)
                        self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                        self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))
                        

        self.back = Button(
                      text= "back",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.back.bind(on_press=self.back_fun6)
        
        
        self.edit_duty_id_getter = TextInput(hint_text="ID")
        self.edit_duty_button = Button(text= "edit",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        self.window.add_widget(self.edit_duty_id_getter)
        self.window.add_widget(self.edit_duty_button)
        self.edit_duty_button.bind(on_press=self.edit_duty)
        self.window.add_widget(self.back)    
    def back_fun4(self,instance):
        self.see_leader_fun(self.user_name.text)
    def comment_fun(self,instance):
        self.window.clear_widgets()
        self.window.cols = 1
        reader = duty_file.read()
        for row in reader:
            if str(row[1]) == self.edit_duty_id_getter.text:
                s = ""
                com_txt = eval(row[9])
                for i in com_txt:
                    s += i + "\n"
                self.comments_text = Label(
                        text=s ,
                        font_size= 18,
                        color= '#00FFCE'
                        )
                self.window.add_widget(self.comments_text)
        self.new_comm = TextInput(hint_text="new comment")
        self.window.add_widget(self.new_comm)
        
        
        self.new_comm_button = Button(text= "new",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        self.window.add_widget(self.new_comm_button)
        self.new_comm_button.bind(on_press=self.new_comm_fun)
        self.back = Button(
                      text= "back",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.back.bind(on_press=self.back_fun5)
        
        self.window.add_widget(self.back)
        
    def back_fun5(self,instance):
        self.duty_page("salam")
    def new_comm_fun(self,instance):
        reader = duty_file.read()
        for row in reader:
            if str(row[1]) == self.edit_duty_id_getter.text:
                comm_list = eval(row[9])
                comm_list.append(str(datetime.datetime.now()) + "  " + self.user_name.text + " : " + self.new_comm.text)
                history_list = eval(row[10])
        l = []
        for row in reader:
            if row[1] != self.edit_duty_id_getter.text:
                l.append(row)
        with open("info/duty.csv","w",newline="") as f:
            Writer=csv.writer(f)
            Writer.writerows(l) 
        duty = project.Duty(proj_id=self.proj_id_conf.text,title=self.edit_duty_name.text,description=self.edit_duty_des.text ,priority=self.edit_duty_priority.text,
                            status=self.edit_duty_status.text,start=self.edit_duty_start.text,end=self.edit_duty_end.text,members=self.edit_duty_members.text , ID=self.edit_duty_id.text
                            , history=history_list , comments=comm_list)
        duty.save()
        logging.info(f"""added new comment""")
        self.comment_fun("salam")
    def history_fun(self , instance):
        reader = duty_file.read()
        hist = []
        for row in reader:
            if str(row[1]) == self.edit_duty_id_getter.text:
                hist = eval(row[10])
        s = ""
        for i in hist:
            s += i + "\n"
        popup = Popup(title='Test popup', content=Label(text=s),
              auto_dismiss=True)
        popup.open()
    def edit_duty(self,id_changed):
        self.window.clear_widgets()
        self.window.cols = 1
        reader = duty_file.read()
        df = pd.read_csv("info/duty.csv")
        for i , ID in zip(list(df['ID'].index),list(df['ID'])):
            if ID == self.edit_duty_id_getter.text:
                self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                self.window.add_widget(self.edit_duty_name)
                self.window.add_widget(self.edit_duty_id)
                self.window.add_widget(self.edit_duty_des)
                self.window.add_widget(self.edit_duty_start)
                self.window.add_widget(self.edit_duty_end)
                self.window.add_widget(self.edit_duty_members)
                self.window.add_widget(self.edit_duty_priority)
                self.window.add_widget(self.edit_duty_status)
                self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))
                self.history = Button(text= "history",
                            size_hint= (1,0.5),
                            bold= True,
                            background_color ='#00FFCE')
                                
                                
                self.window.add_widget(self.history)
                self.history.bind(on_press=self.history_fun)
                self.comment = Button(text= "comment",
                            size_hint= (1,0.5),
                            bold= True,
                            background_color ='#00FFCE')
                                
                                
                self.window.add_widget(self.comment)
                self.comment.bind(on_press=self.comment_fun)
                self.duty_edit_second = Button(text= "edit",
                            size_hint= (1,0.5),
                            bold= True,
                            background_color ='#00FFCE')
                self.window.add_widget(self.duty_edit_second)
                self.duty_edit_second.bind(on_press=self.edit_second_fun1)
                self.back = Button(text= "back",
                            size_hint= (1,0.5),
                            bold= True,
                            background_color ='#00FFCE')
                self.window.add_widget(self.back)
                self.back.bind(on_press=self.back_fun10)
    def back_fun10(self,instance):
        self.duty_page('salam')
    def edit_second_fun1(self,instance):
        reader = duty_file.read()
        for row in reader:
            if str(row[1]) == self.edit_duty_id_getter.text:
                history_list = eval(row[10])
                if str(row[5]) != self.edit_duty_priority.text:
                    history_list.append(f"""{self.user_name.text} has updated priority in {datetime.datetime.now()}""")
                if str(row[6]) != self.edit_duty_status.text:
                    history_list.append(f"""{self.user_name.text} has updated status in {datetime.datetime.now()}""")
                history_list.append(f"""{self.user_name.text} has updated duty in {datetime.datetime.now()}""")
        l = []
        for row in reader:
            if row[1] != self.edit_duty_id_getter.text:
                l.append(row)
        with open("info/duty.csv","w",newline="") as f:
            Writer=csv.writer(f)
            Writer.writerows(l) 
        duty = project.Duty(proj_id=self.proj_id_conf.text,title=self.edit_duty_name.text,description=self.edit_duty_des.text ,priority=self.edit_duty_priority.text,
                            status=self.edit_duty_status.text,start=self.edit_duty_start.text,end=self.edit_duty_end.text,members=self.edit_duty_members.text , ID=self.edit_duty_id.text
                            ,history=history_list)
        duty.save()
        logging.info(f"""edited a duty""")
        self.duty_page(self.proj_id_conf)
    def make_duty_link(self,instance):
        self.make_duty(self.proj_id_conf)
    def make_duty(self,proj_id):
        duty = project.Duty(proj_id=proj_id.text,title=self.duty_name.text,description=self.duty_des.text ,priority=self.duty_priority.text,
                            status=self.duty_status.text,start=self.duty_start.text,end=self.duty_end.text,members=self.duty_members.text)
        duty.save()
        logging.info(f"""made a duty""")
        self.duty_page(self.proj_id_conf)
        

    def see_member_fun_link(self,instance):
        self.see_member_fun(self.user_name.text)
    def see_member_fun(self,user_name):
        self.window.clear_widgets()
        self.window.cols = 1
        reader = project_file.read()
        for Id , title , des , leader , member in reader:
            if user_name in member.split(','):
                self.show = Label(
                        text= f"""{Id , title , des }""",
                        font_size= 18,
                        color= '#00FFCE'
                        )
                self.window.add_widget(self.show)
                self.proj_id_conf = TextInput(hint_text="ID")
        self.window.add_widget(self.proj_id_conf)
        self.submit = Button(text= "submit",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        
        
        self.window.add_widget(self.submit)
        self.submit.bind(on_press=self.duty_page_link1)
        self.back = Button(
                      text= "back",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.back.bind(on_press=self.back_fun8)
        
        self.window.add_widget(self.back)
        
    def back_fun8(self,instance):
        self.see_proj_fun(self.user_name.text)
    def duty_page_link1(self , instance):
        self.duty_page1(self.proj_id_conf.text)
    def duty_page1(self,proj_id):
        self.window.clear_widgets()
        self.window.cols = 10
        df = pd.read_csv("info/duty.csv")
        df.sort_values(by=['Priority'] , inplace=True)
        print(df['Proj_Id'])
        self.window.add_widget(Label(text=f"""BackLog"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))

        for i,proj in zip(list(df.index),list(df['Proj_Id'])):
            print(proj , self.proj_id_conf.text)
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 1: 
                    self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))
                    
        self.window.add_widget(Label(text=f"""TODO"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))

        for i,proj in zip(list(df.index),list(df['Proj_Id'])):
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 2: 
                    self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))
                    

                
        self.window.add_widget(Label(text=f"""DOING"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))


        for i,proj in zip(list(df.index),list(df['Proj_Id'])):
            
                if int(self.proj_id_conf.text) == int(proj):
                    if int(df["Status"][i]) == 3: 
                        self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                        self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                        self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                        self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                        self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                        self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                        self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                        self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                        self.window.add_widget(self.edit_duty_name)
                        self.window.add_widget(self.edit_duty_id)
                        self.window.add_widget(self.edit_duty_des)
                        self.window.add_widget(self.edit_duty_start)
                        self.window.add_widget(self.edit_duty_end)
                        self.window.add_widget(self.edit_duty_members)
                        self.window.add_widget(self.edit_duty_priority)
                        self.window.add_widget(self.edit_duty_status)
                        self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                        self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))
                        

                    
        self.window.add_widget(Label(text=f"""DONE"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))


        for i,proj in zip(list(df.index),list(df['Proj_Id'])):
            
                if int(self.proj_id_conf.text) == int(proj):
                    if int(df["Status"][i]) == 4: 
                        self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                        self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                        self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                        self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                        self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                        self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                        self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                        self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                        self.window.add_widget(self.edit_duty_name)
                        self.window.add_widget(self.edit_duty_id)
                        self.window.add_widget(self.edit_duty_des)
                        self.window.add_widget(self.edit_duty_start)
                        self.window.add_widget(self.edit_duty_end)
                        self.window.add_widget(self.edit_duty_members)
                        self.window.add_widget(self.edit_duty_priority)
                        self.window.add_widget(self.edit_duty_status)
                        self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                        self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))
                        

        self.window.add_widget(Label(text=f"""Archived"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))
        self.window.add_widget(Label(text=f"""--------"""))


        for i,proj in zip(list(df.index),list(df['Proj_Id'])):
                if int(self.proj_id_conf.text) == int(proj):
                    if int(df["Status"][i]) == 5: 
                        self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                        self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                        self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                        self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                        self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                        self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                        self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                        self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                        self.window.add_widget(self.edit_duty_name)
                        self.window.add_widget(self.edit_duty_id)
                        self.window.add_widget(self.edit_duty_des)
                        self.window.add_widget(self.edit_duty_start)
                        self.window.add_widget(self.edit_duty_end)
                        self.window.add_widget(self.edit_duty_members)
                        self.window.add_widget(self.edit_duty_priority)
                        self.window.add_widget(self.edit_duty_status)
                        self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                        self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))
                        

        self.back = Button(
                      text= "back",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.back.bind(on_press=self.back_fun6)
        
        
        self.edit_duty_id_getter = TextInput(hint_text="ID")
        self.edit_duty_button = Button(text= "edit",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        self.window.add_widget(self.edit_duty_id_getter)
        self.window.add_widget(self.edit_duty_button)
        self.edit_duty_button.bind(on_press=self.edit_duty1)
        self.window.add_widget(self.back)    
    def back_fun6(self,instance):
        self.see_member_fun(self.user_name.text)
    
    def comment_fun1(self,instance):
        self.window.clear_widgets()
        self.window.cols = 1
        reader = duty_file.read()
        for row in reader:
            if str(row[1]) == self.edit_duty_id_getter.text:
                s = ""
                com_txt = eval(row[9])
                for i in com_txt:
                    s += i + "\n"
                self.comments_text = Label(
                        text=s ,
                        font_size= 18,
                        color= '#00FFCE'
                        )
                self.window.add_widget(self.comments_text)
        
        self.new_comm = TextInput(hint_text="new comment")
        self.window.add_widget(self.new_comm)
        
        
        self.new_comm_button = Button(text= "new",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        self.window.add_widget(self.new_comm_button)
        self.new_comm_button.bind(on_press=self.new_comm_fun2)
        self.back = Button(
                      text= "back",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.back.bind(on_press=self.back_fun7)
        
        self.window.add_widget(self.back)
        
    def back_fun7(self,instance):
        self.duty_page1("salam")
    def new_comm_fun2(self,instance):
        reader = duty_file.read()
        for row in reader:
            if row[1] == self.edit_duty_id.text:
                comm_list = eval(row[9])
                comm_list.append(str(datetime.datetime.now()) + "  " + self.user_name.text + " : " + self.new_comm.text)
                history_list = eval(row[10])
        l = []
        for row in reader:
            if row[1] != self.edit_duty_id.text:
                l.append(row)
        with open("info/duty.csv","w",newline="") as f:
            Writer=csv.writer(f)
            Writer.writerows(l) 
        duty = project.Duty(proj_id=self.proj_id_conf.text,title=self.edit_duty_name.text,description=self.edit_duty_des.text ,priority=self.edit_duty_priority.text,
                            status=self.edit_duty_status.text,start=self.edit_duty_start.text,end=self.edit_duty_end.text,members=self.edit_duty_members.text , ID=self.edit_duty_id.text
                            , history=history_list , comments=comm_list)
        duty.save()
        logging.info(f"""added a comment""")
        self.comment_fun1("salam")
        
    def history_fun1(self,instance):
        reader = duty_file.read()
        hist = []
        for row in reader:
            if str(row[1]) == self.edit_duty_id.text:
                hist = eval(row[10])
        s = ""
        for i in hist:
            s += i + "\n"
        popup = Popup(title='Test popup', content=Label(text=s),
              auto_dismiss=True)
        popup.open()
    def edit_duty_link1(self,instance):
        if self.user_name.text in self.edit_duty_members.text.split(","):
            self.edit_duty1()
        else:
            self.duty_page1(self.proj_id_conf)
    def edit_duty1(self,id_changed):
        self.window.clear_widgets()
        self.window.cols = 1
        reader = duty_file.read()
        df = pd.read_csv("info/duty.csv")
        for i , ID in zip(list(df['ID'].index),list(df['ID'])):
            if ID == self.edit_duty_id_getter.text:
                self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                self.edit_duty_des = TextInput(text=f"""{df['Description'][i]}""")
                self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                self.edit_duty_members = TextInput(text=f"""{df['Members'][i]}""")
                self.edit_duty_priority = TextInput(text=f"""{df['Priority'][i]}""")
                self.edit_duty_status = TextInput(text=f"""{df['Status'][i]}""")
                self.window.add_widget(self.edit_duty_name)
                self.window.add_widget(self.edit_duty_id)
                self.window.add_widget(self.edit_duty_des)
                self.window.add_widget(self.edit_duty_start)
                self.window.add_widget(self.edit_duty_end)
                self.window.add_widget(self.edit_duty_members)
                self.window.add_widget(self.edit_duty_priority)
                self.window.add_widget(self.edit_duty_status)
                self.window.add_widget(Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                self.window.add_widget(Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))
                self.history = Button(text= "history",
                            size_hint= (1,0.5),
                            bold= True,
                            background_color ='#00FFCE')
                                
                                
                self.window.add_widget(self.history)
                self.history.bind(on_press=self.history_fun)
                self.comment = Button(text= "comment",
                            size_hint= (1,0.5),
                            bold= True,
                            background_color ='#00FFCE')
                                
                                
                self.window.add_widget(self.comment)
                
                self.comment.bind(on_press=self.comment_fun1)
                
                self.duty_edit_second = Button(text= "edit",
                            size_hint= (1,0.5),
                            bold= True,
                            background_color ='#00FFCE')
                self.window.add_widget(self.duty_edit_second)
                self.duty_edit_second.bind(on_press=self.edit_second_fun)
                self.back = Button(text= "back",
                            size_hint= (1,0.5),
                            bold= True,
                            background_color ='#00FFCE')
                self.window.add_widget(self.back)
                self.back.bind(on_press=self.back_fun10)
    def back_fun10(self,instance):
        self.duty_page1('salam')
    def edit_second_fun(self,instance):
        if self.user_name.text in self.edit_duty_members.text.split(","):
            reader = duty_file.read()
            for row in reader:
                if str(row[1]) == self.edit_duty_id.text:
                    history_list = eval(row[10])
                    if str(row[5]) != self.edit_duty_priority.text:
                        history_list.append(f"""{self.user_name.text} has updated priority in {datetime.datetime.now()}""")
                    if str(row[6]) != self.edit_duty_status.text:
                        history_list.append(f"""{self.user_name.text} has updated status in {datetime.datetime.now()}""")
                    history_list.append(f"""{self.user_name.text} has updated duty in {datetime.datetime.now()}""")
            l = []
            for row in reader:
                if row[1] != self.edit_duty_id.text:
                    l.append(row)
            with open("info/duty.csv","w",newline="") as f:
                Writer=csv.writer(f)
                Writer.writerows(l) 
            duty = project.Duty(proj_id=self.proj_id_conf.text,title=self.edit_duty_name.text,description=self.edit_duty_des.text ,priority=self.edit_duty_priority.text,
                                status=self.edit_duty_status.text,start=self.edit_duty_start.text,end=self.edit_duty_end.text,members=self.edit_duty_members.text , ID=self.edit_duty_id.text
                                ,history=history_list)
            duty.save()
            logging.info(f"""edited a duty""")
            self.duty_page1(self.proj_id_conf)
        else:
            self.window.add_widget(Label(text="you can not edit this duty\n you are not a member "))
        

    
    def make_proj_fun_link(self,instance):
        self.make_proj_fun(self.user_name.text)
    def make_proj_fun(self,user_name):
         self.window.clear_widgets()
         self.proj_title = TextInput(hint_text="Project Name")
         self.window.add_widget(self.proj_title)

    # Project description input
         self.proj_description = TextInput(hint_text="Description", multiline=True)
         self.window.add_widget(self.proj_description)
        
         self.proj_id = TextInput(hint_text="ID", multiline=True)
         self.window.add_widget(self.proj_id)
         self.proj_members = TextInput(hint_text="Members", multiline=True)
         self.window.add_widget(self.proj_members)

        
         self.submit = Button(text= "submit",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE')
        
         self.window.add_widget(self.submit)
         self.submit.bind(on_press=self.new_proj_button_fun_linker)
         self.back = Button(
                      text= "back",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
         self.back.bind(on_press=self.back_fun3)
        
         self.window.add_widget(self.back)
        
    def back_fun3(self,instance):
        self.project_page(self.user_name.text)
    def new_proj_button_fun_linker(self, instance):
        self.new_proj_button_fun(self.user_name.text)
    def new_proj_button_fun(self,user_name):
        proj = project.Project()
        proj.create(id=self.proj_id.text , title=self.proj_title.text , description=self.proj_description.text , leader=user_name , members=self.proj_members.text)
        logging.info(f"""made a new project""")

if __name__ == "__main__":
    SayHello().run()
