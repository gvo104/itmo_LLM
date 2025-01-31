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
        access_token = await token_task

        try:
            sources_data = await sources_task
            print(f"{sources_data =}")
            # Формируем строку с ссылками
            sources = ", ".join([item["url"] for item in sources_data])
            sources_list = sources.split(', ')
            # formatted_sources = [url.split('/')[0] + '//' + url.split('/')[2] for url in sources_list]
            # Формируем строку из трех summary
            summary_text = "\n".join([item["summary"] for item in sources_data])
            print(f"{summary_text =}")
        except:
            summary_text = " "
            sources_list = []
        raw_response = send_prompt(request.query, access_token, summary_text)
        print(f"{raw_response =}")

        # Обрабатываем ответ
        response_data = json.loads(raw_response)
        response_data['reasoning'] += ' Ответ получен моделью GigaChat-Pro.'
        print(f"{response_data =}")

        try:
            answer=response_data.get("answer")
            easoning=response_data.get("reasoning", "")
        except:
            answer = 1
            easoning=response_data
        return QueryResponse(
            id=request.id,
            answer=answer,
            reasoning=easoning,
            sources=sources_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))