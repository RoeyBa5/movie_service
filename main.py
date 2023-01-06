import uvicorn as uvicorn
from fastapi import FastAPI

from api.handlers import movies


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(movies, prefix='/api/prices', tags=['movies'])

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
