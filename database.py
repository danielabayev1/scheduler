import sqlite3
from datetime import date, timedelta


class DBManager:
    DATE = 0
    HOUR = 1
    ACTIVITY = 2
    INITIAL_DATE = date(2021, 1, 1)

    def __init__(self):
        self.conn = sqlite3.connect('schedule.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS SCHEDULE(
                                date integer,
                                hour text,
                                activity text,
                                primary key(date,hour))""")
        self.conn.commit()

    def insert_activity(self, activity):
        self.cur.execute('INSERT INTO SCHEDULE VALUES(:DATE,:HOUR,:ACTIVITY)',
                         {'DATE': activity[self.DATE],  'HOUR': activity[self.HOUR],
                          'ACTIVITY': activity[self.ACTIVITY]})
        self.conn.commit()

    def get_activities_by_date(self, real_date):
        db_date = (real_date - self.INITIAL_DATE).days
        self.cur.execute('SELECT * FROM SCHEDULE WHERE date=:date',
                         {'date': db_date})
        self.conn.commit()
        return self.cur.fetchall()

    def get_all_rows(self):
        self.cur.execute('SELECT * FROM SCHEDULE')
        self.conn.commit()
        return self.cur.fetchall()

    def get_this_week_data(self):
        cur_date = int((date.today() - self.INITIAL_DATE).days)
        self.cur.execute('SELECT * FROM SCHEDULE WHERE date>=:date and date<:date+7', {'date': cur_date})
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
# d.insert_activity((90, '15:00', 'shitting'))
# d.insert_activity((100, '15:00', 'shitting'))
# d.insert_activity((94, '15:00', 'shitting'))
# d.insert_activity((95, '15:00', 'shitting'))
# d.update_activity(('24.3', 'thur', '15:00', 'peeing'))
print(d.get_this_week_data())
d.close_connection()
