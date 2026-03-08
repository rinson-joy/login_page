import flask as fl
import pymongo as pm
from functools import wraps
import os

# Connect to MongoDB
client = pm.MongoClient("mongodb+srv://rinsonjoy530_:1212@fatty.we0zaf4.mongodb.net/")
db = client["juicy"]
col = db["userdata"]

app = fl.Flask(__name__, static_folder="beaut")
app.secret_key = "super_secret_key_123" # Change this for production

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"Checking access for: {fl.request.path}")
        print(f"Current Session: {dict(fl.session)}")
        if "user" not in fl.session:
            print("Access denied: User not in session. Redirecting to login.")
            return fl.redirect(fl.url_for("login"))
        print(f"Access granted to: {fl.session['user']}")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@app.route('/home')
def home():
    return fl.render_template("home.html", name="Menu")

@app.route('/register', methods=['GET', 'POST'])
def add_user():
    if fl.request.method == 'GET':
        return fl.render_template("register.html", name="Register")
    
    data = fl.request.get_json(silent=True) or fl.request.form
    username = data.get("username")
    password = data.get("password")
    role = "user" # Default role
    
    if not username or not password:
        return fl.jsonify({"message": "Missing username or password"}), 400
        
    if col.find_one({"username": username}):
        return fl.jsonify({"message": "Username already exists"}), 400
        
    col.insert_one({"username": username, "password": password, "role": role})
    return fl.jsonify({
        "message": "User added successfully",
        "username": username, 
        "role": role
    }), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    if fl.request.method == 'GET':
        return fl.render_template("login.html", name="Login")
    
    data = fl.request.get_json(silent=True) or fl.request.form
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    
    print(f"Login attempt for: {username} with role: {role}")
    
    if not username or not password or not role:
        return fl.jsonify({"message": "Missing fields"}), 400
        
    user = col.find_one({"username": username, "password": password, "role": role})
    if user:
        fl.session.clear() # Clear any old session data
        fl.session["user"] = user["username"]
        fl.session["role"] = user["role"]
        print(f"Login successful for {username}. Session set.")
        return fl.jsonify({
            "message": "Login successful",
            "username": user["username"],
            "role": user["role"]
        }), 200
    
    print("Login failed: Invalid credentials")
    return fl.jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout')
def logout():
    username = fl.session.get("user")
    fl.session.clear()
    print(f"User {username} logged out.")
    return fl.redirect(fl.url_for("login"))

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_user():
    if fl.request.method == 'GET':
        return fl.render_template("delete.html", name="Delete")
    # ... (rest of delete logic)
    return fl.jsonify({"message": "Delete logic here"}), 200

@app.route('/contents')
@login_required
def contents():
    return fl.render_template("contents.html", name="Contents")

@app.route('/attendance')
@login_required
def attendance():
    return fl.render_template("attendance.html", name="Attendance")

@app.route('/fees')
@login_required
def fees():
    return fl.render_template("fees.html", name="Fees")

@app.route('/debug_session')
def debug_session():
    return fl.jsonify(dict(fl.session))

if __name__ == "__main__":
    
    app.run(debug=True, port=5000)
