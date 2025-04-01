# Signal Processing for Condition Monitoring
This Python library is intended to be used for signal processing in condition monitoring.

This module is focused on the signal processing methods which are commonly used in vibration based condition monitorig. For example the processing methods used in MEV781 - Vibration Based Condition Montioring and other useful functions frequently used in signal processing investigations.

# Installation
```
pip install signal_processing_basics
```

# Errors:
Please feel free to contact me, Justin Smith, through 66smithjustin@gmail.com if you notice any issues.

# About the Author:
I am currently a mechanical engineering Masters candidate at the University of Pretoria performing research in the Center for Asset Integrity Management. I am focusing on vibration based condition monitoring systems for axial fans. Linkedin: https://www.linkedin.com/in/justin-s-507338116/

# To Do's
Add useful code from BTT test notebooks (such as the get_threshold function, get_dataframe function and so on)
Update the get_displacement_signal function to handle a MPR signal and not just an OPR signal
Update filter funtion to use filtfilt as its a function of past and future so the filter wont lag the input (https://stackoverflow.com/questions/13740348/how-to-apply-a-filter-to-a-signal-in-python/13740532#13740532)
might be a good idea to have more filtering options