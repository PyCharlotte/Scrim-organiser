import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address
me = "unilolscrims@gmail.com"
you = "matthewknight9@hotmail.com"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Scrim Opportunities"
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
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

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

import emailscrims
server=emailscrims.Server()
server.login()
server.send(msg)
server.logoff()
