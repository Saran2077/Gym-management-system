from connection import Connection

class Owner(Connection):
    def __init__(self, database):
        self.database = database
        Connection.__init__(self, database=database)

    def member_details(self):
        values = {
            'name': '',
            'age': '',
            'joined_date': '',
            'address': '',
            'contact': ''
        }
        while True:
            name = input('Enter the name of the Member: ')
            if name.replace(" ","") == "":
                print("Name can't be empty")
                continue
            values['name'] = name
            while True:
                age = input('Enter the age of the member: ')
                if age.replace(" ","") == "":
                    print("Age can't ve empty")
                    continue
                if not age.isdigit():
                    print("Age should br in number")
                    continue
                if int(age) < 1:
                    print("Age can't be negative")
                    continue
                values['age'] = age
                break
            while True:
                address = input("Enter the city of the member: ")
                if address.replace(" ","") == "":
                    print("Address can't be empty")
                    continue
                values['address'] = address
                break
            while True:
                contact = input("Enter the number of the member: ")
                if contact.replace(" ","") == "":
                    print("Number can't be empty")
                    continue
                if not contact.isdigit():
                    print("Phone number should be in number")
                    continue
                if len(contact) != 10:
                    print("Phone number should be in 10 digits")
                    continue
                if contact[0] == '0':
                    print("Phone number can't starts with 0")
                    continue
                values['contact'] = contact
                break
            return values

    def add_member(self):
        self.use_gym(self.database)
        data = self.member_details()
        m_id = [m_id[0] for m_id in self.fetchData(table_name='member', columns='m_id')]
        m_id = m_id[-1]+1 if m_id else 1
        self.insert(table_name='member', columns="M_ID, M_NAME, M_AGE, M_CONTACT, M_ADDRESS, M_JOINDATE, M_PAID", values=f'''{m_id}, "{data['name']}", "{data['age']}", "{data['contact']}", "{data['address']}",CURRENT_DATE() , "No"''')

    def remove_member(self):
        self.use_gym(self.database)
        while True:
            id = input("Enter the id or name of the member: ")
            if id.replace(" ","") == "":
                print("Id or name can't be empty")
                continue
            break
        if id.isdigit():
            data = self.condition_fetch(table_name='member', columns='M_ID, M_NAME, M_AGE, M_CONTACT, M_ADDRESS, M_JOINDATE', condition='M_ID', value=id)
            if data:
                columns = ['M_ID', 'M_NAME', 'M_AGE', 'M_CONTACT', 'M_ADDRESS', 'M_JOINDATE']
                self.prettyPrint(columns, data)
                ask = input("Enter y to delete: ")
                if ask == 'y':
                    self.delete(table_name='member', columns='M_ID', value=id)
            else:
                print('There is no member in that id')
                self.remove_member()
        else:
            data = self.condition_fetch(table_name='member', columns='M_ID, M_NAME, M_AGE, M_CONTACT, M_ADDRESS, M_JOINDATE', condition='M_NAME', value=id)
            if data:
                columns = ['M_ID', 'M_NAME', 'M_AGE', 'M_CONTACT', 'M_ADDRESS', 'M_JOINDATE']
                self.prettyPrint(columns, data)
                id = input("Enter the id of the member you want to remove: ")
                data = self.condition_fetch(table_name='member', columns='M_ID, M_NAME, M_AGE, M_CONTACT, M_ADDRESS, M_JOINDATE', condition='M_ID', value=id)
                if data:
                    columns = ['M_ID', 'M_NAME', 'M_AGE', 'M_CONTACT', 'M_ADDRESS', 'M_JOINDATE']
                    self.prettyPrint(columns, data)
                    ask = input("Enter y to delete: ")
                    if ask == 'y':
                        self.delete(table_name='member', columns='M_ID', value=id)
                else:
                    print('There is no member in that id')
                    self.remove_member()

            else:
                print("There is no member in that name")
                self.remove_member()

    def search_records(self):
        self.use_gym(gym_name=self.database)
        while True:
            id = input("You can search for a member using id or name: ").lower()
            if id.replace(" ",'') == '':
                print("Name or id can't be empty...")
                continue
            if id.replace(" ",'') == 'q':
                return
            break
        if id.isdigit():
            data = self.condition_fetch(table_name='member', columns='M_ID, M_NAME, M_AGE, M_CONTACT, M_ADDRESS, M_JOINDATE', condition='M_ID', value=id)
            if data:
                columns = ['M_ID', 'M_NAME', 'M_AGE', 'M_CONTACT', 'M_ADDRESS', 'M_JOINDATE']
                self.prettyPrint(columns, data)
            else:
                print('There is no member in that id')
        else:
            data = self.condition_fetch(table_name='member', columns = 'M_ID, M_NAME, M_AGE, M_CONTACT, M_ADDRESS, M_JOINDATE', condition='M_NAME', value=id)
            if data:
                columns = ['M_ID', 'M_NAME', 'M_AGE', 'M_CONTACT', 'M_ADDRESS', 'M_JOINDATE']
                self.prettyPrint(columns, data)

            else:
                print("There is no member in that name")

    def print_members(self):
        self.use_gym(gym_name=self.database)
        data = self.fetchData(table_name='member', columns='M_ID, M_NAME, M_AGE, M_CONTACT, M_ADDRESS, M_JOINDATE')
        columns = ['M_ID', 'M_NAME', 'M_AGE', 'M_CONTACT', 'M_ADDRESS', 'JOINED_DATE']
        if data:
            self.prettyPrint(columns, data)
        else:
            print("No members are in the gym")

    def fee_structure(self):
        self.use_gym(gym_name='admin')
        g_id = self.condition_fetch(table_name="gym_details", columns="G_ID", condition="GYM_NAME", value=self.database)[0][0]
        data = self.condition_fetch(table_name="gym_fee_structure", columns="DURATION, FEE", condition="G_ID", value=g_id)
        data_dict = {i[0].split()[0]: i[1] for i in data}
        if data:
            columns = ['Duration', 'Fee']
            self.prettyPrint(columns, data)
        else:
            print("Error Occured")
        return data_dict

    def pay_fee(self):
        self.use_gym(gym_name=self.database)
        ts = self.fetchData(table_name='transaction', columns="TS_ID")
        ts_id = ts[-1][0]+1 if ts else 1
        while True:
            m_id = input("Enter the id of the member: ")
            data = [i[0] for i in self.fetchData(table_name='member', columns='m_id')]
            if m_id.replace(" ", '') == '':
                print("Id can't be empty")
                continue
            if m_id.lower() == 'q':
                return
            if not m_id.isdigit():
                print("Id must be in number")
                continue
            if int(m_id) not in data:
                print("Id don't exist")
                continue
            break
        data = self.fee_structure()
        while True:
            ask = input("Choose a plan: ")
            if ask.replace(" ",'') == '':
                print("Month can't be empty")
                continue
            if ask.lower() == 'q':
                return
            if ask not in data:
                print("Wrong plan choosen")
                continue
            break
        self.use_gym(gym_name=self.database)
        self.insert(table_name='transaction', columns="TS_ID, M_ID, DURATION, PAID_DATE, EXPIRY_DATE", values=f'''{ts_id}, {m_id}, {ask}, CURRENT_DATE(), DATE_ADD(CURRENT_DATE(), INTERVAL {ask} MONTH)''')

    def fee_not_paid(self):
        self.use_gym(gym_name=self.database)
        self.cursor.execute("SELECT M_ID, M_NAME, M_AGE, M_CONTACT, M_ADDRESS FROM MEMBER WHERE M_ID NOT IN (SELECT M_ID FROM TRANSACTION WHERE CURRENT_DATE() < EXPIRY_DATE)")
        data = self.cursor.fetchall()
        columns = ['M_ID', 'M_NAME', 'AGE', 'CONTACT', 'LOCATION']
        self.prettyPrint(columns, data)

    def option(self):
        print("Enter q to back")
        while True:
            print("1. Add a member")
            print("2. Remove a member")
            print("3. Search")
            print("4. All members of the gym")
            print("5. Fee not paid")
            print("6. Pay fee")
            opt = input("Enter a option: ")
            if opt.replace(" ","").lower() == 'q':
                return
            if opt.replace(" ", "") == "":
                print("Option can't be empty")
                self.option()
            elif not opt.isdigit():
                print("Option should be in number")
                self.option()
            elif int(opt) < 0 or int(opt) > 6:
                print("Invalid option")
                self.option()
            else:
                if opt == '1':
                    self.add_member()
                elif opt == '2':
                    self.remove_member()
                elif opt == '3':
                    self.search_records()
                elif opt == '4':
                    self.print_members()
                elif opt == '5':
                    self.fee_not_paid()
                elif opt == '6':
                    self.pay_fee()

'''        3.Change gym details
            1.Gym fees
            2.Gym timing
        7.pay_trainee
        6.fee_expired
    7.announce offers
8.announce leave'''

owner = Owner('kingfitness')
owner.option()