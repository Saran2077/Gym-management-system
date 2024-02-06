import mysql.connector

class Connection:
    def __init__(self, database):
        self.create_server_connection = mysql.connector.connect(
            host="127.0.0.10",
            user="root",
            passwd="2580",
            database=database
        )
        self.cursor = self.create_server_connection.cursor()

    def create_gym(self):

