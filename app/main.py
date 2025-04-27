from flask import Flask, jsonify, request
import mysql.connector
import json

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host="mysql_db",
        user="root",
        password="password",
        database="test_db"
    )
    return connection

@app.route('/create_table', methods=['POST'])
def create_table():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Table 'users' created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insert_data', methods=['POST'])
def insert_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Missing 'name' or 'email' field"}), 400

        query = f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "User data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()

        return jsonify(users), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        user_id = request.args.get('id')
        cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
