from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import bcrypt
from word import create_modern_clean_template
import os
import traceback

# Initialize Flask app
app = Flask(__name__)
from flask_cors import cross_origin
CORS(app)

# Connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname="resumeDB",          # your database name
        user="postgres",            # your postgres username
        password="112255",  # your postgres password here
        host="localhost",
        port="5432"
    )
    conn.autocommit = True  # Important! So changes are saved without needing conn.commit()
    cur = conn.cursor()
    print("✅ Database connected successfully!")
except Exception as e:
    print("❌ Failed to connect to database:", e)

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Please provide username, email, and password.'}), 400

    try:
        # Check if user already exists
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            return jsonify({'message': 'User already exists!'})

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert new user
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password.decode('utf-8'))
        )

        print(f"✅ New user '{username}' inserted successfully!")
        return jsonify({'message': 'Signup successful!'})

    except Exception as e:
        print("❌ Error during signup:", e)
        return jsonify({'message': 'Server error during signup.'}), 500

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Please provide username and password.'}), 400

    try:
        # Find user
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if not user:
            return jsonify({'message': 'User not found'})

        stored_password = user[3]  # Assuming password is 4th column in table

        # Compare passwords
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            print(f"✅ User '{username}' logged in successfully!")
            return jsonify({'message': f'Welcome back, {username}!'})

        return jsonify({'message': 'Invalid credentials'})

    except Exception as e:
        print("❌ Error during login:", e)
        return jsonify({'message': 'Server error during login.'}), 500

# Start the server
if __name__ == '__main__':
    app.run(port=3001, debug=True)

# New route to generate resume document
from flask import send_file

@app.route('/generate_resume', methods=['POST', 'OPTIONS'])
@cross_origin()
def generate_resume():
    user_data = request.get_json()
    if not user_data:
        return jsonify({'message': 'No user data provided'}), 400

    output_path = os.path.join(os.getcwd(), 'generated_resume.docx')
    try:
        create_modern_clean_template(output_path, user_data)
        return send_file(output_path, as_attachment=True, download_name='resume.docx')
    except Exception as e:
        print(f"Error generating resume: {str(e)}")
        traceback.print_exc()
        return jsonify({'message': f'Error generating resume: {str(e)}'}), 500
