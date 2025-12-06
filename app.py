from flask import Flask, jsonify, render_template

app = Flask(__name__)

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


if __name__ == '__main__':
    # app.run() # production mode
    app.run(debug=True) # development mode