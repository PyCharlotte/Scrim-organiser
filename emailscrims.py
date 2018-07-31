import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        self.server.quit()

class Message(MIMEMultipart):
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
