#	1. Find out some way of finding names of district offices (maybe not possible without automating the browser) - https://nyks.nic.in/compile/namken.aspx
#					Possibilities - There is a javascript command(1 liner) that executes whenever an option is clicked, Find some way to know what all commands does a browser execute after we click... search for it

from html_table_parser import parser_functions as parse
import urllib.request
from bs4 import BeautifulSoup
import requests
#import random, string
#import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

global __login
__login = True

app = Flask(__name__)	#instantiating the class with __name__
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:15035@localhost/data'
db = SQLAlchemy(app)	#SQLAlchemy Object

class Data(db.Model):
	__tablename__ = 'base_records'
	name=db.Column(db.String)#(60))
	email = db.Column(db.String, unique=True)#(60))
	passwd = db.Column(db.String)#(50))
	address = db.Column(db.String, primary_key = True)
	district = db.Column(db.String)#(30))
	contact_info = db.Column(db.String, unique=True)#)

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
	name = db.Column(db.String(60))
	email = db.Column(db.String(60), primary_key = True)
	date_time = db.Column(db.String(20))	#May make it datetime late

	def __init__(self, name, email, date_time):
		self.name = name
		self.email = email
		self.date_time = date_time

def add_to_attendance(dbase , obj_list):
	for obj in obj_list:
		if dbase.session.query(type(obj)).filter(User_Attendance.email == obj.email).count() == 0:
			dbase.session.add(obj)
	dbase.session.commit()


@app.route('/') #'/' represents the 'home_page'
def home():	#Function name can be anything
	temp = input("Enter number : ")
	if __login == False:
		print("Login is False")
		return portal_login()
	user = User_Attendance('Aditya Gupta', 'ag15035@gmail.com', '2020-01-16 14:09:00')
	reg = Data('Aditya Gupta', 'ag15035@gmail.com', 'Adi@15', 'NIT Patna, Patna - 800005', 'Mahendru', 'Mobile - 8882060206')
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
#	passwd = request.form[]
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
	return str(state_offices);

@app.route('/about')
def about():
	return "This is the an Attendance System using speech verification and geolocation for verfication purposes."

def get_curr_time():
	res = urlopen('http://just-the-time.appspot.com/')
	result = res.read().strip()
	return result.decode('utf-8')

if __name__ == '__main__':
	app.run(debug=True)

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



#MAY CAUSE DATA LEAK (USEFUL FOR SAMPLE CREATION)... SEGREGATE THESE FUNCTIONS -
"""
twoD_table = parse.make2d(state_offices)
	l_obj = []
	for i in range(8):
		name = randomString(5)
		email = randomString(5)
		obj = Data(name, email, i, twoD_table[i+2][1], twoD_table[i+2][0], twoD_table[i+2][2].replace('                                 ','\n') )
						#TODO - Deal more intelligently with the address and contact_info, ie. extract the contacts instead of replacing spaces
		l_obj.append(obj)
	add_to_data(db,l_obj)
	

def add_to_data(dbase , obj_list):
	for obj in obj_list:
		if dbase.session.query(Data).filter(Data.email == obj.email).count() == 0 and dbase.session.query(Data).filter(Data.address == obj.address).count() == 0 and dbase.session.query(Data).filter(Data.contact_info == obj.contact_info).count() == 0:
			dbase.session.add(obj)	
	dbase.session.commit()
def randomString(stringLength=10):	#Only for Sample collection
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


"""