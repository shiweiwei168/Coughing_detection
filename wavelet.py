#wavelet.py
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

t=np.linspace(-1,1,200,endpoint=False)
sig= np.cos(2*np.pi*7*t)+signal.gausspulse(t-0.4,fc=2)
widths= np.arange(1,31)
cwtmatr= signal.cwt(sig,signal.ricker,widths)
print(cwtmatr[20])
plt.subplot(2,1,1)
plt.plot(sig)
plt.subplot(2,1,2)
plt.imshow(cwtmatr,extent=[-1,1,1,31], cmap='PRGn',aspect='auto',vmax=abs(cwtmatr).max(),vmin=-abs(cwtmatr).max())
plt.show()