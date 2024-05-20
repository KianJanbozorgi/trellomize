import pandas as pd
import random
import project
from menu import *
from user import *
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

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
    # def build2(self):
    #     layout = BoxLayout(orientation='vertical')

    # # Project name input
    #     self.project_name_input = TextInput(hint_text="Project Name")
    #     layout.add_widget(self.project_name_input)

    # # Project description input
    #     self.project_description_input = TextInput(hint_text="Project Description", multiline=True)
    #     layout.add_widget(self.project_description_input)

    #     self.greeting = Label(
    #                     text= f"""It worked""",
    #                     font_size= 18,
    #                     color= '#00FFCE'
    #                     )
    #     layout.add_widget(self.greeting)
    # # Add project button
    #     # self.add_project_button = Button(text="Add Project")
    #     # self.add_project_button.bind(on_press=self.add_project)
    #     # layout.add_widget(self.add_project_button)

    # # (Optional) Project list display

    #     return layout
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
        return self.window
    def sign_in_button_fun(self,instance):
        user = User()
        if user.sign_up(email=self.user_email.text , password=self.user_password.text , username=self.user_name.text):
             self.project_page(self.user_name.text)

        
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
        return self.window
    def log_in_button_fun(self,instance):
        user = User()
        if user.log_in(username=self.user_name.text , password=self.user_password.text):
            self.project_page(self.user_name.text)
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
        
        self.window.add_widget(self.make_proj_button)
        self.window.add_widget(self.see_proj_button)
        self.make_proj_button.bind(on_press=self.make_proj_fun_link)
        self.see_proj_button.bind(on_press=self.see_proj_fun_link)
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
        # self.see_member_button.bind(on_press=self.see_member_fun_link)
    def see_leader_fun_link(self,instance):
        self.see_leader_fun(self.user_name.text)
    def see_leader_fun(self,user_name):
        self.window.clear_widgets()
        reader = project_file.read()
        for Id , title , des , leader , member in reader:
            print(title, des, leader, member , user_name)
            if leader == user_name:
                print(leader)
                self.show = Label(
                        text= f"""{Id , title , des }""",
                        font_size= 18,
                        color= '#00FFCE'
                        )
                self.window.add_widget(self.show) 
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
    def new_proj_button_fun_linker(self, instance):
        self.new_proj_button_fun(self.user_name.text)
    def new_proj_button_fun(self,user_name):
        proj = project.Project()
        proj.create(id=self.proj_id.text , title=self.proj_title.text , description=self.proj_description.text , leader=user_name , members=self.proj_members.text)
# run Say Hello App Calss
if __name__ == "__main__":
    SayHello().run()

