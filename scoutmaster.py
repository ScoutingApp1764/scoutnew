#!/usr/bin/python
#This is a fork of scoutmaster.py with an html frontend, which is a fork of...
#FORK OF SCOUT.PY, TKINTER REMOVED
from flask import Flask,request,send_file,render_template
app = Flask(__name__)
import sqlite3 as sq
import sys

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
	["gotStuck","check","Got stuck"]
]
didC = False
for arg in sys.argv:
    if arg == "-c":
	print"ur a dum"

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
		#try:
		req = request.form.get(str(i))
		if req == None:
			req = 0

		res.append( str(int(str(req))) )
		print(str(i))
		print("="+res[i])
		print(str(i) == "29")
		#except:
		#	failure()
		#	return "<p>Something went wrong with the data. Did you enter text in number boxes? Try hitting the back arrow and resubmitting the data, without text in number boxes.</p><!--you've not caused database errors, the database is sanitized --input is converted to a number before entry-->"
	#insert into db
	
	sql = sq.connect("MASTERDB")
	m=sql.cursor()
        m.execute("INSERT INTO Data VALUES("+str(res)[1:-1]+")")
	sql.commit()
	sql.close()

#m.executemany("INSERT INTO Data VALUES("+what+")",res)	
	return "<script>window.history.back()</script><p>Git javascript m8</p></script>"

sql=sq.connect("MASTERDB")
@app.route("/master")
def serverEnd():
	m=sql.cursor()
	return render_template("server.html",letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(),   alls = m.execute("SELECT * FROM Data ORDER BY teamNum").fetchall()) #BOY, SURE HOPE THIS DOESN'T GET AN DATABASE ERROR
	s.close()
@app.route('/itemSort/<s>')
def itemSort(s):
	s=int(s) #can never be too safe
	sql=sq.connect("MASTERDB")
	m=sql.cursor()
	return render_template("server.html",s=s,itemSort = True,letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(),   alls = m.execute("SELECT teamNum, "+letable[s][0]+" FROM Data ORDER BY teamNum").fetchall()) #BOY, SURE HOPE THIS DOESN'T GET AN DATABASE ERROR
	sql.close()
	

@app.route('/teamSort/<s>')
def teamSort(s):
	s=int(s) #can never be too safe
	sql=sq.connect("MASTERDB")
	m=sql.cursor()
	return render_template("server.html",letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(),   alls = m.execute("SELECT * FROM Data WHERE teamNum = "+str(s)+" ORDER BY teamNum").fetchall()) #BOY, SURE HOPE THIS DOESN'T GET AN DATABASE ERROR








if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=82)
