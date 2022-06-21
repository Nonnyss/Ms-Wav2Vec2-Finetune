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
from youtubesearchpython import VideosSearch
#import streamlit.components.v1 as components
import pydub
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


def audio_analysis(audio):
        if audio!=0:
            output = query(API_URL_Non,audio)
            
            with st.expander("Result"):
                predict = output.get('text')

                
                videosSearch = VideosSearch(predict, limit = 2)
                result = videosSearch.result()
                l = result.get('result')
                st.subheader(l[0].get('title'))

                watch = l[0].get('link')

                frame = f'<iframe src="http://www.youtube.com/embed/{watch[-11:]}" width="560" height="315" frameborder="0" allowfullscreen></iframe>'
                st.markdown(frame, unsafe_allow_html=True)

        else:

            paths = glob('/content/split_*.wav')
            sentence = ""
            for i in range(len(paths)):
                path = f'/content/split_{i+1}.wav'
                with open(f"{path}", "rb") as wavfile:
                    input_wav = wavfile.read()
                rate, data = read(io.BytesIO(input_wav))
                bytes_wav = bytes()
                byte_io = io.BytesIO(bytes_wav)
                write(byte_io, rate, data)
                audio = byte_io.read()
                
                while(True):
                    Te = query(API_URL_Non,audio)
                    if 'text' in Te:
                        sentence1+=Te['text']
                        break


            with st.expander("Result"):
                st.write(f"{sentence}")

                


def audio_file():
    uploaded_file = st.file_uploader("Upload file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        st.audio(bytes_data,'audio/mp3')
        if st.button("Find your fav Song!"):
            audio_analysis(bytes_data)




option = st.sidebar.selectbox(
            'Input',
            ('Audio',))

st.write('Your selected:', option)
if option == 'Audio':
    audio_file()
#if option == 'Sing':
#    st_audiorec()































