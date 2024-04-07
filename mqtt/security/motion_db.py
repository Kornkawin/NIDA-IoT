import sqlite3


def create_connection(database):
    connection = None
    try:
        connection = sqlite3.connect(database)
    except sqlite3.Error as e:
        print(e)
    return connection


class MotionSensor:
    table_name = 'motion_sensor'
    cnx: sqlite3.Connection
    objects = []

    @classmethod
    def setup(cls, cnx: sqlite3.Connection):
        cls.cnx = cnx
        sql = f"""SELECT name FROM sqlite_master WHERE type = 'table'
                  AND name = '{cls.table_name}'"""
        c = cls.cnx.cursor()
        c.execute(sql)
        if c.fetchone() is not None:
            cls.get()
        else:
            cls.create_table()

    @classmethod
    def create_table(cls):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {cls.table_name} (
            id INTEGER PRIMARY KEY,
            device_name text NOT NULL,
            timestamp text NOT NULL,
            status text NOT NULL)
        """
        try:
            c = cls.cnx.cursor()
            c.execute(sql)
        except sqlite3.Error as e:
            print(e)

    @classmethod
    def get(cls):
        sql = f"""SELECT * FROM {cls.table_name}"""
        try:
            c = cls.cnx.cursor()
            c.execute(sql)
            cls.objects = [item for item in map(
                cls.from_database, c.fetchall())]
        except sqlite3.Error as e:
            print(e)

    @classmethod
    def insert(cls, motion_sensor):
        sql = f"""INSERT INTO {cls.table_name} (device_name, timestamp, status)
                 VALUES (?, ?, ?)"""
        params = (motion_sensor.device_name,
                  motion_sensor.timestamp, motion_sensor.status)
        with cls.cnx:
            c = cls.cnx.cursor()
            c.execute(sql, params)
            motion_sensor.id = c.lastrowid

        cls.objects.append(motion_sensor)

    @classmethod
    def from_database(cls, data):
        item = cls(data[0], data[1], data[2], data[3])
        return item

    def __init__(self, id=0, device_name='', timestamp='', status=''):
        self.id = id
        self.device_name = device_name
        self.timestamp = timestamp
        self.status = status

    def __str__(self):
        return f'{self.id} {self.device_name} {self.timestamp} {self.status}'
