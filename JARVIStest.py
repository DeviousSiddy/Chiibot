#_____________________________________________________J.A.R.V.I.S________________________________________________________
#Python modules used for this programm
import asyncio
from re import T
import sys
import speech_recognition as sr
import pywhatkit
import pywhatkit as kit
import datetime
import wikipedia
import pyjokes
import webbrowser
import time
import subprocess
import os
import cv2
import random
from requests import get
import smtplib
import psutil
import instaloader
import pyautogui
import PyPDF2
from Recordings import Record_Option
from PIL import ImageGrab
import pyaudio
import wave
import numpy as np 
from PhoneNumer import Phonenumber_location_tracker
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from JarvisUi import Ui_JarvisUI
from state import state
from pywikihow import search_wikihow
import speedtest
from pytube import YouTube
import qrcode
import voice_engine
import applets

#Set our engine to "Pyttsx3" which is used for text to speech in Python 
#and sapi5 is Microsoft speech application platform interface 
#we will be using this for text to speech function.
#engine = pyttsx3.init('sapi5')
#voices = engine.getProperty('voices')
#engine.setProperty('voice',voices[1].id) #index '0' for 'David'(male) voice index '1' for 'zira'(female) voice
engine = voice_engine.VoiceEngine()
engine.start()
listener = sr.Recognizer()

