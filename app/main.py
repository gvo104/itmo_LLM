from fastapi import FastAPI
from api.endpoints import router
import uvicorn

app = FastAPI()

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    # Включение подробного вывода ошибок
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
