from fastapi import APIRouter, HTTPException
from api.schemas import QueryRequest, QueryResponse
from models.model_interface import get_access_token, send_prompt
from models.search_interface import search_itmo_news
import json
import asyncio

router = APIRouter()

@router.post("/request", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        sources_task = asyncio.create_task(search_itmo_news(request.query))
        token_task = asyncio.create_task(get_access_token())

        sources, access_token = await asyncio.gather(sources_task, token_task)
        print(f"{sources =}")

        raw_response = send_prompt(request.query, sources, access_token)
        print(f"{raw_response =}")

        response_data = json.loads(raw_response)
        response_data['reasoning'] += ' Ответ получен моделью GigaChat-Pro.'
        print(f"{response_data =}")

        return QueryResponse(
            id=request.id,
            answer=response_data.get("answer"),
            reasoning=response_data.get("reasoning", ""),
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))