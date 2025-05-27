import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database', 'car_database.db')

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS CarDetails (
                        Plate TEXT PRIMARY KEY,
                        Owner TEXT,
                        Model TEXT,
                        Color TEXT)''')

    conn.commit()
    conn.close()

def insert_car_details(plate, owner, model, color):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO CarDetails VALUES (?, ?, ?, ?)", (plate, owner, model, color))
    conn.commit()
    conn.close()

def get_car_details(plate_number):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM CarDetails WHERE Plate=?", (plate_number,))
    result = cursor.fetchone()
    
    conn.close()
    return result if result else "No details found."

# Example usage
if __name__ == "__main__":
    create_database()
    insert_car_details('HD 5031', 'sweety', 'Toyota car ', 'Blue')
    print(get_car_details('HD 5031'))
