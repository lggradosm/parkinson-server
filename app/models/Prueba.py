from sqlalchemy import Column, Integer, String, TIMESTAMP
from config.database import Base

class Prueba(Base):
  __tablename__ = "pruebas"
  id = Column(Integer, primary_key=True, index=True)
  resultado = Column(Integer, nullable=False)
  fecha = Column(TIMESTAMP, nullable=False) 
  usuario_id = Column(Integer,  nullable=False)  