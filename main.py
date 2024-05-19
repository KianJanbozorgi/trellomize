import pandas as pd
import random
import project

def authorization(x,y):
    df = pd.read_csv('users.csv')
    m = list(df['password'].loc[df['username'] == x])
    if len(m) == 0:
        return "username not found"
    else:
        if m[0] == y :
            return "you loged in successfully"
        else:
            return "password not found"



# x = input('username :')
# z = input('email :')
# y = input('password :')

# f = open('users.csv', 'a' )
# f.write(f"""{x},{y},{z}
# """)
# f.close()

x = input('username :')
y = input('password :')

a = project.Project()
b = project.Duty()
a.add_duties(b)
print(a.duties[0].status)
print(authorization(x,y))
