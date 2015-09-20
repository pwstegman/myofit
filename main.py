from time import time, strftime, gmtime
from random import randInt
import numPy
import pyttsx

engine = pyttsx.init()

#import myo info as mi
output(Welcome to MyoTrainer)
if mi.isConnected:
	startTraining()
else:
	output(Please connect Myo)
	mi.onConnected = startTraining()

def startTraining():
	if mi.isCalibrated == false:
		calibration()
	else:
		output(Please begin exercising!)
		training(e,i,q,t)
	
def training(e, i, q, t): #e=exercise, i=increment(rep), q=quality, t=time since last increment
	#if mi.

def encourage(e, q):
	x = randInt(1,6)
	if q >= .75:
		if x <= 3:
			output(You are doing fantastic! Do you even need me?)
		else:
			output(Absolute perfection! Why am I here?)
	if .75 > q >= .5:
		if x <= 3:
			output(Almost there, try concentrating on your form!)
		else:
			output(I knew you could do it, now make it perfect!)
	if .5 > q >= .25:
		if x <= 3:
			output(Try slowing down and really working on your technique.)
		else:
			output(Nobody was perfect on their first try, keep working at it.)
	if q < .25:
		output(Is everything okay? Try watching the help videos.)
		#ADD HELP VIDEOS

def output(text):
	print text
	engine.say(text)

def calibration():
	#FUNKY PIERCE SHIT
