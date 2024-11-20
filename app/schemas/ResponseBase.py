from pydantic import BaseModel
from typing import Optional, TypeVar,Generic

T = TypeVar("T")

class ResponseBase(BaseModel, Generic[T]):
  status: int
  message: str
  data: Optional[T]