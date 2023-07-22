import sqlite3
import os

database_path = 'urlshortner.db'  # Replace with the desired database file path

# Check if the database file exists
if os.path.exists(database_path):
    # Open the existing database
    conn = sqlite3.connect(database_path)
else:
    # Create a new database and connect to it
    conn = sqlite3.connect(database_path)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()


def add_url(original_url, shortened_url):
    try:
        
        
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

        conn.commit()
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}") 
    finally:
        conn.close()    


def delete_url():
    pass      



def show_stored_url():
    
    cursor.execute('SELECT * FROM shortenedURL')
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    return data


def fetch_mapped_url(short_code):
    
    # Retrieve the original URL from the database based on the short code
    cursor.execute('SELECT original_url FROM shortenedURL WHERE shortened_url = ?', (short_code,))
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    return result