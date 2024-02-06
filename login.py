

while True:
    user_details = {"saran" : "saran"}
    username = input("Enter Username: ")
    if username in user_details:
        password = input('Enter your password: ')
        if password == user_details[username]:
            break
        else:
            print("Username and Password does'nt match ")
    else:
        print('Emter a valid username')