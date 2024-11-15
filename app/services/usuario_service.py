
from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.UsuarioBase  import UsuarioRequest
from models.Usuario import Usuario
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import bcrypt

async def create_usuario(usuario:UsuarioRequest, db: Session ):
  try:
    query = select(Usuario).where(Usuario.usuario == usuario.usuario)
    result = await db.execute(query)
    existe_usuario = result.scalar_one_or_none()
    if existe_usuario:
      raise HTTPException(status_code=400, detail="El usuario ya existe.")
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        apellidos=usuario.apellidos,
        fecha_nacimiento=usuario.fecha_nacimiento,
        sexo=usuario.sexo,
        usuario=usuario.usuario,
        contrasena=hash_password(usuario.contrasena),  
        estado=usuario.estado,
    )
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario
  except SQLAlchemyError as e:
    db.rollback()
    print(e)
    return False

def hash_password(password:str) -> str:
  salt = bcrypt.gensalt(rounds=10)
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  
  return hashed_password.decode('utf-8')  

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))