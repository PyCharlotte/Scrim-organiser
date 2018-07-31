import emailscrims
import csv

class Team:
    def __init__(self, attributes, freelist):
        self.freelist=freelist

        self.attributes=attributes
        #self.attributes["name"]=name
        #self.attributes["wins"]=wins
        #self.attributes["captain"]=captain
        #self.attributes["email"]=email    

    def findCompatibleTimes(self, other):
        compatible_times=[]
        for timeslot1 in self.freelist:
            for timeslot2 in other.freelist:
                if timeslot1.isSame(timeslot2):
                    compatible_times.append(timeslot1)
        return compatible_times

    def get(self, attribute):
        return self.attributes[attribute]

class Timeslot:
    def __init__(self, day, time):
        self.day=day
        self.time=time

    def __str__(self):
        return self.day+" "+self.time

    def isSame(self, other):
        if self.time==other.time and self.day==other.day:
            return True

def processFirstRow(row):
    for index in range(len(row)):
        if "When are you free?" in row[index]:
            split_point=index-1
            attribute_names=row[:split_point]
    
    times=[]
    #print(split_point)
    #print(row[split_point:])
    for header in row[split_point:]:
        x=header.split("[")[1]
        y=x.split("]")[0]
        times.append(y)
    #print(times)
    return times, attribute_names

def processRow(row, times, attribute_names):
    attributes={}
    for index in range(len(attribute_names)):
        attributes[attribute_names[index]]=row[index]

    freelist=[]
    split_point=len(attribute_names)
    #print(split_point)
    for each in range(len(row[split_point:])):
        days=row[split_point:][each].split(";")
        for day in days:
            if day !="":
                freelist.append(Timeslot(day, times[each]))

    team=Team(attributes, freelist)
    return team  

def getTeams():    
    teams=[]
    with open("scrims.csv") as csvfile:
        reader=csv.reader(csvfile)
        times, attribute_names=processFirstRow(reader.__next__())
        for row in reader:
            teams.append(processRow(row, times, attribute_names))
    return teams
   
teams=getTeams()
msg=emailscrims.PlainTextMessage(teams[0], teams)
eserver=emailscrims.Server()
eserver.login()
#eserver.send(msg)
eserver.logoff()
