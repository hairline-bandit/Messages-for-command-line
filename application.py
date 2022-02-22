import requests, ast
from encryptdecrypt import encrypt, decrypt
# Add view sent and inbox
username = ""
password = ""
url = "https://hairlinebandit.pythonanywhere.com/"
path = ""
def login():
    global username
    global password
    print("===========================================")
    user = input("Enter username: ")
    passw = input("Enter password: ")
    r = requests.post(url + "login", data={"user": user, "passw": passw})
    resp = ast.literal_eval(r.text)
    if resp["a"] == "no user":
        print("Username not found")
        exit()
    elif resp["a"] == "wrong password":
        print("Incorrect password")
        exit()
    username = user
    password = passw
    print("Successful login!")

def create():
    global username
    global password
    print("===========================================")
    user = input("Enter username (NO SPACES): ")
    passw = input("Enter password (At least 8 characters): ")
    r = requests.post(url + "makeacc", data={"user":user, "passw":passw})
    resp = ast.literal_eval(r.text)
    if resp["a"] == "illegal charater":
        print("You had a space, or you input a 0 length username")
        exit()
    elif resp["a"] == "duplicate user":
        print("Someone is already using that username")
        exit()
    elif resp["a"] == "short password":
        print("Password was less than 8 character")
        exit()
    print("Success!")
    username = user
    password = passw

def refresh():
    r = requests.post(url + "refresh", data={"user": username, "passw": password})
    resp = ast.literal_eval(r.text)
    try:
        if resp["a"] == "no user":
            print("Username does not exist")
            exit()
        elif resp["a"] == "wrong password":
            print("Wrong password")
            exit()
        elif resp["a"] == "no data":
            print("No new messages")
    except:
        with open(path + "messages_from_" + username + ".txt", "a+") as f:
            f.write(encrypt(resp["data"], password) + "\n!@!@!@!@!@#!$@%!^@$#^!^@%#$\n")

def send_message(user):
    refresh()
    print("===========================================\n")
    print("Message history:\n")
    d = {}
    # Times
    a1 = []
    # Messages
    a2 = []
    with open(path + "messages_from_" + username + ".txt", "r") as f:
        tmp = f.read()
        if len(tmp) == 0:
            print("No messages received from that user\n")
        else:
            tmp2 = tmp.split('\n!@!@!@!@!@#!$@%!^@$#^!^@%#$\n')
            aa = [decrypt(i, password) if len(i) > 0 else "" for i in tmp2]
            for i in aa:
                if len(i) > 0 and i.lstrip("\n").split(":")[0] == user:
                    tmp3 = int(i.split(":")[1])
                    d[tmp3] = i.lstrip("\n")
                    a1.append(tmp3)
    with open(path + "messages_to_" + username + ".txt", "r") as f:
        tmp = f.read()
        if len(tmp) == 0:
            print("No messages sent to that user\n")
        else:
            tmp2 = tmp.split("\n!@!@!@!@!@#!$@%!^@$#^!^@%#$\n")
            aa = [decrypt(i, password) if len(i) > 0 else "" for i in tmp2]
            for i in aa:
                if len(i) > 0 and i.lstrip("\n").split(":")[0] == user:
                    tmp3 = int(i.split(":")[1])
                    d[tmp3] = i.lstrip("\n").replace(user, username, 1)
                    a1.append(tmp3)
    if len(a1) > 0:
        a1.sort()
        for i in a1:
            a2.append(d[i])
        for i in a2:
            print(i)
        print("\nNote that timestamps are seconds from epoch (look up a converter to get the datetime)\n")
    msg = input("Enter the message: ")
    #user, receive, message, passw
    r = requests.post(url + "msg", data={"user":username, "receive":user, "message":msg, "passw":password})
    # Only write to sent message file if response = valid
    resp = ast.literal_eval(r.text)
    if resp["a"] == "no sender":
        print("You username invalid")
        exit()
    elif resp["a"] == "wrong password":
        print("Wrong password")
        exit()
    elif resp["a"] == "no receiver":
        print("No user found to send messages to")
        exit()
    with open(path+"messages_to_" + username + ".txt", "a+") as f:
        f.write(encrypt(resp["b"], password) + "\n!@!@!@!@!@#!$@%!^@$#^!^@%#$\n")
    print("Message sent successfully")

def inbox():
    refresh()
    print("===========================================\n")
    print("Inbox:\n")
    d = {}
    # Times
    a1 = []
    # Messages
    a2 = []
    with open(path + "messages_from_" + username + ".txt", "r") as f:
        tmp = f.read()
        if len(tmp) == 0:
            print("Inbox empty\n")
        else:
            tmp2 = tmp.split('\n!@!@!@!@!@#!$@%!^@$#^!^@%#$\n')
            aa = [decrypt(i, password) if len(i) > 0 else "" for i in tmp2]
            if len(aa) > 0:
                for i in aa:
                    if len(i) > 1:
                        tmp3 = int(i.split(":")[1])
                        d[tmp3] = i.lstrip("\n")
                        a1.append(tmp3)
            else:
                print("Inbox empty\n")
    if len(a1) > 0:
        a1.sort()
        for i in a1:
            a2.append(d[i])
        for i in a2:
            print(i)
        print("\nNote that timestamps are seconds from epoch (look up a converter to get the datetime)\n")

def sent():
    print("===========================================\n")
    print("Sent messages:\n")
    d = {}
    # Times
    a1 = []
    # Messages
    a2 = []
    with open(path + "messages_to_" + username + ".txt", "r") as f:
        tmp = f.read()
        if len(tmp) == 0:
            print("No messages sent\n")
        else:
            tmp2 = tmp.split('\n!@!@!@!@!@#!$@%!^@$#^!^@%#$\n')
            aa = [decrypt(i, password) if len(i) > 0 else "" for i in tmp2]
            if len(aa) > 0:
                for i in aa:
                    if len(i) > 1:
                        tmp3 = int(i.split(":")[1])
                        d[tmp3] = i.lstrip("\n")
                        a1.append(tmp3)
            else:
                print("No messages sent\n")
    if len(a1) > 0:
        a1.sort()
        for i in a1:
            a2.append(d[i])
        for i in a2:
            print(i)
        print("\nNote that timestamps are seconds from epoch (look up a converter to get the datetime)\n")

def main():
    logor = input("Would you like to 'login' or 'create' an account: ")
    if logor == "login":
        login()
    elif logor == "create":
        create()
    else:
        exit()
    with open(path+"messages_to_" + username + ".txt", "a+") as f:
        pass
    with open(path+"messages_from_" + username + ".txt", "a+") as f:
        pass
    refresh()
    print("===========================================")
    while True:
        print("Press ctrl+c at any time to exit (you will automatically be logged out)")
        print("===========================================")
        choice = input("Do you want to 'message' someone, view 'inbox', view 'sent' messages, or 'exit': ")
        if choice == "message":
            j = input("Who do you want to message: ")
            send_message(j)
        elif choice == "inbox":
            inbox()
        elif choice == "sent":
            sent()
        else:
            exit()

if __name__ == "__main__":
    main()