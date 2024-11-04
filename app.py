from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
# Database setup
def init_db():
    conn = sqlite3.connect('survey.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article1 TEXT NOT NULL,
            article2 TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Sample data: pairs of articles (article1, article2)
article_pairs = [
    ("Article 1 Text Here...", "Article 2 Text Here..."),
    ("Another Article 1 Text...", "Another Article 2 Text..."),
    # Add more article pairs as needed
]

@app.route('/')
def survey():
    # Select a random article pair
    article1, article2 = article_pairs[0]  # For simplicity, we use the first pair here
    return render_template('survey.html', article1=article1, article2=article2)

@app.route('/submit', methods=['POST'])
def submit():
    article1 = request.form['article1']
    article2 = request.form['article2']
    response = request.form['response']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Save response to the database
    conn = sqlite3.connect('survey.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO responses (article1, article2, response, timestamp) VALUES (?, ?, ?, ?)',
                   (article1, article2, response, timestamp))
    conn.commit()
    conn.close()
    
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return "<h1>Thank you for participating!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
