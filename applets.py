import time
import datetime
from requests import get
import os
from bs4 import BeautifulSoup
import qrcode
import cv2
import pywhatkit as kit
import speedtest
import pyjokes
from pywikihow import search_wikihow
import webbrowser
import wikipedia
from pytube import YouTube
import PyPDF2
import smtplib
import instaloader
import psutil

#Wish
def wish(self):
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M %p")
    day = self.Cal_day()
    print(t)
    if (hour>=0) and (hour <=12) and ('AM' in t):
        self.engine.talk(f'Good morning boss, its {day} and the time is {t}')
    elif (hour >= 12) and (hour <= 16) and ('PM' in t):
        self.engine.talk(f"good afternoon boss, its {day} and the time is {t}")
    else:
        self.engine.talk(f"good evening boss, its {day} and the time is {t}")

#Weather forecast
def temperature(self):
    IP_Address = get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/'+IP_Address+'.json'
    geo_reqeust = get(url)
    geo_data = geo_reqeust.json()
    city = geo_data['city']
    search = f"temperature in {city}"
    url_1 = f"https://www.google.com/search?q={search}"
    r = get(url_1)
    data = BeautifulSoup(r.text,"html.parser")
    temp = data.find("div",class_="BNeawe").text
    self.engine.talk(f"current {search} is {temp}")

#qrCodeGenerator
def qrCodeGenerator(self):
    self.engine.talk(f"Boss enter the text/link that you want to keep in the qr code")
    input_Text_link = input("Enter the Text/Link : ")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=4,
    )
    QRfile_name = (str(datetime.datetime.now())).replace(" ","-")
    QRfile_name = QRfile_name.replace(":","-")
    QRfile_name = QRfile_name.replace(".","-")
    QRfile_name = QRfile_name+"-QR.png"
    qr.add_data(input_Text_link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"QRCodes\{QRfile_name}")
    self.engine.talk(f"Boss the qr code has been generated")

#Mobile camera
def Mobilecamra(self):
    import urllib.request
    import numpy as np
    try:
        self.engine.talk(f"Boss openinging mobile camera")
        URL = "http://_IP_Webcam_IP_address_/shot.jpg" #Discription for this is available in the README file
        while True:
            imag_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
            img = cv2.imdecode(imag_arr,-1)
            cv2.imshow('IPWebcam',img)
            q = cv2.waitKey(1)
            if q == ord("q"):
                self.engine.talk(f"Boss closing mobile camera")
                break
        cv2.destroyAllWindows()
    except Exception as e:
        print("Some error occured")

#Web camera
#NOTE to exit from the web camera press "ESC" key 
def webCam(self):    
    self.engine.talk('Opening camera')
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        cv2.imshow('web camera',img)
        k = cv2.waitKey(50)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


#Whatsapp
def whatsapp(self,command):
    try:
        command = command.replace('send a message to','')
        command = command.strip()
        name,numberID,F = self.SearchCont(command)
        if F:
            print(numberID)
            self.engine.talk(f'Boss, what message do you want to send to {name}')
            message = self.take_Command()
            hour = int(datetime.datetime.now().hour)
            min = int(datetime.datetime.now().minute)
            print(hour,min)
            if "group" in command:
                kit.sendwhatmsg_to_group(numberID,message,int(hour),int(min)+1)
            else:
                kit.sendwhatmsg(numberID,message,int(hour),int(min)+1)
            self.engine.talk("Boss message have been sent")
        if F==False:
            self.engine.talk(f'Boss, the name not found in our data base, shall I add the contact')
            AddOrNot = self.take_Command()
            print(AddOrNot)
            if ("yes" in AddOrNot) or ("add" in AddOrNot) or ("yeah" in AddOrNot) or ("yah" in AddOrNot):
                self.AddContact()
            elif("no" in AddOrNot):
                self.engine.talk('Ok Boss')
    except:
        print("Error occured, please try again")


#Add contacts
def AddContact(self):
    self.engine.talk(f'Boss, Enter the contact details')
    name = input("Enter the name :").lower()
    number = input("Enter the number :")
    NumberFormat = f'"{name}":"+91{number}"'
    ContFile = open("Contacts.txt", "a") 
    ContFile.write(f"{NumberFormat}\n")
    ContFile.close()
    self.engine.talk(f'Boss, Contact Saved Successfully')

#Search Contact
def SearchCont(self,name):
    with open("Contacts.txt","r") as ContactsFile:
        for line in ContactsFile:
            if name in line:
                print("Name Match Found")
                s = line.split("\"")
                return s[1],s[3],True
    return 0,0,False

