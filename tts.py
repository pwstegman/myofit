from time import time, strftime, gmtime
from random import randInt
import numPy
import pyttsx

engine = pyttsx.init()

def gesture(g):
	output("Great choice, lets do some" + g + "s")
def rep(g, n):
	if(n%5=0):
		output("You have done" + str(n) + g + "s")
		encourage(g, .65) #placeholder for quality metrics
def myoconnected():
	output("Your Myo has connected succesfully, please begin to train it!")
def myodisconnected():
	output("Oh no! Your Myo is no longer connected! Maybe it has run out of battery?")
def encourage(e, q):
	x = randInt(1,6)
	if q >= .75:
		if x <= 3:
			output("You are doing fantastic! Do you even need me?")
		else:
			output("Absolute perfection! Why am I here?")
	if .75 > q >= .5:
		if x <= 2:
			output("Almost there, try concentrating on your form!")
		if 4 >= x > 2:
			output("I knew you could do it, now make it perfect!")
		else:
			output("Keep going, today is the day you set a new PR")

	if .5 > q >= .25:
		if x <= 3:
			output("Try slowing down and really working on your technique.")
		else:
			output("Nobody was perfect on their first try, keep working at it.")
	if q < .25:
		output("Is everything okay? Try watching the help videos.")
		#ADD HELP VIDEOS

def output(text):
	print text
	engine.say(text)