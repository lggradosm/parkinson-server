from fastapi import APIRouter, Depends
from schemas.PruebaBase import PruebaRequest
from schemas.ResponseBase import ResponseBase
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from services.prueba_service import get_all_by_user

router = APIRouter()
@router.get("/{usuario_id}", response_model=ResponseBase)
async def registrar_usuario(usuario_id: int, db:AsyncSession = Depends(get_db)):
  prueba_model = PruebaRequest(
    usuario_id=usuario_id
  )
  pruebas = await get_all_by_user(prueba_model, db)
  return pruebas
  
