import sqlite3
import time
from classes.neighbours import NeighboursPayload
from classes.nodes import NodesPayload

DB_NAME = "devices.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id TEXT PRIMARY KEY,
            rssi INTEGER,
            last_seen TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id TEXT PRIMARY KEY,
            location TEXT,
            last_seen REAL
        );
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices_neighbour (
            id TEXT,
            rsid INT,
            node_id TEXT
        );
    ''')
    conn.commit()
    conn.close()

def insert_or_update(data: NodesPayload):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = time.time()
    c.execute("""
        INSERT INTO devices (id, location, last_seen)
        VALUES (?, ?)
        ON CONFLICT(id) DO UPDATE SET
            last_seen=excluded.last_seen,
            location=excluded.location
    """, (data.uid, data.location, now))
    conn.commit()
    conn.close()

def insert_neighbours(data: NeighboursPayload):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM devices_neighbour WHERE node_id = ?", (data.node_id,))  # Clear old data
    for neighbour in data.neighbours:
        c.execute("""
            INSERT INTO devices_neighbour (id, rsid, node_id)
            VALUES (?, ?, ?)
        """, (neighbour['id'], neighbour['rssi'], data.node_id))
    conn.commit()
    conn.close()

def get_active_devices(threshold_sec: int = 30):
    cutoff = time.time() - threshold_sec
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM devices WHERE last_seen > ?", (cutoff,))
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
