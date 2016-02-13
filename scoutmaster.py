#!/usr/bin/python
#This is a fork of scoutmaster.py with an html frontend, which is a fork of...
#FORK OF SCOUT.PY, TKINTER REMOVED
import sqlite3
from flask import Flask,request,send_file,render_template,g
app = Flask(__name__)
import sys

letable = [
	["teamNum","updown","Team num"],
        ["roundNum","updown","Round Num"], #Syntax: Variable Name, type, human name, [radiobutton options]. Variable names really only help with teamNum and if fort debugging via interacting with the database directly
	["posi","radio","Position",["Red 1","Red 2","Red 3","Blue 1","Blue 2","Blue 3"]], #Here is a radiobutton-the extra table is the choices for the radiobutton.
	["autoHead","head","Autonomous"],
	["sallyScrossed","check","Crossed Sallydoors"],
	["drawCrossed","check","Crossed drawbridge"],
	["roughCrossed","check","Crossed rough terrain"],
	["stoneCrossed","check","Crossed stone wall"],
	["moatCrossed","check","Crossed moat"],
	["sawCrossed","check","Crossed seasaw"],
	["lowCrossed","check","Crossed lowbar"],
	["rampCrossed","check","Crossedramp"],
	["gateCrossed","check","Crossed gate"],
	["pickedBall","check","Picked up a ball"],
	["startedBall","check","Started w/ ball"],
	["shotBall","radio","Shot ball",["Didn't","Low","High"]],
	["wasntABrick","check","Moved to ramp"],
	["teleHead","head","Teleop"],
	["teleCSally","updown","Crossed sallywood"],
	["teleCRough","updown","Crossed rough terrain"],
	["teleCStone","updown","Crossed stone wall"],
	["teleCMoat","updown","Crossed moat"],
	["teleCSaw","updown","Crossed seasaw"],
	["teleCLow","updown","Crossedlowbar"],
	["teleCRamp","updown","Crossed ramp"],
	["teleCGate","updown","Crossed gate"],
	["ballsPicked","updown","Balls picked up"],
	["lowScored","updown","High scored"],
	["highScored","updown","Low scored"],
	["strategy","radio","Strategy",["Spy", "Defense", "Attack", "Defense" "Destroyer", "Multipurpose", "Other"]],
	["gaveBall","updown","Number of balls given to teammate"],
	["recBall","updown","Number of balls recieved from team"],
	["manipFail","check","Manipulator failure"],
	["explodes","check","Spontaneous combustion"],
	["gotStuck","check","Got stuck"],
	["paperweight","check","Didn't move at all"],
]
doNotStart = False
for arg in sys.argv:
    if arg == "-c":
	doNotStart = True
	print"Really clear database? [y/n]"
	if raw_input() == "y":
		s = sqlite3.connect("MASTERDB")
		m = s.cursor()
		#m.execute("DELETE FROM Data WHERE 1=1")
		m.execute("DROP TABLE IF EXISTS Data")
		s.commit()
		print("Database cleared. Recreating template and continuing with application startup.")
		
		strTable = ""
		for _list in letable:
			strTable = strTable+_list[0]+" INT,"
		m.executescript("CREATE TABLE Data ("+strTable[0:-1]+");")
		s.commit()
		s.close()
		


def get_db():
    sql = getattr(g, 'MASTERDB', None)
    if sql is None:
        sql = g._database = sqlite3.connect("MASTERDB") 
	return sql

@app.route('/')
def clientEnd():

	return render_template('client.html', test="Testing... 1... 2... 3...",letable=letable)

@app.route("/submit", methods=['GET','POST']) #change back to post
def clientSubmit():
	res = []	

	i = -1
	for _ in letable:
		i = i +1
		try:
			req = request.form.get(str(i))
			if req == None:
				req = 0

			res.append( str(int(str(req))) )
		except:
			failure()
			return "<p>Something went wrong with the data. Did you enter text in number boxes? Try hitting the back arrow and resubmitting the data, without text in number boxes.</p><!--you've not caused database errors, the database is sanitized --input is converted to a number before entry-->"
	#insert into db
	
	sql=get_db()
	m=sql.cursor()
        m.execute("INSERT INTO Data VALUES("+str(res)[1:-1]+")")
	sql.commit()

