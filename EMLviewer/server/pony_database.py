from pony.orm import Required, PrimaryKey, Database, db_session, \
    set_sql_debug, commit, TransactionError

"""
Instead of using the complicated database_manager.py,
pony_database.py save the .eml to the database for you

However, combined the database_manager.py functions,
you can also retrieve/extract and delete .eml files from the database
"""


def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as _file:
        blob_data = _file.read()
    return blob_data


DB = Database()


class EmlTable(DB.Entity):
    name = PrimaryKey(str, auto=True)
    eml = Required(buffer)


DB.bind(provider='sqlite', filename='database.sqlite', create_db=True)
DB.generate_mapping(create_tables=True)
set_sql_debug(True)


@db_session
def add_eml(name, eml_path):
    try:
        eml_file = convert_to_binary_data(eml_path)
        EmlTable(name=name, eml=eml_file)
        commit()
        print(name + " inserted successfully as a BLOB into the table")
        # Pony does not save objects in the database immediately
        # These objects will be saved only after the commit() function is called
        # database session cache will be cleared automatically
        # database connection will be returned to the pool
    except TransactionError as ex_error:
        print ex_error
