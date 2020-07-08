from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "test my first app with azure, Hello World!"