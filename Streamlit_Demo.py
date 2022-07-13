import streamlit as st
import requests
import json
import os
import librosa, librosa.display
import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np
import IPython
from scipy.io import wavfile
import scipy.signal
import time
from datetime import timedelta as td
from glob import glob
from scipy.io.wavfile import read, write
import io
import sounddevice as sd
import IPython.display as ipd
from youtubesearchpython import VideosSearch
#import streamlit.components.v1 as components
from pydub import AudioSegment
import pydub
import time

API_TOKEN = "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"
API_URL_Non = "https://api-inference.huggingface.co/models/Nonnyss/music-wav2vec2-th-finetune"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

#parent_dir = os.path.dirname(os.path.abspath(__file__))
#build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
#st_audiorec = components.declare_component("st_audiorec", path=build_dir)


st.title('Music Recognition🎤')

def query(API_URL,data):
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


def search(audio):
    output = query(API_URL_Non,audio)           
    # with st.expander("Result"):
    rawpredict = output.get('text')
    predict = f'เพลง {rawpredict}'
    with st.expander('View model prediction.'):
        st.write(rawpredict)            
    videosSearch = VideosSearch(predict, limit = 2)
    result = videosSearch.result()
    l = result.get('result')
    st.subheader(l[0].get('title'))

    watch = l[0].get('link')

    frame = f'<iframe src="http://www.youtube.com/embed/{watch[-11:]}" width="560" height="315" frameborder="0" allowfullscreen></iframe>'
    st.markdown(frame, unsafe_allow_html=True)


def timer(duration):
    while duration: 
        mins, secs = divmod(duration, 60) 
        timer = f"{secs} seconds Left"
        # print(timer, end=" \r") 
        timerst.markdown(timer)
        time.sleep(1) 
        duration -= 1
    timerst.markdown("Recording Ended")
    


def record_audio(filename):
    

    sap=44000  
    duration = 7
    #start recording 
    myrecording = sd.rec(int(duration * sap), samplerate=sap, channels=2)
    timer(duration)  
    # st.write("Stop") 
    
    sd.wait()
    

    write(filename, sap, myrecording)
    



def audio_file():
    uploaded_file = st.file_uploader("Upload file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        st.audio(bytes_data,'audio/mp3')
        if st.button("Find your fav Song!"):
            print(type(bytes_data))
            search(bytes_data)

def voice():
    if st.button('Record your audio'): 
        filename ="sing.mp3"
        record_audio(filename)

        audiofile = open('sing.mp3', 'rb')
        audio_bytes = audiofile.read()
        st.audio(audio_bytes, format='mp3')
        #print(type(audio_bytes))
        # audio_bytes = audiofile.getvalue()
        # st.audio(audio_bytes,'audio/mp3')


        #if st.button("Find your fav Song!"):
        search(audio_bytes)




option = st.sidebar.selectbox(
            'Input',
            ('Upload Audio File 🎸 ','Record your own voice 🎼 '))

st.write('Your selected:', option)
if option == 'Upload Audio File 🎸 ':
    audio_file()
if option == 'Record your own voice 🎼 ':
    st.subheader("Record your audio, exceed 7 seconds.")
    timerst = st.empty()
    voice()































