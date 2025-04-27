from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
import time

app = Flask(__name__)

def get_db_connection(retries=5, delay=2):
    """Establish a database connection with retries."""
    for attempt in range(1, retries + 1):
        try:
            connection = mysql.connector.connect(
                host="mysql_db",
                user="root",
                password="password",
                database="test_db"
            )
            if connection.is_connected():
                print("[DB] Connection successful")
                return connection
        except Error as e:
            print(f"[DB] Attempt {attempt} failed: {e}")
            time.sleep(delay)
    raise ConnectionError("Failed to connect to database after multiple attempts.")

@app.route('/create_table', methods=['POST'])
def create_table():
    """Create the 'users' table if it does not exist."""
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100),
                        email VARCHAR(100)
                    )
                """)
                connection.commit()
        return jsonify({"message": "Table 'users' created successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/insert_data', methods=['POST'])
def insert_data():
    connection = None
    cursor = None
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Missing 'name' or 'email' field"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        connection.commit()
        return jsonify({"message": "User data inserted successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/get_users', methods=['GET'])
def get_users():
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/delete_user', methods=['POST'])
def delete_user():
    connection = None
    cursor = None
    try:
        user_id = request.args.get('id')
        if not user_id:
            return jsonify({"error": "Missing 'id' parameter"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
