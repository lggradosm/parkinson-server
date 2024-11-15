from config.database import Base
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean

class Usuario(Base):

  __tablename__ = "usuarios"
  id = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(50), nullable=False)
  apellidos = Column(String(50), nullable=False)
  fecha_nacimiento = Column(Date, nullable=False)
  sexo = Column(String(10), nullable=False)
  usuario = Column(String(50), unique=True, nullable=False)
  contrasena = Column(String(100), nullable=False)
  estado = Column(Boolean, default=True)