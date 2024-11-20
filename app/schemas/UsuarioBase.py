from pydantic import BaseModel, Field
from typing import Optional, TypeVar
from datetime import date

class UsuarioBase(BaseModel):
    nombres: Optional[str] = Field(..., min_length=1, max_length=100, example="Gabriel")
    apellidos: Optional[str] = Field(..., min_length=1, max_length=100, example="Grados")
    nombre_usuario: Optional[str] = Field(..., min_length=3, max_length=100, example="gabrielgrados")
    contrasena: Optional[str] = Field(..., min_length=6, max_length=255, example="password123")
    genero: Optional[str] = Field(None, max_length=20, example="Masculino")  # Opcional
    fecha_nacimiento: Optional[date] = Field(None, example="1990-01-01")  # Opcional
    estado: Optional[int] = 1  # Por defecto 1

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    nombre_usuario: str
    contrasena: str

class UsuarioResponse(BaseModel):
    id: int
    nombres:str
    apellidos: str
    nombre_usuario: str
    genero: str
    fecha_nacimiento: date
    estado: int