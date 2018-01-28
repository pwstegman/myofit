# MyoFit
Myo Fitness Tracking AI and Personal Trainer

## Background
Thalmic Labs developed the Myo to work as a 'hackable' [electromyograph](https://en.wikipedia.org/wiki/Electromyography).  The Myo is designed to recognize five different hand gestures and rudimentary arm motion.  We wanted more than that.  

## What We Did
Though the Myo SDK only supports five gestures, one can access the raw EMG data from the device as well.  Using this raw data we computed the root mean square (rms) for each of the eight individual sensors on the Myo.  This allowed us to turn the constantly variable electrical potentials on your skin into eight integers.  <br><br> The real <b>magic</b> starts here. <br><br>  Our eight-dimensional vector is "plotted" allowing us to compare it to the calibrated values for each workout.  The comparison is done using a k-nearest neighbor system.  But this didn't allow us to get the fidelity we wanted from the system.  So we added in accelerometer data from the IMU to allow us reliably tell the difference between up and down in push ups, sit ups, and pull ups. <br><br> On top of all of this we overlaid a rudimentary AI/trainer.  The trainer can tell you how many reps you have done, offer encouragement, and give you metrics about your exercise.

## How We Did It
The whole project is written in Python.  We used pyttsx for text-to speech, and kivy for our GUI.  [myo-python](https://github.com/NiklasRosenstein/myo-python) was used to interface with the Myo.

## FAQ
#### Can you preload exercises?
Yes, but no.  It would be possible to save the data you generate in a given session, however it is unlikely to be particularly useful.  It is rare that two people can use the same calibrated settings, and even slight displacements of the Myo can throw off the data.  It is best to dedicate two minutes at the beginning of each session to proper calibration.



Made by [Pierce Stegman](https://github.com/pwstegman), [Peter Rohrer](https://github.com/peterjrohrer), and [Rushi Shah](https://github.com/2016rshah) at Hack The North 2015.
