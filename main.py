from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title='Все проекты Криса Поля',
    description=' Здесь представлены все проекты Криса Поля с альбомами и песнями в них'
)

class ProjectBase(BaseModel):
    number: int  # Исправлено: numder -> number
    project: str = Field(..., example='Tumor', description='Проекты')
    albums: str = Field(..., example='Un gott', description='Альбомы')
    sing: str = Field(..., example='Wir', description='Песни')

class ProjectCreate(BaseModel):
    pass 

class Album(BaseModel):
    id: int
    nam: str = Field(..., example='BlutEngel', description='Группа')
    song: str = Field(..., example='Alles', description='Песня')

class AlbumCreate(BaseModel):
    nam: str = Field(..., example='BlutEngel', description='Группа')
    song: str = Field(..., example='Alles', description='Песня')

# База данных
group = [
    {'id': 1, 'nam': 'Blutengel', 'song': 'Alles'},
    {'id': 2, 'nam': 'Tumor', 'song': 'Wir'}
]

album_id_counter = 3

@app.get('/album', response_model=List[Album], summary='Все проекты Криса Поля')
def get_albums(albums: Optional[str] = None):
    if albums:
        # Исправлено: поиск идет по ключу 'nam', так как ключа 'project' в group нет
        filtered_albums = [b for b in group if albums.lower() in b['nam'].lower()]
        return filtered_albums 
    return group  # Исправлено: возвращаем весь список group, если фильтр пустой

@app.get('/album/{album_id}', response_model=Album, summary='Получить альбом по номеру')
def get_album_by_id(album_id: int):  # Исправлено: имя функции изменено во избежание конфликта, аргумент совпадает с {album_id}
    # Исправлено: поиск идет по ключу 'id', а не 'numder'
    album = next((b for b in group if b['id'] == album_id), None)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Альбом не найден')
    return album

@app.post('/albums', response_model=Album, status_code=status.HTTP_201_CREATED, summary='Новый альбом')
def create_album(album_in: AlbumCreate):
    global album_id_counter
    new_album = album_in.model_dump()
    new_album['id'] = album_id_counter
    group.append(new_album)
    album_id_counter += 1
    return new_album

@app.put('/albums/{album_id}', response_model=Album, summary='Изменение информации в альбоме')
def update_album(album_id: int, album_in: AlbumCreate):  # Исправлено: {book_id} в пути заменено на {album_id}
    album = next((b for b in group if b['id'] == album_id), None)  # Исправлено: сохраняем в album, а не в book
    if not album:  # Исправлено: проверка переменной album вместо некорректной albums
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Альбом не найден')
    
    album.update(album_in.model_dump())
    return album 

@app.delete('/albums/{album_id}', status_code=status.HTTP_204_NO_CONTENT, summary='Удалить альбом')
def delete_album(album_id: int):  # Исправлено: убрана лишняя скобка ')' из пути эндпоинта
    global group
    album = next((b for b in group if b['id'] == album_id), None)  # Исправлено: условие == вместо !=, переменная album вместо book
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Альбом не найден') 
    
    # Исправлено: b['id'] вместо b('id')
    group = [b for b in group if b['id'] != album_id]
    return None

    


    








                   

                      