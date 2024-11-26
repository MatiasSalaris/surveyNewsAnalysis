import psycopg2
from psycopg2 import sql
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import random
import json
import os

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=os.environ.get("DB_PORT", 5432)
    )

# Initialize the database table
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id SERIAL PRIMARY KEY,
            article1 TEXT NOT NULL,
            article2 TEXT NOT NULL,
            response_source TEXT NOT NULL,
            response_argument TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Call this during app initialization
init_db()

# Load article pairs from JSON file
def load_article_pairs(filename='article_pairs.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

article_pairs = load_article_pairs()

@app.route('/')
def survey():
    selected_pair = random.choice(article_pairs)
    return render_template('survey.html', article1=selected_pair['article1'], article2=selected_pair['article2'])

@app.route('/submit', methods=['POST'])
def submit():
    article1 = request.form['article1']
    article2 = request.form['article2']
    response_source = request.form['response_source']
    response_argument = request.form['response_argument']
    timestamp = datetime.now()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO responses (article1, article2, response_source, response_argument, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        ''',
        (article1, article2, response_source, response_argument, timestamp)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
