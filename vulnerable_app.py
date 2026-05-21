from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
database = 'users.db'

def init_db():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', 'password123'))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string("""
        <h1>Login</h1>
        <form action="/login" method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username"><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
        <br>
        <form action="/search" method="GET">
            <label for="query">Search Users:</label>
            <input type="text" id="query" name="query">
            <input type="submit" value="Search">
        </form>
    """)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # Vulnerable SQL query - SQL Injection possible
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return f"<h1>Welcome, {user[1]}!</h1>"
    else:
        return "<h1>Invalid Credentials</h1>"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return "<h1>Please provide a search query.</h1>"

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # Another vulnerable SQL query - SQL Injection possible
    search_query = f"SELECT username FROM users WHERE username LIKE '%{query}%'"
    cursor.execute(search_query)
    results = cursor.fetchall()
    conn.close()

    if results:
        user_list = "<br>".join([user[0] for user in results])
        return f"<h1>Search Results:</h1><p>{user_list}</p>"
    else:
        return "<h1>No users found.</h1>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
