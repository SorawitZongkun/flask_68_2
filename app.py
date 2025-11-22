from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    return jsonify(message="Welcome to the Home Page!")

if __name__ == '__main__':
    # app.run() # production mode
    app.run(debug=True) # development mode