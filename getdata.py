import myo as libmyo; libmyo.init()
import time
import sys
from process import *

numsensors = 11
samples = [[] for i in range(numsensors)]
training = {"features":[], "output":[]}
state = ""
featurespertrain = 16
currenttrain = 0
numsamples = 32
gesture = ""
currentacc = [];

def train(data):
    print(data)
    global currenttrain, state, samples
    for i in range(len(data)):
        samples[i].append(data[i])
    if len(samples[0]) >= numsamples:
        rms = list(extractFeatures(samples[:8]))+list(map(np.mean,samples[8:]))
        training["features"].append(rms)
        training["output"].append(gesture)
        currenttrain += 1
        for i in range(numsensors):
            samples[i] = samples[i][numsamples//4:]
        print("Collected feature", currenttrain, "/", featurespertrain, "for", gesture, [int(i) for i in rms])
        if currenttrain >= featurespertrain:
            state = ""
            currenttrain = 0
            samples = [[] for i in range(numsensors)]
            print("Done collecting data for", gesture)

def stream(data):
    global samplest
    for i in range(len(data)):
        samples[i].append(data[i])
    if len(samples[0]) >= numsamples:
        rms = list(extractFeatures(samples[:8]))+list(map(np.mean,samples[8:]))
        for i in range(numsensors):
            samples[i] = samples[i][numsamples//4:]
        print("It's", classify(training["features"], training["output"], rms))

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

    def on_rssi(self, myo, timestamp, rssi):
        self.rssi = rssi

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
        data = list(emg)+currentacc
        if state == "train":
            train(data)
        if state == "stream":
            stream(data)

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

# Listen to keyboard interrupts and stop the hub in that case.
try:
    while hub.running:
        time.sleep(0.25)
        if state != "":
            continue
        action = input("Do you want to train or stream? ")
        if action == "train" or action == "t":
            gesture = input("What gesture? ")
            state = "train"
        elif action == "stream" or action == "s":
            state = "stream"
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Quit streaming")
                state = ""
except KeyboardInterrupt:
    print("\nQuitting ...")
finally:
    print("Shutting down hub...")
    hub.shutdown()