import pyttsx

def speak(letter):
	engine = pyttsx.init()	
	engine.say(letter)
	engine.runAndWait()
