import sqlite3
from sqlite3 import Error
from datetime import datetime
from icecream import ic

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
        # print(pp)
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


def init_db(database):  # Todo update keepAlive
    tables = [
        """CREATE TABLE IF NOT EXISTS `data` (
            `name` TEXT NOT NULL,
            `status` TEXT NOT NULL,
            `keepAlive` TEXT NOT NULL,
            `lastUpdated` TEXT NOT NULL,
            FOREIGN KEY(`name`) REFERENCES `iot_devices`(`name`)
        );""",
        """CREATE TABLE IF NOT EXISTS `iot_devices` (
            `sys_id` INTEGER PRIMARY KEY,
            `name` TEXT NOT NULL UNIQUE,
            `value` TEXT,
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


def update_data_database(deviceName, status, db_file="IoT_DB.db"):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(f"INSERT INTO data (lastUpdated,status) VALUES (?,?) where Name = {deviceName}",
              (status, timestamp()))
    conn.commit()
    conn.close()
    print("db updated")


def update_keepAlive(deviceName, keepAlive, db_file="IoT_DB.db"):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("UPDATE data SET keepAlive = ?, lastUpdated = ? WHERE name = ?",
              (keepAlive, timestamp(), deviceName))
    conn.commit()
    conn.close()
    print("keepAlive updated in DB")


def add_IOT_data(name, status,keepAlive):
    """
    Add new IOT device data into the data table
    :param conn:
    :param :
    :return: last row id
    """
    sql = ''' INSERT INTO data(name, lastUpdated, status,keepAlive)
              VALUES(?,?,?,?) '''
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql, [name, timestamp(), status,keepAlive])
        conn.commit()
        conn.close()
        return
    else:
        print("Error! cannot create the database connection.")


def create_IOT_dev(name, value, units, location, dev_pub_topic, dev_sub_topic):
    """
    Create a new IOT device into the iot_devices table
    :param conn:
    :param :
    :return: sys_id
    """
    sql = ''' INSERT INTO iot_devices(name, value, units, location, dev_pub_topic, dev_sub_topic)
              VALUES(?,?,?,?,?,?) '''
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql, [name, value, units, location, dev_pub_topic, dev_sub_topic])
        conn.commit()
        conn.close()
        return
    else:
        print("Error! cannot create the database connection.")


def insert_new_device(name, status, keepAlive, value, units, location, dev_pub_topic, dev_sub_topic):
    add_IOT_data(name, status,keepAlive)
    create_IOT_dev(name, value, units, location, dev_pub_topic, dev_sub_topic)
    print(f"Inserted new device to DB: {name}")
    return


# def update_db(device, status, value):
#     sql1 = f'''UPDATE data SET status = ?, lastUpdated = ? WHERE name = ? '''
#     sql2 = f'''UPDATE iot_devices SET value = ? WHERE name = ? '''
#     conn = create_connection()
#     if conn is not None:
#         cur = conn.cursor()
#         cur.execute(sql1, (status, timestamp(), device))
#         cur.execute(sql2, (value, device))
#         conn.commit()
#         conn.close()
#         print(f"Database updated: {device}\n")
#     else:
#         print("Error! cannot create the database connection.")

def update_db(device, status, value):
    sql_check_device = '''SELECT COUNT(*) FROM data WHERE name = ?'''
    sql_update_data = '''UPDATE data SET status = ?, lastUpdated = ? WHERE name = ?'''
    sql_update_iot_devices = '''UPDATE iot_devices SET value = ? WHERE name = ?'''
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql_check_device, (device,))
        result = cur.fetchone()[0]
        if result > 0:  # Device exists in the database
            cur.execute(sql_update_data, (status, timestamp(), device))
            cur.execute(sql_update_iot_devices, (value, device))
            conn.commit()
            conn.close()
            print(f"Database updated: {device}\n")
        else:
            print(f"Device not found in the database: {device}\n")
    else:
        print("Error! cannot create the database connection.")

def get_device_status(device_name):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT status FROM data WHERE name = ?", (device_name,))
        row = c.fetchone()
        if row:
            return row[0]  # Return the status value
        else:
            return None  # Return None if device not found
    except sqlite3.Error as e:
        print("Error retrieving device status:", e)
        return None
    finally:
        conn.close()


def get_device_value(device_name):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT value FROM iot_devices WHERE name = ?", (device_name,))
        row = c.fetchone()
        if row:
            return row[0]  # Return the status value
        else:
            return None  # Return None if device not found
    except sqlite3.Error as e:
        print("Error retrieving device status:", e)
        return None
    finally:
        conn.close()


if __name__ == '__main__':
    database = "IoT_DB.db"
    init_db(database)
    insert_new_device("RGB", 'off', '0', '(0,0,0)', '(R,G,B)', 'Room1', '','DvirH/Light/RGB')
    insert_new_device("DH-11_Temperature", 'off', '0', '0', 'º', 'Room1', 'DvirH/Temperature', '')
    insert_new_device("DH-11_Humidity", 'off', '0', '0', '%', 'Room1', 'DvirH/Humidity', '')
    insert_new_device("Airconditioner", 'off', '0', '25', 'º', 'Room1', '', 'DvirH/Airconditioner')
    insert_new_device("WaterLevel", 'off', '0', '0', 'mm', 'Room1', 'DvirH/WaterLevel','')
    insert_new_device("DoorLock", 'off', '0', '', 'on/off', 'Room1', '', 'DvirH/DoorLock')
