#!/usr/bin/python
#This is a fork of scoutmaster.py with an html frontend, which is a fork of...
#FORK OF SCOUT.PY, TKINTER REMOVED
from flask import Flask,request,send_file,render_template
app = Flask(__name__)
import sqlite3 as sq
import sys

letable = [
        ["roundNum","updown","Round Num"],["teamNum","updown","Team num"],["posi","radio","Position",["Red 1","Red 2","Red 3","Blue 1","Blue 2","Blue 3"]],["sallyScrossed","check","A: Crossed Sallydoors"],["drawCrossed","check","A: Crossed drawbridge"],["roughCrossed","check","A: Crossed rough terrain"],["stoneCrossed","check","A: Crossed stone wall"],["moatCrossed","check","A: Crossed moat"],["sawCrossed","check","A: Crossed seasaw"],["lowCrossed","check","A: Crossed lowbar"],
        ["rampCrossed","check","A: Crossedramp"],["gateCrossed","check","A: Crossed gate"],["pickedBall","check","A:Picked up a ball"],["startedBall","check","A: Started w/ ball"],["shotBall","radio","A: Shot ball",["High","Low","Didn't"]],["teleCSally","updown","Crossed sallywood"],["teleCRough","updown","Crossed rough terrain"],["teleCStone","updown","Crossed stone wall"],["teleCMoat","updown","Crossed moat"],["teleCSaw","updown","Crossed seasaw"],["teleCLow","updown","Crossedlowbar"],["teleCRamp","updown","Crossed ramp"],["teleCGate","updown","Crossed gate"],["ballsPicked","updown","Balls picked up"],["lowScored","updown","High scored"],["highScored","updown","Low scored"],["strategy","radio","Strategy",["Spy", "Defense", "Attack", "Defense" "Destroyer", "Multipurpose", "Other"]],["gaveBall","check","Gave ball to teammate"],["recBall","check","Recieved ball from team"],["gotStuck","check","Got stuck"]
]
class commandline():
    def __init__(self,tdb):
        print("Scoutmaster.py Command-prompt\nExit - Exit\nDump - Dump the masterdb contents\nBdump - More cleanly dump the database contents\nParse - Parse database and dump\nTest - Current testing thing\nHelp - Additional commands\nRescan - Rescan the database\nparse - Parse the data & print a graph\nexcel - Make the masterdb into an excel spreadsheet")

        self.tdb = tdb
    def startInput(self):
        seperation = "      "
        while True:
            inp = raw_input("Scoutmaster> ")
            inp=inp.lower()
            #Very simple, kinda bad command prompt. Just enough to get the job done.
            if inp == "exit":
                break
            elif inp == "dump":
                dmp = self.tdb.dump()
                print(str(dmp)+":")
                for data in dmp:
                    print(data)
            elif inp == "dump ehead":
                for _tab in letable:
                    print(_tab[2] + " Is " + _tab[0])
                print("Done.")
            elif inp == "dump types":
                for _tab in letable:
                    print(_tab[1] + " Is " + _tab[0])
                print("Done.")

            elif inp == "bdump":
                dmp = self.tdb.dump()
                print(str(dmp)+":")
                sys.stdout.write("    ")
                for _tab in letable:                #NAMES
                    sys.stdout.write(_tab[0][0:5]+"|" + seperation[1:len(_tab[0])*-1])
                print
                i = 1;
                sep = "|"
                for data in dmp:
                    if len(data) > 0:
                        _i = str(i)
                        if len(_i) == 1:
                            _i="0"+_i
                        sys.stdout.write(_i+"> ")
                    i=i+1
                    if sep == "|": # Alternate seperators to make reading down lines easier
                        sep = "="
                    else:
                        sep = "|"
                    for rdata in data:              #NUMBERS
                        doet = True;
                        sys.stdout.write(str(rdata) + seperation[1:len(str(rdata))*-1]+sep)
                    print
                print("Done.")
            elif inp == "excel":
                print("Making database into excel spreadsheet...")
                self.tdb.excel()
                print("Done.")

            elif inp == "test":
                print("1.. 2.. 3..")
            elif inp == "help":
                print("Scoutmaster.py Command-prompt\nExit - Exit\nDump (ehead)(types)- Dump the masterdb(or exel header)(or data types) contents\nBdump - More cleanly dump the database contents\nParse - Parse database and dump\nTest - Current testing thing\nHelp - Additional commands\nclear - Clear the screen\ncleardatabase - Clears database, after prompting you to make sure that's what you wanted to do.\nstartg - Starts the GUI\nRescan - Rescan the database\nscout - Launch the scoutingclient\nparse - Parse the data & print a graph\nexcel - Make the masterdb into an excel spreadsheet")
            elif inp == "clear":
                print(chr(27) + "[2J")
            elif inp == "cleardatabase":
                yn = raw_input("DO YOU REALLY WISH TO CLEAR THE MASTER DATABASE? THIS CANNOT BE UNDONE. [y/n] > ")
                yn=yn.lower()
                if yn == "y":
                    print("Clearing database...")
                    print(self.tdb.cleardb())
                    self.tdb.commit()
                    print("Database cleared. RIP in peace.")
                else:
                    print("Database was not cleared.")
            elif inp == "rmrow":
                yn = raw_input("DO YOU REALLY WISH TO DELETE A ROW? THIS CANNOT BE UNDONE. ENTER THE ROW NUMBER OR N TO CANCEL [number/n] > ")
                yn=yn.lower()
                if yn == "n":
                    print("Database was not cleared.")
                else:
                    self.tdb.rmrow(yn)
                    self.tdb.commit()

            elif inp == "rescan":
                self.tdb.databaseImport()
                print("Done.")
            elif inp == "parse":
                parsed = self.tdb.parsenreturn()
                print(parsed)
            elif inp == "scout":
                print("nyi")
            else:
                print("Command not found.")











