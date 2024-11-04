from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import random
import json
import os

app = Flask(__name__)

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

# Load article pairs from JSON file
def load_article_pairs(filename='article_pairs.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Sample data: pairs of articles (article1, article2)
article_pairs = load_article_pairs()

@app.route('/')
def survey():
    # Select a random article pair from the list
    selected_pair = random.choice(article_pairs)  # Randomly select a pair
    article1 = selected_pair['article1']
    article2 = selected_pair['article2']
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
    return render_template('thank_you.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
