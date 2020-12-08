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
        self.title("Coughing Detection")
        self.minsize(640, 480)
        self.labelFrame = ttk.LabelFrame(self, text = "Choose a Wav File")
        self.labelFrame.grid(column = 0, row = 1)
        self.button()
        self.abutton()
        self.result=ttk.Label(text="")
        self.result.grid(column = 0, row = 2, padx = 10, pady = 10)
        self.reTree = ttk.Treeview(self, columns="#1")
        self.reTree.grid(column = 0, row = 3, columnspan=2)
        self.reTree.heading("#0",text="Start Time")
        self.reTree.heading("#1",text="Duration")
        self.reTree.column("#0", minwidth=200, width=200, stretch=YES)
        self.reTree.column("#1", minwidth=200, width=200, stretch=YES)
        self.iids = []

    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse for File",command = self.fileDialog)
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
        self.result.configure(text="A total of " + str(len(reList)) + " cough" + ("s were" if len(reList) > 1 else " was") + " detected!")
        # clear the list from previous results
        for iid in self.iids:
            self.reTree.delete(iid)
        self.iids.clear()
        # show new results
        for r in reList:
            self.iids.append(self.reTree.insert("", "end", text=("{0:.6g}".format(r[0]) + " s"), values=("{0:.6g}".format(r[1]) + " s")))

        #show the 

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
    
    #Feature extraction
    f_list=list()
    f_list = fe(scale_list)
    #print(f_list)
    #check the rules to detect coughing
    #regroup the feature_list base on the distance d<500
    d=500 
    g_list=list()
    group=[]
    for f in f_list:
        
        if not group:
            group.append(f)
            #print('first',f)
        elif (f[0]-group[-1][1])<d:
            group.append(f)
            #print('ddd',group)
        else:
            if len(group)>2: # group member must >=3 
                g_list.append(group)
            group=[]
            group.append(f)
    if len(group)>2: # group member must >=3
        g_list.append(group)
    print(g_list)
    
    #if this program cannot fit for some examples, we can analyze the groups.
    #for example, group max min value, length of feature.

    #cover to time
    result=[]
    for g in g_list:
        time = g[0][0]/22050
        During = (g[-1][0]-g[0][0])/22050 
        result.append([time,During])
    print(result)
    return result

#Feature extraction,
# original signal after cwt (00000++++0----0+++++0000000)  
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
    widths= (800)
    ex= signal.cwt(sig,signal.ricker,widths)
    return ex



#gui

root = Root()
root.mainloop()
    




