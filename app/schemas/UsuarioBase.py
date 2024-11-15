from pydantic import BaseModel, Field
from datetime import date

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    apellidos: str = Field(..., min_length=1, max_length=50)
    fecha_nacimiento: date
    sexo: str = Field(..., regex="^(Masculino|Femenino)$")
    usuario: str = Field(..., min_length=3, max_length=50)
    contrasena: str = Field(..., min_length=6)
    estado: bool = True

    class Config:
        orm_mode = True
class UsuarioRequest(UsuarioBase):
  class Config:
    orm_mode = True