import myo as libmyo; libmyo.init()
import time
import sys
from process import *
from tkinter import *

root = Tk()
root.title("Hack the North Myo Fit")

numsensors = 8
samples = [[] for i in range(numsensors)]
training = {"features":[], "output":[]}
subtrain = {}
state = ""
featurespertrain = 16
currenttrain = 0
numsamples = 128
gesture = ""
currentacc = [];
reps = {}
phase = 0
lastgesture = ""
lastsubg = ""

def train(emg):
    global currenttrain, state, samples
    for i in range(len(emg)):
        samples[i].append(emg[i])
    if len(samples[0]) >= numsamples:
        rms = extractFeatures(samples)
        training["features"].append(rms)
        training["output"].append(gesture)
        currenttrain += 1
        for i in range(numsensors):
            samples[i] = samples[i][numsamples//4:]
        w1.set(str(currenttrain) + "/" + str(featurespertrain))
        w2.set(str([int(i) for i in rms]))
        if currenttrain >= featurespertrain:
            state = ""
            currenttrain = 0
            samples = [[] for i in range(numsensors)]
            print("Done collecting data for", gesture)
            w1.set("Done")
            w2.set("")

def subPos(gesture, acc):
    return classify(subtrain[gesture]["features"], subtrain[gesture]["output"], acc)

def stream(emg):
    global samples, phase, reps, lastgesture, lastsubg
    for i in range(len(emg)):
        samples[i].append(emg[i])
    if len(samples[0]) >= numsamples:
        rms = extractFeatures(samples)
        for i in range(numsensors):
            samples[i] = samples[i][numsamples//4:]
        gesture = classify(training["features"], training["output"], rms)
        if not lastgesture == gesture:
            print("It's", gesture)
            w1.set(gesture)
            #tts.gesture(gesture)
            lastgesture = gesture
        if gesture in subtrain:
            sp = subPos(gesture, currentacc)
            if not lastsubg == sp:
                print("Subtrain is", sp)
                lastsubg = sp
            if sp == "down":
                phase += 1
            if sp == "up" and phase >= 2:
                phase = 0
                if gesture not in reps:
                    reps[gesture] = 1
                else:
                    reps[gesture] += 1
                print("Rep number", reps[gesture])
                w2.set(str(reps[gesture]))
                #tts.rep(gesture, reps[gesture])


class Listener(libmyo.DeviceListener):
    """
    Listener implementation. Return False from any function to
    stop the Hub.
    """

    def __init__(self):
        super(Listener, self).__init__()
        self.orientation = None
        self.pose = libmyo.Pose.rest
        self.emg_enabled = True
        self.locked = False
        self.rssi = None
        self.emg = None
        self.last_time = 0

    def on_connect(self, myo, timestamp, firmware_version):
        myo.vibrate('short')
        myo.vibrate('short')
        myo.request_rssi()
        myo.request_battery_level()
        myo.set_stream_emg(libmyo.StreamEmg.enabled)
        #tts.myoconnected()

    def on_rssi(self, myo, timestamp, rssi):
        self.rssi = rssi
        print("RSSI", rssi)

    def on_pose(self, myo, timestamp, pose):
        self.pose = pose

    def on_orientation_data(self, myo, timestamp, orientation):
        self.orientation = orientation

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        global currentacc
        currentacc = list(acceleration)

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        pass

    def on_emg_data(self, myo, timestamp, emg):
        self.emg = emg
        if state == "train":
            train(emg)
        if state == "stream":
            stream(emg)

    def on_unlock(self, myo, timestamp):
        self.locked = False

    def on_lock(self, myo, timestamp):
        self.locked = True

    def on_event(self, kind, event):
        """
        Called before any of the event callbacks.
        """

    def on_event_finished(self, kind, event):
        """
        Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub.
        """

    def on_pair(self, myo, timestamp, firmware_version):
        """
        Called when a Myo armband is paired.
        """

    def on_unpair(self, myo, timestamp):
        """
        Called when a Myo armband is unpaired.
        """

    def on_disconnect(self, myo, timestamp):
        """
        Called when a Myo is disconnected.
        """
        #tts.myodisconnected()

    def on_arm_sync(self, myo, timestamp, arm, x_direction, rotation,
                    warmup_state):
        """
        Called when a Myo armband and an arm is synced.
        """

    def on_arm_unsync(self, myo, timestamp):
        """
        Called when a Myo armband and an arm is unsynced.
        """

    def on_battery_level_received(self, myo, timestamp, level):
        """
        Called when the requested battery level received.
        """
        w2.set("Battery " + str(level) + "%")

    def on_warmup_completed(self, myo, timestamp, warmup_result):
        """
        Called when the warmup completed.
        """

print("Connecting to Myo ... Use CTRL^C to exit.")
print("If nothing happens, make sure the Bluetooth adapter is plugged in,")
print("Myo Connect is running and your Myo is put on.")
hub = libmyo.Hub()
hub.set_locking_policy(libmyo.LockingPolicy.none)
hub.run(200, Listener())

def tktrain():
    global state, gesture
    gesture = e1.get()
    state = "train"

def tkstream():
    global state
    state = "stream"

def tksubtrain():
    global subtrain
    subpos = e2.get()
    maing = e1.get()
    if maing not in subtrain:
        subtrain[maing] = {"features":[], "output":[]}
    subtrain[maing]["features"].append(currentacc)
    subtrain[maing]["output"].append(subpos)
    print("Stored", currentacc, "for", maing,"as", subpos)

def tkstopstream():
    state = ""

fc = ("Helvetica", 32, "bold")

button1 = Button(root, text='Train', command=tktrain, font=fc)
button1.pack(fill=X)
e1 = Entry(font=fc)
e1.pack(fill=X)
button2 = Button(root, text='Stream', command=tkstream, font=fc)
button2.pack(fill=X)
button3 = Button(root, text='Subtrain', command=tksubtrain, font=fc)
button3.pack(fill=X)
e2 = Entry(font=fc)
e2.pack(fill=X)
button4 = Button(root, text='Stop stream', command=tkstopstream, font=fc)
button4.pack(fill=X)
w1 = StringVar()
w1l = Label(root, textvariable=w1, font=fc)
w1l.pack(fill=X)
w2 = StringVar()
w2l = Label(root, textvariable=w2, font=fc)
w2l.pack(fill=X)

root.mainloop()
hub.shutdown()
