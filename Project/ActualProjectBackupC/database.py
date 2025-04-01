import mysql.connector
from config import DB_CONFIG

# Ensure MySQL uses native authentication
DB_CONFIG['auth_plugin'] = 'mysql_native_password'

# Connect to MySQL
connection = mysql.connector.connect(**DB_CONFIG)
cursor = connection.cursor()

# Ensure the table exists with the correct structure
cursor.execute("""
    CREATE TABLE IF NOT EXISTS game_state (
        id INT PRIMARY KEY,
        high_score INT DEFAULT 0
    )
""")
connection.commit()

# Check if a row exists
cursor.execute("SELECT COUNT(*) FROM game_state WHERE id=1")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO game_state (id, high_score) VALUES (1, 0)")
    connection.commit()

# Function to save high score
def save_game(high_score):
    cursor.execute("UPDATE game_state SET high_score=%s WHERE id=1", (high_score,))
    connection.commit()

# Function to load high score
def load_game():
    cursor.execute("SELECT high_score FROM game_state WHERE id=1")
    result = cursor.fetchone()
    return result[0] if result else 0
