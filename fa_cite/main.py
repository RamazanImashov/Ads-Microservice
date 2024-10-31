# main.py (FastAPI)
from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from pathlib import Path
import uvicorn

from src.advertisements.router import router as advertisement_router


app = FastAPI()


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc:ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )

app.include_router(advertisement_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8082, log_level="info")
