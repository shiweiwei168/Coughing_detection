#to show the example's signal and cwt

import librosa
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import tkinter as tk



#functions for bandpass
def butter_bandpass(lowcut,highcut,fs,order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order,[low,high],btype='stop')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut,fs,order=5):
    b, a = butter_bandpass(lowcut,highcut,fs, order=order)
    
    y = signal.lfilter(b, a, data)
    return y


#wavelet cwt ex1

#read the target signal from the wav file.
sig, sr=librosa.load("t1.wav")
#print(len(sig), sr)

#bandpass to remove the noise

sig = butter_bandpass_filter(sig,5000.0,11000.0,sr, 5)
#print(len(sig), sr)

#create the plot to show the ex1
t=np.linspace(1,len(sig),len(sig))
widths= np.arange(1200,1250)
ex1= signal.cwt(sig,signal.ricker,widths)

plt.figure('t1.wav')
plt.subplot(2,1,1)
plt.plot(sig)
plt.subplot(2,1,2)
plt.imshow(ex1,extent=[-1,1,800,810], cmap='PRGn',aspect='auto',vmax=abs(ex1).max(),vmin=-abs(ex1).max())
plt.show(block=False)


#wavelet cwt ex2
#read the target signal from the wav file.
sig, sr=librosa.load("t2.wav")
#print(len(sig), sr)

#bandpass to remove the noise
sig = butter_bandpass_filter(sig,5000.0,11000.0,sr, 5)
#print(len(sig), sr)

#create the plot to show the ex2
t=np.linspace(1,len(sig),len(sig))
widths= np.arange(800,850)
ex2= signal.cwt(sig,signal.ricker,widths)


plt.figure('ex2.wav')
plt.subplot(2,1,1)
plt.plot(sig)
plt.subplot(2,1,2)
plt.imshow(ex2,extent=[-1,1,800,850], cmap='PRGn',aspect='auto',vmax=abs(ex2).max(),vmin=-abs(ex2).max())
plt.show(block=False)


#wavelet cwt ex3

#read the target signal from the wav file.
sig, sr=librosa.load("ex3.wav")
print(len(sig), sr)

#bandpass to remove the noise
sig = butter_bandpass_filter(sig,5000.0,11000.0,sr, 5)
print(len(sig), sr)

#create the plot to show the ex3
t=np.linspace(1,len(sig),len(sig))
widths= np.arange(800,850)
ex3= signal.cwt(sig,signal.ricker,widths)
print(ex3[0],ex3[0][0])
plt.figure('ex3.wav')
plt.subplot(2,1,1)
plt.plot(sig)
plt.subplot(2,1,2)
plt.imshow(ex3,extent=[-1,1,800,810], cmap='PRGn',aspect='auto',vmax=abs(ex3).max(),vmin=-abs(ex3).max())
plt.show(block=True)


#gui






#click event 

    #read target file.
    #remove <5000 & >10000 noise.
    #cwt.
    #compare with ex1,ex2,ex3
    #get 