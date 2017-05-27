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

categorySorter = "Team Number"

layout = {
	"Team Number":{"type":"forumElement","tooltip":"The number of the team you are scouting."},
	"Test":{"type":"forumElement","style":"color: #00ff00;"},
	"Text":{"type":"text","text":"Error: The forum could not be loaded. Please contact your scouting lead.", "style":"color:#00ff00;"},
	"lol":{"type":"pic","image":"lowbar.png"},
	"checktest":{"type":"forumElement"},
	"texttest":{"type":"forumElement"},
	"radiotest":{"type":"forumElement"},
}
layoutOrder = [
	"Team Number","Test","Text","lol","checktest","texttest","radiotest","noexist",
]


formtable = {
	"Team Number":{"type":"updown","ordernum":0},
	"checktest":{"type":"check","ordernum":1},
	"texttest":{"type":"text","ordernum":2},
	"radiotest":{"type":"radio","ordernum":3,"buttons":["first btn","2nd btn","3rd btn"]},

} 
forumOrder = [
	"Team Number","checktest","texttest","radiotest"
]

def clrdb():
	s = sqlite3.connect("MASTERDB")
	m = s.cursor()
	m.execute("DROP TABLE IF EXISTS Data")
	s.commit()

	strTable = ""
	for name in forumOrder:
		if formtable[name]["type"] == "text":
			strTable = strTable+"["+name+"]"+" TEXT,"
		else:
			strTable = strTable+"["+name+"]"+" INT,"
	m.executescript("CREATE TABLE Data ("+strTable[0:-1]+");")
	s.commit()
	s.close()

global sql_question_marks
sql_question_marks = ""
def gen_sql_question_marks():
	for _ in formtable:
		global sql_question_marks
		sql_question_marks = sql_question_marks+"?,"
	sql_question_marks = sql_question_marks[0:-1]

gen_sql_question_marks()


doNotStart = False
secureMode = False
paranoidMode = False
xxs=False
debug = False
masterMode = False
host = '0.0.0.0'
for arg in sys.argv:
	if arg == "-c":
		doNotStart = True
		print"Really clear database? [y/n]"
		if raw_input() == "y":
			clrdb()
			print("Database cleared. Recreating template and quitting.")
	elif arg == "-m":
		masterMode = True
	elif arg == "--help":

		doNotStart = True
		print'''Usage: sudo python scoutmaster.py
Options:
-c	Clear the database
-s	Secure mode--No uploading databases
-p	Paranoid mode--No uploading or using the client
-spam	Create a 200 entries of randomized scouting data
-xxs	Debug option to host on a different port to test uploading databases
-d	Debug mode. You want this if you're modifying code.
-m	Master mode. Disables clear and disables uploading the database to somewhere else'''

	elif arg == "-s": #secure mode
		masterMode = True
		secureMode = True #basically, just turns off the ability to upload SQL databases--useful if you where to be running this on a non-secure network
	elif arg == "-p":
		masterMode = True
		secureMode = True #This is for running this specifically somewhere you really don't want people adding stuff to the database--say you are showing everyone your scouting data.
		paranoidMode = True
	elif arg == "-xxs":
		xxs = True
	elif arg == "-d":
		debug = True
		host = '127.0.0.1'
	elif arg == "-spam":
		doNotStart = True
		allData =[]
		for _ in range(0,200):
			cData = []
			for item in formtable:
				if item[0] == "["+categorySorter+"]":
					cData.append(random.randrange(1000))
				elif item[1] == "radio":
					cData.append(random.randrange(len(item[4])-1))
				elif item[1] == "text":
					cData.append("2lazy4randomtext")
				elif item[1] == "updown":
					cData.append(random.randrange(10))
				else:
					cData.append(random.randrange(0,2))
			allData.append(tuple(cData))
		s = sqlite3.connect("MASTERDB")
		m = s.cursor()
		m.executemany("INSERT INTO Data VALUES ("+sql_question_marks+")",allData)
		m.close()
		s.commit()
		s.close()





