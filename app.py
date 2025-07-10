from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'jyoti'  

# Updated Database connection to remote MySQL server
db = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12789296",
    password="EZYKQIlfAW",
    database="sql12789296",
    port=3306
)
cursor = db.cursor(buffered=True)  # buffered=True helps with multiple queries

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/dashboard')
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        cursor.execute("SELECT * FROM notes WHERE user_id=%s", (session['user_id'],))
        notes = cursor.fetchall()
        return render_template('dashboard.html', notes=notes, username=session['username'])
    return redirect('/login')

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'user_id' in session:
        if request.method == 'POST':
            content = request.form['content']
            cursor.execute("INSERT INTO notes (user_id, content) VALUES (%s, %s)", (session['user_id'], content))
            db.commit()
            return redirect('/dashboard')
        return render_template('add_note.html')
    return redirect('/login')

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 'user_id' in session:
        # Only allow deletion of this user's own note
        cursor.execute("DELETE FROM notes WHERE id = %s AND user_id = %s", (note_id, session['user_id']))
        db.commit()
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run()
