#!/usr/bin/env python3
"""database.py - store incidents in a containerized PostgreSQL database."""

import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# Load secrets from the .env file in the project root
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "infrawatch"),
    "user": os.getenv("DB_USER", "infrawatch"),
    "password": os.getenv("DB_PASSWORD"),
}

def get_conn():
    """Open a connection to the Postgres container."""
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    """Create the incidents table if it doesn't already exist."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id SERIAL PRIMARY KEY,
            timestamp TEXT,
            component TEXT,
            severity TEXT,
            action TEXT,
            outcome TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def log_incident(component, severity, action, outcome):
    """Record one incident row."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO incidents (timestamp, component, severity, action, outcome) '
        'VALUES (%s, %s, %s, %s, %s)',
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         component, severity, action, outcome)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_all_incidents():
    """Return every incident, newest first."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'SELECT timestamp, component, severity, action, outcome '
        'FROM incidents ORDER BY id DESC'
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
