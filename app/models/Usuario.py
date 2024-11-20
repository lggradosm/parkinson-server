from sqlalchemy import Column, Integer, String, Date
from config.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)  # VARCHAR(100), NOT NULL
    apellidos = Column(String(100), nullable=False)  # VARCHAR(100), NOT NULL
    nombre_usuario = Column(String(100), unique=True, nullable=False)  # VARCHAR(100), UNIQUE
    contrasena = Column(String(255), nullable=False)  # VARCHAR(255), NOT NULL
    genero = Column(String(20), nullable=True)  # VARCHAR(20), puede ser NULL
    fecha_nacimiento = Column(Date, nullable=True)  # DATE, puede ser NULL
    estado = Column(Integer, default=1)  # INT con valor por defecto 1