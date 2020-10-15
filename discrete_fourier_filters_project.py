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

def plotAudio(ax, in_signal, out_signal, title1, title2):
    ax[0].set_title(title1)
    ax[1].set_title(title2)
    ax[0].plot(in_signal)
    ax[1].plot(out_signal)
    
# %% Read audio file and save only the first minute of it

fileName = "Back_In_Black.wav"

# First minute of the audio, mono
x, fs = lb.load(fileName, mono=True, 
                         duration=60.0)

x_original = x.copy()
# h signal
with open('./filter/low_pass_coefficients.csv', newline='') as csvfile:
    low_pass_filter = list(csv.reader(csvfile))
    h = np.array(low_pass_filter[0], dtype='float32')
    
# %% 1. Convolution computing
y_convolution = scipy.signal.convolve(h, x)

# %% 2. DFT: Overlap-and-add 
L = len(x)
K = len(h)
N = 4410
CONVOLVE_SIZE = N+K-1
Y_OA_SIZE = K+L-1
y_overlap_add = np.zeros(Y_OA_SIZE)

for m in range(0, Y_OA_SIZE-N,N):
    
    # Gets x decomposition in m signals
    # x_m size N
    x_m = x[m:m+N].copy()
    
    # Padding both signals 
    # to N+K-1 size
    x_m = np.pad(x_m, (0, K-1),
                 'constant', constant_values=(0,0))
    
    h_pad = np.pad(h, (0, CONVOLVE_SIZE - K),
                 'constant', constant_values=(0,0))
    
    # Circular convolve h*x_m with size N+K-1
    m_convolve = scipy.signal.convolve(h_pad, np.concatenate((x_m, x_m)))
    m_convolve = m_convolve[:CONVOLVE_SIZE]
    
    # Adding process to output
    y_overlap_add[m:m+CONVOLVE_SIZE] = y_overlap_add[m:m+CONVOLVE_SIZE] + \
                                       m_convolve
    
# %% 3. DFT: Overlap-and-save 
L = len(x)
K = len(h)
N = 4410
CONVOLVE_SIZE = N
Y_OS_SIZE = K+L-1
y_overlap_save = np.zeros(Y_OS_SIZE)

# Padding K-1 0 to input
x = np.pad(x, (K-1, 0),
                 'constant', constant_values=(0,0))

for m in range(0, Y_OS_SIZE-N-K+1,N-K+1):
    
    # Gets x decomposition in m signals
    # x_m size N
    x_m = x[m:m+N].copy()
        
    # Padding signal h 
    # to N size    
    h_pad = np.pad(h, (0, N-K),
                 'constant', constant_values=(0,0))
    
    
    # Circular convolve h*x_m with size N
    m_convolve = scipy.signal.convolve(h_pad, np.concatenate((x_m, x_m)))
    
    # Discards K-1 first convolution samples
    # and gets N-(K-1) samples following these
    # K-1+COLVOLVE_SIZE-(K-1) = CONVOLVE_SIZE
    m_convolve = m_convolve[K-1:CONVOLVE_SIZE]

    
    # Adding process to output
    y_overlap_save[m:m+CONVOLVE_SIZE-K+1] = y_overlap_save[m:m+CONVOLVE_SIZE-K+1] + \
                                            m_convolve
    

# %% 4. Output saving
#################################
##    Plot all in one plot     ##
#################################

# fig, axs = plt.subplots(3)
# fig.suptitle('Filtered signals')
# axs[0].set_title('Linear Convolution')
# axs[1].set_title('Overlap And Add')
# axs[2].set_title('Overlap And Save')
# axs[0].plot(y_convolution)
# axs[1].plot(y_overlap_add)
# axs[2].plot(y_overlap_save)
# plt.show()

#################################
##    Plot each one separated  ##
#################################

fig1, axs1 = plt.subplots(2)
fig2, axs2 = plt.subplots(2)
fig3, axs3 = plt.subplots(2)

plotAudio(axs1, x, y_convolution, 'Input Signal', 'Linear Convolution')
plotAudio(axs2, x, y_overlap_add, 'Input Signal', 'Overlap And Add')
plotAudio(axs3, x, y_overlap_save, 'Input Signal', 'Overlap And Save')

plt.show()

sf.write('output_convolution.wav', y_convolution, fs, subtype='PCM_24')
sf.write('output_overlap_add.wav', y_overlap_add, fs, subtype='PCM_24')
sf.write('output_overlap_save.wav', y_overlap_save, fs, subtype='PCM_24')
