import logging
import sqlite3

logger = logging.getLogger("__name__")

class MusicDatabase():
    def __init__(self, connection_string, check=False):
        self.set_conn(connection_string)
        self.set_cursor(self.get_conn())
        self.set_type("sqlite3")

        # music table
        column_names = ["id","album","albumartist","artist","audio_offset","bitrate","comment","composer","disc","disc_total","duration","filesize","genre","samplerate", "title", "track", "track_total", "year", "location"]
        column_types = ["INTEGER", "VARCHAR", "VARCHAR", "VARCHAR", "INTEGER", "INTEGER", "VARCHAR", "VARCHAR", "INTEGER", "INTEGER", "FLOAT", "INTEGER", "VARCHAR", "INTEGER", "VARCHAR", "INTEGER", "INTEGER", "INTEGER", "VARCHAR"]
        column_extras = ["INCREMENTAL PRIMARY KEY", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        self.music_columns = [column_names, column_types, column_extras]

        if check:
            tables = self.table_info()
            if "music" not in tables:
                self.create_table("music", self.music_columns)
            logger.info("All tables present in database!")

    def create_table(self, table_name, columns_info):
        """Create a table with table_name as name and columns_info as columns"""
        query = "CREATE TABLE IF NOT EXISTS " + table_name + " ("
        for i in range(0, len(columns_info[0])):
            query += columns_info[0][i] + " " + columns_info[1][i] + " " + columns_info[2][i] + ","
        # Delete latest character and raplace it with the create ending
        query = query[:-1]
        query = query + ");"

        try:
            self.cursor.execute(query)
        except Exception as e:
            logger.debug(query)
            logger.error("Unable to create: " + table_name)
            logger.error(e)

    def insert_data_table(self, table_name, columns, data):
        """
        Inserts data rows in a table specified by table_name.
        data is a list of tuples 
        """
        query = "INSERT INTO " + table_name + " ("
        for i in range(len(columns[0])):
            query += columns[0][i] + ","
        query = query[:-1]
        query = query + ") VALUES ("

        for i in range(len(columns[0])):
            query += "?, "
        query = query[:-2]
        query = query + ");"

        try:
            self.cursor.executemany(query, data)
            self.conn.commit()
        except Exception as e:
            logger.debug(query)
            logger.error("Unable to add data rows")
            logger.error(e)            

    def update_data_table(self, table_name, data, where, string=False):
        """
        Update a row in a table specified by table_name
        data is a dict of the columns and data you want to update
        where is a string that defines which records to update
        """
        query = "UPDATE "  + table_name + " SET " 
        for column, value in data.items():
            if string:
                query += column + " = '" + str(value) + "' ,"
            else:
                query += column + " = " + str(value) + " ,"
        query = query[:-1]
        query += " WHERE " + where
        
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            logger.debug(query)
            logger.error("Unable to update row")
            logger.error(e)

    def get_data_table(self, table_name, columns, where):
        """"
        Get the data from a table specified by table_name.
        columns is a list of the columns you want to have
        where is the column string
        A tuple is returned.
        """
        result = ()
        query = "SELECT "
        for column in columns[0]:
            query += column + ","
        query = query[:-1]  
        query += " FROM " + table_name + " WHERE " + where + ";"

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        except Exception as e:
            logger.debug(query)
            logger.error("Unable to get data")
            logger.error(e)

        return result

    def get_max_from_column(self, table_name, column):
        """Get the row in which the maximum of a specified column is present""" 
        self.cursor.execute("SELECT max(" + column + ") FROM " + table_name)
        return self.cursor.fetchone()

    def get_min_from_column(self, table_name, column):
        """Get the row in which the maximum of a specified column is present""" 
        self.cursor.execute("SELECT min(" + column + ") FROM " + table_name)
        return self.cursor.fetchone()

    def add_column_to_table(self, table_name, column):
        """Add a column to the database specified by the table_name and the column as string"""
        query = "ALTER TABLE " + table_name + " ADD COLUMN " + column + " varchar(32)"

        try:
            self.cursor.execute(query)
        except Exception as e:
            logger.debug(query)
            logger.error("Unable to add column")
            logger.error(e)

    def delete_table(self, table_name):
        """Delete a specific table"""
        query = "DROP TABLE " + table_name
        try:
            self.cursor.execute(query)
        except Exception as e:
            logger.debug(query)
            logger.error("Unable to delete: " + table_name)
            logger.error(e)

    def table_info(self):
        """Get the name of the tables present in the database"""
        table_names = []
        query = "SELECT name FROM sqlite_master WHERE type ='table';"
        try:
            self.cursor.execute(query)
            names = self.cursor.fetchall()
            for name in names:
                table_names.append(name[0])

        except Exception as e:
            logger.debug(query)
            logger.error("Unable to get table info")
            logger.error(e)
        return list(table_names)

    def columns_info(self, table_name):
        """Get column names and types from a table. Returns 2 dimensional array"""
        column_names = []
        query = "PRAGMA table_info(" + table_name + ")"
        try:
            self.cursor.execute(query)
            names = self.cursor.fetchall()
            for name in names:
                column_names.append(name[1])
        except Exception as e:
            logger.debug(query)
            logger.error("Unable to get column info of: " + table_name)
            logger.error(e)
        return column_names

    def close(self):
        """Close database connection"""
        self.conn.close()

    ### GET ###

    def get_conn(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def get_type(self):
        return self.type

    ### SET ###

    def set_conn(self, connection_string):
        try:
            self.conn = sqlite3.connect(connection_string)
        except Exception as e:
            logger.critical("Unable to connect to database with connection string: " + connection_string)
            logger.critical(e)
            exit()
    
    def set_cursor(self, conn):
        self.cursor = conn.cursor()

    def set_type(self, db_type):
        self.type = db_type

    