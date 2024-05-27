import pandas as pd
import project
import csv
from user import *
from kivy.app import App
import datetime
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
import logging


logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO)


class SayHello(App):
    def build(self) -> Widget:
        """Initialize the main window and set up the first page."""
        # Create instances of User and Project classes
        self.user = User()
        self.proj = project.Project()

        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.first_page("")

        return self.window

    def first_page(self, instance: Widget) -> None:
        """Display the initial page with options to sign up or log in."""
        self.window.clear_widgets()

        # Create Label and Buttons
        self.greeting = Label(
            text="Hi, sign up please!\nIf you already have an account log in, please!", font_size=22, color='#00FFCE')
        self.button_sign = Button(text="Sign up", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.button_log = Button(text="Log in", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')

        # Add widgets to the window
        self.window.add_widget(self.greeting)
        self.window.add_widget(self.button_sign)
        self.window.add_widget(self.button_log)

        # Bind button press events to corresponding methods
        self.button_sign.bind(on_press=self.sign_in)
        self.button_log.bind(on_press=self.log_in)

    def sign_in(self, instance: Widget) -> None:
        """Display the sign-up page."""
        self.window.clear_widgets()

        # Create TextInput fields and Buttons
        self.username = TextInput(hint_text="UserName")
        self.user_password = TextInput(
            hint_text="Password", multiline=True, password=True)
        self.user_email = TextInput(hint_text="Email", multiline=True)
        self.submit = Button(text="Submit", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.back = Button(text="Back", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.invalid_input = Label(font_size=20, color='#FF0000')

        # Add widgets to the window
        self.window.add_widget(self.username)
        self.window.add_widget(self.user_password)
        self.window.add_widget(self.user_email)
        self.window.add_widget(self.submit)
        self.window.add_widget(self.back)
        self.window.add_widget(self.invalid_input)

        # Bind button press events to corresponding methods
        self.submit.bind(on_press=self.sign_in_button_fun)
        self.back.bind(on_press=self.first_page)

    def sign_in_button_fun(self, instance: Widget) -> None:
        """Handle the sign-up form submission."""
        try:
            self.user.sign_up(email=self.user_email.text,
                              password=self.user_password.text, username=self.username.text)
            self.is_manager("")
            logging.info(f"{self.username.text} signed in")
            # Clear any previous error message
            self.invalid_input.text = ""
        except ValueError as ex:
            # Display the error message if sign-up fails
            self.invalid_input.text = str(ex)

    def log_in(self, instance: Widget) -> None:
        """Display the log-in page."""
        self.window.clear_widgets()

        self.username = TextInput(hint_text="UserName")

        # Create TextInput fields and Buttons
        self.user_password = TextInput(
            hint_text="Password", multiline=True, password=True)
        self.submit = Button(text="Submit", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.back = Button(text="Back", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.invalid_input = Label(font_size=20, color='#FF0000')

        # Add widgets to the window
        self.window.add_widget(self.username)
        self.window.add_widget(self.user_password)
        self.window.add_widget(self.submit)
        self.window.add_widget(self.back)
        self.window.add_widget(self.invalid_input)

        # Bind button press events to corresponding methods
        self.submit.bind(on_press=self.log_in_button_fun)
        self.back.bind(on_press=self.first_page)

    def log_in_button_fun(self, instance: Widget) -> None:
        """Handle the log-in form submission."""
        try:
            self.user.log_in(username=self.username.text,
                             password=self.user_password.text)
            self.is_manager("")
            logging.info(f"{self.username.text} logged in")
            # Clear any previous error message
            self.invalid_input.text = ""
        except (ValueError, PermissionError) as ex:
            # Display the error message if log-in fails
            self.invalid_input.text = str(ex)

    def is_manager(self, instance: Widget) -> None:
        """Display options based on whether the user is a manager."""
        self.window.clear_widgets()

        # Display a greeting message
        self.greeting = Label(
            text=f"Hi, {self.username.text}", font_size=22, color='#00FFCE')
        self.window.add_widget(self.greeting)

        # Check if the user is a manager and display appropriate options
        if self.user.is_manager():
            # If user is a manager, display a button to change user access
            self.access_button = Button(text="change user access", font_size=20, size_hint=(
                1, 0.5), bold=True, background_color='#00FFCE')
            self.window.add_widget(self.access_button)
            self.access_button.bind(on_press=self.change_access)

        # Call the project_page method to display project-related options
        self.project_page("")

    def project_page(self, instance: Widget) -> None:
        """Display project-related options."""
        # Create buttons for creating projects, viewing projects, and going back
        self.make_proj_button = Button(text="make a project", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.see_proj_button = Button(text="see projects", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.back = Button(text="back", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')

        # Add buttons to the window
        self.window.add_widget(self.make_proj_button)
        self.window.add_widget(self.see_proj_button)
        self.window.add_widget(self.back)

        # Bind button press events to corresponding methods
        self.make_proj_button.bind(on_press=self.make_proj_fun)
        self.see_proj_button.bind(on_press=self.see_proj_fun)
        self.back.bind(on_press=self.log_in)

    def change_access(self, instance: Widget) -> None:
        """Display access change options."""
        self.window.clear_widgets()

        # Create buttons for activating or deactivating accounts and going back
        self.active_account = Button(text="active", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.deactive_account = Button(text="deactive", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.back = Button(text="Back", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')

        # Add buttons to the window
        self.window.add_widget(self.active_account)
        self.window.add_widget(self.deactive_account)
        self.window.add_widget(self.back)

        # Bind button press events to corresponding methods
        self.active_account.bind(on_press=self.active_accont_page_func)
        self.deactive_account.bind(on_press=self.deactive_accont_page_func)
        self.back.bind(on_press=self.is_manager)

    def active_accont_page_func(self, instance: Widget) -> None:
        """Display the active account page."""
        self.window.clear_widgets()

        # Create TextInput field for member account, Submit button, and Back button
        self.active_member_account = TextInput(hint_text="member")
        self.submit = Button(text="Submit", size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.back = Button(text="Back", size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')

        # Add widgets to the window
        self.window.add_widget(self.active_member_account)
        self.window.add_widget(self.submit)
        self.window.add_widget(self.back)
        self.window.add_widget(self.invalid_input)

        # Bind button press events to corresponding methods
        self.submit.bind(on_press=self.active_account_func)
        self.back.bind(on_press=self.change_access)

    def active_account_func(self, instance: Widget) -> None:
        """Handle account activation."""
        try:
            self.user.active_account(self.active_member_account.text)

            # Clear any previous error message
            self.invalid_input.text = ""
        except ValueError as ex:
            # Display the error message if activation fails
            self.invalid_input.text = str(ex)

    def deactive_accont_page_func(self, instance: Widget) -> None:
        """Display the deactivate account page."""
        self.window.clear_widgets()

        # Create TextInput field for member account, Submit button, and Back button
        self.deactive_member_account = TextInput(hint_text="member")
        self.submit = Button(text="Submit", size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.back = Button(text="Back", size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')

        # Add widgets to the window
        self.window.add_widget(self.deactive_member_account)
        self.window.add_widget(self.submit)
        self.window.add_widget(self.back)
        self.window.add_widget(self.invalid_input)

        # Bind button press events to corresponding methods
        self.submit.bind(on_press=self.deactive_account_func)
        self.back.bind(on_press=self.change_access)

    def deactive_account_func(self, instance: Widget) -> None:
        """Handle account deactivation."""
        try:
            self.user.deactive_account(self.deactive_member_account.text)
            # Clear any previous error messag
            self.invalid_input.text = ""
        except ValueError as ex:
            # Display the error message if deactivation fails
            self.invalid_input.text = str(ex)

    def make_proj_fun(self, instance: Widget) -> None:
        """Display the create project page."""
        self.window.clear_widgets()

        # Create TextInput fields for project title, description, ID, Submit button, and Back button
        self.proj_title = TextInput(hint_text="Project Title")
        self.proj_description = TextInput(
            hint_text="Description", multiline=True)
        self.proj_id = TextInput(hint_text="ID", multiline=True)
        self.submit = Button(text="Submit", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.back = Button(text="back", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.invalid_input = Label(font_size=20, color='#FF0000')

        # Add widgets to the window
        self.window.add_widget(self.proj_title)
        self.window.add_widget(self.proj_description)
        self.window.add_widget(self.proj_id)
        self.window.add_widget(self.submit)
        self.window.add_widget(self.back)
        self.window.add_widget(self.invalid_input)

        # Bind button press events to corresponding methods
        self.submit.bind(on_press=self.make_proj_button_fun)
        self.back.bind(on_press=self.is_manager)

    def make_proj_button_fun(self, instance: Widget) -> None:
        """Handle project creation form submission."""
        try:
            self.proj.create(id=self.proj_id.text, title=self.proj_title.text,
                             description=self.proj_description.text, leader=self.username.text)
            logging.info(f"{self.username.text} made a new project")
            # Clear any previous error message
            self.invalid_input.text = ""

        except ValueError as ex:
            # Display the error message if project creation fails
            self.invalid_input.text = str(ex)

    def see_proj_fun(self, instance: Widget) -> None:
        """Display the list of projects."""
        self.window.clear_widgets()

        # Create buttons for filtering projects by leader or member, and going back
        self.see_leader_button = Button(text="Leader", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.see_member_button = Button(text="Member", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.back = Button(text="back", font_size=20, size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.invalid_input = Label(font_size=20, color='#FF0000')

        # Add widgets to the window
        self.window.add_widget(self.see_leader_button)
        self.window.add_widget(self.see_member_button)
        self.window.add_widget(self.back)
        self.window.add_widget(self.invalid_input)

        # Bind button press events to corresponding methods
        self.see_leader_button.bind(on_press=self.see_leader_fun)
        self.see_member_button.bind(on_press=self.see_member_fun)
        self.back.bind(on_press=self.is_manager)

    def see_leader_fun(self, instance: Widget) -> None:
        """Display projects led by the user and options to manage them."""
        try:
            projects = self.proj.leader_projects(self.user)
            self.window.clear_widgets()
            # Add label for projets info, TextInput field for project ID, Submit button and Back button
            for project in projects:
                self.show = Label(text=project, font_size=20, color='#00FFCE')
                self.window.add_widget(self.show)
            self.proj_id_conf = TextInput(hint_text="ID")
            self.submit = Button(text="submit", font_size=20, size_hint=(
                1, 0.5), bold=True, background_color='#00FFCE')
            self.back = Button(text="back", font_size=20, size_hint=(
                1, 0.5), bold=True, background_color='#00FFCE')

            # Add widgets to the window
            self.window.add_widget(self.proj_id_conf)
            self.window.add_widget(self.submit)
            self.window.add_widget(self.back)

            # Bind button press events to corresponding methods
            self.submit.bind(on_press=self.edit_proj_fun)
            self.back.bind(on_press=self.see_proj_fun)

            # Clear any previous error message
            self.invalid_input.text = ""
        except (FileNotFoundError, ValueError) as ex:
            # Display the error message if an error occurs
            self.invalid_input.text = str(ex)

    def see_member_fun(self, instance: Widget) -> None:
        """Display projects where the user is a member and provide options to manage duties."""
        self.window.cols = 1
        try:
            projects = self.proj.user_projects(self.user)
            self.window.clear_widgets()

            # Display projects where the user is a member
            for project in projects:
                self.show = Label(text=project, font_size=20, color='#00FFCE')
                self.window.add_widget(self.show)

            # Add TextInput field for project ID, Submit button, and Back button
            self.proj_id_conf = TextInput(hint_text="ID")
            self.submit = Button(text="submit", font_size=20, size_hint=(
                1, 0.5), bold=True, background_color='#00FFCE')
            self.back = Button(text="back", font_size=20, size_hint=(
                1, 0.5), bold=True, background_color='#00FFCE')

            # Add widgets to the window
            self.window.add_widget(self.proj_id_conf)
            self.window.add_widget(self.submit)
            self.window.add_widget(self.back)

            # Bind button press events to corresponding methods
            self.submit.bind(on_press=self.duty_page_link1)
            self.back.bind(on_press=self.see_proj_fun)

            # Clear any previous error message
            self.invalid_input.text = ""
        except (FileNotFoundError, ValueError) as ex:
            # Display the error message if an error occurs
            self.invalid_input.text = str(ex)

    def edit_proj_fun(self, instance: Widget) -> None:
        """Display options to edit a project."""
        self.window.cols = 1
        try:
            self.window.clear_widgets()

            # Create buttons for managing tasks, editing members, deleting project, and going back
            self.tasks = Button(text="Tasks", size_hint=(
                1, 0.5), bold=True, background_color='#00FFCE', font_size=20)
            self.edit_members = Button(text="edit members", size_hint=(
                1, 0.5), bold=True, background_color='#00FFCE', font_size=20)
            self.delete_project = Button(text="delete", size_hint=(
                1, 0.5), bold=True, background_color='#00FFCE', font_size=20)
            self.back = Button(text="back", size_hint=(
                1, 0.5), bold=True, background_color='#00FFCE', font_size=20)

            # Add buttons to the window
            self.window.add_widget(self.tasks)
            self.window.add_widget(self.edit_members)
            self.window.add_widget(self.delete_project)
            self.window.add_widget(self.back)

            # Bind button press events to corresponding methods
            self.tasks.bind(on_press=self.duty_page)
            self.edit_members.bind(on_press=self.edit_members_fun)
            self.delete_project.bind(on_press=self.delete_project_fun)
            self.back.bind(on_press=self.see_leader_fun)

            # Clear any previous error message
            self.invalid_input.text = ""
        except ValueError as ex:
            # Display the error message if an error occurs
            self.invalid_input.text = str(ex)

    def delete_project_fun(self, instance: Widget) -> None:
        """Delete a project."""
        self.proj.delete_project(self.proj_id_conf.text)
        logging.info(f"""deleted project""")
        self.see_proj_fun("")

    def edit_members_fun(self, instance: Widget) -> None:
        """Display options to add or delete project members."""
        self.window.clear_widgets()

        # Create buttons for adding member, deleting member, and going back
        self.add_member_button = Button(text="Add member", size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.delete_member_button = Button(text="Delete member", size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.edit_member_back_button = Button(text="Back", size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.invalid_input = Label(font_size=20, color='#FF0000')

        # Add buttons to the window
        self.window.add_widget(self.add_member_button)
        self.window.add_widget(self.delete_member_button)
        self.window.add_widget(self.edit_member_back_button)
        self.window.add_widget(self.invalid_input)

        # Bind button press events to corresponding methods
        self.add_member_button.bind(on_press=self.add_member_func)
        self.delete_member_button.bind(on_press=self.delete_member_func)
        self.edit_member_back_button.bind(on_press=self.edit_proj_fun)

    def add_member_func(self, instance: Widget) -> None:
        """Display form to add new members."""
        try:
            self.window.clear_widgets()

            # Create TextInput field for adding members, Submit button, and Back button
            self.add_member = TextInput(hint_text="members")
            self.add_member_submit_button = Button(text="Submit", size_hint=(
                1, 0.5), bold=True, background_color='#00FFCE')
            self.add_member_back_button = Button(text="Back", size_hint=(
                1, 0.5), bold=True, background_color='#00FFCE')

            # Add buttons to the window
            self.window.add_widget(self.add_member)
            self.window.add_widget(self.add_member_submit_button)
            self.window.add_widget(self.add_member_back_button)

            # Bind button press events to corresponding methods
            self.add_member_submit_button.bind(on_press=self.add_members_func)
            self.add_member_back_button.bind(on_press=self.edit_members_fun)

            # Clear any previous error message
            self.invalid_input.text = ""

        except ValueError as ex:
            # Display the error message if an error occurs
            self.invalid_input.text = str(ex)

    def add_members_func(self, instance: Widget) -> None:
        """Add new members to the project."""
        self.proj.add_member_func(self.add_member.text, self.proj_id_conf.text)
        self.edit_proj_fun("")
        logging.info(f"""{self.username.text} edited project members""")

    def delete_member_func(self, instance: Widget) -> None:
        """Display form to delete members."""
        try:
            self.window.clear_widgets()

            # Create TextInput field for deleting members, Submit button, and Back button
            self.delete_member = TextInput(hint_text="members")
            self.delete_member_submit_button = Button(
                text="Submit", size_hint=(1, 0.5), bold=True, background_color='#00FFCE')
            self.delete_member_back_button = Button(
                text="Back", size_hint=(1, 0.5), bold=True, background_color='#00FFCE')

            # Add widgets to the window
            self.window.add_widget(self.delete_member)
            self.window.add_widget(self.delete_member_submit_button)
            self.window.add_widget(self.delete_member_back_button)

            # Bind button press events to corresponding methods
            self.delete_member_submit_button.bind(
                on_press=self.delete_members_func)
            self.delete_member_back_button.bind(on_press=self.edit_members_fun)

            # Clear any previous error message
            self.invalid_input.text = ""
        except ValueError as ex:
            # Display the error message if an error occurs
            self.invalid_input.text = str(ex)

    def delete_members_func(self, instance: Widget) -> None:
        """Delete members from the project."""
        self.proj.delete_member_func(
            self.delete_member.text, self.proj_id_conf.text)
        self.edit_proj_fun("")
        logging.info(f"""{self.username.text} edited project members""")

    def duty_page(self, instance: Widget) -> None:
        """Display duty page with duties categorized by status."""
        self.window.clear_widgets()
        self.window.cols = 10
        self.duty_name = TextInput(text=" no name")
        self.duty_des = TextInput(text="no data")
        self.duty_start = TextInput(text=f"""{datetime.datetime.now()}""")
        self.duty_end = TextInput(
            text=f"""{datetime.datetime.now() + datetime.timedelta(hours=24)}""")
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
        self.window.add_widget(Label(
            text=f"""form\n 1 to 4\n low\n medium\n high\n critical\n""", font_size=12))
        self.window.add_widget(Label(
            text=f"""from\n 1 to 5\n \nbacklog \ntodo \nready \ndone \narchived""", font_size=12))

        self.make_duty_button = Button(text="make",
                                       size_hint=(1, 0.5),
                                       bold=True,
                                       background_color='#00FFCE')

        self.window.add_widget(self.make_duty_button)
        self.make_duty_button.bind(on_press=self.make_duty_link)

        df = pd.read_csv("info/duty.csv")
        df.sort_values(by=['Priority'], inplace=True)
        print(df['Proj_Id'])
        self.window.add_widget(Label(text=f"""BackLog"""))
        for _ in range(9):
            self.window.add_widget(Label(text=f"""--------"""))

        for i, proj in zip(list(df.index), list(df['Proj_Id'])):
            print(proj, self.proj_id_conf.text)
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 1:
                    self.edit_duty_name = TextInput(
                        text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(
                        text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(
                        text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(
                        text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(
                        text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(
                        text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(
                        Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(
                        Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))

        self.window.add_widget(Label(text=f"""TODO"""))
        for _ in range(9):
            self.window.add_widget(Label(text=f"""--------"""))

        for i, proj in zip(list(df.index), list(df['Proj_Id'])):
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 2:
                    self.edit_duty_name = TextInput(
                        text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(
                        text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(
                        text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(
                        text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(
                        text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(
                        text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(
                        Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(
                        Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))

        self.window.add_widget(Label(text=f"""DOING"""))
        for _ in range(9):
            self.window.add_widget(Label(text=f"""--------"""))

        for i, proj in zip(list(df.index), list(df['Proj_Id'])):

            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 3:
                    self.edit_duty_name = TextInput(
                        text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(
                        text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(
                        text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(
                        text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(
                        text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(
                        text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(
                        Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(
                        Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))

        self.window.add_widget(Label(text=f"""DONE"""))
        for _ in range(9):
            self.window.add_widget(Label(text=f"""--------"""))

        for i, proj in zip(list(df.index), list(df['Proj_Id'])):
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 4:
                    self.edit_duty_name = TextInput(
                        text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(
                        text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(
                        text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(
                        text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(
                        text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(
                        text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(
                        Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(
                        Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))

        self.window.add_widget(Label(text=f"""Archived"""))
        for _ in range(9):
            self.window.add_widget(Label(text=f"""--------"""))

        for i, proj in zip(list(df.index), list(df['Proj_Id'])):
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 5:
                    self.edit_duty_name = TextInput(
                        text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(
                        text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(
                        text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(
                        text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(
                        text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(
                        text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(
                        Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(
                        Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))

        self.back = Button(
            text="back",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE',
        )

        self.back.bind(on_press=self.edit_proj_fun)

        self.edit_duty_id_getter = TextInput(hint_text="ID")
        self.edit_duty_button = Button(text="edit",
                                       size_hint=(1, 0.5),
                                       bold=True,
                                       background_color='#00FFCE')
        self.window.add_widget(self.edit_duty_id_getter)
        self.window.add_widget(self.edit_duty_button)
        self.edit_duty_button.bind(on_press=self.edit_duty)
        self.window.add_widget(self.back)

    def comment_fun(self, instance: Widget) -> None:
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
                    text=s,
                    font_size=18,
                    color='#00FFCE'
                )
                self.window.add_widget(self.comments_text)
        self.new_comm = TextInput(hint_text="new comment")
        self.window.add_widget(self.new_comm)

        self.new_comm_button = Button(text="new",
                                      size_hint=(1, 0.5),
                                      bold=True,
                                      background_color='#00FFCE')
        self.window.add_widget(self.new_comm_button)
        self.new_comm_button.bind(on_press=self.new_comm_fun)
        self.back = Button(
            text="back",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE',
        )
        self.back.bind(on_press=self.duty_page)

        self.window.add_widget(self.back)

    def new_comm_fun(self, instance: Widget) -> None:
        reader = duty_file.read()
        for row in reader:
            if str(row[1]) == self.edit_duty_id_getter.text:
                comm_list = eval(row[9])
                comm_list.append(str(datetime.datetime.now()) + "  " +
                                 self.username.text + " : " + self.new_comm.text)
                history_list = eval(row[10])
        l = []
        for row in reader:
            if row[1] != self.edit_duty_id_getter.text:
                l.append(row)
        with open("info/duty.csv", "w", newline="") as f:
            Writer = csv.writer(f)
            Writer.writerows(l)
        duty = project.Duty(proj_id=self.proj_id_conf.text, title=self.edit_duty_name.text, description=self.edit_duty_des.text, priority=self.edit_duty_priority.text,
                            status=self.edit_duty_status.text, start=self.edit_duty_start.text, end=self.edit_duty_end.text, members=self.edit_duty_members.text, ID=self.edit_duty_id.text, history=history_list, comments=comm_list)
        duty.save()
        logging.info(f"""added new comment""")
        self.comment_fun("")

    def history_fun(self, instance: Widget) -> None:
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

    def edit_duty(self, id_changed):
        self.window.clear_widgets()
        self.window.cols = 1
        reader = duty_file.read()
        df = pd.read_csv("info/duty.csv")
        for i, ID in zip(list(df['ID'].index), list(df['ID'])):
            if ID == self.edit_duty_id_getter.text:
                self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                self.edit_duty_des = TextInput(
                    text=f"""{df['Description'][i]}""")
                self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                self.edit_duty_members = TextInput(
                    text=f"""{df['Members'][i]}""")
                self.edit_duty_priority = TextInput(
                    text=f"""{df['Priority'][i]}""")
                self.edit_duty_status = TextInput(
                    text=f"""{df['Status'][i]}""")
                self.window.add_widget(self.edit_duty_name)
                self.window.add_widget(self.edit_duty_id)
                self.window.add_widget(self.edit_duty_des)
                self.window.add_widget(self.edit_duty_start)
                self.window.add_widget(self.edit_duty_end)
                self.window.add_widget(self.edit_duty_members)
                self.window.add_widget(self.edit_duty_priority)
                self.window.add_widget(self.edit_duty_status)
                self.window.add_widget(
                    Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                self.window.add_widget(
                    Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))
                self.history = Button(text="history",
                                      size_hint=(1, 0.5),
                                      bold=True,
                                      background_color='#00FFCE')

                self.window.add_widget(self.history)
                self.history.bind(on_press=self.history_fun)
                self.comment = Button(text="comment",
                                      size_hint=(1, 0.5),
                                      bold=True,
                                      background_color='#00FFCE')

                self.window.add_widget(self.comment)
                self.comment.bind(on_press=self.comment_fun)
                self.duty_edit_second = Button(text="edit",
                                               size_hint=(1, 0.5),
                                               bold=True,
                                               background_color='#00FFCE')
                self.window.add_widget(self.duty_edit_second)
                self.duty_edit_second.bind(on_press=self.edit_second_fun1)
                self.back = Button(text="back",
                                   size_hint=(1, 0.5),
                                   bold=True,
                                   background_color='#00FFCE')
                self.window.add_widget(self.back)
                self.back.bind(on_press=self.duty_page)

    def edit_second_fun1(self, instance: Widget) -> None:
        reader = duty_file.read()
        for row in reader:
            if str(row[1]) == self.edit_duty_id_getter.text:
                history_list = eval(row[10])
                if str(row[5]) != self.edit_duty_priority.text:
                    history_list.append(f"""{self.username.text} has updated priority in {
                                        datetime.datetime.now()}""")
                if str(row[6]) != self.edit_duty_status.text:
                    history_list.append(f"""{self.username.text} has updated status in {
                                        datetime.datetime.now()}""")
                history_list.append(f"""{self.username.text} has updated duty in {
                                    datetime.datetime.now()}""")
        l = []
        for row in reader:
            if row[1] != self.edit_duty_id_getter.text:
                l.append(row)
        with open("info/duty.csv", "w", newline="") as f:
            Writer = csv.writer(f)
            Writer.writerows(l)
        duty = project.Duty(proj_id=self.proj_id_conf.text, title=self.edit_duty_name.text, description=self.edit_duty_des.text, priority=self.edit_duty_priority.text,
                            status=self.edit_duty_status.text, start=self.edit_duty_start.text, end=self.edit_duty_end.text, members=self.edit_duty_members.text, ID=self.edit_duty_id.text, history=history_list)
        duty.save()
        logging.info(f"""edited a duty""")
        self.duty_page(self.proj_id_conf)

    def make_duty_link(self, instance: Widget) -> None:
        self.make_duty(self.proj_id_conf)

    def make_duty(self, proj_id):
        duty = project.Duty(proj_id=proj_id.text, title=self.duty_name.text, description=self.duty_des.text, priority=self.duty_priority.text,
                            status=self.duty_status.text, start=self.duty_start.text, end=self.duty_end.text, members=self.duty_members.text)
        duty.save()
        logging.info(f"""made a duty""")
        self.duty_page(self.proj_id_conf)

    def duty_page_link1(self, instance: Widget) -> None:
        self.duty_page1(self.proj_id_conf.text)

    def duty_page1(self, proj_id):
        self.window.clear_widgets()
        self.window.cols = 10
        df = pd.read_csv("info/duty.csv")
        df.sort_values(by=['Priority'], inplace=True)
        print(df['Proj_Id'])
        self.window.add_widget(Label(text=f"""BackLog"""))
        for _ in range(9):
            self.window.add_widget(Label(text=f"""--------"""))

        for i, proj in zip(list(df.index), list(df['Proj_Id'])):
            print(proj, self.proj_id_conf.text)
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 1:
                    self.edit_duty_name = TextInput(
                        text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(
                        text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(
                        text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(
                        text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(
                        text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(
                        text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(
                        Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(
                        Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))

        self.window.add_widget(Label(text=f"""TODO"""))
        for _ in range(9):
            self.window.add_widget(Label(text=f"""--------"""))

        for i, proj in zip(list(df.index), list(df['Proj_Id'])):
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 2:
                    self.edit_duty_name = TextInput(
                        text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(
                        text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(
                        text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(
                        text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(
                        text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(
                        text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(
                        Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(
                        Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))

        self.window.add_widget(Label(text=f"""DOING"""))
        for _ in range(9):
            self.window.add_widget(Label(text=f"""--------"""))

        for i, proj in zip(list(df.index), list(df['Proj_Id'])):

            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 3:
                    self.edit_duty_name = TextInput(
                        text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(
                        text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(
                        text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(
                        text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(
                        text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(
                        text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(
                        Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(
                        Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))

        self.window.add_widget(Label(text=f"""DONE"""))
        for _ in range(9):
            self.window.add_widget(Label(text=f"""--------"""))

        for i, proj in zip(list(df.index), list(df['Proj_Id'])):
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 4:
                    self.edit_duty_name = TextInput(
                        text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(
                        text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(
                        text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(
                        text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(
                        text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(
                        text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(
                        Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(
                        Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))

        self.window.add_widget(Label(text=f"""Archived"""))
        for _ in range(9):
            self.window.add_widget(Label(text=f"""--------"""))

        for i, proj in zip(list(df.index), list(df['Proj_Id'])):
            if int(self.proj_id_conf.text) == int(proj):
                if int(df["Status"][i]) == 5:
                    self.edit_duty_name = TextInput(
                        text=f"""{df['Title'][i]}""")
                    self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                    self.edit_duty_des = TextInput(
                        text=f"""{df['Description'][i]}""")
                    self.edit_duty_start = TextInput(
                        text=f"""{df['Start'][i]}""")
                    self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                    self.edit_duty_members = TextInput(
                        text=f"""{df['Members'][i]}""")
                    self.edit_duty_priority = TextInput(
                        text=f"""{df['Priority'][i]}""")
                    self.edit_duty_status = TextInput(
                        text=f"""{df['Status'][i]}""")
                    self.window.add_widget(self.edit_duty_name)
                    self.window.add_widget(self.edit_duty_id)
                    self.window.add_widget(self.edit_duty_des)
                    self.window.add_widget(self.edit_duty_start)
                    self.window.add_widget(self.edit_duty_end)
                    self.window.add_widget(self.edit_duty_members)
                    self.window.add_widget(self.edit_duty_priority)
                    self.window.add_widget(self.edit_duty_status)
                    self.window.add_widget(
                        Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                    self.window.add_widget(
                        Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))

        self.back = Button(
            text="back",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE',
        )
        self.back.bind(on_press=self.see_member_fun)

        self.edit_duty_id_getter = TextInput(hint_text="ID")
        self.edit_duty_button = Button(text="edit",
                                       size_hint=(1, 0.5),
                                       bold=True,
                                       background_color='#00FFCE')
        self.window.add_widget(self.edit_duty_id_getter)
        self.window.add_widget(self.edit_duty_button)
        self.edit_duty_button.bind(on_press=self.edit_duty1)
        self.window.add_widget(self.back)

    def comment_fun1(self, instance: Widget) -> None:
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
                    text=s,
                    font_size=18,
                    color='#00FFCE'
                )
                self.window.add_widget(self.comments_text)

        self.new_comm = TextInput(hint_text="new comment")
        self.window.add_widget(self.new_comm)

        self.new_comm_button = Button(text="new",
                                      size_hint=(1, 0.5),
                                      bold=True,
                                      background_color='#00FFCE')
        self.window.add_widget(self.new_comm_button)
        self.new_comm_button.bind(on_press=self.new_comm_fun2)
        self.back = Button(
            text="back",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE',
        )
        self.back.bind(on_press=self.duty_page1)

        self.window.add_widget(self.back)

    def new_comm_fun2(self, instance: Widget) -> None:
        reader = duty_file.read()
        for row in reader:
            if row[1] == self.edit_duty_id.text:
                comm_list = eval(row[9])
                comm_list.append(str(datetime.datetime.now()) + "  " +
                                 self.username.text + " : " + self.new_comm.text)
                history_list = eval(row[10])
        l = []
        for row in reader:
            if row[1] != self.edit_duty_id.text:
                l.append(row)
        with open("info/duty.csv", "w", newline="") as f:
            Writer = csv.writer(f)
            Writer.writerows(l)
        duty = project.Duty(proj_id=self.proj_id_conf.text, title=self.edit_duty_name.text, description=self.edit_duty_des.text, priority=self.edit_duty_priority.text,
                            status=self.edit_duty_status.text, start=self.edit_duty_start.text, end=self.edit_duty_end.text, members=self.edit_duty_members.text, ID=self.edit_duty_id.text, history=history_list, comments=comm_list)
        duty.save()
        logging.info(f"""added a comment""")
        self.comment_fun1("")

    def history_fun1(self, instance: Widget) -> None:
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

    def edit_duty_link1(self, instance: Widget) -> None:
        if self.username.text in self.edit_duty_members.text.split(","):
            self.edit_duty1()
        else:
            self.duty_page1(self.proj_id_conf)

    def edit_duty1(self, id_changed):
        self.window.clear_widgets()
        self.window.cols = 1
        reader = duty_file.read()
        df = pd.read_csv("info/duty.csv")
        for i, ID in zip(list(df['ID'].index), list(df['ID'])):
            if ID == self.edit_duty_id_getter.text:
                self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                self.edit_duty_id = TextInput(text=f"""{df['ID'][i]}""")
                self.edit_duty_des = TextInput(
                    text=f"""{df['Description'][i]}""")
                self.edit_duty_start = TextInput(text=f"""{df['Start'][i]}""")
                self.edit_duty_end = TextInput(text=f"""{df['End'][i]}""")
                self.edit_duty_members = TextInput(
                    text=f"""{df['Members'][i]}""")
                self.edit_duty_priority = TextInput(
                    text=f"""{df['Priority'][i]}""")
                self.edit_duty_status = TextInput(
                    text=f"""{df['Status'][i]}""")
                self.window.add_widget(self.edit_duty_name)
                self.window.add_widget(self.edit_duty_id)
                self.window.add_widget(self.edit_duty_des)
                self.window.add_widget(self.edit_duty_start)
                self.window.add_widget(self.edit_duty_end)
                self.window.add_widget(self.edit_duty_members)
                self.window.add_widget(self.edit_duty_priority)
                self.window.add_widget(self.edit_duty_status)
                self.window.add_widget(
                    Label(text=f"""{project.Priority(int(df['Priority'][i])).name}"""))
                self.window.add_widget(
                    Label(text=f"""{project.Status(int(df['Status'][i])).name}"""))
                self.history = Button(text="history",
                                      size_hint=(1, 0.5),
                                      bold=True,
                                      background_color='#00FFCE')

                self.window.add_widget(self.history)
                self.history.bind(on_press=self.history_fun)
                self.comment = Button(text="comment",
                                      size_hint=(1, 0.5),
                                      bold=True,
                                      background_color='#00FFCE')

                self.window.add_widget(self.comment)

                self.comment.bind(on_press=self.comment_fun1)

                self.duty_edit_second = Button(text="edit",
                                               size_hint=(1, 0.5),
                                               bold=True,
                                               background_color='#00FFCE')
                self.window.add_widget(self.duty_edit_second)
                self.duty_edit_second.bind(on_press=self.edit_second_fun)
                self.back = Button(text="back",
                                   size_hint=(1, 0.5),
                                   bold=True,
                                   background_color='#00FFCE')
                self.window.add_widget(self.back)
                self.back.bind(on_press=self.duty_page1)

    def edit_second_fun(self, instance: Widget) -> None:
        if self.username.text in self.edit_duty_members.text.split(","):
            reader = duty_file.read()
            for row in reader:
                if str(row[1]) == self.edit_duty_id.text:
                    history_list = eval(row[10])
                    if str(row[5]) != self.edit_duty_priority.text:
                        history_list.append(f"""{self.username.text} has updated priority in {
                                            datetime.datetime.now()}""")
                    if str(row[6]) != self.edit_duty_status.text:
                        history_list.append(f"""{self.username.text} has updated status in {
                                            datetime.datetime.now()}""")
                    history_list.append(f"""{self.username.text} has updated duty in {
                                        datetime.datetime.now()}""")
            l = []
            for row in reader:
                if row[1] != self.edit_duty_id.text:
                    l.append(row)
            with open("info/duty.csv", "w", newline="") as f:
                Writer = csv.writer(f)
                Writer.writerows(l)
            duty = project.Duty(proj_id=self.proj_id_conf.text, title=self.edit_duty_name.text, description=self.edit_duty_des.text, priority=self.edit_duty_priority.text,
                                status=self.edit_duty_status.text, start=self.edit_duty_start.text, end=self.edit_duty_end.text, members=self.edit_duty_members.text, ID=self.edit_duty_id.text, history=history_list)
            duty.save()
            logging.info(f"""edited a duty""")
            self.duty_page1(self.proj_id_conf)
        else:
            self.window.add_widget(
                Label(text="you can not edit this duty\n you are not a member "))


if __name__ == "__main__":
    SayHello().run()
