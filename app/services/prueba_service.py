
from sqlalchemy.orm import Session
from schemas.PruebaBase  import PruebaBase, PruebaRequest
from schemas.ResponseBase import ResponseBase
from models.Prueba import Prueba
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from datetime import datetime
from sqlalchemy.future import select

async def create_prueba(prueba:PruebaBase, db: Session )->ResponseBase:
  try:
    prueba_model = Prueba(
      resultado=prueba.resultado,
      fecha= datetime.now(),
      usuario_id=prueba.usuario_id
    )
    db.add(prueba_model)
    db.commit()
    db.refresh(prueba_model)
  
    return ResponseBase(status=200, message="Prueba creada", data={
      "resultado": prueba_model.resultado
    })
  except SQLAlchemyError as e:
    db.rollback()
    print(e)
    return ResponseBase(status=500, message="Server Error", data=None)
  
async def get_all_by_user(prueba: PruebaRequest, db:Session)-> ResponseBase:
  try:
    query = select(Prueba).where(Prueba.usuario_id == prueba.usuario_id).order_by(Prueba.fecha.desc())
    result = db.execute(query)
    pruebas = result.scalars().all()
    if not pruebas:
      return ResponseBase(status=404, message="Aun no tiene pruebas", data=[])
    pruebas_response = [
      {
        "id": prueba.id,
        "resultado": prueba.resultado,
        "fecha": prueba.fecha.isoformat(), 
        "usuario_id": prueba.usuario_id
      }
      for prueba in pruebas
    ]
    return ResponseBase(status=200, message="Pruebas obtenidas", data=pruebas_response)
  except SQLAlchemyError as e:
    print(e)
    return ResponseBase(status=500, message="Server Error", data=None)
  
