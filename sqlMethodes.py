import sqlite3
from sqlite3 import Error
from datetime import datetime


def timestamp():
    return str(datetime.fromtimestamp(datetime.timestamp(datetime.now()))).split('.')[0]


def create_connection(db_file='IoT_DB.db'):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        pp = ('Conected to version: ' + sqlite3.version)
        print(pp)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def init_db(database):
    tables = [
        """CREATE TABLE IF NOT EXISTS `data` (
            `name` TEXT NOT NULL,
            `LastUpdated` TEXT NOT NULL,
            `value` TEXT NOT NULL,
            FOREIGN KEY(`name`) REFERENCES `iot_devices`(`name`)
        );""",
        """CREATE TABLE IF NOT EXISTS `iot_devices` (
            `sys_id` INTEGER PRIMARY KEY,
            `name` TEXT NOT NULL UNIQUE,
            `status` TEXT,
            `units` TEXT,
            `location` TEXT,
            `dev_pub_topic` TEXT NOT NULL,
            `dev_sub_topic` TEXT NOT NULL
        );"""
    ]

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tables
        for table in tables:
            create_table(conn, table)
        conn.close()
    else:
        print("Error! cannot create the database connection.")


def update_data_database(deviceName, status, db_file="IoT_DB.db"):  # Todo
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(f"INSERT INTO data (LastUpdated,value) VALUES (?,?,?) where Name = {deviceName}",
              (status, timestamp()))
    conn.commit()
    conn.close()
    print("db updated")


def add_IOT_data(name, value):
    """
    Add new IOT device data into the data table
    :param conn:
    :param :
    :return: last row id
    """
    sql = ''' INSERT INTO data(name, LastUpdated, value)
              VALUES(?,?,?) '''
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql, [name, timestamp(), value])
        conn.commit()
        conn.close()
        return
    else:
        print("Error! cannot create the database connection.")


def create_IOT_dev(name, status, units, location, dev_pub_topic, dev_sub_topic):
    """
    Create a new IOT device into the iot_devices table
    :param conn:
    :param :
    :return: sys_id
    """
    sql = ''' INSERT INTO iot_devices(name, status, units, location, dev_pub_topic, dev_sub_topic)
              VALUES(?,?,?,?,?,?) '''
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql, [name, status, units, location, dev_pub_topic, dev_sub_topic])
        conn.commit()
        conn.close()
        return
    else:
        print("Error! cannot create the database connection.")


def insert_new_device(name, value, status, units, location, dev_pub_topic, dev_sub_topic):
    create_IOT_dev(name, status, units, location, dev_pub_topic, dev_sub_topic)
    add_IOT_data(name, value)
    return


if __name__ == '__main__':
    database = "IoT_DB.db"  # Replace 'your_database_file_path.db' with your actual database file path
    init_db(database)
    # insert_new_device("RGB",0,'Off','NULL','Room1','DvirH/LightPub/RGB','DvirH/Light/RGB')
