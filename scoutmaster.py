#!/usr/bin/python
#This is a fork of scoutmaster.py with an html frontend, which is a fork of...
#FORK OF SCOUT.PY, TKINTER REMOVED
import string
import json
import random
import sqlite3
import sys
from os import listdir


#Syntax: Variable Name, type, human name, [radiobutton options]. Variable names really only help with teamNum and if fort debugging via interacting with the database directly
letable = [
	["teamNum","updown","Team num","The team number"],
        ["roundNum","updown","Round Num","The round number"], 
	["isRed","check","Is on red team","Is the robot on the red team?"],
	["posi","radio","Position","The position--starting from the closest to you and going to the farthest--the robot is in",["Position 1","Position 2","Position 3"]], 
	["autoHead","head","Autonomous"],
	["sallyScrossed","check","Crossed Sallyport","Wheather the robot crossed the sallyport in autonomous"],
	["drawCrossed","check","Crossed drawbridge","Wheather the robot crossed the drawbridge in autonomous"],
	["roughCrossed","check","Crossed rough terrain","Wheather the robot crossed the rought terrain in autonomous"],
	["stoneCrossed","check","Crossed stone wall","Wheather the robot crossed the stone wall in autonomous"],
	["moatCrossed","check","Crossed moat","Wheather the robot crossed the moat in autonomous"],
	["sawCrossed","check","Crossed seasaw","Wheather the robot crossed the seasaw in autonomous"],
	["lowCrossed","check","Crossed lowbar","Wheather the robot crossed the lowbar in autonomous"],
	["rampCrossed","check","Crossed ramp","Wheather the robot crossed the ramp in autonomous"],
	["gateCrossed","check","Crossed gate", "Wheather the robot crossed the gate in autonomous"],
	["pickedBall","check","Picked up a ball","Did the robot pick up a ball in autonomous?"],
	["startedBall","check","Started w/ ball","Did the robot start with a ball in autonomous?"],
	["shotBall","radio","Shot ball","Did the robot shoot a ball in autonomous? Where?",["Didn't","Low","High"]],
	["wasntABrick","check","Moved to ramp","Did the robot move to the ramp in autonomous?"],
	["teleHead","head","Teleop"],
	["teleCSally","updown","Crossed sallyport","Number of times the robot crossed the sallyport in teleop"],
	["teleCRough","updown","Crossed rough terrain","Number of times the robot crossed the rough terrain in teleop"],
	["teleCStone","updown","Crossed stone wall","Number of times the robot crossed the stone wall in teleop"],
	["teleCMoat","updown","Crossed moat","Number of times the robot crossed the moat in teleop"],
	["teleCSaw","updown","Crossed seasaw","Number of times the robot crossed the seasaw in teleop"],
	["teleCLow","updown","Crossed lowbar","Number of times the robot crossed the lowbar in teleop"],
	["teleCRamp","updown","Crossed ramp","Number of times the robot crossed the ramp in teleop"],
	["teleCGate","updown","Crossed gate","Number of times the robot crossed the gate in teleop"],
	["ballsPicked","updown","Balls picked up","Number of times the robot picked up a ball in teleop"],
	["lowScored","updown","High scored","Number of times the robot scored in the high goal in teleop"],
	["highScored","updown","Low scored","Number of times the robot scored in the low goal in teleop"],
	["strategy","radio","Strategy","Strategy deployed. Be sure to fill in \"other\" ONLY if you checked it on here.",["Spy", "Defense", "Attack", "Defense" "Destroyer", "Multipurpose", "Other"]],
	["strategyOther","text","Other textbox (leave blank if not other)","Fill this in ONLY if you checked other above. Be concise."],
	["gaveBall","updown","Number of balls given to teammate","Did the robot give a ball to another teammate?"],
	["recBall","updown","Number of balls recieved from team","Did the robot recieve a ball from another teammate?"],
	["scaledTower","check","Climbed tower","Did the robot climb the tower during the last 30 seconds?"],
	["manipFail","check","Manipulator failure","Did the robot's manipulator fail technically or physically (not an operator error) during operation?"],
	["explodes","check","Spontaneous combustion","Did the robot sustain battery damaged, sparking wires, or fire during operation?"],
	["gotStuck","check","Got stuck","Did the robot get itself in a position where it struggled significantly or did not get out of?"],
	["paperweight","check","Didn't move at all","Was the robot a paperweight?"],
]
what = ""
for _ in letable:
	what = what+"?,"
