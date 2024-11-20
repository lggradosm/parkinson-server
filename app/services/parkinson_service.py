import numpy as np
from parselmouth.praat import call
from schemas.PruebaBase import PruebaBase
from schemas.ResponseBase import ResponseBase
from services.prueba_service import create_prueba
import parselmouth
import pandas as pd
import joblib
import re
from scipy.signal import butter, lfilter
from sqlalchemy.orm import Session


async def detect_parkinson (audio_path, usuario_id , db: Session):
    try:
        # Procesar archivo de audio
        print("usuario_id" + str(usuario_id))
        sound = parselmouth.Sound(str(audio_path))
        f0min, f0max, startTime, endTime = 75, 300, 0, 0
        unit = "Hertz"
        
        # Extraer características
        (meanF0,localJitter,localabsoluteJitter, rapJitter, ppq5Jitter,ddpJitter,localShimmer,localdbShimmer,apq3Shimmer, apq5Shimmer, apq11Shimmer,ddaShimmer, nhr, hnr) = get_features(
        sound, unit, startTime, endTime, f0min, f0max)
        if(is_voice(localJitter, float(hnr), float(meanF0))):
            # Crear DataFrame
            dataframe = pd.DataFrame(np.column_stack([localJitter,localabsoluteJitter, rapJitter, ppq5Jitter,ddpJitter,localShimmer,localdbShimmer,apq3Shimmer, apq5Shimmer, apq11Shimmer,ddaShimmer, nhr, hnr]), 
                    columns=["MDVP:Jitter(%)","MDVP:Jitter(Abs)","MDVP:RAP","MDVP:PPQ","Jitter:DDP","MDVP:Shimmer","MDVP:Shimmer(dB)","Shimmer:APQ3","Shimmer:APQ5","MDVP:APQ","Shimmer:DDA","NHR","HNR"])
            dataframe = dataframe.apply(pd.to_numeric, errors="coerce")
            dataframe.to_csv('./export/features_extracted.csv', index=False)

            # Cargar modelo y escalador
            model = joblib.load("./export/modelo.pkl")
            if model is None:
                raise ValueError("El modelo no se cargó correctamente.")

            scaler = joblib.load("./export/scaler.pkl")
            if scaler is None:
                raise ValueError("El escalador no se cargó correctamente.")
            
            # Escalar datos
            scaled_new_data = pd.DataFrame(scaler.transform(dataframe), columns=dataframe.columns)
            # Predicción
            prediction = model.predict(scaled_new_data)
            prueba = PruebaBase(resultado=prediction[0], usuario_id=usuario_id)
            result = await create_prueba(prueba, db)
            if result.status == 200:
                return "Positivo" if prediction[0] == 1 else "Negativo"
            else: 
                return "Error"
        else:
            return "No se detecto voz"
    except Exception as e:
        print(f"Error en `detect_parkinson`: {e}")
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

    return meanF0,localJitter,localabsoluteJitter, rapJitter, ppq5Jitter,ddpJitter,localShimmer,localdbShimmer,apq3Shimmer, apq5Shimmer, apq11Shimmer,ddaShimmer, nhr, hnr



def is_voice(localJitter, hnr, meanF0, threshold_hnr=10, threshold_f0_min=75, threshold_f0_max=300)->bool:
    if hnr < threshold_hnr:
        return False  # HNR bajo indica ruido o silencio
    
    if not (threshold_f0_min <= meanF0 <= threshold_f0_max):
        return False  # Frecuencia fuera del rango típico de voz
    
    if localJitter is None or localJitter <= 0:
        return False  # Jitter nulo o negativo no es característico de voz
    
    return True