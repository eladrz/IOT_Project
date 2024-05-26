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
 
    def update_data(self, sys_id, name=None, status=None, keepAlive=None, value = None):
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
                    
                    else:
                        if value is not None:
                            c.execute("UPDATE iot_devices SET value=? WHERE sys_id=?", (value, sys_id))
                            conn.commit()
                        else:
                            print("No updates provided.")
                else:
                    print(f"Error! System ID {sys_id} not found in the database.")
            except sqlite3.Error as e:
                print(e)
            finally:
                conn.close()
        else:
            print("Error! Cannot create the database connection.")

    def create_IOT_dev(self,sys_id, name, value, units, location, dev_pub_topic, dev_sub_topic):
    
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
                
                print("New IoT device added to database")
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



# Example usage:
if __name__ == '__main__':
    db = IoTDatabase()
    db.init_db()
    db.print_database()




