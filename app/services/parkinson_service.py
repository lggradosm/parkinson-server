from pydub import AudioSegment
import numpy as np
from io import BytesIO
from parselmouth.praat import call
import parselmouth
import pandas as pd
import joblib
import re


def detect_parkinson (audio_path):
    sound = parselmouth.Sound(str(audio_path))
    f0min = 75
    f0max = 300
    startTime = 0
    endTime = 0
    unit = "Hertz"
    (meanF0,maxf0,minf0,localJitter,localabsoluteJitter, rapJitter, ppq5Jitter,ddpJitter,localShimmer,localdbShimmer,apq3Shimmer, apq5Shimmer, apq11Shimmer,ddaShimmer, nhr, hnr) = get_features(
    sound, unit, startTime, endTime, f0min, f0max)
    dataframe = pd.DataFrame(np.column_stack([meanF0,maxf0,minf0,localJitter,localabsoluteJitter, rapJitter, ppq5Jitter,ddpJitter,localShimmer,localdbShimmer,apq3Shimmer, apq5Shimmer, apq11Shimmer,ddaShimmer, nhr, hnr]), 
                  columns=["MDVP:Fo(Hz)","MDVP:Fhi(Hz)","MDVP:Flo(Hz)","MDVP:Jitter(%)","MDVP:Jitter(Abs)","MDVP:RAP","MDVP:PPQ","Jitter:DDP","MDVP:Shimmer","MDVP:Shimmer(dB)","Shimmer:APQ3","Shimmer:APQ5","MDVP:APQ","Shimmer:DDA","NHR","HNR"])
    dataframe = dataframe.apply(pd.to_numeric, errors="coerce")
    model = joblib.load("./export/modelo.pkl")
    scaler = joblib.load("./export/scaler.pkl")
    scaled_new_data = scaler.transform(dataframe.values)
    prediction = model.predict(scaled_new_data)
    if (prediction[0] == 1):
        return True
    else:
        return False


def get_features(voiceID, unit, startTime, endTime,f0min,f0max):
    sound = parselmouth.Sound(voiceID) 

    pitch = call(sound, "To Pitch", float(startTime), 75, 300) 

    meanF0 = call(pitch, "Get mean", startTime, endTime, unit) 

    maxf0 = call(pitch, "Get maximum", startTime, endTime, unit, "Parabolic")

    minf0 = call(pitch, "Get minimum", startTime, endTime, unit, "Parabolic")

    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)

    localJitter = call(pointProcess, "Get jitter (local)", startTime, endTime, 0.0001, 0.02, 1.3)

    pulses = call([sound, pitch], "To PointProcess (cc)")
    voice_report = call([sound, pitch, pulses], "Voice report", startTime, endTime, f0min, f0max, 1.3, 1.6, 0.03, 0.45)
    voice_report_array=re.findall(r'-?\d+\.?\d*',voice_report)
    hnr = voice_report_array[-1]
    nhr = voice_report_array[-2]
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", startTime, endTime, 0.0001, 0.02, 1.3)

    rapJitter = call(pointProcess, "Get jitter (rap)", startTime, endTime, 0.0001, 0.02, 1.3)

    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", startTime, endTime, 0.0001, 0.02, 1.3)

    ddpJitter = call(pointProcess, "Get jitter (ddp)", startTime, endTime, 0.0001, 0.02, 1.3)

    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", startTime, endTime, 0.0001, 0.02, 1.3, 1.6)

    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", startTime, endTime, 0.0001, 0.02, 1.3, 1.6)

    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", startTime, endTime, 0.0001, 0.02, 1.3, 1.6)

    apq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", startTime, endTime, 0.0001, 0.02, 1.3, 1.6)

    apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", startTime, endTime, 0.0001, 0.02, 1.3, 1.6)

    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", startTime, endTime, 0.0001, 0.02, 1.3, 1.6)

    return meanF0,maxf0,minf0,localJitter,localabsoluteJitter, rapJitter, ppq5Jitter,ddpJitter,localShimmer,localdbShimmer,apq3Shimmer, apq5Shimmer, apq11Shimmer,ddaShimmer, nhr, hnr

