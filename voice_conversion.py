# -*- coding: utf-8 -*-
"""Voice conversion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CP1lleX5wLMmvvyEGpEWOlAQJNDhZ64R
"""

!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

fid = drive.ListFile({'q':"title='Dataset_KS.zip'"}).GetList()[0]['id']
data = drive.CreateFile({'id': fid})
data.GetContentFile('Dataset_KS.zip')

!unzip Dataset_KS.zip -d ''

"""#Voice Conversion"""

!pip install praat-parselmouth

import librosa
import IPython.display as ipd
import math
import parselmouth
import os
import soundfile as sf

"""Calculate semitones between two frequencies"""

def calculate_semitones_between(f1, f2):
  return 12 * math.log(f2/f1,2)

"""Calculate the maximum frequency of an audio sample"""

def calculate_frequency(path):
  sound = parselmouth.Sound(path)
  pitch = sound.to_pitch()
  pitch_values = pitch.selected_array['frequency']
  return max(pitch_values)

"""Calculate the slowdown factor"""

def slow_factor(sr1, sr2):
  return sr2/sr1

objectivePitch = [309, 255, 253]
objectiveSR = [5, 7]
adultMeanSR = 11

"""Calculate the average frequency of the samples"""

archivos = os.listdir('.')
current = 0
count = 0
for audio in archivos:
  if audio.endswith('.wav'):
    filename = audio
    hz = calculate_frequency(filename)
    current += hz
    count += 1
adultMeanPitch = current / count

"""Modify audios according to a specific pitch and speaking rate"""

for audio in archivos:
  if audio.endswith('.wav'):
    semitones = calculate_semitones_between(adultMeanPitch, 309)
    filename = audio
    y, sr = librosa.load(filename, sr = 192000)
    y_ps = librosa.effects.pitch_shift(y, sr, n_steps = semitones)
    y_sr = librosa.effects.time_stretch(y_ps, slow_factor(adultMeanSR, 5))
    sf.write('VC/'+ str(309) + '_' + audio, y_sr, sr)