what = what[0:-1]
doNotStart = False
secureMode = False
paranoidMode = False
xxs=False
for arg in sys.argv:
    if arg == "-c":
	doNotStart = True
	print"Really clear database? [y/n]"
	if raw_input() == "y":
		s = sqlite3.connect("MASTERDB")
		m = s.cursor()
		m.execute("DROP TABLE IF EXISTS Data")
		s.commit()
		print("Database cleared. Recreating template and quitting.")
		
		strTable = ""
		for _list in letable:
			if _list[1] == "text":
				strTable = strTable+_list[0]+" TEXT,"
			else: 
				strTable = strTable+_list[0]+" INT,"
		m.executescript("CREATE TABLE Data ("+strTable[0:-1]+");")
		s.commit()
		s.close()
    elif arg == "--help":
	doNotStart = True
	print'''Usage: sudo python scoutmaster.py
Options:
-c	Clear the database
-s	Secure mode--No uploading databases
-p 	Paranoid mode--No uploading or using the client
-spam	Create a 200 entries of randomized scouting data
-xxs	Debug option to host on a different port to test uploading databases'''
	
    elif arg == "-s": #secure mode
	secureMode = True #basically, just turns off the ability to upload SQL databases--useful if you where to be running this on a non-secure network
    elif arg == "-p":
	secureMode = True #This is for running this specifically somewhere you really don't want people adding stuff to the database--say you are showing everyone your scouting data.
	paranoidMode = True
    elif arg == "-xxs":
	xxs = True
    elif arg == "-spam":
	allData =[]
	for _ in range(0,25):
		cData = []
		for item in letable:
			if item[0] == "teamNum":
				cData.append(random.randrange(1000)) 
			elif item[1] == "radio":
				cData.append(random.randrange(len(item[4])-1))
			elif item[1] == "text":
				cData.append("2lazy4randomtext")
			elif item[1] == "updown":
				cData.append(random.randrange(10))
			else:
				cData.append(random.randrange(1))
		allData.append(tuple(cData))
	s = sqlite3.connect("MASTERDB")
	m = s.cursor()
	m.executemany("INSERT INTO Data VALUES ("+what+")",allData)
	m.close()
	s.commit()
	s.close()

		
	
		
		
