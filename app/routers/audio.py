from fastapi import  File, UploadFile, APIRouter, Form, Depends
from fastapi.responses import JSONResponse
from pathlib import Path
from services.parkinson_service import detect_parkinson
from services.drive_service import upload_file_to_drive
from services.audio_service import convert_to_wav, save_audio_tmp
from parselmouth.praat import call
from schemas.PacienteBase import PacienteRequest
from services.paciente_service import create_paciente, get_all_pacientes, get_total_pacientes
import json
from config.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter()

@router.post("/detectar")
async def detectar(file: UploadFile = File(...),  paciente: str = Form(...), db: Session = Depends(get_db)):
  try:
    (wav_io, file_name, audio,file_name) = convert_to_wav(file.file.read(),file.filename.rsplit('.', 1)[0])
    upload_file_to_drive(wav_io, file_name)
    audio_path = Path("uploaded_files/test.wav")
    save_audio_tmp(audio, audio_path)
    parkinson = detect_parkinson(audio_path)
    paciente_json = json.loads(paciente)
    paciente_data = {
      "nombre": paciente_json.get("nombre"),
      "genero": paciente_json.get("genero"),
      "edad": paciente_json.get("edad"),
      "estado": 1,
      "file_name":file_name
    }
    paciente_request = PacienteRequest(**paciente_data)
    create_paciente(paciente_request, db)
    if(parkinson == False): 
      return JSONResponse(content={"message":"No presenta síntomas"}, status_code=200)
    return JSONResponse(content={"message":"Parkinson"}, status_code=200)
  except Exception as e:
      print(e)
      return JSONResponse(content={"message": str(e)}, status_code=500)


@router.post("/guardar")
async def guardar(file: UploadFile = File(...),  paciente: str = Form(...), db: Session = Depends(get_db)):
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
    create_paciente(paciente_request, db)
    return JSONResponse(content={"message":"Guardado"}, status_code=201)
  except Exception as e:
    print(e)
    return JSONResponse(content={"message": str(e)}, status_code=500)


@router.get("/bd")
def get_pacientes (db: Session = Depends(get_db)):
  data = get_all_pacientes(db)
  return JSONResponse(content={"data": data}, status_code=500)

@router.get("/bd/total")
def get_pacientes (db: Session = Depends(get_db)):
  data = get_total_pacientes(db)
  return JSONResponse(content={"total": data}, status_code=500)
