from connection import Connection

class Admin(Connection):
    def __init__(self):
        Connection.__init__(self, database='admin')

    def gym_details(self):
        details = {
            'location': '',
            'gym_fee': {},
            'owner_id': '',
            'owner_name': '',
            'owner_contact': '',
            'owner_address': '',
            'username': '',
            'password': ''
        }
        while True:
            print('Enter q to go back...')
            location = input('Enter the gym location: ')
            if location.lower().replace(" ", '') == 'q':
                return
            if location.replace(' ', '') == '':
                print("Location can't be empty")
                continue
            details['location'] = location
            break
        print('Enter the fee structure for your gym')
        while True:
            month = input('Enter the no of months: ')
            if month.lower().replace(" ", '') == 'q':
                return
            if month.replace(" ", '') == '':
                print('Months cant be empty...')
                continue
            if not month.isdigit():
                print('Months should be in integer')
                continue
            if month in details['gym_fee']:
                print('Month is already exists...')
                continue
            if int(month) < 1 or int(month) > 12:
                print('Enter a valid month')
                continue
            while True:
                fee = input(f'Enter the fee for {month} months: ')
                if fee.lower().replace(" ", '') == 'q':
                    return
                if fee.replace(" ", '') == '':
                    print('Fees cant be empty...')
                    continue
                if not fee.isdigit():
                    print('Fees should be in integer')
                    continue
                details['gym_fee'][month+(" month" if month == '1' else " months")] = fee
                break

            ask = input('Enter y to add fee structure or n to break: ')
            if ask != 'y':
                break

        while True:
            o_name = input("Enter the manager's name: ")
            if o_name.lower().replace(" ", '') == 'q':
                return
            if o_name.replace(" ", '') == '':
                print("Manager name can't be empty...")
                continue
            details['owner_name'] = o_name
            while True:
                o_contact = input("Enter the manager's contact: ")
                if o_contact.lower().replace(" ", '') == 'q':
                    return
                if o_contact.replace(" ", '') == '':
                    print("Manager name can't be empty...")
                    continue
                if not o_contact.isdigit():
                    print('Phone no should be in numbers...')
                    continue
                if o_contact[0] == '0':
                    print("Phone Number can't starts with 0...")
                    continue
                details['owner_contact'] = o_contact
                break
            while True:
                o_address = input("Enter the manager's address: ")
                if o_address.lower().replace(" ", '') == 'q':
                    return
                if o_address.replace(" ", '') == '':
                    print("Address can't be empty...")
                    continue
                details['owner_address'] = o_address
                break
            break
        details['username'] = o_name+o_contact[:5]
        details['password'] = o_contact
        print(details)
        return details

    def add_gym(self):
        g_id = [g_id[0] for g_id in (self.fetchData(table_name='gym_details'))]
        o_id = [o_id[0] for o_id in (self.fetchData(table_name='owner_details', columns='o_id'))]
        gym_details = [gym[0] for gym in self.fetchData(table_name='gym_details', columns='GYM_NAME')]
        o_id = o_id[-1]+1 if o_id else 1
        g_id = g_id[-1]+1 if g_id else 1
        gym_name = input('Enter the name of the Gym: ').lower()

        if gym_name in gym_details:
            print('Already Gym name exists...')
            self.add_gym()
        elif gym_name.replace(" ", '') == '':
            print("Gym name can't be empty")
            self.add_gym()
        else:
            values = self.gym_details()
            if values:
                self.insert(table_name='gym_details', columns="G_ID, GYM_NAME, GYM_LOCATION", values=f'''{g_id} ,"{gym_name}", "{values['location']}"''')
                for i in values['gym_fee']:
                    self.insert(table_name='gym_fee_structure', columns="G_ID, DURATION, FEE", values=f'''{g_id}, '{i}', "{values['gym_fee'][i]}"''')
                self.insert(table_name='owner_details', columns="O_ID, O_NAME, O_CONTACT, O_ADDRESS, USERNAME, PASSWORD, G_ID", values=f'''{o_id}, "{values['owner_name']}", "{values['owner_contact']}", "{values['owner_address']}", "{values['username']}", "{values['password']}", {g_id}''')
                self.create_gym(gym_name=gym_name)
                #ClearScreen
                print(f'Username: {values["username"]}')
                print(f'Password: {values["password"]}')
            else:
                self.add_gym()



    def remove_gym(self):
        gym_details = [gym[0] for gym in self.fetchData(table_name='gym_details', columns='GYM_NAME')]
        print(gym_details)
        gym_name = input('Enter the name of the Gym to remove: ')
        if gym_name in gym_details:
            g_id = self.condition_fetch(table_name='gym_details', columns='g_id', condition='GYM_NAME', value=gym_name)[0][0]
            o_id = self.condition_fetch(table_name='owner_details', columns='o_id', condition='O_ID', value=g_id)[0][0]

            self.delete_gym(gym_name=gym_name)
            self.use_gym(gym_name='admin')
            self.delete(table_name='gym_fee_structure', columns='g_id', value=g_id)
            self.delete(table_name='owner_details', columns='o_id', value=o_id)
            self.delete(table_name='gym_details', columns='g_id', value=g_id)
            print('Successfully removed...')
        elif gym_name.replace(" ", '') == '':
            print("Gym name can't be empty")
            self.remove_gym()
        else:
            print('Enter a valid gym name')
            self.remove_gym()

    def option(self):
        print("Enter q to back")
        while True:
            print("1. Add a Gym")
            print("2. Remove a Gym")
            opt = input("Enter a option: ")
            if opt.lower() == 'q':
                return
            if opt.replace(" ","") == "":
                print("Option can't be empty")
                self.option()
            elif not opt.isdigit():
                print("Option should be in number")
                self.option()
            elif int(opt) < 0 or int(opt) > 2:
                print("Invalid option")
                self.option()
            else:
                if opt == '1':
                    self.add_gym()
                elif opt == '2':
                    self.remove_gym()