#Display all contacts
def Display(self):
    ContactsFile = open("Contacts.txt","r")
    count=0
    for line in ContactsFile:
        count+=1
    ContactsFile.close()
    ContactsFile = open("Contacts.txt","r")
    self.engine.talk(f"Boss displaying the {count} contacts stored in our data base")    
    for line in ContactsFile:
        s = line.split("\"")
        print("Name: "+s[1])
        print("Number: "+s[3])
    ContactsFile.close()

#search contact
def NameIntheContDataBase(self,command):
    line = command
    line = line.split("number in contacts")[0]
    if("tell me" in line):
        name = line.split("tell me")[1]
        name = name.strip()
    else:
        name= line.strip()
    name,number,bo = self.SearchCont(name)
    if bo:
        print(f"Contact Match Found in our data base with {name} and the mboile number is {number}")
        self.engine.talk(f"Boss Contact Match Found in our data base with {name} and the mboile number is {number}")
    else:
        self.engine.talk("Boss the name not found in our data base, shall I add the contact")
        AddOrNot = self.take_Command()
        print(AddOrNot)
        if ("yes add it" in AddOrNot)or ("yeah" in AddOrNot) or ("yah" in AddOrNot):
            self.AddContact()
            self.engine.talk(f'Boss, Contact Saved Successfully')
        elif("no" in AddOrNot) or ("don't add" in AddOrNot):
            self.engine.talk('Ok Boss')

#Internet spped
async def InternetSpeed(self):
    await self.as_talk("Wait a few seconds boss, checking your internet speed")
    st = speedtest.Speedtest()
    dl = st.download()
    dl = dl/(1000000) #converting bytes to megabytes
    up = st.upload()
    up = up/(1000000)
    print(dl,up)
    await self.as_talk(f"Boss, we have {dl} megabytes per second downloading speed and {up} megabytes per second uploading speed")
    
#Search for a process how to do
def How(self):
    self.engine.talk("How to do mode is is activated")
    while True:
        self.engine.talk("Please tell me what you want to know")
        how = self.take_Command()
        try:
            if ("exit" in how) or("close" in how):
                self.engine.talk("Ok sir how to mode is closed")
                break
            else:
                max_result=1
                how_to = search_wikihow(how,max_result)
                assert len(how_to) == 1
                how_to[0].print()
                self.engine.talk(how_to[0].summary)
        except Exception as e:
            self.engine.talk("Sorry sir, I am not able to find this")

#Communication commands
def comum(self,command):
    print(command)
    if ('hi'in command) or('hai'in command) or ('hey'in command) or ('hello' in command) :
        self.engine.talk("Hello boss what can I help for u")
    else :
        self.No_result_found()

#Fun commands to interact with jarvis
def Fun(self,command):
    print(command)
    if 'your name' in command:
        self.engine.talk("My name is jarvis")
    elif 'my name' in command:
        self.engine.talk("your name is Sujith")
    elif 'university name' in command:
        self.engine.talk("you are studing in Amrita Vishwa Vidyapeetam, with batcheloe in Computer Science and Artificail Intelligence") 
    elif 'what can you do' in command:
        self.engine.talk("I talk with you until you want to stop, I can say time, open your social media accounts,your open source accounts, open google browser,and I can also open your college websites, I can search for some thing in google and I can tell jokes")
    elif 'your age' in command:
        self.engine.talk("I am very young that u")
    elif 'date' in command:
        self.engine.talk('Sorry not intreseted, I am having headache, we will catch up some other time')
    elif 'are you single' in command:
        self.engine.talk('No, I am in a relationship with wifi')
    elif 'joke' in command:
        self.engine.talk(pyjokes.get_joke())
    elif 'are you there' in command:
        self.engine.talk('Yes boss I am here')
    elif 'tell me something' in command:
        self.engine.talk('boss, I don\'t have much to say, you only tell me someting i will give you the company')
    elif 'thank you' in command:
        self.engine.talk('boss, I am here to help you..., your welcome')
    elif 'in your free time' in self.command:
        self.engine.talk('boss, I will be listening to all your words')
    elif 'i love you' in command:
        self.engine.talk('I love you too boss')
    elif 'can you hear me' in command:
        self.engine.talk('Yes Boss, I can hear you')
    elif 'do you ever get tired' in command:
        self.engine.talk('It would be impossible to tire of our conversation')
    else :
        self.No_result_found()

