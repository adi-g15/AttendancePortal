import urllib.request
from bs4 import BeautifulSoup
import requests
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
import random, string

global __login
global __name
global __email
global __office_id
global __admin_login
global __admin_name
global __admin_email

__login = False
__name = 'Login'
__email = 'nya@a.si'
__office_id = 0
__admin_login = False
__admin_name = 'Login'
__admin_email = 'admin@none.si'


app = Flask(__name__)	#instantiating the class with __name__
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:15035@localhost/data'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pwxrydafvrmfcl:6412326133c93c304a373c0b02c8e434a493f89bc8e1370881695a82d4b08a4b@ec2-107-20-173-2.compute-1.amazonaws.com:5432/d4ja5ips6mte0?sslmode=require'
db = SQLAlchemy(app)	#SQLAlchemy Object

class Data(db.Model):	#Table of officer names
	__tablename__ = 'base_records'
	office_id = db.Column(db.Integer)
	name=db.Column(db.String)#(60))
	email = db.Column(db.String, primary_key=True)#(60))
	passwd = db.Column(db.String)#(50))
	address = db.Column(db.String)
	district = db.Column(db.String)#(30))
	contact_info = db.Column(db.String)#)
	latitude = db.Column(db.Float, nullable = False)
	longtitude = db.Column(db.Float, nullable = False)
	verificationProfileId = db.Column(db.String, nullable = False)

	def __init__(self, office_id, name, email, passwd, address, district, contact_info, latitude, longtitude, verifyID):
		self.office_id = office_id
		self.name = name
		self.email = email
		self.passwd = passwd
		self.address = address
		self.district = district
		self.contact_info = contact_info
		self.latitude = latitude
		self.longtitude = longtitude
		self.verificationProfileId = verifyID

class User_Attendance(db.Model):
	__tablename__ = 'attendance'
	office_id = db.Column(db.Integer)
	name = db.Column(db.String(60))
	email = db.Column(db.String(60), primary_key = True)
	date = db.Column(db.String, nullable = False)	#May make it datetime late
	time = db.Column(db.String, nullable = False)
	lat_long = db.Column(db.String, nullable = False)
	voice_confidence = db.Column(db.String, nullable = False)

	def __init__(self, office_id, name, email, date, time, lat_long, voice_confidence):
		self.office_id = office_id
		self.name = name
		self.email = email
		self.date = date
		self.time = time
		self.lat_long = lat_long
		self.voice_confidence = voice_confidence

class AdminData(db.Model):	#Table of officer names
	__tablename__ = 'admin_records'
	name=db.Column(db.String)#(60))
	email = db.Column(db.String, primary_key=True)#(60))
	passwd = db.Column(db.String)#(50))
	contact_info = db.Column(db.String)#)
	latitude = db.Column(db.Float, nullable = False)
	longtitude = db.Column(db.Float, nullable = False)
	verificationProfileId = db.Column(db.String, nullable = False)

	def __init__(self, name, email, passwd, contact_info, latitude, longtitude, verifyID):
		self.name = name
		self.email = email
		self.passwd = passwd
		self.contact_info = contact_info
		self.latitude = latitude
		self.longtitude = longtitude
		self.verificationProfileId = verifyID

@app.route('/create_sample')
def create_sample_Data():
	list_obj = []
	for i in range(10):
		name = randomString(5)
		email = randomString(2) + '@' + randomString(1) + '.' + randomString(2)
		pwd = randomString(4)
		address = randomString(45)
		district = randomString(10)
		contact_info = randomString(45)
		latitude = 1.00 + i
		longtitude = 1.50 + i
#		verifyID = '5aa30aba-8d0a-4b3c-a2dc-c57b4c757488'	#adi
		verifyID = 'a45424a2-26ee-4e9f-8e3a-97ce66508d80'	#adig
#		verifyID = 'df875785-9088-406f-97c1-db1de325b5b7'	#Abhishek
#		verifyID = 'b8b2bd45-34a1-4b8b-a381-289ab7caf1c9'	#Rabin
		list_obj.append(Data(i,name,email,pwd,address,district,contact_info,latitude,longtitude, verifyID))
	add_to_data(db, list_obj)
	return "Sample created"


