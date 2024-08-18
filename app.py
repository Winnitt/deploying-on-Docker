from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import os

# Create an instance of the Flask class
app = Flask(__name__)

# Configure MySQL database connection
app.config['MYSQL_HOST'] = "localhost"  # Assuming MySQL is on the same machine
app.config['MYSQL_USER'] = os.environ.get('mysql_user', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('mysql_password', 'my-secret-pw')
app.config['MYSQL_DB'] = os.environ.get('mysql_db', 'flaskapp')

# Initialize MySQL
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        try:
            # Fetching the data from the form
            userDetails = request.form
            name = userDetails['name']
            email = userDetails['email']

            # Insert data into the database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(name, email) VALUES (%s, %s)", (name, email))
            mysql.connection.commit()
            cur.close()
            return 'success'
        except Exception as e:
            # Log the error and show an error page or message
            print(f"Error: {str(e)}")
            return f"An error occurred: {str(e)}"
    return render_template('index.html')

if __name__ == '__main__':
    # Run Flask app with debug mode enabled
    app.run(host="0.0.0.0", port=5000, debug=True)
