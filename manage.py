import argparse
parser = argparse.ArgumentParser()
parser.add_argument("create-user")
parser.add_argument("--username", type=str)
parser.add_argument("--password", type=str)
args = parser.parse_args()

print(args.username, args.password)
f = open('users.txt' , 'a')
f.write(f"""{args.username},{args.password}""" , 'end')
f.close()