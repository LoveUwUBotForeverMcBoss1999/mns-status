from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# Database configuration
db_configuration = {
    'host': 'db.aurex.lk',
    'user': 'u11_GsZ09Z9Etg',
    'password': 'FWUwF6O9OxGOj3O+L@Pcmy+L',
    'database': 's11_McBoss'
}

@app.route('/')
def index():
    # Connect to the database
    connection = pymysql.connect(**db_configuration)
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Query the database
    cursor.execute("SELECT * FROM authme")
    records = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    return render_template('index.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
