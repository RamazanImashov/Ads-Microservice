# main.py (FastAPI)
from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import uvicorn
import os

from src.advertisements.router import router as advertisement_router


app = FastAPI(root_path="/ads")


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc:ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )


@app.get("/ads/openapi.json", include_in_schema=False)
async def get_openapi_json():
    return FileResponse(os.path.join(os.getcwd(), "openapi.json"))


app.include_router(advertisement_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8082, log_level="info")
