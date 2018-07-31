import csvscrims
import emailscrims
import email

def createMessage(team, teams):
    msg=email.message.EmailMessage()
    msg["Subject"]="Scrim Oppurtunities"
    msg["To"]=team.email
    content=""

    for each in teams:
        if each is not team:
            times=team.findCompatibleTimes(each)
            if times!=[]:
                content=content+"\n"+str(each)
                for each2 in times:
                    content=content+str(each2)+"\n"
    print(content)
    msg.set_content(content)
    return msg


    
teams=csvscrims.getTeams()
msg=createMessage(teams[0], teams)
eserver=emailscrims.Server()
eserver.login()
eserver.send(msg)
eserver.logoff()