if not doNotStart:
	from flask import Flask,request,send_file,render_template,g,Response,send_from_directory
	app = Flask(__name__)
	def get_db():
		sql = getattr(g, 'MASTERDB', None)
		if sql is None:
			sql = g._database = sqlite3.connect("MASTERDB")
		return sql

	@app.route('/')
	def reroute():
		return render_template("redirect.html",url="/client/")

	@app.route('/client/',methods=["POST","GET"])
	def clientEnd(evil = False):
		if paranoidMode:
			return '<!DOCTYPE html><html><head><meta http-equiv=\"refresh\" content=\"0;url=/master\"></head><body><p>Sorry, the host has turned submitting data off.</p></body></html>'
		elif request.method == "POST":
			res = []
			i =-1
			for name in forumOrder:
				i=i+1
				#try:
				var = request.form.get(name)
				if formtable[name]["type"] != "text":
					try:
						var = int(var) #make sure no text is put in in place of a number
					except: #1337 H4X0RS!
						print("fail to get value for "+str(i))
						var = 0
				if var == None:
					var = 0
				res.append(var)
			#insert into db

			sql=get_db()
			m=sql.cursor()
			m.executemany("INSERT INTO Data VALUES("+sql_question_marks+")",[tuple(res)])
			sql.commit()
		return render_template('client.html',formtable=formtable, layout=layout,evil = evil,layoutOrder=layoutOrder)
	@app.route("/allvilliansarelemons/")
	def evil():
		return clientEnd(evil = True)




	@app.route("/master/")
	def serverEnd():
		sql=get_db()
		m=sql.cursor()

		return render_template("server.html",secureMode=secureMode,formtable=formtable, teams = m.execute("SELECT DISTINCT ["+categorySorter+"] FROM Data").fetchall(), alls = m.execute("SELECT * FROM Data ORDER BY ["+categorySorter+"]").fetchall(), layout=layout, forumOrder=forumOrder)
		s.close()
	@app.route('/itemSort/<s>')
	def itemSort(s):
		s=int(s) #can never be too safe
		sql=get_db()
		m=sql.cursor()
		return render_template("server.html",secureMode = secureMode,s=s,itemSort = True,formtable=formtable, teams = m.execute("SELECT DISTINCT ["+categorySorter+"] FROM Data").fetchall(),   alls = m.execute("SELECT ["+categorySorter+"], "+formtable[s][0]+" FROM Data ORDER BY ["+categorySorter+"]").fetchall(), layout=layout, forumOrder=forumOrder)
	@app.route('/itemSortLarge/<s>')
	def itemSort2(s):
		s=int(s) #can never be too safe
		sql=get_db()
		m=sql.cursor()
		return render_template("server.html",secureMode = secureMode,s=s,itemSort = True,formtable=formtable, teams = m.execute("SELECT DISTINCT ["+categorySorter+"] FROM Data").fetchall(),   alls = m.execute("SELECT ["+categorySorter+"], "+formtable[s][0]+" FROM Data ORDER BY "+formtable[s][0]+"").fetchall(), layout=layout, forumOrder=forumOrder)





	@app.route('/teamSort/<s>')
	def teamSort(s):
		s=int(s) #can never be too safe
		sql=get_db()
		m=sql.cursor()
		return render_template("server.html",secureMode = secureMode,formtable=formtable, teams = m.execute("SELECT DISTINCT ["+categorySorter+"] FROM Data").fetchall(),   alls = m.execute("SELECT * FROM Data WHERE ["+categorySorter+"] = "+str(s)+" ORDER BY ["+categorySorter+"]").fetchall(), layout=layout, forumOrder=forumOrder)




	#for ty in formtable:
	#	for 6:
	#		addavg data[i][o]
	@app.route("/avg/<s>")
	def brilliance(s,functioned = False):
		s=int(s) #can never be too safe
		sql=get_db()
		m=sql.cursor()
		teamall = m.execute("SELECT * FROM Data WHERE ["+categorySorter+"] = "+str(s)+" ORDER BY ["+categorySorter+"]").fetchall()
		fakeall = []
		length = float(len(teamall))
		i = -1
		for ty in formtable: #go through formtable
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
		return render_template("server.html",secureMode = secureMode,avg=True,formtable=formtable, teams = m.execute("SELECT DISTINCT ["+categorySorter+"] FROM Data").fetchall(), alls = [fakeall], layout=layout, forumOrder=forumOrder)

	@app.route("/allavg/")
	def allavg():
		sql = get_db()
		m=sql.cursor()
		teams = m.execute("SELECT DISTINCT ["+categorySorter+"] FROM Data").fetchall()
		fakealls=[]
		for team in teams:
			fakealls.append(brilliance(team[0],True))

		return render_template("server.html",secureMode = secureMode,avg=True,formtable=formtable, teams = m.execute("SELECT DISTINCT ["+categorySorter+"] FROM Data").fetchall(), alls = fakealls,allAvg=True, layout=layout, forumOrder=forumOrder)


	@app.route("/min/<s>")
	def _min(s,_isMax = False):
		s=int(s) #can never be too safe
		sql=get_db()
		m=sql.cursor()
		teamall = m.execute("SELECT * FROM Data WHERE ["+categorySorter+"] = "+str	 (s)+" ORDER BY ["+categorySorter+"]").fetchall()
		fakeall = []
		length = len(teamall)
		i = -1
		for ty in formtable:
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
		return render_template("server.html",secureMode = secureMode,minmax=minmax,formtable=formtable, teams = m.execute("SELECT DISTINCT ["+categorySorter+"] FROM Data").fetchall(), alls = [fakeall], layout=layout, forumOrder=forumOrder)
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
			return render_template("msg.html",msg="Sorry, the host has turned off exporting JSON\'d databases.")

		randnum = str(random.randrange(999999))
		_file = open("exportedDb_"+randnum,"w")
		_file.write(jsondb())
		_file.close()
		return render_template("msg.html",msg="Database can be found at exportedDB_"+randnum)


	@app.route("/uploaddb/",methods=["GET","POST"])
	def uploaddb():
		if masterMode:
			return render_template('msg.html',msg='Sorry, the host has turned off uploading JSON\'d databases.')

		#upload our database to the master
		if request.method == "POST":
			ip = request.form.get("ip")
			if ip == "127.0.0.1" or ip=="localhost":
				return render_template("msg.html",msg="Cannot submit to yourself. Find the master IP address.")
			jsoned = jsondb()
			return render_template("uploaddb_ok.html",ip=ip,json=jsoned)

		return render_template("uploaddb.html")

	def jsonToSql(jsoned):
		#get it out of json
		sql = get_db()
		m=sql.cursor()
		data= json.loads(jsoned) # tuple > list is sql ? format
		for listed in data:
			print("INSERT INTO Data VALUES("+sql_question_marks+")",[tuple(listed)])
			m.executemany("INSERT INTO Data VALUES("+sql_question_marks+")",[tuple(listed)])
		m.close()
		sql.commit()
	@app.route("/clear")
	def clearP():
		if masterMode:
			return render_template("msg.html",msg="Sorry, the host has turned off clearing the database.")
		clrdb()
		return render_template("redirect.html",url="/client")
	@app.route("/uploaddb_up/",methods=["POST"])
	def securityVulnerability():
		print("uploaddb_up requerst")
		if secureMode:
			return render_template('msg.html',msg='Sorry, the host has turned off uploading JSON\'d databases.')
		jsoned = request.form.get("json")
		jsonToSql(jsoned)
		return render_template("redirect.html",url="http://127.0.0.1:9001/clear")



	@app.route("/importdbs/")
	def importDbs():
		if secureMode:
			return render_template('msg.html',msg='Sorry, the host has turned off uploading JSON\'d databases.')

		location = "rawDatabases/"
		print("list " + str(listdir(location)))
		for tfile in listdir(location):
			if tfile[0:1] != ".":
				_file = open(location + tfile)
				jsonToSql(_file.read())
				_file.close()


		return "<!DOCTYPE html><html><head><meta http-equiv=\"refresh\" content=\"0;url=/master/\"></head><body><p>Hit the back button on your browser. The redirect failed, however your scouting data was submitted successfully.</p></body></html>" #doesn't really need to be its own file or template.

	@app.route("/layout",methods=['GET','POST'])
	def modify_layout():
		return render_template("modify_layout.html",secureMode=secureMode,formtable=formtable,layout=layout)

	@app.route("/layout_preview") #TODO
	def layout_preview():
		return "TODO"




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
	@app.route("/defstyle.css")
	def defstyle():
		return servefile("defstyle.css","text/css")
	@app.route("/img/<path:path>")
	def img(path):
		response=send_from_directory("img",path)
		#err()
		response.mimetype="image/jpeg" #; error()

		return response





	if __name__ == '__main__' and not doNotStart:
		port =	9001
		if xxs:
			port = 83


		app.run(debug=debug, host=host,port=port)
