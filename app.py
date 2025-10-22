from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "votes.db"

# Ensure database exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            option TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    option = request.form['option']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO votes (option) VALUES (?)", (option,))
    conn.commit()
    conn.close()
    return redirect(url_for('results'))

@app.route('/results')
def results():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT option, COUNT(*) FROM votes GROUP BY option")
    results = c.fetchall()
    conn.close()

    # Extract vote counts
    counts = {row[0]: row[1] for row in results}
    python_votes = counts.get('Python', 0)
    java_votes = counts.get('Java', 0)
    total = python_votes + java_votes

    return render_template('results.html',
                           python_votes=python_votes,
                           java_votes=java_votes,
                           total=total)

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(debug=True)