if not doNotStart:
	from flask import Flask,request,send_file,render_template,g,Response
	app = Flask(__name__)
	def soap(washed): #!!!!!!!!!!!!!!!!!canidate for deletion!!!!!!!!!!!!!!!!!!!!!!!!!!1
		washed = str(washed) #scrub off any unicode. Okay, actually, probably throw an error for unicode. Better than an incident with the database.
		string.replace(washed,"\x00","NUL") #Nullify any null-character attempts
		string.replace(washed,'"','""') #no little bobby tables	
		string.replace(washed,"'","''") #no little bobby tables	
		return washed


	def get_db():
	    sql = getattr(g, 'MASTERDB', None)
	    if sql is None:
		sql = g._database = sqlite3.connect("MASTERDB") 
		return sql

	@app.route('/')
	def clientEnd():
		if paranoidMode:
			return '<!DOCTYPE html><html><head><meta http-equiv=\"refresh\" content=\"0;url=/master\"></head><body><p>Sorry, the host has turned submitting data off.</p></body></html>'
		return render_template('client.html',letable=letable)


	#this will be used in clientSubmit and in the sql submitting

	@app.route("/submit", methods=['POST']) #change back to post
	def clientSubmit():
		if paranoidMode:
			return '<!DOCTYPE html><html><head></head><body><p>Sorry, the host has turned submitting data off.</p></body></html>'
		res = []
		i = -1
		for ty in letable:
			i = i +1
			#try:
			var = request.form.get(str(i))
			if ty[1] != "text":
				try:
					var = str(int(var)) #make sure no text is put in in place of a number
				except: #1337 H4X0RS!
					var = 0
			if var == None:
				var = 0
			res.append(var)
			#except:
			#	return "<p>Something went wrong with the data. Did you enter text in number boxes? Try hitting the back arrow and resubmitting the data, without text in number boxes.</p><!--you've not caused database errors, the database is sanitized"
		#insert into db
		
		sql=get_db()
		m=sql.cursor()
		m.executemany("INSERT INTO Data VALUES("+what+")",[tuple(res)])
		sql.commit()

	#m.executemany("INSERT INTO Data VALUES("+what+")",res)	
		return "<!DOCTYPE html><html><head><meta http-equiv=\"refresh\" content=\"0;url=/#top\"></head><body><p>Hit the back button on your browser. The redirect failed, however your scouting data was submitted successfully.</p></body></html>" #doesn't really need to be its own file or template. 

	@app.route("/master/")
	def serverEnd():
		sql=get_db()
		m=sql.cursor()
		return render_template("server.html",secureMode=secureMode,letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(),   alls = m.execute("SELECT * FROM Data ORDER BY teamNum").fetchall()) 
		s.close()
	@app.route('/itemSort/<s>')
	def itemSort(s):
		s=int(s) #can never be too safe
		sql=get_db()
		m=sql.cursor()
		return render_template("server.html",secureMode = secureMode,s=s,itemSort = True,letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(),   alls = m.execute("SELECT teamNum, "+letable[s][0]+" FROM Data ORDER BY teamNum").fetchall()) 
		

	@app.route('/teamSort/<s>')
	def teamSort(s):
		s=int(s) #can never be too safe
		sql=get_db()
		m=sql.cursor()
		return render_template("server.html",secureMode = secureMode,letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(),   alls = m.execute("SELECT * FROM Data WHERE teamNum = "+str(s)+" ORDER BY teamNum").fetchall()) 




	#for ty in letable:
	#	for 6:
	#		addavg data[i][o] 	
	@app.route("/avg/<s>")
	def brilliance(s,functioned = False):
		s=int(s) #can never be too safe
		sql=get_db()
		m=sql.cursor()
		teamall = m.execute("SELECT * FROM Data WHERE teamNum = "+str(s)+" ORDER BY teamNum").fetchall()
		fakeall = []
		length = float(len(teamall))
		i = -1
		for ty in letable: #go through letable
			i = i+1 # fake a range for loo
			if ty[1] == "radio": #different method of handling radio buttons
				fakeall.append([]) # we will have a table of avg times radiobutton was checked
				for radios in ty[4]: #iterate thru the optinos and create a 0 value for them
					fakeall[i].append(0.0)
			else:
				fakeall.append(0.0)#normal
			for o in range(int(length)):
				if ty[1] == "radio":
					#Go to the radio button's table, then go to that specific radio button option that was checked this time arround
					#Add a 1 divided by the total ammount of radio buttons to it if it was checked this time
					#We get which radio button was checked by the value of the the radio button 
					try:
						fakeall[i][teamall[o][i]] = fakeall[i][teamall[o][i]] + (1.0/length)
					except:
						fakeall[i][teamall[o][i]] = "An error occured while trying to average this data"
				elif ty[1] == "text":
					fakeall[i] = "Cannot average text fields."
				else:
					try:
						fakeall[i] = fakeall[i]+(float(teamall[o][i])/length)
					except:
						fakeall[i] = "An error occured while trying to average this data"
		if functioned:
			return fakeall
		return render_template("server.html",secureMode = secureMode,avg=True,letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(), alls = [fakeall]) 

	@app.route("/allavg/")
	def allavg():
		sql = get_db()
		m=sql.cursor()
		teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall()
		fakealls=[]
		for team in teams:
			fakealls.append(brilliance(team[0],True))
		
		return render_template("server.html",secureMode = secureMode,avg=True,letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(), alls = fakealls)


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
					try:
						if _isMax:
							fakeall[i] = max(fakeall[i],teamall[o][i])
						else:
							fakeall[i] = min(fakeall[i],teamall[o][i])
					except:
						fakeall[i] = "An error occured while trying to min or max this data"
		minmax = "min"
		if _isMax:
			minmax = "max"
		return render_template("server.html",secureMode = secureMode,minmax=minmax,letable=letable, teams = m.execute("SELECT DISTINCT teamNum FROM Data").fetchall(), alls = [fakeall]) 
	@app.route("/max/<s>")
	def _max(s):
		return _min(s,True)

	def jsondb():
		sql = get_db()
		m=sql.cursor()
		sqall = m.execute("SELECT * FROM Data").fetchall()
		return json.dumps(sqall,sort_keys = False)		

	@app.route("/exportdb/")
	def exportdb():
		if secureMode:
			return '<!DOCTYPE html><html><head></head><body><p>Sorry, the host has turned off exporting JSON\'d databases.</p></body></html>'

		_file = open("exportedDb_"+str(random.randrange(9999)),"w")
		_file.write(jsondb())
		_file.close()
		return '<!DOCTYPE html><html><head></head><body><p>Database can be found at exportedDB_ and then a random number.</p></body></html>'


	@app.route("/uploaddb/",methods=["GET","POST"])
	def uploaddb():
		#upload our database to the master
		if request.method == "POST":
			ip = request.form.get("ip")
			json = jsondb()			
			return render_template("uploaddb_ok.html",ip=ip,json=jsoned)

		return render_template("uploaddb.html")
			
	def jsonToSql(jsoned):
		#get it out of json
		sql = get_db()
		m=sql.cursor()
		data= json.loads(jsoned) # tuple > list is sql ? format
		for listed in data:
			print("INSERT INTO Data VALUES("+what+")",[tuple(listed)])
			m.executemany("INSERT INTO Data VALUES("+what+")",[tuple(listed)])
		m.close()
		sql.commit()

	@app.route("/importdbs/")
	def importDbs():
		if secureMode:
			return '<!DOCTYPE html><html><head></head><body><p>Sorry, the host has turned off uploading JSON\'d databases.</p></body></html>'#well, when you put it like that it makes me want to turn it off always
			
		location = "rawDatabases/"
		print("list " + str(listdir(location)))	
		for tfile in listdir(location):
			if tfile[0:1] != ".":
				_file = open(location + tfile)
				jsonToSql(_file.read())
				_file.close()


		return "<!DOCTYPE html><html><head><meta http-equiv=\"refresh\" content=\"0;url=/master/\"></head><body><p>Hit the back button on your browser. The redirect failed, however your scouting data was submitted successfully.</p></body></html>" #doesn't really need to be its own file or template. 


	@app.route("/uploaddb_up/",methods=["POST"])
	def securityVulnerability():
		print("uploaddb_up requerst")
		if secureMode:
			return '<!DOCTYPE html><html><head></head><body><p>Sorry, the host has turned off uploading JSON\'d databases.</p></body></html>'#well, when you put it like that it makes me want to turn it off always
		jsoned = request.form.get("json")
		jsontoSql(jsoned)
		return "<!DOCTYPE html><html><head><meta http-equiv=\"refresh\" content=\"0;url=/#top\"></head><body><p>Hit the back button on your browser. The redirect failed, however your scouting data was submitted successfully.</p></body></html>" #doesn't really need to be its own file or template. 


	
	def servefile(path,mime):
		_file = open(path,"r")
		_res = _file.read()
		_file.close()
		resp = Response(response=_res,
                	status=200,
                	mimetype=mime
		)
		return resp

	@app.route("/Chart.js")
	def chartjs():
		return servefile("Chart.js","text/javascript")	
	@app.route("/bootstrap.min.js")
	def bootJs():
		return servefile("bootstrap.min.js","text/javascript")
	@app.route("/bootstrap.min.css")
	def bootCss():
		return servefile("bootstrap.min.css","text/css")
	@app.route("/jquery.min.js")
	def jqJs():
		return servefile("jquery.min.js","text/javascript")
	




	if __name__ == '__main__' and not doNotStart:
		port =	82
		if xxs:
			port = 83
		
		app.run(debug=True, host='0.0.0.0',port=port)
