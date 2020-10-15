#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discrete Fourier filtering using 
overlap&add, overlap&save, and convolution

Algorithms: based on book Diniz P.S.R., et al.
Digital signal processing System analysis and design 

Created on Tue Oct 13 16:05:58 2020

@author: shothogun -  Otho Teixeira Komatsu
"""
import librosa as lb
import csv
import matplotlib.pyplot as plt
import scipy.signal
import numpy as np
import soundfile as sf

# %% Read audio file and save only the first minute of it

fileName = "Back_In_Black.wav"

# First minute of the audio, mono
x, fs = lb.load(fileName, mono=True, 
                         duration=60.0)

# h signal
with open('./filter/low_pass_coefficients.csv', newline='') as csvfile:
    low_pass_filter = list(csv.reader(csvfile))
    h = np.array(low_pass_filter[0], dtype='float32')
    
# %% 1. Convolution computing
y_convolution = scipy.signal.convolve(h, x)

# %% 2. DFT: Overlap-and-add 
x_len = len(x)
K = len(h)
N = 4410
CONVOLVE_SIZE = N+K-1
y_size = CONVOLVE_SIZE + ((x_len//N) - 1)*N
y_overlap_add = np.zeros(y_size)
h_length = len(h)

for m in range(0, y_size-N,N):
    
    # Gets x decomposition in m signals
    # x_m size N
    x_m = x[m:m+N].copy()
    
    # Padding both signals 
    # to N+K-1 size
    x_m = np.pad(x_m, (0, K-1),
                 'constant', constant_values=(0,0))
    
    h_pad = np.pad(h, (0, CONVOLVE_SIZE - h_length),
                 'constant', constant_values=(0,0))
    
    # Circular convolve with size N+K-1
    m_convolve = scipy.signal.convolve(h_pad, np.concatenate((x_m, x_m)))
    m_convolve = m_convolve[:CONVOLVE_SIZE]
    
    # Adding process to output
    y_overlap_add[m:m+CONVOLVE_SIZE] = y_overlap_add[m:m+CONVOLVE_SIZE] + \
                                       m_convolve
    
# %% 3. DFT: Overlap-and-save 





# %% 4. Output saving

plt.plot(y_overlap_add)
plt.show()

sf.write('output_convolition.wav', y_convolution, fs, subtype='PCM_24')
sf.write('output_overlap_add.wav', y_overlap_add, fs, subtype='PCM_24')
#sf.write('output_convolition.wav', data, samplerate, subtype='PCM_24')
