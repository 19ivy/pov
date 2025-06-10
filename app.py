
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El usuario ya existe"
    conn.close()
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return f"Bienvenido {username}!"
    else:
        return "Credenciales incorrectas"

@app.route('/edit', methods=['POST'])
def edit():
    old_username = request.form['old_username']
    new_username = request.form['new_username']
    new_password = request.form['new_password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET username = ?, password = ? WHERE username = ?', (new_username, new_password, old_username))
    conn.commit()
    conn.close()
    return f"Usuario actualizado a {new_username}"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
