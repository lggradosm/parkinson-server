from fastapi import Depends
from schemas.PacienteBase  import PacienteRequest
from config.database import get_db
from sqlalchemy.orm import Session
from models.Paciente import Paciente
from sqlalchemy.exc import SQLAlchemyError


def create_paciente(paciente:PacienteRequest, db: Session ):
  try:
    new_paciente = Paciente(**paciente.model_dump())
    db.add(new_paciente)
    db.commit()
    db.refresh(new_paciente)
    return True
  except SQLAlchemyError as e:
    db.rollback()
    print(e)
    return False