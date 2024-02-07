from connection import Connection

conn = Connection(database='admin')

a = conn.fetchData(table_name='gym_details')
print(a)

while True:
    user_details = {"saran" : "saran"}
    username = input("Enter Username: ")
    if username == 'admin@123':
        continue
    else:
        if username in user_details:
            password = input('Enter your password: ')
            if password == user_details[username]:
                break
            else:
                print("Username and Password does'nt match ")
        else:
            print('Emter a valid username')