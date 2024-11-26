@app.route('/submit', methods=['POST'])
def submit():
    article1 = request.form['article1']
    article2 = request.form['article2']
    
    # Convert form data to boolean
    response_source = request.form['response_source'] == 'True'
    response_argument = request.form['response_argument'] == 'True'
    
    # Debug: Print the parsed boolean responses
    print(f"Response Source: {response_source}")
    print(f"Response Argument: {response_argument}")
    
    # Get timestamp for when the response was submitted
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save response to the database
    try:
        conn = psycopg2.connect(get_db_connection_url())
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO responses (article1, article2, response_source, response_argument, timestamp) VALUES (%s, %s, %s, %s, %s)',
            (article1, article2, response_source, response_argument, timestamp)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('thank_you'))
    except Exception as e:
        print(f"Error saving to database: {e}")
        return f"Error saving to database: {e}", 500
