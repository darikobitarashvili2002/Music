from fastapi import FastAPI
from app.routers import albums
app = FastAPI(
    title='Все проекты Криса Поля',
    description=' Здесь представлены все проекты Криса Поля с альбомами и песнями в них'
)

app.include_router(albums.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Добро пожаловать в архив проектов Криса Поля! Перейдите на /docs для просмотра API."}

    

    








                   

                      