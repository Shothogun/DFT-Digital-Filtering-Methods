%% Code designed by Victor Fabre Figueiredo %%
%% Tarefa 3 da matéria Processamento de Sinais Digitais - UnB - 2020
% Realizar a filtragem de um sinal de áudio utilizando um filtro passa-baixa 
% por 3 métodos diferentes:
%   1 - Convolução no domínio do tempo;
%   2 - Overlap and add;
%   3 - Overlap and save.
% Todos os três métodos devem apresentar os mesmos resultados.
%% Read audio file and save only the first minute of it
fileName = 'Back_In_Black.mp3';
[orig_audio,Fs] = audioread(fileName);
[x,fs] = audioread(fileName, [1, 60*Fs]); %first minute of the audio
%% Convertion of stereo audio to mono audio (DO NOT CHANGE!) %%
[m, n] = size(x);
if n == 2
    y = x(:, 1) + x(:, 2);
    peakAmp = max(abs(y)); 
    y = y/peakAmp;
    peakL = max(abs(x(:, 1)));
    peakR = max(abs(x(:, 2))); 
    maxPeak = max([peakL peakR]);
    y = y*maxPeak;    
else
    y = x;
end
%% Generate or load filter
%low_pass = designfilt('lowpassfir', 'FilterOrder', 1000, 'CutoffFrequency', 500, 'SampleRate', 44100);
low_pass = load('low_pass_filter.mat');
low_pass = low_pass.low_pass;
low_pass_coeff = low_pass.Coefficients;
%low_pass_coeff = load('low_pass_coefficients.mat');
%% Do your processing here


%% Listen to, plot and save your results

% sound(y,Fs);
% sound(convolution,Fs);
% sound(overlap_add,Fs);
% sound(overlap_save,Fs);

% figure
% hold on
% pspectrum(y,Fs)
% pspectrum(convolution,Fs)
% hold off

% figure
% hold on
% pspectrum(y,Fs)
% pspectrum(overlap_add,Fs)
% hold off

% figure
% hold on
% pspectrum(y,Fs)
% pspectrum(overlap_save,Fs)
% hold off

% audiowrite('convolution_{PrimeiroNome_Matricula}.mp3',convolution,Fs)
% audiowrite('overlap_add_{PrimeiroNome_Matricula}.mp3',overlap_add,Fs)
% audiowrite('overlap_save_{PrimeiroNome_Matricula}.mp3',overlap_save,Fs)