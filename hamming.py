#!/usr/bin/ipython -pylab

# Copyright 2010, Bill Cox, all rights reserved.  This program may be freely
# distributed under the terms of the GPL license, version 2.

from pylab import *
from scipy import *

sampleRate = 10000

def computeNoiseBandwidth(response):
    total = 0.0
    peak = -1e50
    for i in range(sampleRate/2):
        if response[i] > peak:
	    peak = response[i]
    peak = peak*peak
    for i in range(sampleRate/2):
        total += response[i]*response[i]/peak
    return total

def genResponse(freq):
    signal=zeros(sampleRate)
    for i in range(sampleRate):
        signal[i] = sin(2*pi*freq*i/sampleRate)

    window=zeros(sampleRate)
    for i in range(sampleRate):
        window[i] = 0.54 - 0.46*cos(2*pi*i/sampleRate)

    # Apply the window function to the signal
    windowedSignal = window*signal

    # Compute the FFT
    fftOut = fft(windowedSignal)
    return abs(fftOut[:sampleRate/2])

worstValue = -1e50
worstFreq = 0.0
for i in range(100):
    freq = 1000.0 + i/100.0
    response = genResponse(freq)
    testFreq = 1.1*freq
    if response[testFreq] > worstValue:
	worstValue = response[testFreq]
        worstFreq = freq
	print "Worst freq = %f" % worstFreq

response = genResponse(worstFreq)
plot(20*log10(response[900:1100]))
response = genResponse(1000)
B = computeNoiseBandwidth(response)
print "B = %f" % B
