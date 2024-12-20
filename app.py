import psycopg2
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import random
import json
import os
from urllib.parse import urlparse

app = Flask(__name__)

# Load article pairs from JSON file
def load_article_pairs(filename='article_pairs.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {filename}: {e}")
        return []

# Global variable to store the article pairs
article_pairs = load_article_pairs()

# Parse DATABASE_URL for connection details
def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL environment variable not set")
    result = urlparse(db_url)
    return psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

# Initialize the database
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id SERIAL PRIMARY KEY,
                content_index  INTEGER NOT NULL,
                current_content TEXT NOT NULL,
                target_content TEXT NOT NULL,
                response_source BOOLEAN NOT NULL,
                response_argument BOOLEAN NOT NULL,
                timestamp TIMESTAMP NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

# Initialize the database on app startup
init_db()

@app.route('/')
def survey():
    if not article_pairs:
        return "No article pairs available. Please check the JSON file.", 500

    selected_pair = random.choice(article_pairs)
    return render_template(
        'survey.html',
        content_index =selected_pair['content_index '],
        current_content=selected_pair['current_content'],
        target_content=selected_pair['target_content'],
    )

@app.route('/submit', methods=['POST'])
def submit():
    try:
        content_index  = int(request.form['content_index '])  # Convert content_index  to integer
        current_content = request.form['current_content']
        target_content = request.form['target_content']
        response_source = request.form['response_source'] == 'True'
        response_argument = request.form['response_argument'] == 'True'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO responses (content_index , current_content, target_content, response_source, response_argument, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''',
            (content_index , current_content, target_content, response_source, response_argument, timestamp)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('thank_you'))
    except Exception as e:
        print(f"Error saving to database: {e}")
        return f"Error saving to database: {e}", 500

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
