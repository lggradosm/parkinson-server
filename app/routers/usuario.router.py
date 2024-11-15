from fastapi import APIRouter, Depends, HTTPException
from models.Usuario import Usuario
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config.database import get_db
from services.usuario_service import create_usuario

router = APIRouter()
@router.post("/usuario", response_model=Usuario)
async def registrar_usuario(usuario:Usuario, db:AsyncSession = Depends(get_db)):
  try:
    nuevo_usuario = await create_usuario(usuario, db)
    if not nuevo_usuario:
        raise HTTPException(status_code=500, detail="Error al crear el usuario")
    return nuevo_usuario
  except HTTPException as e:
    raise e
  except Exception as e:
      print(e)
      raise HTTPException(status_code=500, detail="Error interno del servidor")