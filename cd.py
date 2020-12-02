import librosa
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

#GUI
class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Coughing detection")
        self.minsize(320, 200)
        self.labelFrame = ttk.LabelFrame(self, text = "Choose a Wav File")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
        self.button()
        self.abutton()
        self.result=ttk.Label(text="1")
        self.result.grid(column=1,row=3)
 
 
    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)
 
 
    def fileDialog(self):
 
        self.filename = filedialog.askopenfilename(initialdir =  "/home/weishi/cse4340", title = "Select A File", filetypes =
        (("wav files","*.wav"),("mp3 files","*.mp3")) )
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.filename)
 
    def abutton(self):
        self.abutton = ttk.Button(text = "Analyze", command = self.fileAnalyze)
        self.abutton.grid(column=1, row=1)
 
    def fileAnalyze(self):
        self.result.configure(text="analyzing")
        reList = analyze(self.filename)
        # shows the relist


def analyze(filename):
    
    #read target file.
    sig, sr=librosa.load(filename)
    #remove <5000 & >10000 noise.
    #cwt.
    #compare with ex1,ex2,ex3
    #get 

    #cwt ex1-2-3
    ex1=cwt("ex1.wav")
    ex2=cwt("ex2.wav")
    ex3=cwt("ex3.wav")
    

    #Feature extraction




    l=(0,0,0)
    return l

def FE(nda): #Feature extraction
    for 






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

def cwt(Filename):  #cwt example
    #wavelet cwt 
    #read the target signal from the wav file.
    sig, sr=librosa.load("ex1.wav")
    #print(len(sig), sr)
    #bandpass to remove the noise
    sig = butter_bandpass_filter(sig,5000.0,11000.0,sr, 5)
    #print(len(sig), sr)

    #create the plot to show the ex1
    t=np.linspace(1,len(sig),len(sig))
    widths= np.arange(800,900)
    ex= signal.cwt(sig,signal.ricker,widths)
    return ex



#gui

root = Root()
root.mainloop()
    




