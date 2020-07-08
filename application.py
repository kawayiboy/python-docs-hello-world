from datetime import datetime
from flask import Flask, render_template
from flask import request
import sys
# import json
import ngender
app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/about/")
def about():
	return render_template("about.html")

@app.route("/contact/")
def contact():
	return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
	return render_template(
		"hello_there.html",
		name=name,
		date=datetime.now()
	)

@app.route("/api/data")
def get_data():
	return app.send_static_file("data.json")

@app.route('/nameform/')
def nameform():
	return render_template('form_submit.html')

@app.route('/pharsename/', methods=['POST'])
def pharsename():
	name=request.form['yourname']
	# email=request.form['youremail']
	#name = u'姓名:' + name
	possibility = ngender.guess(name)
	print(possibility)
	return render_template('form_action.html', name=name, email=possibility[0])

# @app.route("/")
# def hello():
#     return "test my first app with azure, Hello World!"

# if __name__=="__main__":
# 	app.config['JSON_AS_ASCII'] = False
# 	app.run( 
# 		host="0.0.0.0",
# 		port=int("5000"))