#Social media accounts commands
def social(self,command):
    print(command)
    if 'facebook' in command:
        self.engine.talk('opening your facebook')
        webbrowser.open('https://www.facebook.com/')
    elif 'whatsapp' in command:
        self.engine.talk('opening your whatsapp')
        webbrowser.open('https://web.whatsapp.com/')
    elif 'instagram' in command:
        self.engine.talk('opening your instagram')
        webbrowser.open('https://www.instagram.com/')
    elif 'twitter' in command:
        self.engine.talk('opening your twitter')
        webbrowser.open('https://twitter.com/Suj8_116')
    elif 'discord' in command:
        self.engine.talk('opening your discord')
        webbrowser.open('https://discord.com/channels/@me')
    else :
        self.No_result_found()
    
#clock commands
async def Clock_time(self,command):
    time = datetime.datetime.now().strftime('%I:%M %p')
    print(time)
    await self.as_talk("Current time is "+time)

#calender day
def Cal_day(self):
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',4: 'Thursday', 5: 'Friday', 6: 'Saturday',7: 'Sunday'}
    
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)    
        return day_of_the_week

#shedule function for remembering todays plans
#NOTE For example I have declared my college timetable you can declare anything you want
def shedule(self):
    day = self.Cal_day().lower()
    self.engine.talk("Boss today's shedule is")
    Week = {"monday" : "Boss from 9:00 to 9:50 you have Cultural class, from 10:00 to 11:50 you have mechanics class, from 12:00 to 2:00 you have brake, and today you have sensors lab from 2:00",
    "tuesday" : "Boss from 9:00 to 9:50 you have English class, from 10:00 to 10:50 you have break,from 11:00 to 12:50 you have ELectrical class, from 1:00 to 2:00 you have brake, and today you have biology lab from 2:00",
    "wednesday" : "Boss today you have a full day of classes from 9:00 to 10:50 you have Data structures class, from 11:00 to 11:50 you have mechanics class, from 12:00 to 12:50 you have cultural class, from 1:00 to 2:00 you have brake, and today you have Data structures lab from 2:00",
    "thrusday" : "Boss today you have a full day of classes from 9:00 to 10:50 you have Maths class, from 11:00 to 12:50 you have sensors class, from 1:00 to 2:00 you have brake, and today you have english lab from 2:00",
    "friday" : "Boss today you have a full day of classes from 9:00 to 9:50 you have Biology class, from 10:00 to 10:50 you have data structures class, from 11:00 to 12:50 you have Elements of computing class, from 1:00 to 2:00 you have brake, and today you have Electronics lab from 2:00",
    "saturday" : "Boss today you have a full day of classes from 9:00 to 11:50 you have maths lab, from 12:00 to 12:50 you have english class, from 1:00 to 2:00 you have brake, and today you have elements of computing lab from 2:00",
    "sunday":"Boss today is holiday but we can't say anything when they will bomb with any assisgnments"}
    if day in Week.keys():
        self.engine.talk(Week[day])

#college resources commands
#NOTE Below are some dummy links replace with your college website links
def college(self,command):
    print(command)
    if 'teams' in command:
        self.engine.talk('opening your microsoft teams')
        webbrowser.open('https://teams.microsoft.com/')
    elif 'stream' in command:
        self.engine.talk('opening your microsoft stream')
        webbrowser.open('https://web.microsoftstream.com/')
    elif 'outlook' in command:
        self.engine.talk('opening your microsoft school outlook')
        webbrowser.open('https://outlook.office.com/mail/')
    elif 'amrita portal' in command:
        self.engine.talk('opening your amrita university management system')
        webbrowser.open('https://aumsam.amrita.edu/')
    elif 'octave' in command:
        self.engine.talk('opening Octave online')
        webbrowser.open('https://octave-online.net/')
    else :
        self.No_result_found()

#Online classes
def OnlineClasses(self,command):
    print(command)
    #Keep as many "elif" statemets based on your subject Eg: I have kept a dummy links for JAVA and mechanics classes link of MS Teams
    if("java" in command):
        self.engine.talk('opening DSA class in teams')
        webbrowser.open("https://teams.microsoft.com/java")
    elif("mechanics" in command):
        self.engine.talk('opening mechanics class in teams')
        webbrowser.open("https://teams.microsoft.com/mechanics")
    elif 'online classes' in command:
        self.engine.talk('opening your microsoft teams')
        webbrowser.open('https://teams.microsoft.com/')

