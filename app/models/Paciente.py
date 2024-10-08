from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime

class Paciente(Base):
  __tablename__ = "pacientes"

  id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
  nombre = Column(String)
  genero = Column(String)
  edad = Column(Integer)
  estado = Column(Integer)
  file_name = Column(String)
  created_at = Column(DateTime)