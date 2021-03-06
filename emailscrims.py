import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage

class Server:
    def __init__(self):
        self.address="unilolscrims@gmail.com"
        self.password=input("Email password: ")

    def login(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        try:
            self.server.login(self.address, self.password)
        except smtplib.SMTPAuthenticationError:
            print("Probably an incorrect password")
            raise Exception("Login fail")

    def send(self, msg):
        msg["From"]="unilolscrims@gmail.com"
        self.server.send_message(msg)

    def logoff(self):
        self.server.quit()

class PlainTextMessage(EmailMessage):
    def __init__(self, team):
        EmailMessage.__init__(self)
        self["Subject"]="Scrim Oppurtunities"
        self["To"]=team.get("Your Email")
        self.content="""
Hello there!
Please see your potential scrim partners for this week below.

Your Team:
"""

        self.addTeam(team, team.freelist)
        self.content=self.content+"\nPotential Scrim Partners:\n"
   
        compatible_teams=team.getCompatibleTeams()
        if compatible_teams!=[]:
            for pair in compatible_teams:
                self.addTeam(pair[0],pair[1])
        else:        
            self.noTeam()
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

        self.content=self.content+str(details_template % (team.get("Team Name"),team.get("University"), team.get("Wins in NUEL")))
        for timeslot in timeslots:
            self.content=self.content+str(timeslot)+"\n"
        
##      Contact captain at email
        contact_template="Contact %s at %s or use IGN: %s \n"
        self.content=self.content+str(contact_template % (team.get("Your Name"), team.get("Your Email"), team.get("Your IGN")))

class HTMLMessage(MIMEMultipart):
    def __init__(self, team):
        MIMEMultipart.__init__(self, "alternative")
        self.team=team
        self.initHeaders()
        self.initText()
        self.initHTML()
        self.join()

    def initHeaders(self):
        self['Subject'] = "Potential Scrims"
        self['To'] = self.team.get("Your Email")

    def initText(self):
        plain_msg=PlainTextMessage(self.team)
        self.text=plain_msg.get_content()

    def addTeam(self, team, freelist):
##        <p><strong>Name&nbsp;</strong><em>University</em></p>
##        <p>Wins : number</p>
##        <p>Avaliable at:</p>
        details_template="""
                        <p><strong>%s&nbsp;</strong><em>%s</em></p>
                        <p>Wins : %s</p>
                        <p>Avaliable at:</p>
                        """
        self.html=self.html+str(details_template % (team.get("Your Name"),team.get("University"),team.get("Wins in NUEL")))

        self.html=self.html+"""
                            <ul>
                            """
        timeslot_template="""
                          <li>%s</li>
                          """
        for timeslot in freelist:            
            self.html=self.html+str(timeslot_template % timeslot)

        self.html=self.html+"""
                            </ul>
                            """
##        <p>Contact Matthew Knight at <a href="mailto:mdk16@ic.ac.uk">mdk16@ic.ac.uk</a></p>
##        <p>&nbsp;</p>
        contact_template="""
                         <p>Contact %s at <a href="mailto:%s">%s</a></p>
                         <p>&nbsp;</p>
                         """
        self.html=self.html+str(contact_template % (team.get("Your Name"),team.get("Your Email"), team.get("Your Email")))

    def noTeam(self):
        self.html=self.html+"""
                            <p>There were no teams that could scrim with you this week ;(.</p>
                            """

    def initHTML(self):
        self.html= """\
                    <html>
                      <head></head>
                      <body>
                    <p>Hello there!</p>
                    <p>Please see your potential scrim partners for this week below.</p>
                    <p><span style="text-decoration: underline;">Your Team</span></p>
                    """
        self.addTeam(self.team, self.team.freelist)

        self.html=self.html+"""
                            <p><span style="text-decoration: underline;">Potential Scrim Partners</span></p>
                            """
        compatible_teams=self.team.getCompatibleTeams()
        if compatible_teams != []:
            for pair in compatible_teams:
                self.addTeam(pair[0],pair[1])
        else:
            self.noTeam()

        self.html=self.html+"""        
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
