from flask import Flask,render_template,request,url_for
from flask_assets import Bundle,Environment
from flask import flash, redirect
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import pyodbc 
import time

uname = "project1"
pword = "user_1234"
server = "DESKTOP-4MCSRV7"
db1 = "rdbms"

cnxn = pyodbc.connect(driver="{SQL Server}", host=server, database=db1,user=uname, password=pword)

cursor = cnxn.cursor()

print("Connection Establishing...")
time.sleep(1.0)
print("Connected to Deepbug_Chat SQL",db1,"database")

app=Flask(__name__)
app.config['SECRET_KEY']='password'

curr_user='user1'

@app.route('/home')
def index():
	return render_template('Rdbms.html')
@app.route('/patients')
def patients():
	return render_template('Rdbms_patient.html',user=curr_user)
@app.route('/review')
def review():
	return render_template('Rdbms_review.html')
@app.route("/pres")
def pres():
	return render_template("Rdbms_App.html")

@app.route('/send',methods=['GET','POST'])
def send():
	if request.method == 'POST':
		uid=request.form['LoginID']
		passkey=request.form['LoginPassword']
		querystring = "SELECT password from Patients where username='"+uid+"'"
		cursor.execute(querystring)
		row = cursor.fetchone()
		if check_password_hash(row.password,passkey):
			curr_user=uid
			return redirect("/patients")
	return render_template('Rdbms.html')

@app.route('/reg',methods=['GET','POST'])
def reg():
	if request.method == 'POST':
		name=request.form['Name']
		lname=request.form['LName']
		email=request.form['email']
		passkey=generate_password_hash(request.form['RegPassword'])
		querystring = "SELECT P#Id from Patients"
		cursor.execute(querystring)
		results = cursor.fetchall()
		list1=[]
		for r in results:
			list1.append(r[0])
		user_n=(sorted(list1).pop())+1
		username='user'+str(int(user_n))
		querystring = "Insert into Patients(P#ID,Name,Email,username,password) Values ("+str(user_n)+",'"+str(name)+" "+str(lname)+"','"+str(email)+"','"+str(username)+"','"+str(passkey)+"')"
		cursor.execute(querystring)
		cursor.commit()
		curr_user=username
		return redirect('/patients')
	return render_template('Rdbms.html')

@app.route('/disease',methods=['GET','POST'])
def disease():
	s1,s2,s3,s4,s5="NULL","NULL","NULL","NULL","NULL"
	if request.method == 'POST':
		user={}
		s1=request.form['Symptom1']
		user['S1']=s1
		s2=request.form['Symptom2']
		user['S2']=s2
		s3=request.form['Symptom3']
		user['S3']=s3
		s4=request.form['Symptom4']
		user['S4']=s4
		s5=request.form['Symptom5']
		user['S5']=s5
		str1="('"+str(s1)+"','"+str(s2)+"','"+str(s3)+"','"+str(s4)+"','"+str(s5)+"')"
		querystring="Select Name,Category from Disease where S1 in"+str1+" and S2 in "+str1+" and S3 in"+str1+" and S4 in"+str1+" and S5 in"+str1
		cursor.execute(querystring)
		results=cursor.fetchone()
		category=results.Category
		querystring="Select * from Doctors where Category='"+category+"'"
		cursor.execute(querystring)
		results=cursor.fetchone()
		user['doctor']=results.D_Name


		query="Select * from Patients where username='"+curr_user+"'"
		cursor.execute(query)
		results=cursor.fetchall()
		user["name"]=results[0].Name
		user['dob']=results[0].DOB
		list_past=[]
		for i in results:
			query="Select Name from Disease where D_ID='"+str(i.D_ID)+"'"
			row=cursor.execute(query).fetchall()
			list_past.append(row[0][0])
		user["disease"]=list_past


		return render_template("Rdbms_App.html",user=user)
	return render_template("Rdbms_patient.html")
if __name__=='__main__':
	app.run(debug=True)
