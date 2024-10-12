from fastapi import Depends
from schemas.PacienteBase  import PacienteRequest
from config.database import get_db
from sqlalchemy.orm import Session
from models.Paciente import Paciente
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc


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
  
def get_all_pacientes(db: Session):
    try:
        pacientes = db.query(Paciente).filter(Paciente.estado == 1).order_by(desc(Paciente.id)).all()
        pacientes_list = [paciente.__dict__ for paciente in pacientes]
        for paciente in pacientes_list:
            paciente.pop('_sa_instance_state', None)
        return pacientes_list
    except SQLAlchemyError as e:
        print(e)
        return []

def get_total_pacientes(db: Session):
    try:
        total_activos = db.query(Paciente).filter(Paciente.estado == 1).count()
        return total_activos
    except SQLAlchemyError as e:
        print(e)
        return 0