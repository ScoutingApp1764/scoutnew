#!/usr/bin/python
#This is a fork of scoutmaster.py with an html frontend, which is a fork of...
#FORK OF SCOUT.PY, TKINTER REMOVED
import sqlite3
from flask import Flask,request,send_file,render_template,g
app = Flask(__name__)
import sys

didC = False
for arg in sys.argv:
    if arg == "-c":
	print"Really clear database? [y/n]"
	if raw_input() == "y":
		s = sqlite3.connect("MASTERDB")
		m = s.cursor()
		m.execute("DELETE FROM Data WHERE 1=1")
		s.commit()
		s.close()
		print("Database cleared. Recreating template and continuing with application startup.")
		self.s = sq.connect("MASTERDB") #This will make a very-obvously-declared master database
		self.m = self.s.cursor()
		#self.m.executescript("CREATE TABLE Data IF NOT EXISTS")
		strTable = ""
		for _list in letable:
			strTable = strTable+_list[0]+" INT,"
			print(strTable[0:-1])
			self.m.executescript("CREATE TABLE IF NOT EXISTS Data ("+strTable[0:-1]+");")

letable = [
        ["roundNum","updown","Round Num"], #Syntax: Variable Name, type, human name, [radiobutton options]
	["teamNum","updown","Team num"],
	["posi","radio","Position",["Red 1","Red 2","Red 3","Blue 1","Blue 2","Blue 3"]], #Here is a radiobutton-the extra table is the choices for the radiobutton.
	["sallyScrossed","check","A: Crossed Sallydoors"],
	["drawCrossed","check","A: Crossed drawbridge"],
	["roughCrossed","check","A: Crossed rough terrain"],
	["stoneCrossed","check","A: Crossed stone wall"],
	["moatCrossed","check","A: Crossed moat"],
	["sawCrossed","check","A: Crossed seasaw"],
	["lowCrossed","check","A: Crossed lowbar"],
	["rampCrossed","check","A: Crossedramp"],
	["gateCrossed","check","A: Crossed gate"],
	["pickedBall","check","A:Picked up a ball"],
	["startedBall","check","A: Started w/ ball"],
	["shotBall","radio","A: Shot ball",["High","Low","Didn't"]],
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
	["gaveBall","check","Gave ball to teammate"],
	["recBall","check","Recieved ball from team"],
	["manipFail","check","Manipulator failure"],
	["explodes","check","Spontaneous combustion"],
	["gotStuck","check","Got stuck"]
]
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
	print(request.form.get("0"))
	res = []	

	i = -1
	for _ in letable:
		i = i +1
		try:
			req = request.form.get(str(i))
			if req == None:
				req = 0

			res.append( str(int(str(req))) )
			print(str(i))
			print("="+res[i])
			print(str(i) == "29")
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
	length = len(teamall)
	i = -1
	for ty in letable:
		i = i+1
		fakeall.append(0)
		for o in range(length-1):
			fakeall[i] = fakeall[i]+(teamall[o][i]/length)
	

	#purposeerror()
	return render_template("server.html",letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(), alls = fakeall) #BOY, SURE HOPE THIS DOESN'T GET AN DATABASE ERROR



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=82)
    #get_db().close() 
