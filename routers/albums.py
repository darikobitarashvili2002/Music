from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.schemas import Album, AlbumCreate
from app.database import group_db, album_id_counter

router = APIRouter(
    prefix="/albums",
    tags=["Альбомы и Проекты"]
)

@router.get("", response_model=List[Album], summary="Получить все альбомы")
def get_albums(name: Optional[str] = None):
    if name:
        return [b for b in group_db if name.lower() in b["name"].lower()]
    return group_db

@router.get("/{album_id}", response_model=Album, summary="Получить альбом по ID")
def get_album_by_id(album_id: int):
    album = next((b for b in group_db if b["id"] == album_id), None)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Альбом не найден")
    return album

@router.post("", response_model=Album, status_code=status.HTTP_201_CREATED, summary="Добавить новый альбом")
def create_album(album_in: AlbumCreate):
    global album_id_counter
    new_album = album_in.model_dump()
    new_album["id"] = album_id_counter
    group_db.append(new_album)
    album_id_counter += 1
    return new_album

@router.put("/{album_id}", response_model=Album, summary="Изменить информацию в альбоме")
def update_album(album_id: int, album_in: AlbumCreate):
    album = next((b for b in group_db if b["id"] == album_id), None)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Альбом не найден")
    
    album.update(album_in.model_dump())
    return album

@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить альбом")
def delete_album(album_id: int):
    global group_db
    album = next((b for b in group_db if b["id"] == album_id), None)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Альбом не найден")
    
    group_db = [b for b in group_db if b["id"] != album_id]
    return None