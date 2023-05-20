from fastapi import APIRouter, Depends

from app.api.schemas import ResultSchema
from app.model_manager import ModelManager, get_model_manager

router = APIRouter()


@router.get("/search", response_model=ResultSchema)
def search(query: str, model_manager: ModelManager = Depends(get_model_manager)):
    result = ResultSchema(**model_manager.get_result(query))
    return result
