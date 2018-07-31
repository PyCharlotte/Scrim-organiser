import emailscrims
import csv

class Team:
    def __init__(self, name, wins, captain, email, freelist):
        self.name=name
        self.wins=wins
        self.captain=captain
        self.email=email
        self.freelist=freelist

    def __str__(self):
        return self.name+"\n"+self.wins+"\n"+self.captain+"\n"+self.email+"\n"
        #return string

    def getName(self):
        return self.name

    def getWins(self):
        return self.wins

    def getCaptain(self):
        return self.captain

    def getEmail(self):
        return self.email

    def findCompatibleTimes(self, other):
        compatible_times=[]
        for timeslot1 in self.freelist:
            for timeslot2 in other.freelist:
                if timeslot1.isSame(timeslot2):
                    compatible_times.append(timeslot1)
        return compatible_times

class Timeslot:
    def __init__(self, day, time):
        self.day=day
        self.time=time

    def __str__(self):
        return self.day+" "+self.time

    def isSame(self, other):
        if self.time==other.time and self.day==other.day:
            return True

def getTimes(row):    
    times=[]
    for each in row[5:]:
        x=each.split("[")[1]
        y=x.split("]")[0]
        times.append(y)
    return times

def processRow(row, times):
    name=row[1]
    wins=row[2]
    captain=row[3]
    email=row[4]

    freelist=[]
    for each in range(len(row[5:])):
        days=row[5:][each].split(";")
        for day in days:
            freelist.append(Timeslot(day, times[each]))

    team=Team(name, wins, captain, email, freelist)
    return team  

def getTeams():    
    teams=[]
    with open("scrims.csv") as csvfile:
        reader=csv.reader(csvfile)
        times=getTimes(reader.__next__())
        for row in reader:
            teams.append(processRow(row, times))
    return teams
   
teams=getTeams()
msg=emailscrims.PlainTextMessage(teams[0], teams)
eserver=emailscrims.Server()
eserver.login()
eserver.send(msg)
eserver.logoff()
