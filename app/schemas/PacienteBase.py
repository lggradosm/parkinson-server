from pydantic import BaseModel
from datetime import datetime

class PacienteBase(BaseModel):
  nombre:str
  genero: str
  edad: int
  estado: int
  file_name:str
  class Config: 
    orm_mode = True
  
class PacienteRequest(PacienteBase):
  class Config:
    orm_mode = True

class PacienteResponse(PacienteBase):
  id: int

  class Config:
    orm_mode = True