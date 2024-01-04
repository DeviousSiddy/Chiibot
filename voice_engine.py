import pyttsx3
import speech_recognition as sr
import asyncio


class VoiceEngine(object):
    #Set our engine to "Pyttsx3" which is used for text to speech in Python 
    #and sapi5 is Microsoft speech application platform interface 
    #we will be using this for text to speech function.
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
    def start(self):

        
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice',voices[1].id) #index '0' for 'David'(male) voice index '1' for 'zira'(female) voice
        return self


    #Talk 
    def talk(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
    
    #Async Talk
    async def as_talk(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
        await asyncio.sleep(0.0000001)
        