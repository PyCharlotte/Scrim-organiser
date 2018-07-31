import emailscrims
import csv

class Team:
    def __init__(self, attributes, freelist):
        self.freelist=freelist
        self.attributes=attributes
        self.compatible_teams=[]

    def findCompatibleTimes(self, other):
        compatible_times=[]
        for timeslot1 in self.freelist:
            for timeslot2 in other.freelist:
                if timeslot1.isSame(timeslot2):
                    compatible_times.append(timeslot1)
        if compatible_times != []:
            self.compatible_teams.append([other, compatible_times])

    def get(self, attribute):
        return self.attributes[attribute]

    def getCompatibleTeams(self):
        return self.compatible_teams

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
    """
    Processes the first row of the csv file.
    This find out what attributes are being given and how many
    possible times of the day there are.
    """
    
    for index in range(len(row)):
        if "When are you free?" in row[index]:
            split_point=index-1
            attribute_names=row[:split_point]
    
    times=[]    
    for header in row[split_point:]:
        x=header.split("[")[1]
        y=x.split("]")[0]
        times.append(y)    
    return times, attribute_names

def processRow(row, times, attribute_names):
    """
    Processes subsequent rows of the csv file.
    Encapsulates the team's attributes (details) and the times (timeslots)
    they are free in a Team object.
    """
    
    attributes={}
    for index in range(len(attribute_names)):
        attributes[attribute_names[index]]=row[index]

    freelist=[]
    split_point=len(attribute_names)    
    for time_index in range(len(row[split_point:])):
        days=row[split_point:][time_index].split(";")
        for day in days:
            if day !="":
                freelist.append(Timeslot(day, times[time_index]))

    team=Team(attributes, freelist)
    return team  

def getTeams():
    """
    Processes all rows to generate a list of team objects.
    """
    
    teams=[]
    with open("scrims.csv") as csvfile:
        reader=csv.reader(csvfile)
        times, attribute_names=processFirstRow(reader.__next__())
        for row in reader:
            teams.append(processRow(row, times, attribute_names))
    return teams

def findCompatibilities(teams):
    """
    For each team, determines which other teams have the same
    timeslots free
    """
    for team in teams:
        for other_team in teams:
            if team is not other_team:
                team.findCompatibleTimes(other_team)

def main():    
    teams=getTeams()
    findCompatibilities(teams)
    msgs=[]
    for team in teams:
        msgs.append(emailscrims.PlainTextMessage(team))

    eserver=emailscrims.Server()
    eserver.login()
    for msg in msgs:
        print(msg)
        #eserver.send(msg)
    eserver.logoff()

def main2():
    teams=getTeams()
    findCompatibilities(teams)
    msgs=[]
    for team in teams:
        msgs.append(emailscrims.HTMLMessage(team))

    eserver=emailscrims.Server()
    eserver.login()
    for msg in msgs:
        print(msg)
        eserver.send(msg)
    eserver.logoff()

if __name__=="__main__":
    main2()