#Brower Search commands
def B_S(self,command):
    print(command)
    target1=""
    try:
        # ('what is meant by' in self.command) or ('tell me about' in self.command) or ('who the heck is' in self.command)
        if ('wikipedia' in command):
            target1 = command.replace('search for','')
            target1 = target1.replace('in wikipedia','')
        elif('what is meant by' in command):
            target1 = command.replace("what is meant by"," ")
        elif('tell me about' in command):
            target1 = command.replace("tell me about"," ")
        elif('who the heck is' in command):
            target1 = command.replace("who the heck is"," ")
        print("searching....")
        info = wikipedia.summary(target1,5)
        print(info)
        self.engine.talk("according to wikipedia "+info)
    except :
        self.No_result_found()
    
#Browser
def brows(self,command):
    print(command)
    if 'google' in command:
        self.engine.talk("Boss, what should I search on google..")
        S = self.take_Command()#taking command for what to search in google
        webbrowser.open(f"{S}")
    elif 'edge' in command:
        self.engine.talk('opening your Miscrosoft edge')
        os.startfile('..\\..\\MicrosoftEdge.exe')#path for your edge browser application
    else :
        self.No_result_found()

#google applications selection
#if there is any wrong with the URL's replace them with your browsers URL's
def Google_Apps(self,command):
    print(command)
    if 'gmail' in command:
        self.engine.talk('opening your google gmail')
        webbrowser.open('https://mail.google.com/mail/')
    elif 'maps' in command:
        self.engine.talk('opening google maps')
        webbrowser.open('https://www.google.co.in/maps/')
    elif 'news' in command:
        self.engine.talk('opening google news')
        webbrowser.open('https://news.google.com/')
    elif 'calender' in command:
        self.engine.talk('opening google calender')
        webbrowser.open('https://calendar.google.com/calendar/')
    elif 'photos' in command:
        self.engine.talk('opening your google photos')
        webbrowser.open('https://photos.google.com/')
    elif 'documents' in command:
        self.engine.talk('opening your google documents')
        webbrowser.open('https://docs.google.com/document/')
    elif 'spreadsheet' in command:
        self.engine.talk('opening your google spreadsheet')
        webbrowser.open('https://docs.google.com/spreadsheets/')
    else :
        self.No_result_found()
        
#youtube
def yt(self,command):
    print(command)
    if 'play' in command:
        self.engine.talk("Boss can you please say the name of the song")
        song = self.take_Command()
        if "play" in song:
            song = song.replace("play","")
        self.engine.talk('playing '+song)
        print(f'playing {song}')
        #pywhatkit.playonyt(song) huh?
        print('playing')
    elif "download" in command:
        self.engine.talk("Boss please enter the youtube video link which you want to download")
        link = input("Enter the YOUTUBE video link: ")
        yt=YouTube(link)
        yt.streams.get_highest_resolution().download()
        self.engine.talk(f"Boss downloaded {yt.title} from the link you given into the main folder")
    elif 'youtube' in command:
        self.engine.talk('opening your youtube')
        webbrowser.open('https://www.youtube.com/')
    else :
        No_result_found(self)
    
#Opensource accounts
def open_source(self,command):
    print(command)
    if 'github' in command:
        self.engine.talk('opening your github')
        webbrowser.open('https://github.com/BolisettySujith')
    elif 'gitlab' in command:
        self.engine.talk('opening your gitlab')
        webbrowser.open('https://gitlab.com/-/profile')
    else :
        self.No_result_found()

#Photo shops
def edit(self,command):
    print(command)
    if 'slides' in command:
        self.engine.talk('opening your google slides')
        webbrowser.open('https://docs.google.com/presentation/')
    elif 'canva' in command:
        self.engine.talk('opening your canva')
        webbrowser.open('https://www.canva.com/')
    else :
        self.No_result_found()

#OTT 
def OTT(self,command):
    print(command)
    if 'hotstar' in command:
        self.engine.talk('opening your disney plus hotstar')
        webbrowser.open('https://www.hotstar.com/in')
    elif 'prime' in command:
        self.engine.talk('opening your amazon prime videos')
        webbrowser.open('https://www.primevideo.com/')
    elif 'netflix' in command:
        self.engine.talk('opening Netflix videos')
        webbrowser.open('https://www.netflix.com/')
    else :
        self.No_result_found()

