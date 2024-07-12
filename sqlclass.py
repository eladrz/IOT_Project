import json
import sqlite3
from datetime import datetime


class IoTDatabase:
    def __init__(self, db_file='iot_sensors.db'):
        self.db_file = db_file

    def timestamp(self):
        return str(datetime.fromtimestamp(datetime.timestamp(datetime.now()))).split('.')[0]

    def create_connection(self):
        """ Create a database connection to the SQLite database specified by db_file """
        try:
            conn = sqlite3.connect(self.db_file)
            #print('Connected to SQLite version:', sqlite3.version)
            return conn
        except sqlite3.Error as e:
            print(e)
            return None

    def create_table(self, create_table_sql):
        """ Create a table from the create_table_sql statement """
        conn = self.create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute(create_table_sql)
            except sqlite3.Error as e:
                print(e)
            finally:
                conn.close()
        else:
            print("Error! Cannot create the database connection.")

    def init_db(self):
        tables = [
            """CREATE TABLE IF NOT EXISTS `data` (
                `sys_id` INTEGER,
                `name` TEXT NOT NULL,
                `LastUpdated` TEXT NOT NULL,
                `status` TEXT NOT NULL,
                `keepAlive` TEXT NOT NULL,
                 UNIQUE(`sys_id`)
            );""",
            """CREATE TABLE IF NOT EXISTS `iot_devices` (
                `sys_id` INTEGER,
                `name` TEXT NOT NULL,
                `value` TEXT,
                `units` TEXT,
                `location` TEXT,
                `dev_pub_topic` TEXT NOT NULL,
                `dev_sub_topic` TEXT NOT NULL,
                UNIQUE(`sys_id`)
            );"""
        ]

        for table in tables:
            self.create_table(table)

    def update_data(self, sys_id, name=None, status=None, keepAlive=None, value=None):
        conn = self.create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                # Check if the sys_id exists in the data table
                c.execute("SELECT * FROM data WHERE sys_id=?", (sys_id,))
                row = c.fetchone()
                if row:
                    # Update the existing record with provided values
                    updates = []
                    if name is not None:
                        updates.append("name=?")
                    if status is not None:
                        updates.append("status=?")
                    if keepAlive is not None:
                        updates.append("keepAlive=?")
                    if updates:
                        update_query = "UPDATE data SET LastUpdated=?, " + ", ".join(updates) + " WHERE sys_id=?"
                        values = [self.timestamp()]
                        if name is not None:
                            values.append(name)
                        if status is not None:
                            values.append(status)
                        if keepAlive is not None:
                            values.append(keepAlive)
                        values.append(sys_id)

                        c.execute(update_query, tuple(values))
                        conn.commit()

                        if name is not None:
                            c.execute("UPDATE iot_devices SET name=? WHERE sys_id=?", (name, sys_id))
                            conn.commit()

                    if value is not None:
                        c.execute("UPDATE iot_devices SET value=? WHERE sys_id=?", (value, sys_id))
                        c.execute("UPDATE data SET LastUpdated=? WHERE sys_id=?", (self.timestamp(), sys_id))
                        conn.commit()
                else:
                    print(f"Error! System ID {sys_id} not found in the database.")
            except sqlite3.Error as e:
                print(e)
            finally:
                print(f"db updated for sys_id: {sys_id}")
                conn.close()
        else:
            print("Error! Cannot create the database connection.")

    def create_IOT_dev(self, sys_id, name, value, units, location, dev_pub_topic, dev_sub_topic):

        device = ''' INSERT INTO iot_devices(sys_id, name, value, units, location, dev_pub_topic, dev_sub_topic)
                  VALUES(?,? ,? ,? ,? ,?, ?) '''

        conn = self.create_connection()
        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute(device, (sys_id, name, value, units, location, dev_pub_topic, dev_sub_topic))
                conn.commit()

                cur.execute("INSERT INTO data (sys_id, name, LastUpdated, status, keepAlive) VALUES (?, ?, ?, ?, ?)",
                            (sys_id, name, self.timestamp(), "off", 0))
                conn.commit()

                print(f"New IoT device added to database: {name}")
            except sqlite3.Error as e:
                print(e)
            finally:
                conn.close()
        else:
            print("Error! Cannot create the database connection.")

    def print_database(self):
        """ Print all records from the database """
        conn = self.create_connection()
        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute("SELECT * FROM iot_devices")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
                cur.execute("SELECT * FROM data")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
            except sqlite3.Error as e:
                print(e)
            finally:
                conn.close()
        else:
            print("Error! Database connection is not established.")

    import json

    def sendData(self):
        conn = self.create_connection()
        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute("SELECT * FROM data")
                rows = cur.fetchall()
                data = []
                for i, row in enumerate(rows):
                    device_data = {
                        'sys_id': row[0],
                        'name': row[1],
                        'LastUpdated': row[2],
                        'status': row[3],
                        'keepAlive': row[4]
                    }
                    data.append(device_data)
                formatted_data = json.dumps(data)
                return formatted_data
            except sqlite3.Error as e:
                print(e)
            finally:
                conn.close()
        else:
            print("Error! Database connection is not established.")
            return None


if __name__ == '__main__':
    db = IoTDatabase()
    # db.init_db()
    # db.create_IOT_dev(1, 'RGB', '(0, 0, 0)', 'RGB', 'Room1', '', 'RGB')
    # db.create_IOT_dev(2, 'Temperature', 0, 'º', 'Room1', 'Temperature', '')
    # db.create_IOT_dev(3, 'DoorLock', 0, '', 'Room1', '', 'DoorLock')
    # db.create_IOT_dev(4, 'WaterLevel', 0, 'mm', 'Room1', 'WaterLevel', '')
    # db.create_IOT_dev(5, 'Humidity', 0, '%', 'Room1', 'Humidity', '')
    # db.create_IOT_dev(6, 'Airconditioner', 0, 'º', 'Room1', '', 'Airconditioner')
    db.print_database()