#Main classs where all the functiona are present
class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()
    
    def run(self):
        self.Intro()
    
    #function that will take the commands  to convert voice into text
    def take_Command(self):
        try:
            
            with sr.Microphone() as source:
                #listener = sr.Recognizer()
                print('Listening....')
                listener.pause_threshold = 1
                voice = listener.listen(source,timeout=4,phrase_time_limit=7)
                print("Recognizing...")
                command1 = listener.recognize_google(voice,language='en-US')
                command1 = command1.lower()  
                if 'jarvis' in command1: 
                    command1 = command1.replace('jarvis','')
                
            return command1
        except:
            return 'None'

    async def as_take_Command(self):
        try:
            
            with sr.Microphone() as source:
                #listener = sr.Recognizer()
                print('Listening....')
                listener.pause_threshold = 1
                voice = listener.listen(source,timeout=4,phrase_time_limit=7)
                print("Recognizing...")
                command1 = listener.recognize_google(voice,language='en-US')
                command1 = command1.lower()  
                if 'jarvis' in command1: 
                    command1 = command1.replace('jarvis','')
            await asyncio.sleep(0.0000001)    
            return command1
        except:
            await asyncio.sleep(0.0000001)
            return 'None'
        
    #Jarvis commands controller 
    async def run_jarvis(self):
        self.command = 'None'
        await asyncio.sleep(0.0000001)    
        t = []
        while True:            
            #coros = [command_exe(self.command) for _ in range(2)]
            #await asyncio.gather(*coros)
            comm = await self.get_command()
            if (comm!='None'):
                t.append(asyncio.create_task(self.command_exe(comm)))#command_exe(self.command)))
            await asyncio.gather(*t)
            
        
    async def get_command(self):
        self.command = await self.as_take_Command() #Every time taking command after a task is done
        print(self.command)
        return self.command    

    #Executes commands.    
    async def command_exe(self,command):
        if ('play a song' in command) or ('youtube' in command) or ("download a song" in command) or ("download song" in command) : 
            #commands for opening youtube, playing a song in youtube, and download a song in youtube
            applets.yt(self,command) #function is from line 555
        #Interaction commands with JARVIS
        elif ('your age' in command) or ('are you single'in command) or ('are you there' in command) or ('tell me something' in command) or ('thank you' in command) or ('in your free time' in command) or ('i love you' in command) or ('can you hear me' in command) or ('do you ever get tired' in command):
            self.Fun(command)
        elif 'time' in command : 
            await self.Clock_time(command)
        elif (('hi' in command) and len(command)==2) or ((('hai' in command) or ('hey' in command)) and len(command)==3) or (('hello' in command) and len(command)==5):
            self.comum(command)
        elif ('what can you do' in command) or ('your name' in command) or ('my name' in command) or ('university name' in command):
            self.Fun(command)
        elif ('stop' in command):
            loop = asyncio.get_event_loop()
            loop.stop()
        elif ('joke'in command) or ('date' in command):
            await self.Fun(command)
        #schedule commands for remembering you what is the planns of the day
        elif ("college time table" in command) or ("schedule" in command):
            self.shedule() #function is present from 407
        #It will tell the day Eg : Today is wednesday
        elif ("today" in command):
            day = self.Cal_day()
            await self.as_talk("Today is "+day)
        #commad for opening any weekly meeting links
        #Eg: I have kept a meeting my amFOSS club 
        #Note: the given link is fake!!
        elif ("meeting" in command):
            engine.talk("Ok sir opening meeet")
            webbrowser.open("https://meeting/")
        #command if you don't want the JARVIS to spack until for a certain time
        #Note: I can be silent for max of 10mins
        # Eg: JARVIS keep quiet for 5 minutes 
        elif ('silence' in command) or ('silent' in command) or ('keep quiet' in command) or ('wait for' in command) :
            self.silenceTime(command)
        #Command for opening your social media accounts in webrowser
        #Eg : JARVIS open facebook (or) JARVIS open social media facebook 
        elif ('facebook' in command) or ('whatsapp' in command) or ('instagram' in command) or ('twitter' in command) or ('discord' in command) or ('social media' in command):
            self.social(command)
        #command for opening your OTT platform accounts
        #Eg: open hotstart
        elif ('hotstar' in command) or ('prime' in command) or ('netflix' in command):
            self.OTT(command)
        #Command for opening your online classes links
        elif ('online classes'in command):
            self.OnlineClasses(command)
        #command for opeing college websites
        elif ('open teams'in command) or ('open stream'in command) or ('open sharepoint'in command) or('open outlook'in command)or('open amrita portal'in command)or('open octave'in command):
            self.college(command)
        #command to search for something in wikipedia
        #Eg: what is meant by python in wikipedia (or) search for "_something_" in wikipedia
        elif ('wikipedia' in command) or ('what is meant by' in command) or ('tell me about' in command) or ('who the heck is' in command):
            self.B_S(command)
        #command for opening your browsers and search for information in google
        elif ('open google'in command) or ('open edge'in command) :
            self.brows(command)
        #command to open your google applications
        elif ('open gmail'in command) or('open maps'in command) or('open calender'in command) or('open documents'in command )or('open spredsheet'in command) or('open images'in command) or('open drive'in command) or('open news' in command):
            self.Google_Apps(command)
        #command to open your open-source accounts
        #you can add other if you have
        elif ('open github'in command) or ('open gitlab'in command) :
            self.open_source(command)
        #commands to open presentaion makeing tools like CANVA and GOOGLE SLIDES
        elif ('slides'in command) or ('canva'in command) :
            self.edit(command)
        #Command to open desktop applications
        #It can open : caliculator, notepad,paint, teams(aka online classes), discord, spotify, ltspice,vscode(aka editor), steam, VLC media player
        elif ('open calculator'in command) or ('open notepad'in command) or ('open paint'in command) or ('open online classes'in command) or ('open discord'in command) or ('open ltspice'in command) or ('open editor'in command) or ('open spotify'in command) or ('open steam'in command) or ('open media player'in command):
            self.OpenApp(command)
        #Command to close desktop applications
        #It can close : caliculator, notepad,paint, discord, spotify, ltspice,vscode(aka editor), steam, VLC media player
        elif ('close calculator'in command) or ('close notepad'in command) or ('close paint'in command) or ('close discord'in command) or ('close ltspice'in command) or ('close editor'in command) or ('close spotify'in command) or ('close steam'in command) or ('close media player'in command):
            self.CloseApp(command)
        #command for opening shopping websites 
        #NOTE: you can add as many websites
        elif ('flipkart'in command) or ('amazon'in command) :
            self.shopping(command)
        #command for asking your current location
        elif ('where i am' in command) or ('where we are' in command):
            await applets.locaiton(self)
        #command for opening command prompt 
        #Eg: jarvis open command prompt
        elif ('command prompt'in command) :
            engine.talk('Opening command prompt')
            os.system('start cmd')
        #Command for opening an instagram profile and downloading the profile pictures of the profile
        #Eg: jarvis open a profile on instagram 
        elif ('instagram profile' in command) or("profile on instagram" in command):
            self.Instagram_Pro()
        #Command for opening taking screenshot
        #Eg: jarvis take a screenshot
        elif ('take screenshot' in command)or ('screenshot' in command) or("take a screenshot" in command):
            self.scshot()
        #Command for reading PDF
        #EG: Jarvis read pdf
        elif ("read pdf" in command) or ("pdf" in command):
            self.pdf_reader()
        #command for searching for a procedure how to do something
        #Eg:jarvis activate mod
        #   jarvis How to make a cake (or) jarvis how to convert int to string in programming 
        elif "activate mod" in command:
            loop.subprocess_exec(self.How())
        #command for increaing the volume in the system
        #Eg: jarvis increase volume
        elif ("volume up" in command) or ("increase volume" in command):
            pyautogui.press("volumeup")
            engine.talk('volume increased')
        #command for decreaseing the volume in the system
        #Eg: jarvis decrease volume
        elif ("volume down" in command) or ("decrease volume" in command):
            pyautogui.press("volumedown")
            engine.talk('volume decreased')
        #Command to mute the system sound
        #Eg: jarvis mute the sound
        elif ("volume mute" in command) or ("mute the sound" in command) :
            pyautogui.press("volumemute")
            engine.talk('volume muted')
        #command for opening your mobile camera the description for using this is in the README file
        #Eg: Jarvis open mobile camera
        elif ("open mobile cam" in command):
            self.Mobilecamra()
        #command for opening your webcamera
        #Eg: jarvis open webcamera
        elif ('web cam'in command) :
            self.webCam()
        #Command for creating a new contact
        elif("create a new contact" in command):
            self.AddContact()
        #Command for searching for a contact
        elif("number in contacts" in command):
            self.NameIntheContDataBase(command)
        #Command for displaying all contacts
        elif("display all the contacts" in command):
            self.Display()
        #Command for checking covid status in India
        #Eg: jarvis check covid (or) corona status
        elif ("covid" in command) or  ("corona" in command):
            engine.talk("Boss which state covid 19 status do you want to check")
            s = self.take_Command()
            self.Covid(s)
        #Command for screenRecording
        #Eg: Jarvis start Screen recording
        elif ("recording" in command) or ("screen recording" in command) or ("voice recording" in command):
            try:
                engine.talk("Boss press q key to stop recordings")
                option = command
                Record_Option(option=option)
                engine.talk("Boss recording is being saved")
            except:
                engine.talk("Boss an unexpected error occured couldn't start screen recording")
        #Command for phone number tracker
        elif ("track" in command) or ("track a mobile number" in command):
            engine.talk("Boss please enter the mobile number with country code")
            try:
                location,servise_prover,lat,lng=Phonenumber_location_tracker()
                engine.talk(f"Boss the mobile number is from {location} and the service provider for the mobile number is {servise_prover}")
                engine.talk(f"latitude of that mobile nuber is {lat} and longitude of that mobile number is {lng}")
                print(location,servise_prover)
                print(f"Latitude : {lat} and Longitude : {lng}")
                engine.talk("Boss location of the mobile number is saved in Maps")
            except:
                engine.talk("Boss an unexpected error occured couldn't track the mobile number")
        #command for playing a dowloaded mp3 song in which is present in your system
        #Eg: Jarvis play music
        elif 'music' in command:
            music_dir = 'E:\\music' #change the song path directory if you have songs in other directory
            songs = os.listdir(music_dir)
            for song in songs:
                if song.endswith('.mp3'):
                    os.startfile(os.path.join(music_dir, song))
        #command for knowing your system IP address
        #Eg: jarvis check my ip address
        elif 'ip address' in command:
            ip = get('https://api.ipify.org').text
            print(f"your IP address is {ip}")
            engine.talk(f"your IP address is {ip}")
        #command for seading a whatsapp group and individual message
        #Individual => Eg: send a message to sujith
        #group => Eg: send a message to school group NOTE: mention the name "group" otherwise jarvis cannot detect the name
        elif ('send a message' in command):
            self.whatsapp(command)
        #command for sending an email 
        #Eg: jarvis send email
        elif 'send email' in command:
            self.verifyMail()
        #command for checking the temperature in surroundings
        #jarvis check the surroundings temperature
        elif "temperature" in command:
            self.temperature()
        #Command to generate the qr codes
        elif "create a qr code" in command:
            self.qrCodeGenerator()
        #command for checking internet speed
        #Eg: jarvis check my internet speed
        elif "internet speed" in command:
            await self.InternetSpeed()
        #command for opening Valorant
        #Eg: jarvis open Valorant
        elif "open valorant" in command:
            os.system('"C:\\Riot Games\\Riot Client\\RiotClientServices.exe" --launch-product=valorant --launch-patchline=live')
        #command to make the jarvis sleep
        #Eg: jarvis you can sleep now
        elif ("you can sleep" in command) or ("sleep now" in command):
            engine.talk("Okay boss, I am going to sleep you can call me anytime.")
            self.exit()#loop.stop()
            #break
        #command for waking the jarvis from sleep
        #jarvis wake up
        elif ("wake up" in command) or ("get up" in command):
            engine.talk("boss, I am not sleeping, I am in online, what can I do for u")
        #command for exiting jarvis from the program
        #Eg: jarvis goodbye
        elif ("goodbye" in command) or ("get lost" in command):
            engine.talk("Thanks for using me boss, have a good day")
            sys.exit()
        #command for knowing about your system condition
        #Eg: jarvis what is the system condition
        elif ('system condition' in command) or ('condition of the system' in command):
            engine.talk("checking the system condition")
            self.condition()
        #command for knowing the latest news
        #Eg: jarvis tell me the news
        elif ('tell me news' in command) or ("the news" in command) or ("todays news" in command):
            engine.talk("Please wait boss, featching the latest news")
            self.news()
        #command for shutting down the system
        #Eg: jarvis shutdown the system
        elif ('shutdown the system' in command) or ('down the system' in command):
            engine.talk("Boss shutting down the system in 10 seconds")
            time.sleep(10)
            os.system("shutdown /s /t 5")
        #command for restarting the system
        #Eg: jarvis restart the system
        elif 'restart the system' in command:
            engine.talk("Boss restarting the system in 10 seconds")
            time.sleep(10)
            os.system("shutdown /r /t 5")
        #command for make the system sleep
        #Eg: jarvis sleep the system
        elif 'sleep the system' in command:
            engine.talk("Boss the system is going to sleep")
            os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")

    #Intro msg
    def Intro(self):
        while True:
            self.permission = self.take_Command()
            print(self.permission)
            if ("wake up" in self.permission) or ("get up" in self.permission):
                #self.run_jarvis()
                
                #engine.talk('Hello boss I am jarvis your assistant. please tell me how can i help you')
                #task1 = asyncio.create_task(engine.as_talk('Hello boss I am jarvis your assistant. please tell me how can i help you'))
                #task2 = asyncio.create_task(self.run_jarvis())
                #await task1
                #await task2
                asyncio.run(self.startBot())

            elif ("goodbye" in self.permission) or ("get lost" in self.permission):
                engine.talk("Thanks for using me boss, have a good day")
                sys.exit()
                

    async def startBot(self):
        task1 = asyncio.create_task(engine.as_talk('Hello boss I am jarvis your assistant. please tell me how can i help you'))
        task2 = asyncio.create_task(self.run_jarvis())
        task3 = asyncio.create_task(self.wish())
        await task1
        await task2
        await task3

    #Wish
    async def wish(self):
        hour = int(datetime.datetime.now().hour)
        t = time.strftime("%I:%M %p")
        day = self.Cal_day()
        print(t)
        if (hour>=0) and (hour <=12) and ('AM' in t):
            engine.talk(f'Good morning boss, its {day} and the time is {t}')
        elif (hour >= 12) and (hour <= 16) and ('PM' in t):
            engine.talk(f"good afternoon boss, its {day} and the time is {t}")
        else:
            engine.talk(f"good evening boss, its {day} and the time is {t}")

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
        engine.talk(f"current {search} is {temp}")
    
    #qrCodeGenerator
    def qrCodeGenerator(self):
        engine.talk(f"Boss enter the text/link that you want to keep in the qr code")
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
        engine.talk(f"Boss the qr code has been generated")

    #Mobile camera
    def Mobilecamra(self):
        import urllib.request
        import numpy as np
        try:
            engine.talk(f"Boss openinging mobile camera")
            URL = "http://_IP_Webcam_IP_address_/shot.jpg" #Discription for this is available in the README file
            while True:
                imag_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
                img = cv2.imdecode(imag_arr,-1)
                cv2.imshow('IPWebcam',img)
                q = cv2.waitKey(1)
                if q == ord("q"):
                    engine.talk(f"Boss closing mobile camera")
                    break
            cv2.destroyAllWindows()
        except Exception as e:
            print("Some error occured")

    #Web camera
    #NOTE to exit from the web camera press "ESC" key 
    def webCam(self):    
        engine.talk('Opening camera')
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('web camera',img)
            k = cv2.waitKey(50)
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    
    #covid 
    def Covid(self,s):
        try:
            from covid_india import states
            details = states.getdata()
            if "check in" in s:
                s = s.replace("check in","").strip()
                print(s)
            elif "check" in s:
                s = s.replace("check","").strip()
                print(s)
            elif "tech" in s:
                s = s.replace("tech","").strip()
            s = state[s]
            ss = details[s]
            Total = ss["Total"]
            Active = ss["Active"]
            Cured = ss["Cured"]
            Death = ss["Death"]
            print(f"Boss the total cases in {s} are {Total}, the number of active cases are {Active}, and {Cured} people cured, and {Death} people are death")
            engine.talk(f"Boss the total cases in {s} are {Total}, the number of active cases are {Active}, and {Cured} people cured, and {Death} people are death")
            time.sleep(5)
            engine.talk("Boss do you want any information of other states")
            I = self.take_Command()
            print(I)
            if ("check" in I):
                self.Covid(I)
            elif("no" in I):
                engine.talk("Okay boss stay home stay safe")
            else:
                engine.talk("Okay boss stay home stay safe")
        except:
            engine.talk("Boss some error occured, please try again")
            engine.talk("Boss do you want any information of other states")
            I = self.take_Command()
            if("yes" in I):
                engine.talk("boss, Which state covid status do u want to check")
                Sta = self.take_Command()
                self.Covid(Sta)
            elif("no" in I):
                engine.talk("Okay boss stay home stay safe")
            else:
                engine.talk("Okay boss stay home stay safe")

    #Whatsapp
    def whatsapp(self,command):
        try:
            command = command.replace('send a message to','')
            command = command.strip()
            name,numberID,F = self.SearchCont(command)
            if F:
                print(numberID)
                engine.talk(f'Boss, what message do you want to send to {name}')
                message = self.take_Command()
                hour = int(datetime.datetime.now().hour)
                min = int(datetime.datetime.now().minute)
                print(hour,min)
                if "group" in command:
                    kit.sendwhatmsg_to_group(numberID,message,int(hour),int(min)+1)
                else:
                    kit.sendwhatmsg(numberID,message,int(hour),int(min)+1)
                engine.talk("Boss message have been sent")
            if F==False:
                engine.talk(f'Boss, the name not found in our data base, shall I add the contact')
                AddOrNot = self.take_Command()
                print(AddOrNot)
                if ("yes" in AddOrNot) or ("add" in AddOrNot) or ("yeah" in AddOrNot) or ("yah" in AddOrNot):
                    self.AddContact()
                elif("no" in AddOrNot):
                    engine.talk('Ok Boss')
        except:
            print("Error occured, please try again")

    
    #Add contacts
    def AddContact(self):
        engine.talk(f'Boss, Enter the contact details')
        name = input("Enter the name :").lower()
        number = input("Enter the number :")
        NumberFormat = f'"{name}":"+91{number}"'
        ContFile = open("Contacts.txt", "a") 
        ContFile.write(f"{NumberFormat}\n")
        ContFile.close()
        engine.talk(f'Boss, Contact Saved Successfully')

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
        engine.talk(f"Boss displaying the {count} contacts stored in our data base")    
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
            engine.talk(f"Boss Contact Match Found in our data base with {name} and the mboile number is {number}")
        else:
            engine.talk("Boss the name not found in our data base, shall I add the contact")
            AddOrNot = self.take_Command()
            print(AddOrNot)
            if ("yes add it" in AddOrNot)or ("yeah" in AddOrNot) or ("yah" in AddOrNot):
                self.AddContact()
                engine.talk(f'Boss, Contact Saved Successfully')
            elif("no" in AddOrNot) or ("don't add" in AddOrNot):
                engine.talk('Ok Boss')

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
        engine.talk("How to do mode is is activated")
        while True:
            engine.talk("Please tell me what you want to know")
            how = self.take_Command()
            try:
                if ("exit" in how) or("close" in how):
                    engine.talk("Ok sir how to mode is closed")
                    break
                else:
                    max_result=1
                    how_to = search_wikihow(how,max_result)
                    assert len(how_to) == 1
                    how_to[0].print()
                    engine.talk(how_to[0].summary)
            except Exception as e:
                engine.talk("Sorry sir, I am not able to find this")

    #Communication commands
    def comum(self,command):
        print(command)
        if ('hi'in command) or('hai'in command) or ('hey'in command) or ('hello' in command) :
            engine.talk("Hello boss what can I help for u")
        else :
            self.No_result_found()

    #Fun commands to interact with jarvis
    def Fun(self,command):
        print(command)
        if 'your name' in command:
            engine.talk("My name is jarvis")
        elif 'my name' in command:
            engine.talk("your name is Sujith")
        elif 'university name' in command:
            engine.talk("you are studing in Amrita Vishwa Vidyapeetam, with batcheloe in Computer Science and Artificail Intelligence") 
        elif 'what can you do' in command:
            engine.talk("I talk with you until you want to stop, I can say time, open your social media accounts,your open source accounts, open google browser,and I can also open your college websites, I can search for some thing in google and I can tell jokes")
        elif 'your age' in command:
            engine.talk("I am very young that u")
        elif 'date' in command:
            engine.talk('Sorry not intreseted, I am having headache, we will catch up some other time')
        elif 'are you single' in command:
            engine.talk('No, I am in a relationship with wifi')
        elif 'joke' in command:
            engine.talk(pyjokes.get_joke())
        elif 'are you there' in command:
            engine.talk('Yes boss I am here')
        elif 'tell me something' in command:
            engine.talk('boss, I don\'t have much to say, you only tell me someting i will give you the company')
        elif 'thank you' in command:
            engine.talk('boss, I am here to help you..., your welcome')
        elif 'in your free time' in self.command:
            engine.talk('boss, I will be listening to all your words')
        elif 'i love you' in command:
            engine.talk('I love you too boss')
        elif 'can you hear me' in command:
            engine.talk('Yes Boss, I can hear you')
        elif 'do you ever get tired' in command:
            engine.talk('It would be impossible to tire of our conversation')
        else :
            self.No_result_found()

    #Social media accounts commands
    def social(self,command):
        print(command)
        if 'facebook' in command:
            engine.talk('opening your facebook')
            webbrowser.open('https://www.facebook.com/')
        elif 'whatsapp' in command:
            engine.talk('opening your whatsapp')
            webbrowser.open('https://web.whatsapp.com/')
        elif 'instagram' in command:
            engine.talk('opening your instagram')
            webbrowser.open('https://www.instagram.com/')
        elif 'twitter' in command:
            engine.talk('opening your twitter')
            webbrowser.open('https://twitter.com/Suj8_116')
        elif 'discord' in command:
            engine.talk('opening your discord')
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
        engine.talk("Boss today's shedule is")
        Week = {"monday" : "Boss from 9:00 to 9:50 you have Cultural class, from 10:00 to 11:50 you have mechanics class, from 12:00 to 2:00 you have brake, and today you have sensors lab from 2:00",
        "tuesday" : "Boss from 9:00 to 9:50 you have English class, from 10:00 to 10:50 you have break,from 11:00 to 12:50 you have ELectrical class, from 1:00 to 2:00 you have brake, and today you have biology lab from 2:00",
        "wednesday" : "Boss today you have a full day of classes from 9:00 to 10:50 you have Data structures class, from 11:00 to 11:50 you have mechanics class, from 12:00 to 12:50 you have cultural class, from 1:00 to 2:00 you have brake, and today you have Data structures lab from 2:00",
        "thrusday" : "Boss today you have a full day of classes from 9:00 to 10:50 you have Maths class, from 11:00 to 12:50 you have sensors class, from 1:00 to 2:00 you have brake, and today you have english lab from 2:00",
        "friday" : "Boss today you have a full day of classes from 9:00 to 9:50 you have Biology class, from 10:00 to 10:50 you have data structures class, from 11:00 to 12:50 you have Elements of computing class, from 1:00 to 2:00 you have brake, and today you have Electronics lab from 2:00",
        "saturday" : "Boss today you have a full day of classes from 9:00 to 11:50 you have maths lab, from 12:00 to 12:50 you have english class, from 1:00 to 2:00 you have brake, and today you have elements of computing lab from 2:00",
        "sunday":"Boss today is holiday but we can't say anything when they will bomb with any assisgnments"}
        if day in Week.keys():
            engine.talk(Week[day])

    #college resources commands
    #NOTE Below are some dummy links replace with your college website links
    def college(self,command):
        print(command)
        if 'teams' in command:
            engine.talk('opening your microsoft teams')
            webbrowser.open('https://teams.microsoft.com/')
        elif 'stream' in command:
            engine.talk('opening your microsoft stream')
            webbrowser.open('https://web.microsoftstream.com/')
        elif 'outlook' in command:
            engine.talk('opening your microsoft school outlook')
            webbrowser.open('https://outlook.office.com/mail/')
        elif 'amrita portal' in command:
            engine.talk('opening your amrita university management system')
            webbrowser.open('https://aumsam.amrita.edu/')
        elif 'octave' in command:
            engine.talk('opening Octave online')
            webbrowser.open('https://octave-online.net/')
        else :
            self.No_result_found()
    
    #Online classes
    def OnlineClasses(self,command):
        print(command)
        #Keep as many "elif" statemets based on your subject Eg: I have kept a dummy links for JAVA and mechanics classes link of MS Teams
        if("java" in command):
            engine.talk('opening DSA class in teams')
            webbrowser.open("https://teams.microsoft.com/java")
        elif("mechanics" in command):
            engine.talk('opening mechanics class in teams')
            webbrowser.open("https://teams.microsoft.com/mechanics")
        elif 'online classes' in command:
            engine.talk('opening your microsoft teams')
            webbrowser.open('https://teams.microsoft.com/')

    #Brower Search commands
    def B_S(self,command):
        print(command)
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
            engine.talk("according to wikipedia "+info)
        except :
            self.No_result_found()
        
    #Browser
    def brows(self,command):
        print(command)
        if 'google' in command:
            engine.talk("Boss, what should I search on google..")
            S = self.take_Command()#taking command for what to search in google
            webbrowser.open(f"{S}")
        elif 'edge' in command:
            engine.talk('opening your Miscrosoft edge')
            os.startfile('..\\..\\MicrosoftEdge.exe')#path for your edge browser application
        else :
            self.No_result_found()

    #google applications selection
    #if there is any wrong with the URL's replace them with your browsers URL's
    def Google_Apps(self,command):
        print(command)
        if 'gmail' in command:
            engine.talk('opening your google gmail')
            webbrowser.open('https://mail.google.com/mail/')
        elif 'maps' in command:
            engine.talk('opening google maps')
            webbrowser.open('https://www.google.co.in/maps/')
        elif 'news' in command:
            engine.talk('opening google news')
            webbrowser.open('https://news.google.com/')
        elif 'calender' in command:
            engine.talk('opening google calender')
            webbrowser.open('https://calendar.google.com/calendar/')
        elif 'photos' in command:
            engine.talk('opening your google photos')
            webbrowser.open('https://photos.google.com/')
        elif 'documents' in command:
            engine.talk('opening your google documents')
            webbrowser.open('https://docs.google.com/document/')
        elif 'spreadsheet' in command:
            engine.talk('opening your google spreadsheet')
            webbrowser.open('https://docs.google.com/spreadsheets/')
        else :
            self.No_result_found()
            
    #youtube
    def yt(self,command):
        print(command)
        if 'play' in command:
            engine.talk("Boss can you please say the name of the song")
            song = self.take_Command()
            if "play" in song:
                song = song.replace("play","")
            engine.talk('playing '+song)
            print(f'playing {song}')
            pywhatkit.playonyt(song)
            print('playing')
        elif "download" in command:
            engine.talk("Boss please enter the youtube video link which you want to download")
            link = input("Enter the YOUTUBE video link: ")
            yt=YouTube(link)
            yt.streams.get_highest_resolution().download()
            engine.talk(f"Boss downloaded {yt.title} from the link you given into the main folder")
        elif 'youtube' in command:
            engine.talk('opening your youtube')
            webbrowser.open('https://www.youtube.com/')
        else :
            self.No_result_found()
        
    #Opensource accounts
    def open_source(self,command):
        print(command)
        if 'github' in command:
            engine.talk('opening your github')
            webbrowser.open('https://github.com/BolisettySujith')
        elif 'gitlab' in command:
            engine.talk('opening your gitlab')
            webbrowser.open('https://gitlab.com/-/profile')
        else :
            self.No_result_found()

    #Photo shops
    def edit(self,command):
        print(command)
        if 'slides' in command:
            engine.talk('opening your google slides')
            webbrowser.open('https://docs.google.com/presentation/')
        elif 'canva' in command:
            engine.talk('opening your canva')
            webbrowser.open('https://www.canva.com/')
        else :
            self.No_result_found()

    #OTT 
    def OTT(self,command):
        print(command)
        if 'hotstar' in command:
            engine.talk('opening your disney plus hotstar')
            webbrowser.open('https://www.hotstar.com/in')
        elif 'prime' in command:
            engine.talk('opening your amazon prime videos')
            webbrowser.open('https://www.primevideo.com/')
        elif 'netflix' in command:
            engine.talk('opening Netflix videos')
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
            engine.talk('Opening calculator')
            os.startfile('C:\\Windows\\System32\\calc.exe')
        elif ('paint'in command) :
            engine.talk('Opening msPaint')
            os.startfile('c:\\Windows\\System32\\mspaint.exe')
        elif ('notepad'in command) :
            engine.talk('Opening notepad')
            os.startfile('c:\\Windows\\System32\\notepad.exe')
        elif ('discord'in command) :
            engine.talk('Opening discord')
            os.startfile('..\\..\\Discord.exe')
        elif ('editor'in command) :
            engine.talk('Opening your Visual studio code')
            os.startfile('..\\..\\Code.exe')
        elif ('online classes'in command) :
            engine.talk('Opening your Microsoft teams')
            webbrowser.open('https://teams.microsoft.com/')
        elif ('spotify'in command) :
            engine.talk('Opening spotify')
            os.startfile('..\\..\\Spotify.exe')
        elif ('lt spice'in command) :
            engine.talk('Opening lt spice')
            os.startfile("..\\..\\XVIIx64.exe")
        elif ('steam'in command) :
            engine.talk('Opening steam')
            os.startfile("..\\..\\steam.exe")
        elif ('media player'in command) :
            engine.talk('Opening VLC media player')
            os.startfile("C:\Program Files\VideoLAN\VLC\vlc.exe")
        else :
            self.No_result_found()
            
    #closeapplications function
    def CloseApp(self,command):
        print(command)
        if ('calculator'in command) :
            engine.talk("okay boss, closeing caliculator")
            os.system("taskkill /f /im calc.exe")
        elif ('paint'in command) :
            engine.talk("okay boss, closeing mspaint")
            os.system("taskkill /f /im mspaint.exe")
        elif ('notepad'in command) :
            engine.talk("okay boss, closeing notepad")
            os.system("taskkill /f /im notepad.exe")
        elif ('discord'in command) :
            engine.talk("okay boss, closeing discord")
            os.system("taskkill /f /im Discord.exe")
        elif ('editor'in command) :
            engine.talk("okay boss, closeing vs code")
            os.system("taskkill /f /im Code.exe")
        elif ('spotify'in command) :
            engine.talk("okay boss, closeing spotify")
            os.system("taskkill /f /im Spotify.exe")
        elif ('lt spice'in command) :
            engine.talk("okay boss, closeing lt spice")
            os.system("taskkill /f /im XVIIx64.exe")
        elif ('steam'in command) :
            engine.talk("okay boss, closeing steam")
            os.system("taskkill /f /im steam.exe")
        elif ('media player'in command) :
            engine.talk("okay boss, closeing media player")
            os.system("taskkill /f /im vlc.exe")
        else :
            self.No_result_found()

    #Shopping links
    def shopping(self,command):
        print(command)
        if 'flipkart' in command:
            engine.talk('Opening flipkart online shopping website')
            webbrowser.open("https://www.flipkart.com/")
        elif 'amazon' in command:
            engine.talk('Opening amazon online shopping website')
            webbrowser.open("https://www.amazon.in/")
        else :
            self.No_result_found()

    #PDF reader
    def pdf_reader(self):
        engine.talk("Boss enter the name of the book which you want to read")
        n = input("Enter the book name: ")
        n = n.strip()+".pdf"
        book_n = open(n,'rb')
        pdfReader = PyPDF2.PdfFileReader(book_n)
        pages = pdfReader.numPages
        engine.talk(f"Boss there are total of {pages} in this book")
        engine.talk("plsase enter the page number Which I nedd to read")
        num = int(input("Enter the page number: "))
        page = pdfReader.getPage(num)
        text = page.extractText()
        print(text)
        engine.talk(text)

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
        engine.talk(s)
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
        engine.talk("Boss "+str(k/60)+" minutes over")

    #Mail verification
    def verifyMail(self):
        try:
            engine.talk("what should I say?")
            content = self.take_Command()
            engine.talk("To whom do u want to send the email?")
            to = self.take_Command()
            self.SendEmail(to,content)
            engine.talk("Email has been sent to "+str(to))
        except Exception as e:
            print(e)
            engine.talk("Sorry sir I am not not able to send this email")
    
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
        engine.talk("Wait boss, let me check")
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
            engine.talk(f"Boss i am not sure, but i think we are in {city} city of {state} state of {country} country")
            engine.talk(f"and boss, we are in {tZ} timezone the latitude os our location is {latidute}, and the longitude of our location is {longitude}, and we are using {org}\'s network ")
        except Exception as e:
            engine.talk("Sorry boss, due to network issue i am not able to find where we are.")
            pass

    #Instagram profile
    def Instagram_Pro(self):
        engine.talk("Boss please enter the user name of Instagram: ")
        name = input("Enter username here: ")
        webbrowser.open(f"www.instagram.com/{name}")
        time.sleep(5)
        engine.talk("Boss would you like to download the profile picture of this account.")
        cond = self.take_Command()
        if('download' in cond):
            mod = instaloader.Instaloader()
            mod.download_profile(name,profile_pic_only=True)
            engine.talk("I am done boss, profile picture is saved in your main folder. ")
        else:
            pass

    #ScreenShot
    def scshot(self):
        engine.talk("Boss, please tell me the name for this screenshot file")
        name = self.take_Command()
        engine.talk("Please boss hold the screen for few seconds, I am taking screenshot")
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        engine.talk("I am done boss, the screenshot is saved in main folder.")

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
            engine.talk(f"todays {seq[i]} news is: {headings[i]}")
        engine.talk("Boss I am done, I have read most of the latest news")

    #System condition
    def condition(self):
        usage = str(psutil.cpu_percent())
        engine.talk("CPU is at"+usage+" percentage")
        battray = psutil.sensors_battery()
        percentage = battray.percent
        engine.talk(f"Boss our system have {percentage} percentage Battery")
        if percentage >=75:
            engine.talk(f"Boss we could have enough charging to continue our work")
        elif percentage >=40 and percentage <=75:
            engine.talk(f"Boss we should connect out system to charging point to charge our battery")
        elif percentage >=15 and percentage <=30:
            engine.talk(f"Boss we don't have enough power to work, please connect to charging")
        else:
            engine.talk(f"Boss we have very low power, please connect to charging otherwise the system will shutdown very soon")
        
    #no result found
    def No_result_found(self):
        engine.talk('Boss I couldn\'t understand, could you please say it again.')        

startExecution = MainThread()
class Main(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_JarvisUI()
        self.ui.setupUi(self)
        self.ui.pushButton_4.clicked.connect(self.startTask)
        self.ui.pushButton_3.clicked.connect(self.close)
    
    #NOTE make sure to place a correct path where you are keeping this gifs
    def startTask(self):
        self.ui.movie = QtGui.QMovie("E:/amFOSS/JARVIS/JarvisUI/ironman1.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/amFOSS/JARVIS/ringJar.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/amFOSS/JARVIS/JarvisUI/circle.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/amFOSS/JARVIS/JarvisUI/lines1.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/amFOSS/JARVIS/JarvisUI/ironman3.gif")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/amFOSS/JARVIS/JarvisUI/circle.gif")
        self.ui.label_9.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/amFOSS/JARVIS/JarvisUI/powersource.gif")
        self.ui.label_12.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/amFOSS/JARVIS/JarvisUI/powersource.gif")
        self.ui.label_13.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/amFOSS/JARVIS/JarvisUI/ironman3_flipped.gif")
        self.ui.label_16.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/amFOSS/JARVIS/JarvisUI/Sujith.gif")
        self.ui.label_17.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()
    
    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())



