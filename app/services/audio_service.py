from io import BytesIO
from pydub import AudioSegment
from datetime import datetime
from pathlib import Path
import os


def convert_to_wav(file: bytes,filename, now: datetime):
    try:
      audio_data = BytesIO(file)
      audio = AudioSegment.from_file(audio_data, format="m4a")
      wav_io = BytesIO()
      audio.export(wav_io, format="wav")
      wav_io.seek(0)
      
      timestamp = now.strftime("%d-%m-%y-%H:%M:%S")
      file_name = f"{filename+"_"+timestamp}.wav"
      return wav_io, file_name, audio, file_name
    except Exception as e:
       print(e)

def save_audio_tmp(audio:AudioSegment,audio_path:Path):
  if audio_path.exists():
    os.remove(audio_path)
  audio.export(audio_path, format="wav")
    