@app.route('/create_admin_sample')
def create_admin_Data():
	list_obj = []
	for i in range(10):
		name = randomString(5)
		email = randomString(2) + '@' + randomString(1) + '.' + randomString(2)
		pwd = randomString(4)
		contact_info = randomString(45)
		latitude = 1.00 + i
		longtitude = 1.50 + i
		verifyID = '5aa30aba-8d0a-4b3c-a2dc-c57b4c757488'
		list_obj.append(AdminData(name,email,pwd,contact_info,latitude,longtitude, verifyID))
	add_to_data(db, list_obj)
	return "Admin Sample created"


def add_to_data(dbase , obj_list):
	for obj in obj_list:
		if dbase.session.query(Data).filter(Data.email == obj.email).count() == 0:
			dbase.session.add(obj)	
	dbase.session.commit()

def randomString(stringLength=10):	#Only for Sample collection
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def add_to_attendance(dbase , obj_list):
	for obj in obj_list:
		if dbase.session.query(type(obj)).filter(User_Attendance.email == obj.email).count() == 0:
			dbase.session.add(obj)
	dbase.session.commit()

@app.route('/') #'/' represents the 'home_page'
def home(name = 'Login'):	#Function name can be anything
	return render_template("index.html", text=__name)

@app.route('/admin_home')
def admin_home(name = 'Login'):
	return render_template("admin_index.html", text=__admin_name)

@app.route('/admin_options', methods = ['POST'])
def admin_options():
	email = request.form['user_id']
	pwd=request.form['passwd']
	speech_verify = request.form['id_status']
	global __admin_name
	global __admin_email
	global __admin_login
	__admin_login	= False
	if db.session.query(AdminData).filter(AdminData.email == email).count() == 1:
		for adat in db.session.query(AdminData):
			if adat.passwd==pwd :
				__admin_name = adat.name
				__admin_email = adat.email
				__admin_login = True
	else:
		__admin_login = False
	if( __admin_login == False):
		return admin_home()
	else:
		return render_template('admin_options.html', text=__admin_name)
#IMP. Turn on the distance check, after getting actual data

@app.route('/add_officer')
def add_officer():
	if __admin_login == True :
		return render_template('add_officer.html', text= __admin_name)
	else:
		return render_template('admin_index.html', text= 'Login')

@app.route('/rem_officer')
def rem_officer():
	return render_template('rem_officer.html', text= __admin_name)

@app.route('/get_attendance')
def get_attendance():
	return render_template('get_attendance.html', text= __admin_name)

@app.route('/admin_changes', methods = ['POST'])
def admin_changes():
	command = request.form['command']
	if(command == "Add Officer"):
		office_id = request.form['office_id']
		user_name = request.form['user_id']
		email = request.form['email']
		passwd = request.form['passwd']
		address = request.form['address']
		district = request.form['district']
		contact_info = request.form['contact_info']
		lat = request.form['lat']
		lng = request.form['lng']
		verificationProfileId = request.form['profile_id']
		list_obj = [].append(Data(office_id,user_name,email,passwd,address,district,contact_info,lat,lng, verificationProfileId))
		add_to_data(db, list_obj)
	return "Applied changes"

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
				__name = dat.name
				__email = email
				__office_id = dat.office_id
				__login = True

	else:
		__login = False
	if( __login == False):
		return home()
	else:
		return render_template('verification.html', text=__name)

@app.route('/success', methods = ['POST'])
def success():
	lat = request.form['lat']
	lng = request.form['lng']
	speech_verify = request.form['id_status']
#	voice_confidence = speech_verify.split(':')[1]
	row = Data(0,'','','','','','',0.0,0.0,'null')
	for dat in db.session.query(Data):
		if dat.email==__email :
				row = dat

	if "SUCCESS" in speech_verify.split(':')[0]: # and dist_between_points(lat,lng,row.latitude,row.longtitude) < 50 :
		temp = get_curr_time()
		date = temp[0]
		time = temp[1]
		obj_list = []
		obj_list.append(User_Attendance(__office_id, __name, __email, date, time, str(lat)+' : '+str(lng), 'High' ))
		add_to_attendance(db, obj_list)
		return render_template('success.html', text=__name)
	else:
		return home()		

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
	res = urllib.request.urlopen('http://just-the-time.appspot.com/')
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

def dist_between_points(lat,lng,lat2,lng2):
	import geopy.distance
	coords_1 = (lat,lng)
	coords_2 = (lat2,lng2)
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