class _database():
    def __init__(self):
        self.s = sq.connect("MASTERDB") #This will make a very-obvously-declared master database
        self.m = self.s.cursor()
        #self.m.executescript("CREATE TABLE Data IF NOT EXISTS")
        strTable = ""
        for _list in letable:
            strTable = strTable+_list[0]+" INT,"
        print(strTable[0:-1])
        self.m.executescript("CREATE TABLE IF NOT EXISTS Data ("+strTable[0:-1]+");")
    def t1(self):
        self.m.execute("SELECT SQLITE_VERSION()")
        print(self.m.fetchone())
    def commit(self):
        self.s.commit()
    def cleardb(self):
        return self.m.execute("DELETE FROM Data WHERE 1=1")
    def t2(self):
        #`self.m.execute("INSERT INTO data VALUES(2)")
        self.m.execute("SELECT * FROM Data")
        print("test> "+str(self.m.fetchall()))
        print("^^^")
    def dump(self):
        return self.m.execute("SELECT * FROM Data")
    def rmrow(self,row):
        row=str(row)
        self.m.execute("DELETE FROM Data WHERE oid="+row+";")
    def databaseImport(self):
        self.cleardb()
        location = "rawDatabases/"
        print("list " + str(listdir(location)))
        for tfile in listdir(location):
            if tfile[0:1] != ".":

                print("f " + tfile + " ~ " + location + " dat and " + location+tfile)
                curData = sq.connect(location + tfile)
                cur = curData.cursor()
                cur.execute("SELECT * FROM Data")
                _tab = cur.fetchall()
                print("~"+str(_tab))
                for value in _tab:
                    self.m.execute("INSERT INTO Data VALUES"+str(value))
                    print("INSERT INTO Data VALUES"+str(value))

    def setLeVars(self):
        strTable = ""
        for _list in letable:
            strTable = strTable + str(_list[1].get()) + ","
        self.m.execute("INSERT INTO Data VALUES("+strTable[0:-1]+")")
    def parse(self):
        print"temp"
    def getparsed(self):
        return self.parsed
    def parsenreturn(self):
        self.parse()
        return self.getparsed()
    def excel(self):
        workbook   = xlsxwriter.Workbook('EXCELSPREAD.xlsx')

        worksheet1 = workbook.add_worksheet("Main")
        worksheetavg = workbook.add_worksheet("Avg")
        worksheetmin = workbook.add_worksheet("Min")
        worksheetmax = workbook.add_worksheet("Max")
        worksheet2 = workbook.add_worksheet("Graphs")
        #write toprow
        col = 0;
        for _tab in letable:
            worksheet1.write(0, col, _tab[2])
            worksheetavg.write(0,col,_tab[2])
            worksheetmin.write(0,col,_tab[2])
            worksheetmax.write(0,col,_tab[2])
            col = col+1


















        daters = self.m.execute("SELECT * FROM Data")
        leteams = {}
        row = 0
        for extab in daters:
            if not leteams[extab[1]]: #if the team is not already in the teams list
                leteams[extab[1]] = True
            col = -1
            row = row +1
            for data in extab:
                col = col + 1
                if letable[col][1] == "check":
                    if data == 0:
                        worksheet1.write(row,col,"NO")
                    else:
                        worksheet1.write(row,col,"YES")
                elif letable[col][1] == "radio":
                    worksheet1.write(row,col,letable[col][3][data])
                else:
                    worksheet1.write(row,col,data)

        daters = self.m.execute("SELECT FROM Data WHERE teamNum=")

        #worksheet1.write('A1', 123)

        workbook.close()
    def fin(self):
        self.s.commit()
        self.s.close()
db = _database()
###
#db.databaseImport()
db.t2()
didC = False
for arg in sys.argv:
    if arg == "-c":
        didC = True
        cmd = commandline(db)
        cmd.startInput()
if not didC:
    #automated mode
    #db.databaseImport() #impport database
    #db.excel() #Convert to excel spreadsheet
    print("!!!!!!!!!!DONE, JUST OPEN THE EXCEL DOC!!!!!!!!!")



db.fin()
#make template-readable lists

'''theNames = []
varNames = []
types = []

for thing in letable: #name, types, humanname
	varNames.append(thing[0])
	types.append(thing[1])
	theNames.append(thing[2])
'''	
@app.route('/')
def clientEnd():

	return render_template('client.html', test="Testing... 1... 2... 3...",letable=letable)

@app.route("/submit")
	









if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1',port=82)
