import pandas as pd
import random
import project
from menu import *
from user import *


def main():
    main_menu = Menu(["What do you want to do?", "Sign Up", "Log In", "Exit"])

    console.clear()
    main_menu.display()
    user = User()
    proj = project.Project()
    if main_menu.selected_option == "Sign Up":
        try:
            project.username = user.sign_up()
            print("signed up successfully")
            curses.napms(1000)
            console.clear()
            proj.project_menu(user)
        except Exception as ex:
            print(ex)

    elif main_menu.selected_option == "Log In":
        try:
            project.username = user.log_in()
            print("Log in successfully")
            curses.napms(1000)
            console.clear()
            proj.project_menu(user)
        except Exception as ex:
            print(ex)

    elif main_menu.selected_option == "Exit":
        pass


if __name__ == "__main__":
    main()

# def authorization(x,y):
#     df = pd.read_csv('users.csv')
#     m = list(df['password'].loc[df['username'] == x])
#     if len(m) == 0:
#         return "username not found"
#     else:
#         if m[0] == y :
#             return "you loged in successfully"
#         else:
#             return "password not found"


# x = input('username :')
# z = input('email :')
# y = input('password :')

# f = open('users.csv', 'a' )
# f.write(f"""{x},{y},{z}
# """)
# f.close()

# x = input('username :')
# y = input('password :')

# a = project.Project()
# b = project.Duty()
# a.add_duties(b)
# print(a.duties[0].status)
# print(authorization(x,y))
