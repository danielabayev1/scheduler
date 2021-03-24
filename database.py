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

    def insert_activity(self, activity):
        self.cur.execute('INSERT INTO SCHEDULE VALUES(:DATE,:DAY,:HOUR,:ACTIVITY)',
                         {'DATE': activity[self.DATE], 'DAY': activity[self.DAY], 'HOUR': activity[self.HOUR],
                          'ACTIVITY': activity[self.ACTIVITY]})
        self.conn.commit()

    def get_activities_by_date(self, date):
        self.cur.execute('SELECT * FROM SCHEDULE WHERE date=:date',
                         {'date': date})
        self.conn.commit()
        return self.cur.fetchall()

    def update_activity(self, new_activity):
        self.cur.execute('UPDATE SCHEDULE SET activity = :activity WHERE date=:date AND hour=:hour',
                         {'activity': new_activity[self.ACTIVITY], 'date': new_activity[self.DATE],
                          'hour': new_activity[self.HOUR]})
        self.conn.commit()

    def delete_activity(self, activity):
        self.cur.execute('DELETE FROM SCHEDULE WHERE date=:date AND hour=:hour',
                         {'date': activity[self.DATE],
                          'hour': activity[self.HOUR]})
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


d = DBManager()
# d.insert(('25.3', 'thur', '15:00', 'shitting'))
d.update_activity(('24.3', 'thur', '15:00', 'peeing'))
d.close_connection()
