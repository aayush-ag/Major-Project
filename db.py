import sqlite3
import time

DB_NAME = "devices.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id TEXT,
            rssi INTEGER,
            last_seen REAL
        )
    ''')
    conn.commit()
    conn.close()


def insert_or_update(uid: str, rssi: int):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = time.time()
    c.execute("""
        INSERT INTO devices (id, rssi, last_seen)
        VALUES (?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            rssi=excluded.rssi,
            last_seen=excluded.last_seen
    """, (uid, rssi, now))
    conn.commit()
    conn.close()


def get_active_devices(threshold_sec: int = 30):
    cutoff = time.time() - threshold_sec
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, rssi FROM devices WHERE last_seen > ?", (cutoff,))
    result = c.fetchall()
    conn.close()
    return result


def remove_stale_devices(threshold_sec: int = 30):
    cutoff = time.time() - threshold_sec
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM devices WHERE last_seen < ?", (cutoff,))
    conn.commit()
    conn.close()