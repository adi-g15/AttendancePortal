#	1. Find out some way of finding names of district offices (maybe not possible without automating the browser) - https://nyks.nic.in/compile/namken.aspx
#					Possibilities - There is a javascript command(1 liner) that executes whenever an option is clicked, Find some way to know what all commands does a browser execute after we click... search for it

from html_table_parser import parser_functions as parse
import urllib.request
from bs4 import BeautifulSoup
import requests

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

global __login
__login = True

app = Flask(__name__)	#instantiating the class with __name__

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:15035@localhost/data'
db = SQLAlchemy(app)	#SQLAlchemy Object

class Data(db.Model):
	__tablename__ = 'base_records'
	name=db.Column(db.String(60))
	email = db.Column(db.String(60), unique=True)
	passwd = db.Column(db.String(50))
	address = db.Column(db.String(250), primary_key = True)
	district = db.Column(db.String(30))
	contact_info = db.Column(db.String(150), unique=True)

	def __init__(self, name, email, passwd, address, district, contact_info):
		self.name = name
		self.email = email
		self.passwd = passwd
		self.address = address
		self.district = district
		self.contact_info = contact_info

#Idea to usr different tables for all, has been dropped
class User_Attendance(db.Model):
	__tablename__ = 'attendance'
	date = db.Column(db.String, primary_key =True)

@app.route('/') #'/' represents the 'home_page'
def home():	#Function name can be anything
	if __login == False:
		print("Login is False")
		return portal_login()
	res = requests.get('https://ipinfo.io/')
	data = res.json()
	location = '{%block curr_loc%}\n' + data['city']+'\n{%endblock%}'
	#FUTURE - If 'location' exists in the file, first remove those lines
	"""with open('templates/index.html','a+') as fout:
		content = fout.read()
		if location not in content:
			fout.write('\n')
			fout.write('{%block curr_loc%}\n' + data['city']+'\n'+'{%endblock%}\n')
	"""
	return render_template("index.html", text="Aditya")

@app.route('/portal_login')
def portal_login():
	return render_template("login.html")

@app.route('/verification', methods = ['POST'])
def verification():
	email = request.form['user_id']
	print("This is the email : " + email)
	__login = True
	if(__login == False):
		print("In Verify too, login is false")
		return portal_login()
	else:
		return render_template('verification.html', text="Aditya")

@app.route('/table')	
def table():
	target = 'https://nyks.nic.in/compile/zdaddress.aspx'
	req = urllib.request.Request( url = target)
	f = urllib.request.urlopen(req)	#The actual HTTP Response
	xhtml = f.read()
	soup = BeautifulSoup( xhtml, 'html.parser' )
	state_offices = soup.find( 'table', { 'datakeysname' : 'nykcode', 'id' : 'gridview1' } )
	twoD_table = parse.make2d(state_offices)
	return str(state_offices);

@app.route('/about')
def about():
	return "This is the an Attendance System using speech verification and geolocation for verfication purposes."
"""
@app.route('/location')
def get_location():

	res = requests.get('https://ipinfo.io/')
	data = res.json()
	location = '{%block curr_loc%}\n' + data['city']+'\n{%endblock%}'
	
	with open('templates/location.html','a+') as fout:
		content = fout.read()
		if location not in content:
			fout.write('\n')
			fout.write('{%block curr_loc%}\n' + data['city']+'\n'+'{%endblock%}\n')
	return render_template('location.html')
"""

if __name__ == '__main__':
	app.run(debug=True)