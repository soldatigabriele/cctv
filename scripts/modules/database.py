import platform
import mysql.connector
from settings import *

class NumpyMySQLConverter(mysql.connector.conversion.MySQLConverter):
    """ A mysql.connector Converter that handles Numpy types """

    def _float32_to_mysql(self, value):
        return float(value)

    def _float64_to_mysql(self, value):
        return float(value)

    def _int32_to_mysql(self, value):
        return int(value)

    def _int64_to_mysql(self, value):
        return int(value)

class Database:
    def __init__(self):
        try:
            # Open the connection with the database
            self.connection = mysql.connector.connect(
                host=get_env_value("DB_HOST"),
                user=get_env_value("DB_USERNAME"),
                port=get_env_value("DB_PORT"),
                passwd=get_env_value("DB_PASSWORD")
            )
            self.connection.set_converter_class(NumpyMySQLConverter)

        except:
            print("Error occurred while trying to connect with the database. Check the credentials in the .env")
        # Get a cursor
        try:
            self.cursor = self.connection.cursor()
            self.connected = True
        except:
            print("Cannot instantiate a cursor")

        # Use the Database
        self.cursor.execute("USE " + get_env_value("DB_DATABASE"))

    def insertLog(self, event, description):
        if self.connected:
            self.cursor.execute("INSERT INTO logs (event, description, timestamp) VALUES (%s, %s, CURRENT_TIMESTAMP)", (event, description))
            self.connection.commit()
            return

    def createEvent(self, elements):
        if self.connected:
            self.cursor.execute("INSERT INTO events (filename, processor, timestamp) VALUES (%s, %s, %s)", 
                (elements['filename'], platform.processor(), elements['timestamp']))
            self.connection.commit()
            return self.cursor.lastrowid

    def updateEvent(self, event_id, elements):
        if self.connected:
            for key, value in elements.items():
                # Build the query
                query = "UPDATE events SET {} = %s WHERE id = %s".format(key)
                self.cursor.execute(query, (elements[key], event_id))
                self.connection.commit()
            return True