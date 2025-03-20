import bcrypt
from llama3 import handle_convo

def welcome(username):
    handle_convo(username)


def gainAccess():
    Username = input("Enter your username: ")
    Password = input("Enter your Password: ")

    if Username and Password:
        with open("database.txt", "r") as db:
            data = {}
            for line in db:
                if ',' in line:
                    a, b = line.split(",")
                    data[a.strip()] = b.strip()

        if Username in data:
            hashed = data[Username].strip('b')
            hashed = hashed.replace("'", "")
            hashed = hashed.encode('utf-8')

            if bcrypt.checkpw(Password.encode(), hashed):
                print("Login success!")
                print(f"Hi {Username}")
                welcome(Username)

            else:
                print("Wrong password")
        else:
            print("Username doesn't exist")
    else:
        print("Please attempt login again")


def register():
    Username = input("Enter a username: ")
    Password1 = input("Create password: ")
    Password2 = input("Confirm Password: ")

    if len(Password1) > 8:
        with open("database.txt", "r") as db:
            existing_users = [line.split(",")[0].strip() for line in db if ',' in line]

        if Username:
            if Username in existing_users:
                print("Username exists")
            else:
                if Password1 == Password2:
                    Password1 = Password1.encode('utf-8')
                    Password1 = bcrypt.hashpw(Password1, bcrypt.gensalt())

                    with open("database.txt", "a") as db:
                        db.write(f"{Username}, {Password1}\n")
                        print("User created successfully!")
                        print("Please login to proceed:")
                else:
                    print("Passwords do not match")
        else:
            print("Please provide a username")
    else:
        print("Password too short")


def home():
    while True:
        print("Welcome, please select an option")
        option = input("Login | Signup | Exit: ")

        if option == "Login":
            gainAccess()
            break
        elif option == "Signup":
            register()
        elif option == "Exit":
            print("Goodbye!")
            break
        else:
            print("Please enter a valid option, this is case-sensitive")

