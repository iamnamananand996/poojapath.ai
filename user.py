from flask import jsonify, request
from flask_jwt_extended import create_access_token
from database import connect_db
from flask_jwt_extended import get_jwt_identity

# User Registration Route
def register(bcrypt):
    data = request.get_json()
    print("Data is received:", data)
    username = data.get('username') 
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


def login(bcrypt):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user and bcrypt.check_password_hash(user[1], password):
        access_token = create_access_token(identity=user[0])
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


def book_priest():
    user_id = get_jwt_identity()  # Get user ID from JWT
    data = request.get_json()
    priest_id = data.get('priest_id')

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT availability FROM priests WHERE id = %s", (priest_id,))
    result = cur.fetchone()

    if result and result[0]:  # If priest is available
        cur.execute("UPDATE priests SET availability = FALSE WHERE id = %s", (priest_id,))
        conn.commit()
        message = f"Priest with ID {priest_id} successfully booked by User {user_id}!"
    else:
        message = "Invalid ID or Priest already booked."

    cur.close()
    conn.close()
    return jsonify({"message": message})


