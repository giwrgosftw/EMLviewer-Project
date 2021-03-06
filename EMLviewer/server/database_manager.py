import sqlite3
import os
import shutil

"""
The database_manager handles the functions which control the pony_database and the sqlite3 database.
Specifically:
    1. Creates the sqlite3 database. Specifically, its connection and the Eml Table
    2. Converts the .eml file to binary data (else it can not be saved properly)
    3. Inserts the .eml as BLOB to the sqlite3 database
    4. Deletes .eml files from the pony_database/sqlite3 database
    5. Retrieves/Extracts .eml files from the pony_database/sqlite3 database
"""


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as error:
        print(error)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        connect_ = conn.cursor()
        connect_.execute(create_table_sql)
    except sqlite3.Error as error:
        print(error)


def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as _file:
        blob_data = _file.read()
    return blob_data


# Inserts the selected .eml file into the database (saves as .db)
def insert_blob(name, eml_path):
    try:
        sqlite_connection = sqlite3.connect('database.sqlite')
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite database")
        sqlite_insert_blob_query = """ INSERT INTO EmlTable
                                  (name, eml) VALUES (?, ?)"""

        eml = convert_to_binary_data(eml_path)
        # Convert data into tuple format
        data_tuple = (name, eml)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqlite_connection.commit()  # without it, all the changes will be lost
        print(".eml file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("The sqlite connection is closed")


def write_to_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as _file:
        _file.write(data)
    print("Stored blob data into: ", filename, "\n")


# Exports the selected .eml file from the SQLite database into the database folder
def read_blob_data(name):
    try:
        sqlite_connection = sqlite3.connect('database.sqlite')
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite database")

        if not os.path.exists("./" + "database/"):
            os.makedirs("./" + "database/")

        sql_fetch_blob_query = """SELECT * from EmlTable where name = ?"""
        # executes the query against the database based on the tuple
        cursor.execute(sql_fetch_blob_query, (name,))
        # fetches all the rows of the query and returns them as a list of tuples
        record = cursor.fetchall()
        for row in record:
            # print("name = ", row[0], "eml_file = ", row[1])
            name = row[0]
            eml_file = row[1]

            print("Storing the .eml file on disk \n")

            eml_path = "./" + "database/" + name
            write_to_file(eml_file, eml_path)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("SQLite connection is closed")


# Exports all the .eml files from the SQLite database into the database folder
def read_all_blob_data():
    try:
        sqlite_connection = sqlite3.connect('database.sqlite')
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")

        cursor.execute("SELECT eml FROM EmlTable")  # execute a simple SQL select query
        # eml_ = cursor.fetchall()  # get all the results from the above query
        # Create lists in order to iterate and extract each data from each index
        eml_list = [eml[0] for eml in cursor.execute("SELECT eml FROM EmlTable")]
        names = [name[0] for name in cursor.execute("SELECT name FROM EmlTable")]
        length = len(eml_list)
        for i in range(length):
            # print(names[i])
            print("Storing the .eml file on disk \n")

            if not os.path.exists("./" + "database/"):
                os.makedirs("./" + "database/")

            eml_path = "./" + "database/" + names[i]
            write_to_file(eml_list[i], eml_path)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("SQLite connection is closed")


# Deletes the selected .eml file from the SQLite database and from the database folder
def delete_record(name):
    try:
        sqlite_connection = sqlite3.connect('database.sqlite')
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        sql_delete_blob_query = """DELETE from EmlTable where name = ?"""
        cursor.execute(sql_delete_blob_query, (name,))
        sqlite_connection.commit()

        if os.path.exists("./" + "database/" + name):
            os.remove("./" + "database/" + name)

        print("Record deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("The sqlite connection is closed")


# Deletes all the .eml files from the SQLite database and from the database folder (if exist)
def delete_all_records():
    try:
        sqlite_connection = sqlite3.connect('database.sqlite')
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite database")

        # Deleting single record now
        sql_delete_blob_query = """DELETE from EmlTable"""
        cursor.execute(sql_delete_blob_query)
        sqlite_connection.commit()
        remove_folder("./" + "database/")
        # remove_content("./" + "database/")
        print("Record deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("The sqlite connection is closed")


def remove_folder(folder_path):
    """ param <path> could be relative """

    # if os.path.isfile(path):
    # os.remove(path)  # remove the file

    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a dir.".format(folder_path))


# In case you just want to delete the content of the folder, not the folder itself
def remove_content(folder_dir):
    for filename in os.listdir(folder_dir):
        file_path = os.path.join(folder_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as error:
            raise ValueError('Failed to delete %s. Reason: %s' % (file_path, error))


def main():
    database = r"database.sqlite"

    sql_create_eml_table = """ CREATE TABLE IF NOT EXISTS EmlTable (
                                    name TEXT PRIMARY KEY, eml BLOB NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create the Eml Table
        create_table(conn, sql_create_eml_table)
    else:
        print("Error! Cannot create the database connection.")
