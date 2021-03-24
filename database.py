import sqlite3


class DBManager:
    DATE = 0
    DAY = 1
    HOUR = 2
    ACTIVITY = 3

    def __init__(self):
        self.conn = sqlite3.connect('schedule.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS SCHEDULE(
                                date text,
                                day text,
                                hour text,
                                activity text,
                                primary key(date,hour))""")
        self.conn.commit()

    def insert(self, activity):
        self.cur.execute('INSERT INTO SCHEDULE VALUES(:DATE,:DAY,:HOUR,:ACTIVITY)',
                         {'DATE': activity[self.DATE], 'DAY': activity[self.DAY], 'HOUR': activity[self.HOUR],
                          'ACTIVITY': activity[self.ACTIVITY]})
        self.conn.commit()

    def get_activities(self, date):
        self.cur.execute('SELECT * FROM SCHEDULE WHERE date=:date',
                         {'date': date})
        self.conn.commit()
        return self.cur.fetchall()

    def close_connection(self):
        self.conn.close()


d = DBManager()
d.close_connection()
