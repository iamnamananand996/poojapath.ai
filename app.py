from flask import Flask, jsonify, request
from database import connect_db
from add_data import add_priests
from user import register, login, book_priest
from flask_jwt_extended import jwt_required
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Change this in production

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Define the root route '/'
@app.route('/')
def home():
    return "Welcome to the PoojaPath!"


@app.route('/api/priests',methods=["GET"])
# Function to fetch and display priests
def fetch_priests():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM priests")
    priests = cur.fetchall()

    cur.close()
    conn.close()
    print(" This is a sucessful attempt")
    return jsonify([{"id": p[0], "name": p[1], "experience": p[2], "age": p[3]} for p in priests])
    
    
@app.route('/api/add-initial-data',methods=["POST"])
def add_initila_data():
    return add_priests()
    

# Route to fetch available priests
@app.route("/api/available-priests", methods=["GET"])
def get_available_priests():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, name, experience, age FROM priests WHERE availability = TRUE")
    priests = cur.fetchall()

    cur.close()
    conn.close()
    print(" This is a sucessful attempt")
    return jsonify([{"id": p[0], "name": p[1], "experience": p[2], "age": p[3]} for p in priests])

# Route to book a priest


@app.route('/api/register', methods=['POST'])
def register_user():
    return register()
    
    
@app.route('/api/login', methods=['POST'])
def login_user():
    return login(bcrypt)  


if __name__ == "__main__":
    app.run(debug=True)  # Run the API on http://127.0.0.1:5000