#PC allications
#NOTE: place the correct path for the applications from your PC there may be some path errors so please check the applications places
#if you don't have any mentioned applications delete the codes for that
#I have placed applications path based on my PC path check while using which OS you are using and change according to it
def OpenApp(self,command):
    print(command)
    if ('calculator'in command) :
        self.engine.talk('Opening calculator')
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif ('paint'in command) :
        self.engine.talk('Opening msPaint')
        os.startfile('c:\\Windows\\System32\\mspaint.exe')
    elif ('notepad'in command) :
        self.engine.talk('Opening notepad')
        os.startfile('c:\\Windows\\System32\\notepad.exe')
    elif ('discord'in command) :
        self.engine.talk('Opening discord')
        os.startfile('..\\..\\Discord.exe')
    elif ('editor'in command) :
        self.engine.talk('Opening your Visual studio code')
        os.startfile('..\\..\\Code.exe')
    elif ('online classes'in command) :
        self.engine.talk('Opening your Microsoft teams')
        webbrowser.open('https://teams.microsoft.com/')
    elif ('spotify'in command) :
        self.engine.talk('Opening spotify')
        os.startfile('..\\..\\Spotify.exe')
    elif ('lt spice'in command) :
        self.engine.talk('Opening lt spice')
        os.startfile("..\\..\\XVIIx64.exe")
    elif ('steam'in command) :
        self.engine.talk('Opening steam')
        os.startfile("..\\..\\steam.exe")
    elif ('media player'in command) :
        self.engine.talk('Opening VLC media player')
        os.startfile("C:\Program Files\VideoLAN\VLC\vlc.exe")
    else :
        self.No_result_found()
        
#closeapplications function
def CloseApp(self,command):
    print(command)
    if ('calculator'in command) :
        self.engine.talk("okay boss, closeing caliculator")
        os.system("taskkill /f /im calc.exe")
    elif ('paint'in command) :
        self.engine.talk("okay boss, closeing mspaint")
        os.system("taskkill /f /im mspaint.exe")
    elif ('notepad'in command) :
        self.engine.talk("okay boss, closeing notepad")
        os.system("taskkill /f /im notepad.exe")
    elif ('discord'in command) :
        self.engine.talk("okay boss, closeing discord")
        os.system("taskkill /f /im Discord.exe")
    elif ('editor'in command) :
        self.engine.talk("okay boss, closeing vs code")
        os.system("taskkill /f /im Code.exe")
    elif ('spotify'in command) :
        self.engine.talk("okay boss, closeing spotify")
        os.system("taskkill /f /im Spotify.exe")
    elif ('lt spice'in command) :
        self.engine.talk("okay boss, closeing lt spice")
        os.system("taskkill /f /im XVIIx64.exe")
    elif ('steam'in command) :
        self.engine.talk("okay boss, closeing steam")
        os.system("taskkill /f /im steam.exe")
    elif ('media player'in command) :
        self.engine.talk("okay boss, closeing media player")
        os.system("taskkill /f /im vlc.exe")
    else :
        self.No_result_found()

#Shopping links
def shopping(self,command):
    print(command)
    if 'flipkart' in command:
        self.engine.talk('Opening flipkart online shopping website')
        webbrowser.open("https://www.flipkart.com/")
    elif 'amazon' in command:
        self.engine.talk('Opening amazon online shopping website')
        webbrowser.open("https://www.amazon.in/")
    else :
        self.No_result_found()

#PDF reader
def pdf_reader(self):
    self.engine.talk("Boss enter the name of the book which you want to read")
    n = input("Enter the book name: ")
    n = n.strip()+".pdf"
    book_n = open(n,'rb')
    pdfReader = PyPDF2.PdfFileReader(book_n)
    pages = pdfReader.numPages
    self.engine.talk(f"Boss there are total of {pages} in this book")
    self.engine.talk("plsase enter the page number Which I nedd to read")
    num = int(input("Enter the page number: "))
    page = pdfReader.getPage(num)
    text = page.extractText()
    print(text)
    self.engine.talk(text)

#Time caliculating algorithm
def silenceTime(self,command):
    print(command)
    x=0
    #caliculating the given time to seconds from the speech commnd string
    if ('10' in command) or ('ten' in command):x=600
    elif '1' in command or ('one' in command):x=60
    elif '2' in command or ('two' in command):x=120
    elif '3' in command or ('three' in command):x=180
    elif '4' in command or ('four' in command):x=240
    elif '5' in command or ('five' in command):x=300
    elif '6' in command or ('six' in command):x=360
    elif '7' in command or ('seven' in command):x=420
    elif '8' in command or ('eight' in command):x=480
    elif '9' in command or ('nine' in command):x=540
    self.silence(x)
    
