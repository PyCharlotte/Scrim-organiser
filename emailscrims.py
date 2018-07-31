import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage

class Server:
    def __init__(self):
        self.address="unilolscrims@gmail.com"
        self.password="iclesports"

    def login(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.address, self.password)

    def send(self, msg):
        msg["From"]="unilolscrims@gmail.com"
        self.server.send_message(msg)

    def logoff(self):
        self.server.quit()#

class PlainTextMessage(EmailMessage):
    def __init__(self, team, teams):
        EmailMessage.__init__(self)
        self["Subject"]="Scrim Oppurtunities"
        self["To"]=team.email
        self.content="""
Hello there!
Please see your potential scrim partners for this week below.

Your Team:
"""

        self.addTeam(team, team.freelist)
        self.content=self.content+"\nPotential Scrim Partners:\n"

        for each in teams:
            if each is not team:
                times=team.findCompatibleTimes(each)
                if times==[]:
                    self.noTeam()
                else:
                    self.addTeam(each,times)
                    self.addTeam(each,times)
        print(self.content)
        self.set_content(self.content)     

    def noTeam(self):
        self.content=self.content+"There were no teams that could scrim with you this week ;(."

    def addTeam(self, team, timeslots):        
##        Name, University
##        Wins: number
##        Avaliable at:        
        details_template="""
%s, %s
Wins: %s
Avaliable at:
"""
        
##        -Day Time
        timeslot_template="-%s %s \n"

        self.content=self.content+str(details_template % (team.getName(),team.getName(), team.getWins()))
        for timeslot in timeslots:
            self.content=self.content+str(timeslot_template % (timeslot.day, timeslot.time))
        
##      Contact captain at email
        contact_template="Contact %s at %s \n"
        self.content=self.content+str(contact_template % (team.getCaptain(), team.getEmail()))

class HTMLMessage(MIMEMultipart):
    def __init__(self, team):
        MIMEMultipart.__init__(self)
        self.team=team
        self.initHeaders()
        self.initText()
        self.initHTML()
        self.join()

    def initHeaders(self):
        self['Subject'] = "Potential Scrims"
        self['To'] = self.team.getEmail()

    def initText(self):
        self.text="test"

    def initHTML(self):
        self.html= """\
                    <html>
                      <head></head>
                      <body>
                    <p>Hello there!</p>
                    <p>Please see your potential scrim partners for this week below.</p>
                    <p><span style="text-decoration: underline;">Your Team</span></p>
                    <p><strong>Name&nbsp;</strong><em>University</em></p>
                    <p>Wins : number</p>
                    <p>Avaliable at:</p>
                    <ul>
                    <li>Day 1 Time 1</li>
                    <li>Day 2 Time 2</li>
                    </ul>
                    <p><span style="text-decoration: underline;">Potential Scrim Partners</span></p>
                    <p><strong>Name&nbsp;</strong><em>University</em></p>
                    <p>Wins : number</p>
                    <p>Avaliable at:</p>
                    <ul>
                    <li>Day 1 Time 1</li>
                    <li>Day 2 Time 2</li>
                    </ul>
                    <p>Contact Matthew Knight at <a href="mailto:mdk16@ic.ac.uk">mdk16@ic.ac.uk</a></p>
                    <p>&nbsp;</p>
                    <p><strong>Name&nbsp;</strong><em>University</em></p>
                    <p>Wins : number</p>
                    <p>Avaliable at:</p>
                    <ul>
                    <li>Day 1 Time 1</li>
                    <li>Day 2 Time 2</li>
                    </ul>
                    <p>Contact Name at email</p>
                    <p>&nbsp;</p>
                    <p>Good luck and have fun,</p>
                    <p>ICLeSports</p>
                    <p>&nbsp;<img src="https://s15.postimg.cc/guevyxdaj/e_Sports-logo-no-outline.png" alt="" width=
                      </body>
                    </html>
                    """

    def join(self):
        part1=MIMEText(self.text, 'plain')
        part2=MIMEText(self.html, 'html')
        self.attach(part1)
        self.attach(part2)
