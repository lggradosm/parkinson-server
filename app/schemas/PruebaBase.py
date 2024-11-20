from pydantic import BaseModel, Field
from typing import Optional, TypeVar
from datetime import datetime

class PruebaBase(BaseModel):
    resultado: int = Field(...,  example=1)
    usuario_id: int = Field(..., example=32)
    class Config:
        from_attributes = True

class PruebaResponse(BaseModel):
  resultado: int

class PruebaRequest(BaseModel):
  usuario_id: int
