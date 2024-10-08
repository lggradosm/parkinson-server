from fastapi import  File, UploadFile, APIRouter, Form, Depends
from fastapi.responses import JSONResponse
from pathlib import Path
from services.parkinson_service import detect_parkinson
from services.drive_service import upload_file_to_drive
from services.audio_service import convert_to_wav, save_audio_tmp
from pydub import AudioSegment
import shutil
from parselmouth.praat import call
import numpy as np
import noisereduce as nr
import soundfile as sf
import librosa
import tempfile
import os
from io import BytesIO
from schemas.PacienteBase import PacienteRequest
from services.paciente_service import create_paciente
import json
from config.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter()


@router.get("/drive")
async def drive_list():
  return JSONResponse(content=list_files(), status_code=200)


# REQUIERE "ffmpeg" para convertir de m4a a wav
@router.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...),  paciente: str = Form(...), db: Session = Depends(get_db)):
  try:
    (wav_io, file_name, audio,file_name) = convert_to_wav(file.file.read(),file.filename.rsplit('.', 1)[0])
    upload_file_to_drive(wav_io, file_name)
    audio_path = Path("uploaded_files/test.wav")
    save_audio_tmp(audio, audio_path)
    paciente_json = json.loads(paciente)
    paciente_data = {
      "nombre": paciente_json.get("nombre"),
      "genero": paciente_json.get("genero"),
      "edad": paciente_json.get("edad"),
      "estado": 1,
      "file_name":file_name
    }
    paciente_request = PacienteRequest(**paciente_data)
    response = create_paciente(paciente_request, db)
    if response:
      return JSONResponse(content={"message":"Guardado exitosamente"}, status_code=201)
    print(response)
    return JSONResponse(content={"message":"Error"}, status_code=500)
    
    # print("uploading")
    # audio_data = BytesIO( file.file.read())
    # audio = AudioSegment.from_file(audio_data, format="m4a")
    # wav_io = BytesIO()
    # audio.export(wav_io, format="wav")
    # wav_io.seek(0)
    # file_name = f"{file.filename.rsplit('.', 1)[0]}.wav"
    # upload_file(wav_io, file_name)
    # audio_path = Path("uploaded_files/test.wav")

    # if audio_path.exists():
    #   print("existe")
    #   os.remove(audio_path)
    # audio.export(audio_path, format="wav")
    # return JSONResponse(content={"message":"Negativo"}, status_code=200)

    
    # parkinson = detect_parkinson(audio_path)
    # if(parkinson == False): 
    #   print("Sano")
    #   return JSONResponse(content={"message":"Negativo"}, status_code=200)
    # print("Parkinson")
    # return JSONResponse(content={"message":"Positivo"}, status_code=200)
  except Exception as e:
      print(e)
      return JSONResponse(content={"message": str(e)}, status_code=500)


@router.get("/test")
def test():
  return JSONResponse(content={"message":"test"},status_code=200)

@router.get("/start")
def start():
  try:
    # Ruta de archivo
    file_path = Path("uploaded_files/recording.wav")
    # Comprobando si existe el archivo
    if not file_path.exists():
      return JSONResponse(content={"message": "El archivo de audio no existe."}, status_code=400)
    # Obtener el cambio de amplitud del audio (y), medida de aplitudes por segundo de audio (sr).
    y, sr = librosa.load(file_path)
    # Aplicar reducción de ruido
    reduced_noise =  noise_reducer(y=y, sr=sr, prop_decrease=0.2)

  except Exception as e:
    # Manejar errores y retornar un mensaje de error al cliente
    return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=500)


def noise_reducer(y,sr,prop_decrease):
  reduced_noise = nr.reduce_noise(y=y, sr=sr, prop_decrease=prop_decrease)
  output_file = "uploaded_files/recording_noiseless.wav"
  sf.write(output_file, reduced_noise,sr)
  return reduced_noise
