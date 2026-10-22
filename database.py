"""SQLite: stores the packets and the passes."""
import sqlite3


class Database:
    def __init__(self, path="satellite.db"):
        self.conn = sqlite3.connect(path)
        self.conn.execute("""CREATE TABLE IF NOT EXISTS packets(
            id INTEGER PRIMARY KEY AUTOINCREMENT, mode TEXT, size INTEGER,
            urgency INTEGER, status TEXT DEFAULT 'WAITING', note TEXT DEFAULT '')""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS passes(
            id INTEGER PRIMARY KEY AUTOINCREMENT, link INTEGER, sent INTEGER,
            deferred INTEGER, time_left INTEGER)""")
        self.conn.commit()

    def add(self, mode, size, urgency):
        self.conn.execute("INSERT INTO packets(mode,size,urgency) VALUES(?,?,?)", (mode, size, urgency))
        self.conn.commit()

    def packets(self):
        return self.conn.execute("SELECT id,mode,size,urgency,status,note FROM packets ORDER BY id").fetchall()

    def update(self, pid, status, note):
        self.conn.execute("UPDATE packets SET status=?, note=? WHERE id=?", (status, note, pid))
        self.conn.commit()

    def add_pass(self, link, sent, deferred, time_left):
        self.conn.execute("INSERT INTO passes(link,sent,deferred,time_left) VALUES(?,?,?,?)",
                          (link, sent, deferred, time_left))
        self.conn.commit()

    def passes(self):
        return self.conn.execute("SELECT id,link,sent,deferred,time_left FROM passes ORDER BY id DESC").fetchall()

    def clear(self):
        self.conn.execute("DELETE FROM packets")
        self.conn.execute("DELETE FROM passes")
        self.conn.commit()
