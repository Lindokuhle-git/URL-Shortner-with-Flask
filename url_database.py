from flask import g
import sqlite3
import os

database_path = 'urlshortner.db'  # Replace with the desired database file path

def get_db():
    
    conn = None

    if os.path.exists(database_path):
    # Open the existing database
        conn = sqlite3.connect(database_path, check_same_thread=False)
    else:
        # Create a new database and connect to it
        conn = sqlite3.connect(database_path)
    return conn

def close_db():
    db = getattr(get_db, 'db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.executescript(f.read())


def add_url(original_url, shortened_url):
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS shortenedURL (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        shortened_url TEXT NOT NULL
        )
        ''')

        cursor.execute('''
            INSERT INTO shortenedURL (original_url, shortened_url)
            VALUES (?, ?)
        ''', (original_url, shortened_url))

        db.commit()
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}") 
      


def delete_url():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM shortenedURL')    
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print(f"An error occured: {e}")  



def show_stored_url():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM shortenedURL')
        data = cursor.fetchall()
        return data if data is not None else []
       
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
    


def fetch_mapped_url(short_code):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute('SELECT original_url FROM shortenedURL WHERE shortened_url = ?', (short_code,))
        result = cursor.fetchone()

        return result
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")