#m.executemany("INSERT INTO Data VALUES("+what+")",res)	
	return "<script>window.history.back()</script><p>Git javascript m8</p></script>"

@app.route("/master")
def serverEnd():
	sql=get_db()
	m=sql.cursor()
	return render_template("server.html",letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(),   alls = m.execute("SELECT * FROM Data ORDER BY teamNum").fetchall()) #BOY, SURE HOPE THIS DOESN'T GET AN DATABASE ERROR
	s.close()
@app.route('/itemSort/<s>')
def itemSort(s):
	s=int(s) #can never be too safe
	sql=get_db()
	m=sql.cursor()
	return render_template("server.html",s=s,itemSort = True,letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(),   alls = m.execute("SELECT teamNum, "+letable[s][0]+" FROM Data ORDER BY teamNum").fetchall()) #BOY, SURE HOPE THIS DOESN'T GET AN DATABASE ERROR
	

@app.route('/teamSort/<s>')
def teamSort(s):
	s=int(s) #can never be too safe
	sql=get_db()
	m=sql.cursor()
	return render_template("server.html",letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(),   alls = m.execute("SELECT * FROM Data WHERE teamNum = "+str(s)+" ORDER BY teamNum").fetchall()) #BOY, SURE HOPE THIS DOESN'T GET AN DATABASE ERROR




#for ty in letable:
#	for 6:
#		addavg data[i][o] 	
@app.route("/avg/<s>")
def brilliance(s):
	s=int(s) #can never be too safe
	sql=get_db()
	m=sql.cursor()
	teamall = m.execute("SELECT * FROM Data WHERE teamNum = "+str    (s)+" ORDER BY teamNum").fetchall()
	fakeall = []
	length = float(len(teamall))
	i = -1
	for ty in letable: #go through letable
		i = i+1 # fake a range for loo
		if ty[1] == "radio": #different method of handling radio buttons
			fakeall.append([]) # we will have a table of avg times radiobutton was checked
			for radios in ty[3]: #iterate thru the optinos and create a 0 value for them
				fakeall[i].append(0)
		else:
			fakeall.append(0.0)#normal
		for o in range(int(length)):
			if ty[1] == "radio":
				#Go to the radio button's table, then go to that specific radio button option that was checked this time arround
				#Add a 1 divided by the total ammount of radio buttons to it if it was checked this time
				#We get which radio button was checked by the value of the the radio button 
				fakeall[i][teamall[o][i]] = fakeall[i][teamall[o][i]] + (1.0/length)
			else:
				fakeall[i] = fakeall[i]+(float(teamall[o][i])/length)
	return render_template("server.html",avg=True,letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(), alls = [fakeall]) #BOY, SURE HOPE THIS DOESN'T GET AN DATABASE ERROR



@app.route("/min/<s>")
def _min(s,_isMax = False):
	s=int(s) #can never be too safe
	sql=get_db()
	m=sql.cursor()
	teamall = m.execute("SELECT * FROM Data WHERE teamNum = "+str    (s)+" ORDER BY teamNum").fetchall()
	fakeall = []
	length = len(teamall)
	i = -1
	for ty in letable:
		i = i+1
		if ty[1] == "radio":
			fakeall.append(-1)
		else:
			fakeall.append(teamall[0][i])
			for o in range(length-1):
				if _isMax:
					fakeall[i] = max(fakeall[i],teamall[o][i])
				else:
					fakeall[i] = min(fakeall[i],teamall[o][i])
	minmax = "min"
	if _isMax:
		minmax = "max"
	return render_template("server.html",minmax=minmax,letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(), alls = [fakeall]) #BOY, SURE HOPE THIS DOESN'T GET AN DATABASE ERROR
@app.route("/max/<s>")
def _max(s):
	return _min(s,True)





if __name__ == '__main__' and not doNotStart:
    app.run(debug=True, host='0.0.0.0',port=82)
