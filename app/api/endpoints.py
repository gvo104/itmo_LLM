from fastapi import APIRouter, HTTPException
from api.schemas import QueryRequest, QueryResponse
from models.model_interface import get_access_token, send_prompt
import json

router = APIRouter()

@router.post("/request", response_model=QueryResponse)
def process_query(request: QueryRequest):
    try:
        access_token = get_access_token()
        print(f'{access_token=}')
        raw_response = send_prompt(request.query, access_token)
        print(f'{raw_response=}')
        
        response_data = json.loads(raw_response)
        print(f'{response_data=}')
        return QueryResponse(
            id=request.id,
            answer=response_data.get("answer"),
            reasoning=response_data.get("reasoning", ""),
            sources=response_data.get("sources", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
