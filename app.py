from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'flower_db'

# Secret key for session management
app.config['SECRET_KEY'] = '45scd7v6ib7o87nty8978o65dbsv26s35db468f75go8p9hojpiopmognfurdv'

@app.route('/home', methods=['GET'])
def home():
    # return jsonify(message="Welcome to the Home Page!")
    name = "Anya"
    age = 7
    my_dict = {"name": "Yor", "age": 26}
    # from flask import render_template
    return render_template('home.html', name=name, age=age, my_dict=my_dict)

@app.route('/create', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/store', methods=['POST'])
def store():
    # from flask import request
    if request.method == "POST":
        flower_name = request.form['flowerName']
        flower_price = request.form['flowerPrice']
        flower_place = request.form['flowerPlace']
        flower_description = request.form['flowerDescription']
        print('INPUT: ', flower_name, flower_price, flower_place, flower_description)

        # Connect to database and store the data
        # import mysql.connector
        my_db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        my_cursor = my_db.cursor(dictionary=True)
        # Insert data into the database
        sql = "INSERT INTO flowers (flower_name, flower_price, flower_place, flower_description) VALUES (%s, %s, %s, %s)"
        val = (flower_name, flower_price, flower_place, flower_description)
        my_cursor.execute(sql, val)
        my_db.commit()
        my_db.close()

        # from flask import redirect, session, url_for
        session['alert_status'] = "success"
        session['alert_message'] = "Flower added successfully!"
        return redirect('/')
    else:
        # return "Invalid Request Method", 400
        session['alert_status'] = "fail"
        session['alert_message'] = "Something went wrong!"
        return redirect('/')

@app.route('/', methods=['GET'])
def index():
    # Connect to database and fetch all flowers
    my_db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    my_cursor = my_db.cursor(dictionary=True)
    # Fetch all flowers from the database
    sql = "SELECT * FROM flowers"
    my_cursor.execute(sql)
    flowers = my_cursor.fetchall()
    my_db.close()

    # Show alert message
    if 'alert_status' in session and 'alert_message' in session:
        alert_message = {
            'status': session['alert_status'],
            'message': session['alert_message']
        }
        del session['alert_status']
        del session['alert_message']
    else:
        alert_message = {
            'status': None,
            'message': None
        }
    
    return render_template('index.html', flowers=flowers, alert_message=alert_message)

@app.route('/edit/<int:flower_id>', methods=['GET'])
def edit(flower_id):
    # Connect to database and fetch flower by id
    my_db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    my_cursor = my_db.cursor(dictionary=True)
    # Fetch flower from the database
    sql = "SELECT * FROM flowers WHERE id = %s"
    val = (flower_id,)
    my_cursor.execute(sql, val)
    flower = my_cursor.fetchall()
    my_db.close()

    return render_template('edit.html', flower=flower)

@app.route('/update/<int:flower_id>', methods=['POST'])
def update(flower_id):
    if request.method == "POST":
        flower_name = request.form['flowerName']
        flower_price = request.form['flowerPrice']
        flower_place = request.form['flowerPlace']
        flower_description = request.form['flowerDescription']
        print('UPDATE INPUT: ', flower_name, flower_price, flower_place, flower_description)

        # Connect to database and update the data
        my_db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        my_cursor = my_db.cursor(dictionary=True)
        # Update data in the database
        sql = """
            UPDATE flowers SET
            flower_name=%s,
            flower_price=%s,
            flower_place=%s,
            flower_description=%s
            WHERE id=%s
        """
        val = (flower_name, flower_price, flower_place, flower_description, flower_id)
        my_cursor.execute(sql, val)
        my_db.commit()
        my_db.close()

        session['alert_status'] = "success"
        session['alert_message'] = "Flower updated successfully!"
        return redirect('/')
    else:
        session['alert_status'] = "fail"
        session['alert_message'] = "Something went wrong!"
        return redirect('/')

if __name__ == '__main__':
    # app.run() # production mode
    app.run(debug=True) # development mode