from fastapi import APIRouter, Depends, HTTPException,Request
from schemas.UsuarioBase import UsuarioBase, LoginRequest
from schemas.ResponseBase import ResponseBase
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from services.usuario_service import create_usuario, login
from datetime import date

router = APIRouter()
@router.post("/crear", response_model=ResponseBase)
async def registrar_usuario(usuario: Request, db:AsyncSession = Depends(get_db)):
  usuario_data = await usuario.json()
  fecha_nacimiento =  usuario_data.get("fecha_nacimiento")
  usuario_model = UsuarioBase(
      nombres=usuario_data.get("nombres"),
      apellidos=usuario_data.get("apellidos"),
      contrasena=usuario_data.get("contrasena"),
      nombre_usuario=usuario_data.get("nombreUsuario"),
      genero=usuario_data.get("genero"),
      fecha_nacimiento=date.today(),
      estado=1
      )
  nuevo_usuario = await create_usuario(usuario_model, db)
  return nuevo_usuario
  
@router.post("/login", response_model=ResponseBase)
async def registrar_usuario(usuario: Request, db:AsyncSession = Depends(get_db)):
  usuario_data = await usuario.json()
  usuario_model = LoginRequest(
      contrasena=usuario_data.get("contrasena"),
      nombre_usuario=usuario_data.get("nombreUsuario"),
      )
  return await login(usuario_model, db)
  
