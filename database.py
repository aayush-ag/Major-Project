import os

import psycopg2
import time
from classes.neighbours import NeighboursPayload
from classes.nodes import NodesPayload

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "major"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "192.168.134.30"),
    "port": int(os.getenv("DB_PORT", 5432))
}


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id TEXT PRIMARY KEY,
            location TEXT,
            last_seen DOUBLE PRECISION
        );
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices_neighbour (
            count INT,
            node_id TEXT
        );
    ''')
    conn.commit()
    conn.close()


def insert_or_update(data: NodesPayload):
    conn = get_conn()
    c = conn.cursor()
    now = time.time()
    c.execute("""
        INSERT INTO devices (id, location, last_seen)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            last_seen = EXCLUDED.last_seen,
            location = EXCLUDED.location
    """, (data.id, data.location, now))
    conn.commit()
    conn.close()


def insert_neighbours(data: NeighboursPayload):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM devices_neighbour WHERE node_id = %s", (data.node_id,))
    c.execute("""
        INSERT INTO devices_neighbour (count, node_id)
        VALUES (%s, %s)
    """, (data.neighbours, data.node_id))
    conn.commit()
    conn.close()


def get_active_devices(threshold_sec: int = 30):
    cutoff = time.time() - threshold_sec
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id FROM devices WHERE last_seen > %s", (cutoff,))
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]


def remove_stale_devices(threshold_sec: int = 30):
    cutoff = time.time() - threshold_sec
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM devices WHERE last_seen < %s", (cutoff,))
    conn.commit()
    conn.close()


def get_neighbour_count_all_nodes():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT d.location, dn.count as neighbour_count
        FROM devices_neighbour dn
        JOIN devices d ON dn.node_id = d.id
    """)
    rows = c.fetchall()
    conn.close()
    return [{"location": row[0], "count": row[1]} for row in rows]


def get_active_devices_with_info(threshold_sec: int = 30):
    cutoff = time.time() - threshold_sec
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, location FROM devices WHERE last_seen > %s", (cutoff,))
    rows = c.fetchall()
    conn.close()
    return [{"id": row[0], "location": row[1]} for row in rows]
