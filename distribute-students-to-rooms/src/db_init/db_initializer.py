import mysql.connector

from ..config import DB_CONFIG


class DbConnector:

    def __init__(self):
        self.cnx = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.cnx.cursor(buffered=True)

    def close(self):
        self.cursor.close()
        self.cnx.close()


class DbCreator:

    def __init__(self, connection: DbConnector):
        self.connection = connection

    def create_database(self, db_name):
        try:
            self.connection.cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
            print("Database {} created successfully.".format(db_name))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def use_database(self, db_name):
        try:
            self.connection.cursor.execute('USE {}'.format(db_name))
        except mysql.connector.Error as err:
            print("Database {} does not exist.".format(db_name))
            print(err)
            exit(1)

    def create_tables(self, tables):
        for table_name in tables:
            table_description = tables[table_name]
            self.connection.cursor.execute(table_description)
