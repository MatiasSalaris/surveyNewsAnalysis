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
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
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
init_db()
@app.route('/')
def survey():
    selected_pair = random.choice(article_pairs)
    return render_template('survey.html', article1=selected_pair['article1'], article2=selected_pair['article2'])

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    
@app.route('/submit', methods=['POST'])
def submit():
    article1 = request.form['article1']
    article2 = request.form['article2']
    
    # Convert form data to boolean
    response_source = request.form['response_source'] == 'True'
    response_argument = request.form['response_argument'] == 'True'
    
    # Get timestamp for when the response was submitted
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save response to the database
    try:
        # Get the database connection
        conn = get_db_connection()  # This gets a valid connection object
        cursor = conn.cursor()  # Create cursor from connection
        
        # Now execute the query using the connection and cursor
        cursor.execute(
            'INSERT INTO responses (article1, article2, response_source, response_argument, timestamp) VALUES (%s, %s, %s, %s, %s)',
            (article1, article2, response_source, response_argument, timestamp)
        )
        
        # Commit changes to the database
        conn.commit()
        
        # Close the cursor and connection properly
        cursor.close()
        conn.close()
        
        # Redirect to thank you page
        return redirect(url_for('thank_you'))
    
    except Exception as e:
        print(f"Error saving to database: {e}")
        return f"Error saving to database: {e}", 500

        





