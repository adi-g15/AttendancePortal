#	1. Find out some way of finding names of district offices (maybe not possible without automating the browser) - https://nyks.nic.in/compile/namken.aspx
#					Possibilities - There is a javascript command(1 liner) that executes whenever an option is clicked, Find some way to know what all commands does a browser execute after we click... search for it

#TODO - This is considering single officer at each office... to have functionality for multiple, instead of keeping email for referring to database in '/success', instead have another global address as center code, or address
"""
Current possible probe- verify whether geolocation is working 
TODO - Check if a person has entered at same day by checking today's date and his email id in the attendance table
"""

from html_table_parser import parser_functions as parse
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import random, string
#import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request

global __login
global __name
global __email
global __office_id

#LEARNT - Wherever you do Assignments to a variable with same name as a global one, then before that write 'global var_name', then it will make changes to the global variable

__login = False
__name = 'Login'
__email = 'nya@a.si'
__office_id = 0

app = Flask(__name__)	#instantiating the class with __name__
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:15035@localhost/data'
db = SQLAlchemy(app)	#SQLAlchemy Object

class Data(db.Model):	#Table of officer names
	__tablename__ = 'base_records'
	office_id = db.Column(db.Integer, primary_key = True, unique = False)
	name=db.Column(db.String)#(60))
	email = db.Column(db.String, unique=True)#(60))
	passwd = db.Column(db.String)#(50))
	address = db.Column(db.String)
	district = db.Column(db.String)#(30))
	contact_info = db.Column(db.String)#)
	latitude = db.Column(db.Float, nullable = False)
	longtitude = db.Column(db.Float, nullable = False)

	def __init__(self, office_id, name, email, passwd, address, district, contact_info, latitude, longtitude):
		self.office_id = office_id
		self.name = name
		self.email = email
		self.passwd = passwd
		self.address = address
		self.district = district
		self.contact_info = contact_info
		self.latitude = latitude
		self.longtitude = longtitude

#Idea to usr different tables for all, has been dropped
class User_Attendance(db.Model):
	__tablename__ = 'attendance'
	office_id = db.Column(db.Integer)
	name = db.Column(db.String(60))
	email = db.Column(db.String(60), primary_key = True)
	date = db.Column(db.String, nullable = False)	#May make it datetime late
	#VERY_VERY_IMP -> Make date unique for same person trying to put attendance the second (multiple) time
	time = db.Column(db.String, nullable = False)
	lat_long = db.Column(db.String, nullable = False)

	def __init__(self, office_id, name, email, date, time, lat_long):
		self.office_id = office_id
		self.name = name
		self.email = email
		self.date = date
		self.time = time
		self.lat_long = lat_long

@app.route('/') #'/' represents the 'home_page'
def home(name = 'Login'):	#Function name can be anything
	print(dist_between_points(2.3,5.4))
	return render_template("index.html", text=name)

@app.route('/portal_login')
def portal_login():
	return home()

@app.route('/success', methods = ['POST'])
def success():
	lat = request.form['lat']
	lng = request.form['lng']
	speech_verify = request.form['id_status']
	row = Data(0,'','','','','','',0.0,0.0)
	for dat in db.session.query(Data):
		if dat.email==__email :
				row = dat
	if speech_verify == "SUCCESS" and dist_between_points(str(lat)+' : '+str(lng), str(row.latitude) + ' : ' + str(row.longtitude)) < 50 :
		temp = get_curr_time()
		date = temp[0]
		time = temp[1]
		obj_list = []
		obj_list.append(User_Attendance(__office_id, __name, __email, date, time, str(lat)+' : '+str(lng) ))
		add_to_attendance(db, obj_list)
		return render_template('success.html', text=__name)
	else:
		return home()		

@app.route('/verification', methods = ['POST'])
def verification():
	email = request.form['user_id']
	pwd=request.form['passwd']
	global __name
	global __email
	global	__office_id
	global __login
	__login	= False
	if db.session.query(Data).filter(Data.email == email).count() == 1:
		for dat in db.session.query(Data):
			if dat.passwd==pwd :
#				print('\n\n\n\n\nPassed\n\n\n\n\n\n')
				__name = dat.name
				__email = email
#				print("Email is " + dat.email)
#				print("Office_ID is " + str(dat.office_id))
				__office_id = dat.office_id
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
	date = int(strres[8:10])
	minute = (int(strres[14:16]) + 30)%60 
	hr = int(strres[11:13]) + 5 + int((int(strres[14:16]) + 30)/60)
	date += int(hr/24)
	hr %= 60;
	ret_list.append(strres[:8] + str(date))
	ret_list.append(str(hr) + ':' + str(minute) + ':' + strres[17:])
	print(ret_list[1]) #2020-01-16 16:45:15
	return ret_list

def dist_between_points(lat,lng):
	import geopy.distance
	coords_1 = (0,0)
	coords_2 = (lat,lng)
	return geopy.distance.distance(coords_1,coords_2).m	#Returns distance between them in metres
"""
def haversine_dist_between_points(lat,lng):
	import math
	coords_1 = (0,0)
	coords_2 = (lat,lng)
	radius = 6371  # of earth in km
    dlat = math.radians(lat - coords_1[0])
    dlng = math.radians(lng - coords_1[1])
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist = radius * c
    return dist*1000	#multiplyied by 1000 to get in meters
"""

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

def create_sample_Data():
	list_obj = []
	for i in range(10):
		name = randomString(5)
		email = randomString(5)
		pwd = randomString(4)
		address = randomString(45)
		district = randomString(10)
		contact_info = randomString(45)
		latitude = 1.00 + i
		longtitude = 1.50 + i
		list_obj.append(Data(i,name,email,pwd,address,district,contact_info,latitude,longtitude))
	add_to_data(db, list_obj)

def add_to_data(dbase , obj_list):
	for obj in obj_list:
		if dbase.session.query(Data).filter(Data.email == obj.email).count() == 0:
			dbase.session.add(obj)	
	dbase.session.commit()

def randomString(stringLength=10):	#Only for Sample collection
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
"""

def add_to_attendance(dbase , obj_list):
	for obj in obj_list:
		if dbase.session.query(type(obj)).filter(User_Attendance.email == obj.email).count() == 0:
			dbase.session.add(obj)
	dbase.session.commit()