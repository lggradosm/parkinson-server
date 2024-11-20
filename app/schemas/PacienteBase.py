from pydantic import BaseModel
from datetime import datetime

class PacienteBase(BaseModel):
  nombres:str
  genero: str
  edad: int
  estado: int
  
  file_name:str
  class Config: 
    from_attributes = True
  
class PacienteRequest(PacienteBase):
  class Config:
    from_attributes = True

class PacienteResponse(PacienteBase):
  id: int

  class Config:
    from_attributes = True