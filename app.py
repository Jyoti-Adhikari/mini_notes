import os
import mysql.connector
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'jyoti'

# Database configuration from environment variables with Docker defaults
db_config = {
    'host': os.getenv('DB_HOST', 'db'),  # 'db' is the service name in docker-compose
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'rootpassword'),
    'database': os.getenv('DB_NAME', 'notes_app'),
    'port': int(os.getenv('DB_PORT', '3306'))
}

def get_db_connection():
    """Create a new database connection for each request"""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize database tables if they don't exist"""
    try:
        db = get_db_connection()
        if db is None:
            print("Failed to connect to database for initialization")
            return
        
        cursor = db.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        db.commit()
        cursor.close()
        db.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db_connection()
        if db is None:
            return "Database connection failed"
        
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            return redirect('/login')
        except mysql.connector.IntegrityError:
            return "Username already exists. Please choose a different username."
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            cursor.close()
            db.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db_connection()
        if db is None:
            return "Database connection failed"
        
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            if user:
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect('/dashboard')
            else:
                return "Invalid username or password"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            cursor.close()
            db.close()
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        db = get_db_connection()
        if db is None:
            return "Database connection failed"
        
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM notes WHERE user_id=%s ORDER BY created_at DESC", (session['user_id'],))
            notes = cursor.fetchall()
            return render_template('dashboard.html', notes=notes, username=session['username'])
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            cursor.close()
            db.close()
    return redirect('/login')

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'user_id' in session:
        if request.method == 'POST':
            content = request.form['content']
            db = get_db_connection()
            if db is None:
                return "Database connection failed"
            
            cursor = db.cursor()
            try:
                cursor.execute("INSERT INTO notes (user_id, content) VALUES (%s, %s)", (session['user_id'], content))
                db.commit()
                return redirect('/dashboard')
            except Exception as e:
                return f"Error: {str(e)}"
            finally:
                cursor.close()
                db.close()
        return render_template('add_note.html')
    return redirect('/login')

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 'user_id' in session:
        db = get_db_connection()
        if db is None:
            return "Database connection failed"
        
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM notes WHERE id = %s AND user_id = %s", (note_id, session['user_id']))
            db.commit()
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            cursor.close()
            db.close()
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Initialize database when app starts
with app.app_context():
    init_database()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)