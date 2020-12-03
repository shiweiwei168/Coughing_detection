#to show the example's signal and cwt

import librosa
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import tkinter as tk



def analyze(filename):
    
    #wavelet cwt 
    #read the target signal from the wav file.
    sig, sr=librosa.load(filename)
    #print(len(sig), sr)
    #bandpass to remove the noise
    sig = butter_bandpass_filter(sig,5000.0,11000.0,sr, 5)
    #print(len(sig), sr)

    widths= [800]
    ex= signal.cwt(sig,signal.ricker,widths)
    #covert nd array to list
    scale_list = list(ex[0])
    print(scale_list[3])
    #Feature extraction
    f=list()
    f = fe(scale_list)
    #check the rules to detect coughing
    print(f)

    return f

#Feature extraction,
# original signal (00000++++0----0+++++0000000)  
# 0 <==> (-0.05<v<0.5), 1 <==> (v>0.5),-1 <==> (v<-0.05)
# will return [(start_index,end_index,max,min),(start_index,end_index,max,min)....]
def fe(scale_list):
     # 0 <==> (-0.05<v<0.5), 1 <==> (v>0.5),-1 <==> (v<-0.05) 
    v=0.05
    nv=-0.05
    flag=0
    pmax=0
    pmin=9999
    nmax=-9999
    nmin=0
    start=0
    end=0
    result = list()
    for i in range(len(scale_list)):
        if scale_list[i]>v and flag==0:  #0-->1
            flag=1
            start=i
            pmax=scale_list[i]
            pmin=scale_list[i]
            end=i

        if scale_list[i]>v and flag==1:  #1--->1 update max min and end
            if scale_list[i]>pmax:
                pmax=scale_list[i]
            if scale_list[i]<pmin:
                pmin=scale_list[i]
            end = i

        if scale_list[i]<nv and flag==1:  #1--> -1
            result.append((start,end,pmax,pmin))
            flag=-1
            start=i
            nmax=scale_list[i]
            nmin=scale_list[i]
            end=i
            
        if scale_list[i]<nv and flag==0: #0-->-1 
            flag=-1
            start=i
            nmax=scale_list[i]
            nmin=scale_list[i]
            end=i
        
        if scale_list[i]<nv and flag==-1:  #-1--->-1 update max min and end
            if scale_list[i]>nmax:
                nmax=scale_list[i]
            if scale_list[i]<nmin:
                nmin=scale_list[i]
            end = i

        if scale_list[i]>v and flag==-1:  #-1-->1
            result.append((start,end,nmax,nmin))
            flag=1
            start=i
            pmax=scale_list[i]
            pmin=scale_list[i]
            end=i

        if nv<scale_list[i]<v and flag!=0:   #-1 or 1 --->0  #append 
            if flag ==1:
                result.append((start,end,pmax,pmin))
            else:
                result.append((start,end,nmax,nmin))
            flag=0
            pmax=0
            pmin=9999
            nmax=-9999
            nmin=0
            start=0
            end=0
    return result

        






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
sig, sr=librosa.load("ex5.wav")
print(len(sig), sr)

#bandpass to remove the noise

#sig = butter_bandpass_filter(sig,5000.0,11000.0,sr, 5)
print(len(sig), sr)

#create the plot to show the ex1
t=np.linspace(1,len(sig),len(sig))
widths= np.arange(800,850)
ex1= signal.cwt(sig,signal.ricker,widths)
print(len(ex1[0]),ex1[0][0])
plt.figure('t1.wav')
plt.subplot(2,1,1)
plt.plot(sig)
plt.subplot(2,1,2)
plt.imshow(ex1,extent=[0,len(ex1[0]),800,850], cmap='PRGn',aspect='auto',vmax=abs(ex1).max(),vmin=-abs(ex1).max())
plt.show(block=False)


#wavelet cwt ex2
#read the target signal from the wav file.
sig, sr=librosa.load("ex5.wav")
#print(len(sig), sr)

#bandpass to remove the noise
sig = butter_bandpass_filter(sig,5000.0,11000.0,sr, 5)
#print(len(sig), sr)

#create the plot to show the ex2
t=np.linspace(1,len(sig),len(sig))
widths= np.arange(800,850)
# widths= np.arange(600,650)
ex2= signal.cwt(sig,signal.ricker,widths)
print(ex2)

plt.figure('ex2.wav')
plt.subplot(2,1,1)
plt.plot(sig)
plt.subplot(2,1,2)
plt.imshow(ex2,extent=[-1,1,800,850], cmap='PRGn',aspect='auto',vmax=abs(ex2).max(),vmin=-abs(ex2).max())
plt.show(block=False)


#wavelet cwt ex3

#read the target signal from the wav file.
sig, sr=librosa.load("t3.wav")
print(len(sig), sr)

#bandpass to remove the noise
sig = butter_bandpass_filter(sig,5000.0,11000.0,sr, 5)
print(len(sig), sr)

#create the plot to show the ex3
t=np.linspace(1,len(sig),len(sig))
widths= np.arange(600,650)
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