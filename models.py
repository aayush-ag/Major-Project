from pydantic import BaseModel
from typing import List
import sqlite3

DB_PATH = "devices.db"

class BLEDevice(BaseModel):
    id: str
    rssi: int

class ChatRequest(BaseModel):
    nearest: BLEDevice
    neighbour: List[BLEDevice]
    prompt: str

def create_tables():
    conn = sqlite3.connect(DB_PATH)
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
