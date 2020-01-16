#	1. Find out some way of finding names of district offices (maybe not possible without automating the browser) - https://nyks.nic.in/compile/namken.aspx
#					Possibilities - There is a javascript command(1 liner) that executes whenever an option is clicked, Find some way to know what all commands does a browser execute after we click... search for it

from html_table_parser import parser_functions as parse
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
#import random, string
#import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

global __login
global __name
__login = False
__name = 'Login'

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
#	latitude = db.Column(db.num)

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
	date = db.Column(db.String, unique = True)	#May make it datetime late
	time = db.Column(db.String)
	location = db.Column(db.String)

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
def home(name = 'Login'):	#Function name can be anything
	return render_template("index.html", text=name)

@app.route('/portal_login')
def portal_login():
	return home()

@app.route('/success', methods = ['POST'])
def success():
	return render_template('success.html')

@app.route('/verification', methods = ['POST'])
def verification():
	email = request.form['user_id']
	pwd=request.form['passwd']
	global __name
	global __login
	__login	= False
	if db.session.query(Data).filter(Data.email == email).count() == 1:
		for dat in db.session.query(Data):
			if dat.passwd==pwd :
				__name = dat.name
				__login = True
		#if db.session.query(Data).filter(Data.email == email).passwd == pwd:
		#	__login = True
	else:
		__login = False
	if( __login == False):
		return portal_login()
	else:
		return render_template('verification.html', text=__name)

@app.route('/table')	
def table():
	target = 'https://nyks.nic.in/compile/zdaddress.aspx'
	req = urllib.request.Request( url = target)
	f = urllib.request.urlopen(req)	#The actual HTTP Response
	xhtml = f.read()
	soup = BeautifulSoup( xhtml, 'html.parser' )
	state_offices = soup.find( 'table', { 'datakeysname' : 'nykcode', 'id' : 'gridview1' } )
	return str(state_offices)

@app.route('/about')
def about():
	return "This is the an Attendance System using speech verification and geolocation for verfication purposes."

def get_curr_time():	#Returns Current Date and Time
	res = urlopen('http://just-the-time.appspot.com/')
	result = res.read().strip()
	strres = result.decode('utf-8')
	ret_list = []	#(date,time)
	ret_list.append(strres[:10])
	minute = (int(strres[14:16]) + 30)%60 
	hr = int(strres[11:13]) + 5 + int((int(strres[14:16]) + 30)/60)
	ret_list.append(str(hr) + ':' + str(minute) + ':' + strres[17:])
	print(ret_list[1]) #2020-01-16 16:45:15
	return ret_list

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