#Silence
def silence(self,k):
    t = k
    s = "Ok boss I will be silent for "+str(t/60)+" minutes"
    self.engine.talk(s)
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    self.engine.talk("Boss "+str(k/60)+" minutes over")

#Mail verification
def verifyMail(self):
    try:
        self.engine.talk("what should I say?")
        content = self.take_Command()
        self.engine.talk("To whom do u want to send the email?")
        to = self.take_Command()
        self.SendEmail(to,content)
        self.engine.talk("Email has been sent to "+str(to))
    except Exception as e:
        print(e)
        self.engine.talk("Sorry sir I am not not able to send this email")

#Email Sender
def SendEmail(self,to,content):
    print(content)
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login("YOUR_MAIL_ID","PASWORD")
    server.sendmail("YOUR_MAIL_ID",to,content)
    server.close()

#location
async def locaiton(self):
    self.engine.talk("Wait boss, let me check")
    try:
        IP_Address = get('https://api.ipify.org').text
        print(IP_Address)
        url = 'https://get.geojs.io/v1/ip/geo/'+IP_Address+'.json'
        print(url)
        geo_reqeust = get(url)
        geo_data = geo_reqeust.json()
        city = geo_data['city']
        state = geo_data['region']
        country = geo_data['country']
        tZ = geo_data['timezone']
        longitude = geo_data['longitude']
        latidute = geo_data['latitude']
        org = geo_data['organization_name']
        print(city+" "+state+" "+country+" "+tZ+" "+longitude+" "+latidute+" "+org)
        self.engine.talk(f"Boss i am not sure, but i think we are in {city} city of {state} state of {country} country")
        self.engine.talk(f"and boss, we are in {tZ} timezone the latitude os our location is {latidute}, and the longitude of our location is {longitude}, and we are using {org}\'s network ")
    except Exception as e:
        self.engine.talk("Sorry boss, due to network issue i am not able to find where we are.")
        pass

#Instagram profile
def Instagram_Pro(self):
    self.engine.talk("Boss please enter the user name of Instagram: ")
    name = input("Enter username here: ")
    webbrowser.open(f"www.instagram.com/{name}")
    time.sleep(5)
    self.engine.talk("Boss would you like to download the profile picture of this account.")
    cond = self.take_Command()
    if('download' in cond):
        mod = instaloader.Instaloader()
        mod.download_profile(name,profile_pic_only=True)
        self.engine.talk("I am done boss, profile picture is saved in your main folder. ")
    else:
        pass

#ScreenShot
def scshot(self):
    self.engine.talk("Boss, please tell me the name for this screenshot file")
    name = self.take_Command()
    self.engine.talk("Please boss hold the screen for few seconds, I am taking screenshot")
    time.sleep(3)
    img = pyautogui.screenshot()
    img.save(f"{name}.png")
    self.engine.talk("I am done boss, the screenshot is saved in main folder.")

#News
def news(self):
    MAIN_URL_= "https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=YOUR_NEWS_API_KEY"
    MAIN_PAGE_ = get(MAIN_URL_).json()
    articles = MAIN_PAGE_["articles"]
    headings=[]
    seq = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth'] #If you need more than ten you can extend it in the list
    for ar in articles:
        headings.append(ar['title'])
    for i in range(len(seq)):
        print(f"todays {seq[i]} news is: {headings[i]}")
        self.engine.talk(f"todays {seq[i]} news is: {headings[i]}")
    self.engine.talk("Boss I am done, I have read most of the latest news")

#System condition
def condition(self):
    usage = str(psutil.cpu_percent())
    self.engine.talk("CPU is at"+usage+" percentage")
    battray = psutil.sensors_battery()
    percentage = battray.percent
    self.engine.talk(f"Boss our system have {percentage} percentage Battery")
    if percentage >=75:
        self.engine.talk(f"Boss we could have enough charging to continue our work")
    elif percentage >=40 and percentage <=75:
        self.engine.talk(f"Boss we should connect out system to charging point to charge our battery")
    elif percentage >=15 and percentage <=30:
        self.engine.talk(f"Boss we don't have enough power to work, please connect to charging")
    else:
        self.engine.talk(f"Boss we have very low power, please connect to charging otherwise the system will shutdown very soon")
    
#no result found
def No_result_found(self):
    self.engine.talk('Boss I couldn\'t understand, could you please say it again.')        

