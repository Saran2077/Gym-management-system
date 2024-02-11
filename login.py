from connection import Connection
from admin import Admin
from owner import Owner

conn = Connection(database='admin')

a = conn.fetchData(table_name='gym_details')
admin = Admin()

while True:
    user_name = conn.fetchData(table_name='owner_details', columns='username')
    password = conn.fetchData(table_name='owner_details', columns='password')
    user_details = {u_name[0]:pwd[0] for u_name, pwd in zip(user_name, password)}
    username = input("Enter Username: ")
    if username == 'admin@123':
        admin.option()
    else:
        if username in user_details:
            password = input('Enter your password: ')
            if password == user_details[username]:
                g_id = conn.condition_fetch(table_name='owner_details', columns='G_ID', condition="Username", value=username)[0][0]
                database = conn.condition_fetch(table_name='gym_details', columns="GYM_NAME", condition="G_ID", value=g_id)[0][0]
                owner = Owner(database)
                owner.option()
            else:
                print("Username and Password does'nt match ")
        else:
            print('Enter a valid username')