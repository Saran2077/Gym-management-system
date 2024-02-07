import mysql.connector

class Connection:

    def __init__(self, database='admin'):
        self.create_server_connection = mysql.connector.connect(
            host="127.0.0.10",
            user="root",
            passwd="2580",
            database=database
        )
        self.cursor = self.create_server_connection.cursor()
        self.use_gym(gym_name=database)
        self.member_columns = 'M_ID INT NOT NULL PRIMARY KEY, M_NAME VARCHAR(30), M_AGE INT, M_CONTACT CHAR(10), M_ADDRESS VARCHAR(50), M_JOINDATE DATE, M_PAID VARCHAR(10)'
        self.trainer_columns = 'T_ID INT NOT NULL PRIMARY KEY, T_NAME VARCHAR(50), T_CONTACT CHAR(10), T_ADDRESS VARCHAR(100), T_SALARY DECIMAL(10,2)'
        self.transaction_columns = 'TS_ID INT NOT NULL PRIMARY KEY, M_ID INT, T_ID INT, DURATION INT, PAID_DATE DATE, EXPIRY_DATE DATE'
        self.trainer_assigined_columns = 'M_ID INT, T_ID INT, EXPIRY_DATE DATE'

    def use_gym(self, gym_name):
        self.cursor.execute(f"USE {gym_name}")
    def create_gym(self, gym_name):
        self.cursor.execute(f"CREATE DATABASE {gym_name};")
        self.use_gym(gym_name=gym_name)
        self.__create_table(table_name='member', columns=self.member_columns)
        self.__create_table(table_name='trainer', columns=self.trainer_columns)
        self.__create_table(table_name='transaction', columns=self.transaction_columns)
        self.__create_table(table_name='trainer_assigned', columns=self.trainer_assigined_columns)
        self.create_server_connection.commit()

    def delete_gym(self, gym_name):
        self.cursor.execute(f'DROP DATABASE {gym_name}')
        self.create_server_connection.commit()

    def insert(self, table_name, columns, values):
        print(f'INSERT INTO {table_name}({columns}) ({values})')
        self.cursor.execute(f'INSERT INTO {table_name}({columns}) VALUES({values})')



    def __create_table(self, table_name, columns):
        self.cursor.execute(f"CREATE TABLE {table_name}({columns});")
        self.create_server_connection.commit()

    def fetchData(self, table_name, columns='*'):
        self.cursor.execute(f'SELECT {columns} FROM {table_name}')
        data = self.cursor.fetchall()
        return data

conn = Connection()
# conn.delete_gym('KingFitness')