from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="mysql_db",  # Ensure the MySQL service is correctly configured.
            user="root",
            password="password",  # Ensureaksj;dg the password is correct.
            database="test_db"    # Ensure the database exists or is created.
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/create_table', methods=['POST'])
def create_table():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL
            )
        """)
        connection.commit()
        return jsonify({"message": "Table 'users' created successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/insert_data', methods=['POST'])
def insert_data():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = connection.cursor()
    data = request.get_json()  # Get JSON data from the request

    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing 'name' or 'email' field"}), 400

    name = data['name']
    email = data['email']

    try:
        cursor.execute("""
            INSERT INTO users (name, email) VALUES (%s, %s)
        """, (name, email))
        connection.commit()
        return jsonify({"message": "User data inserted successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
