
from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.UsuarioBase  import UsuarioBase, LoginRequest, UsuarioResponse
from schemas.ResponseBase import ResponseBase
from models.Usuario import Usuario
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import bcrypt

async def create_usuario(usuario:UsuarioBase, db: Session )->ResponseBase:
  try:
    query = select(Usuario).where(Usuario.nombre_usuario == usuario.nombre_usuario)
    result = db.execute(query)
    existe_usuario = result.scalar_one_or_none()
    if existe_usuario:
      return ResponseBase(status=400, message="El usuario ya existe", data=None)
    nuevo_usuario = Usuario(
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        fecha_nacimiento=usuario.fecha_nacimiento,
        genero=usuario.genero,
        nombre_usuario=usuario.nombre_usuario,
        contrasena=hash_password(usuario.contrasena),  
        estado=usuario.estado,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return ResponseBase(status=200, message="Usuario creado", data=None)
  except SQLAlchemyError as e:
    db.rollback()
    print(e)
    return ResponseBase(status=500, message="Server Error", data=None)
  

async def login(usuario:LoginRequest, db: Session )->ResponseBase:
  try:
    query = select(Usuario).where(Usuario.nombre_usuario == usuario.nombre_usuario)
    result = db.execute(query)
    existe_usuario = result.scalar_one_or_none()
    if not existe_usuario:
      return ResponseBase(status=400, message="Usuario y/o contraseñas incorrectas.", data=None)
    if verify_password(usuario.contrasena, existe_usuario.contrasena):
      usuario_response = UsuarioResponse(
        apellidos=existe_usuario.apellidos,
        nombres=existe_usuario.nombres,
        nombre_usuario=existe_usuario.nombre_usuario,
        fecha_nacimiento=existe_usuario.fecha_nacimiento,
        genero=existe_usuario.genero,
        estado=existe_usuario.estado,
        id=existe_usuario.id
      )
      return ResponseBase(status=200, message="Ingreso correctamente", data=usuario_response)
    return ResponseBase(status=400, message="Usuario y/o contraseñas incorrectas.", data=None)
  except Exception as e:
    print(e)
    return ResponseBase(status=500, message="Server Error", data=None)

def hash_password(password:str) -> str:
  salt = bcrypt.gensalt(rounds=10)
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  
  return hashed_password.decode('utf-8')  

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))