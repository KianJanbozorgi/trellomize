import pandas as pd
from datetime import datetime, timedelta
from loguru import logger
import project
from user import *
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

logger.add("app.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")


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
        self.button_sign.bind(on_press=self.sign_up)
        self.button_log.bind(on_press=self.log_in)

    def sign_up(self, instance: Widget) -> None:
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
        self.submit.bind(on_press=self.sign_up_button_fun)
        self.back.bind(on_press=self.first_page)

    def sign_up_button_fun(self, instance: Widget) -> None:
        """Handle the sign-up form submission."""
        try:
            self.user.sign_up(email=self.user_email.text,
                              password=self.user_password.text, username=self.username.text)
            self.is_manager("")
            logger.info(f"{self.username.text} signed up.")
            # Clear any previous error message
            self.invalid_input.text = ""
        except ValueError as ex:
            # Display the error message if sign-up fails
            self.invalid_input.text = str(ex)
            logger.error(f"Sign up failed for {self.username.text}.")

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
            logger.info(f"{self.username.text} logged in.")
            # Clear any previous error message
            self.invalid_input.text = ""
        except (ValueError, PermissionError) as ex:
            # Display the error message if log-in fails
            self.invalid_input.text = str(ex)
            logger.error(f"log in failed for {self.username.text}.")

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
        self.invalid_input.text = ""
        self.window.add_widget(self.invalid_input)

        # Bind button press events to corresponding methods
        self.submit.bind(on_press=self.active_account_func)
        self.back.bind(on_press=self.change_access)

    def active_account_func(self, instance: Widget) -> None:
        """Handle account activation."""
        try:
            self.user.active_account(self.active_member_account.text)
            logger.info(f"{self.username.text} activated {self.active_member_account.text}'s account.")
            # Clear any previous error message
            self.invalid_input.text = ""
        except ValueError as ex:
            # Display the error message if activation fails
            self.invalid_input.text = str(ex)
            logger.error(f"{self.username.text} could not activate {self.active_member_account.text}'s account.")

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
        self.invalid_input.text = ""
        self.window.add_widget(self.invalid_input)

        # Bind button press events to corresponding methods
        self.submit.bind(on_press=self.deactive_account_func)
        self.back.bind(on_press=self.change_access)

    def deactive_account_func(self, instance: Widget) -> None:
        """Handle account deactivation."""
        self.invalid_input.text = ""
        try:
            self.user.deactive_account(self.deactive_member_account.text)
            logger.info(f"{self.username.text} deactivated {self.deactive_member_account.text}'s account.")
            # Clear any previous error message
            self.invalid_input.text = ""
        except ValueError as ex:
            # Display the error message if deactivation fails
            self.invalid_input.text = str(ex)
            logger.error(f"{self.username.text} could not deactivate {self.deactive_member_account.text}'s account.")

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
            logger.info(f"{self.username.text} made a new project with {self.proj_title.text} title.")
            # Clear any previous error message
            self.invalid_input.text = ""

        except ValueError as ex:
            # Display the error message if project creation fails
            self.invalid_input.text = str(ex)
            logger.error(f"Project creation failed by {self.username.text} because a duplicate ID was selected.")

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
            # Add label for projects info, TextInput field for project ID, Submit button and Back button
            for project in projects:
                self.show = Label(text=project, font_size=20, color='#00FFCE')
                self.window.add_widget(self.show)
            
            self.proj_id_conf = TextInput(hint_text="ID")
            self.submit = Button(text="submit", font_size=20, size_hint=(1, 0.5), bold=True, background_color='#00FFCE')
            self.back = Button(text="back", font_size=20, size_hint=(1, 0.5), bold=True, background_color='#00FFCE')

            # Add widgets to the window
            self.window.add_widget(self.proj_id_conf)
            self.window.add_widget(self.submit)
            self.window.add_widget(self.back)
            self.invalid_input.text = ""
            self.window.add_widget(self.invalid_input)

            # Bind button press events to corresponding methods
            self.submit.bind(on_press=self.on_submit_leader)
            self.back.bind(on_press=self.see_proj_fun)

            logger.info(f"{self.username.text} tried to see the projects in which are a leader.")

        except (FileNotFoundError, ValueError) as ex:
            # Display the error message if an error occurs
            self.invalid_input.text = str(ex)
            logger.error(f"{self.username.text}: {ex}")

    def on_submit_leader(self, instance):
        try:
            self.proj.check_id(self.proj_id_conf.text, self.proj.leader_projects(self.user))
            self.edit_proj_fun("")
        except ValueError as ex:
            self.invalid_input.text = str(ex)
            logger.error(f"{self.username.text}: {ex}")

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
            self.proj_id_conf = TextInput(hint_text="id")
            self.submit = Button(text="submit", font_size=20, size_hint=(1, 0.5), bold=True, background_color='#00FFCE')
            self.back = Button(text="back", font_size=20, size_hint=(1, 0.5), bold=True, background_color='#00FFCE')

            # Add widgets to the window
            self.window.add_widget(self.proj_id_conf)
            self.window.add_widget(self.submit)
            self.window.add_widget(self.back)
            self.invalid_input.text = ""
            self.window.add_widget(self.invalid_input)

            # Bind button press events to corresponding methods
            self.submit.bind(on_press=self.on_submit_member)
            self.back.bind(on_press=self.see_proj_fun)

            logger.info(f"{self.username.text} tried to see the projects in which are a member.")

        except (FileNotFoundError, ValueError) as ex:
            # Display the error message if an error occurs
            self.invalid_input.text = str(ex)
            logger.error(f"{self.username.text}: {ex}")

    def on_submit_member(self, instance):
        try:
            self.proj.check_id(self.proj_id_conf.text, self.proj.user_projects(self.user))
            self.duty_page1("")
        except ValueError as ex:
            self.invalid_input.text = str(ex)
            logger.error(f"{self.username.text}: {ex}")

    def edit_proj_fun(self, instance: Widget) -> None:
        """Display options to edit a project."""
        self.window.cols = 1
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

    def delete_project_fun(self, instance: Widget) -> None:
        """Delete a project."""
        project_title = self.proj.delete_project(self.proj_id_conf.text)
        logger.info(f"""{self.username.text} deleted project with {project_title} title.""")
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
        self.window.clear_widgets()

        # Create TextInput field for adding members, Submit button, and Back button
        self.add_member = TextInput(hint_text="member")
        self.add_member_submit_button = Button(text="Submit", size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')
        self.add_member_back_button = Button(text="Back", size_hint=(
            1, 0.5), bold=True, background_color='#00FFCE')

        # Add buttons to the window
        self.window.add_widget(self.add_member)
        self.window.add_widget(self.add_member_submit_button)
        self.window.add_widget(self.add_member_back_button)
        self.invalid_input.text = ""
        self.window.add_widget(self.invalid_input)

        # Bind button press events to corresponding methods
        self.add_member_submit_button.bind(on_press=self.add_members_func)
        self.add_member_back_button.bind(on_press=self.edit_members_fun)

    def add_members_func(self, instance: Widget) -> None:
        """Add new member to the project."""
        try:
            self.proj.add_member_func(self.add_member.text, self.proj_id_conf.text)
            self.edit_proj_fun("")
            logger.info(f"{self.username.text} added {self.add_member.text} to the project.")
        except ValueError as ex:
            self.invalid_input.text = str(ex)
            logger.error(f"{self.username.text}: {ex}")


    def delete_member_func(self, instance: Widget) -> None:
        """Display form to delete members."""
        try:
            self.window.clear_widgets()

            # Create TextInput field for deleting members, Submit button, and Back button
            self.delete_member = TextInput(hint_text="member")
            self.delete_member_submit_button = Button(
                text="Submit", size_hint=(1, 0.5), bold=True, background_color='#00FFCE')
            self.delete_member_back_button = Button(
                text="Back", size_hint=(1, 0.5), bold=True, background_color='#00FFCE')

            # Add widgets to the window
            self.window.add_widget(self.delete_member)
            self.window.add_widget(self.delete_member_submit_button)
            self.window.add_widget(self.delete_member_back_button)
            self.invalid_input.text = ""
            self.window.add_widget(self.invalid_input)

            # Bind button press events to corresponding methods
            self.delete_member_submit_button.bind(
                on_press=self.delete_members_func)
            self.delete_member_back_button.bind(on_press=self.edit_members_fun)

        except ValueError as ex:
            # Display the error message if an error occurs
            self.invalid_input.text = str(ex)

    def delete_members_func(self, instance: Widget) -> None:
        """Delete members from the project."""
        try:
            self.proj.delete_member_func(
                self.delete_member.text, self.proj_id_conf.text)
            self.edit_proj_fun("")
            logger.info(f"{self.username.text} deleted {self.delete_member.text} from the project.")
        except ValueError as ex:
            self.invalid_input.text = str(ex)
            logger.error(f"{self.username.text}: {ex}")

    def duty_page(self, instance: Widget) -> None:
        """Display duty page with duties categorized by status."""
        self.window.clear_widgets()
        self.window.cols = 10

        self.initialize_widgets()
        self.add_new_duty_form()
        self.display_duties()

        self.back = Button(
            text="back",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE',
        )
        self.back.bind(on_press=self.edit_proj_fun)
        self.edit_duty_id_getter = TextInput(hint_text="ID")
        self.edit_duty_button = Button(
            text="edit",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE'
        )
        self.edit_duty_button.bind(on_press=self.edit_duty)

        self.window.add_widget(self.edit_duty_id_getter)
        self.window.add_widget(self.edit_duty_button)
        self.window.add_widget(self.back)

    def initialize_widgets(self):
        """Initialize widgets for the duty page."""
        self.duty_name = TextInput(hint_text="name")
        self.duty_des = TextInput(hint_text="description")
        self.duty_start = TextInput(text=f"{datetime.now()}")
        self.duty_end = TextInput(
            text=f"{datetime.now() + timedelta(hours=24)}")
        self.duty_members = TextInput(hint_text="members")
        self.duty_priority = TextInput(text="1")
        self.duty_status = TextInput(text="1")
        self.make_duty_button = Button(
            text="make",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE'
        )

    def add_new_duty_form(self):
        """Add form for creating a new duty."""
        self.window.add_widget(self.duty_name)
        self.window.add_widget(self.duty_des)
        self.window.add_widget(self.duty_start)
        self.window.add_widget(self.duty_end)
        self.window.add_widget(self.duty_members)
        self.window.add_widget(self.duty_priority)
        self.window.add_widget(self.duty_status)
        self.window.add_widget(Label(
            text="from\n1 to 4\n low\n medium\n high\n critical\n", font_size=12))
        self.window.add_widget(Label(
            text="from\n1 to 5 \nbacklog \ntodo \ndoing \ndone \narchived", font_size=12))
        self.window.add_widget(self.make_duty_button)
        self.make_duty_button.bind(on_press=self.make_duty)

    def display_duties(self):
        """Display duties categorized by status."""
        df = pd.read_csv("info/duty.csv")
        df.sort_values(by=['Priority'], inplace=True)

        for status in project.Status:
            self.create_header(status.name)
            for i, proj in zip(list(df.index), list(df['Project_id'])):
                if int(self.proj_id_conf.text) == int(proj) and int(df["Status"][i]) == status.value:
                    self.add_duty_widgets(i, df)

    def create_header(self, category: str):
        """Create headers for different duty categories."""
        self.window.add_widget(Label(text=category))
        for _ in range(9):
            self.window.add_widget(Label(text="--------"))

    def add_duty_widgets(self, index: int, df: pd.DataFrame):
        """Add widgets for individual duties."""
        self.edit_duty_name = TextInput(text=f"{df['Title'][index]}")
        self.edit_duty_id = TextInput(text=f"{df['Task_id'][index]}")
        self.edit_duty_des = TextInput(text=f"{df['Description'][index]}")
        self.edit_duty_start = TextInput(text=f"{df['Start'][index]}")
        self.edit_duty_end = TextInput(text=f"{df['End'][index]}")
        self.edit_duty_members = TextInput(text=f"{df['Members'][index]}")
        self.edit_duty_priority = TextInput(text=f"{df['Priority'][index]}")
        self.edit_duty_status = TextInput(text=f"{df['Status'][index]}")

        self.window.add_widget(self.edit_duty_name)
        self.window.add_widget(self.edit_duty_id)
        self.window.add_widget(self.edit_duty_des)
        self.window.add_widget(self.edit_duty_start)
        self.window.add_widget(self.edit_duty_end)
        self.window.add_widget(self.edit_duty_members)
        self.window.add_widget(self.edit_duty_priority)
        self.window.add_widget(self.edit_duty_status)
        self.window.add_widget(
            Label(text=f"{project.Priority(int(df['Priority'][index])).name}"))
        self.window.add_widget(
            Label(text=f"{project.Status(int(df['Status'][index])).name}"))

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
                    font_size=20,
                    color='#00FFCE'
                )
                self.window.add_widget(self.comments_text)
        self.new_comm = TextInput(hint_text="new comment")
        self.window.add_widget(self.new_comm)
        self.new_comm_button = Button(text="submit",
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
        self.window.add_widget(self.back)
        self.back.bind(on_press=self.duty_page)

    def new_comm_fun(self, instance: Widget) -> None:
        """Adds a new comment to a duty and updates its history."""
        reader = duty_file.read()
        comm_list = []
        history_list = []
        for row in reader:
            if str(row[1]) == self.edit_duty_id_getter.text:
                comm_list = eval(row[9])
                comm_list.append(str(datetime.now()) + "  " +
                                 self.username.text + " : " + self.new_comm.text)
                history_list = eval(row[10])
        l = []
        for row in reader:
            if row[1] != self.edit_duty_id_getter.text:
                l.append(row)
        duty_file.update(l)
        duty = project.Duty(proj_id=self.proj_id_conf.text, title=self.edit_duty_name.text, description=self.edit_duty_des.text,
                            priority=self.edit_duty_priority.text,status=self.edit_duty_status.text, start=self.edit_duty_start.text,
                            end=self.edit_duty_end.text, members=self.edit_duty_members.text, history=history_list, comments=comm_list)
        duty.save()
        logger.info(f"{self.username.text} added new comment")

    def history_fun(self, instance: Widget) -> None:
        """Displays the history of a duty in a popup window."""
        reader = duty_file.read()
        hist = []
        for row in reader:
            if str(row[1]) == self.edit_duty_id_getter.text:
                hist = eval(row[10])
        s = ""
        for i in hist:
            s += i + "\n"

        close_button = Button(text='Close', size_hint=(1, 0.2))
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=s))
        content.add_widget(close_button)

        popup = Popup(title='Test popup', content=content, auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def edit_duty(self, instance: Widget) -> None:
        """Displays duty details for editing."""
        self.window.clear_widgets()
        self.window.cols = 1
        df = pd.read_csv("info/duty.csv")
        for i, ID in zip(list(df['Task_id'].index), list(df['Task_id'])):
            if ID == self.edit_duty_id_getter.text:
                self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                self.edit_duty_id = TextInput(text=f"""{df['Task_id'][i]}""")
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
        """Updates duty details upon editing and saves changes."""
        reader = duty_file.read()
        for row in reader:
            if str(row[1]) == self.edit_duty_id_getter.text:
                history_list = eval(row[10])
                if str(row[5]) != self.edit_duty_priority.text:
                    history_list.append(f"""{self.username.text} has updated priority in {
                                        datetime.now()}""")
                if str(row[6]) != self.edit_duty_status.text:
                    history_list.append(f"""{self.username.text} has updated status in {
                                        datetime.now()}""")
                history_list.append(f"""{self.username.text} has updated duty in {
                                    datetime.now()}""")
        l = []
        for row in reader:
            if row[1] != self.edit_duty_id_getter.text:
                l.append(row)
        duty_file.update(l)
        duty = project.Duty(proj_id=self.proj_id_conf.text, title=self.edit_duty_name.text, description=self.edit_duty_des.text, priority=self.edit_duty_priority.text,
                            status=self.edit_duty_status.text, start=self.edit_duty_start.text, end=self.edit_duty_end.text, members=self.edit_duty_members.text, history=history_list)
        duty.save()
        logger.info(f"{self.username.text} edited a duty")
        self.duty_page("")

    def make_duty(self, instance: Widget) -> None:
        """Creates a new duty and logs the action."""
        duty = project.Duty(proj_id=self.proj_id_conf.text, title=self.duty_name.text, description=self.duty_des.text, priority=self.duty_priority.text,
                            status=self.duty_status.text, start=self.duty_start.text, end=self.duty_end.text, members=self.duty_members.text)
        duty.save()
        logger.info(f"""{self.username.text} made a duty""")
        self.duty_page("")

    def duty_page1(self, instance: Widget) -> None:
        """Display the duties categorized by status with an option to edit them."""
        self.window.clear_widgets()
        self.window.cols = 10
        df = pd.read_csv("info/duty.csv")
        df.sort_values(by=['Priority'], inplace=True)

        for status in project.Status:
            self.display_category(df, status)

        self.setup_edit_interface()

    def display_category(self, df: pd.DataFrame, status: project.Status) -> None:
        """Display duties under a specific category."""
        self.create_header(status.name)
        for i, proj in zip(list(df.index), list(df['Project_id'])):
            if int(self.proj_id_conf.text) == int(proj) and int(df["Status"][i]) == status.value:
                self.add_duty_widgets(i, df)

    def add_duty_widgets(self, index: int, df: pd.DataFrame) -> None:
        """Add widgets for individual duties."""
        self.edit_duty_name = TextInput(text=f"{df['Title'][index]}")
        self.edit_duty_id = TextInput(text=f"{df['Task_id'][index]}")
        self.edit_duty_des = TextInput(text=f"{df['Description'][index]}")
        self.edit_duty_start = TextInput(text=f"{df['Start'][index]}")
        self.edit_duty_end = TextInput(text=f"{df['End'][index]}")
        self.edit_duty_members = TextInput(text=f"{df['Members'][index]}")
        self.edit_duty_priority = TextInput(text=f"{df['Priority'][index]}")
        self.edit_duty_status = TextInput(text=f"{df['Status'][index]}")

        self.window.add_widget(self.edit_duty_name)
        self.window.add_widget(self.edit_duty_id)
        self.window.add_widget(self.edit_duty_des)
        self.window.add_widget(self.edit_duty_start)
        self.window.add_widget(self.edit_duty_end)
        self.window.add_widget(self.edit_duty_members)
        self.window.add_widget(self.edit_duty_priority)
        self.window.add_widget(self.edit_duty_status)
        self.window.add_widget(
            Label(text=f"{project.Priority(int(df['Priority'][index])).name}"))
        self.window.add_widget(
            Label(text=f"{project.Status(int(df['Status'][index])).name}"))

    def setup_edit_interface(self) -> None:
        """Set up the interface for editing duties."""
        self.back_button = Button(
            text="back",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE'
        )
        self.back_button.bind(on_press=self.see_member_fun)

        self.edit_duty_id_getter = TextInput(hint_text="task id")
        self.edit_duty_button = Button(
            text="edit",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE'
        )
        self.edit_duty_button.bind(on_press=self.edit_duty1)

        self.window.add_widget(self.edit_duty_id_getter)
        self.window.add_widget(self.edit_duty_button)
        self.window.add_widget(self.back_button)

    def comment_fun1(self, instance: Widget) -> None:
        """Displays existing comments and allows adding a new comment to a duty."""
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
                    font_size=20,
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
        """Adds a new comment to a duty and updates its history."""
        reader = duty_file.read()
        for row in reader:
            if row[1] == self.edit_duty_id.text:
                comm_list = eval(row[9])
                comm_list.append(str(datetime.now()) + "  " +
                                 self.username.text + " : " + self.new_comm.text)
                history_list = eval(row[10])
        l = []
        for row in reader:
            if row[1] != self.edit_duty_id.text:
                l.append(row)
        duty_file.update(l)
        duty = project.Duty(proj_id=self.proj_id_conf.text, title=self.edit_duty_name.text, description=self.edit_duty_des.text,
                            priority=self.edit_duty_priority.text,status=self.edit_duty_status.text, start=self.edit_duty_start.text,
                            end=self.edit_duty_end.text, members=self.edit_duty_members.text, history=history_list, comments=comm_list)
        duty.save()
        logger.info(f"""{self.username.text} added a comment""")

    def history_fun1(self, instance: Widget) -> None:
        """Displays the history of a duty in a popup window."""
        reader = duty_file.read()
        hist = []
        for row in reader:
            if str(row[1]) == self.edit_duty_id_getter.text:
                hist = eval(row[10])
        s = ""
        for i in hist:
            s += i + "\n"

        close_button = Button(text='Close', size_hint=(1, 0.2))
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=s))
        content.add_widget(close_button)

        popup = Popup(title='Test popup', content=content, auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def edit_duty_link1(self, instance: Widget) -> None:
        """Checks user membership and allows duty editing if the user is a member."""
        if self.username.text in self.edit_duty_members.text.split(","):
            self.edit_duty1()
        else:
            self.duty_page1("")

    def edit_duty1(self, id_changed):
        """Displays duty details for editing."""
        self.window.clear_widgets()
        self.window.cols = 1
        df = pd.read_csv("info/duty.csv")
        for i, ID in zip(list(df['Task_id'].index), list(df['Task_id'])):
            if ID == self.edit_duty_id_getter.text:
                self.edit_duty_name = TextInput(text=f"""{df['Title'][i]}""")
                self.edit_duty_id = TextInput(text=f"""{df['Task_id'][i]}""")
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
        """Updates duty details upon editing and saves changes."""
        if self.username.text in self.edit_duty_members.text.split(","):
            reader = duty_file.read()
            for row in reader:
                if str(row[1]) == self.edit_duty_id.text:
                    history_list = eval(row[10])
                    if str(row[5]) != self.edit_duty_priority.text:
                        history_list.append(f"""{self.username.text} has updated priority in {
                                            datetime.now()}""")
                    if str(row[6]) != self.edit_duty_status.text:
                        history_list.append(f"""{self.username.text} has updated status in {
                                            datetime.now()}""")
                    history_list.append(f"""{self.username.text} has updated duty in {
                                        datetime.now()}""")
            l = []
            for row in reader:
                if row[1] != self.edit_duty_id.text:
                    l.append(row)
            duty_file.update(l)
            duty = project.Duty(proj_id=self.proj_id_conf.text, title=self.edit_duty_name.text, description=self.edit_duty_des.text,
                                priority=self.edit_duty_priority.text,status=self.edit_duty_status.text, start=self.edit_duty_start.text,
                                end=self.edit_duty_end.text, members=self.edit_duty_members.text, history=history_list)
            duty.save()
            logger.info(f"""{self.username.text} edited a duty""")
            self.duty_page1("")
        else:
            self.window.add_widget(
                Label(text="You can not edit this duty.\nYou are not a member.", font_size=20, color='#FF0000'))


if __name__ == "__main__":
    SayHello().run()
