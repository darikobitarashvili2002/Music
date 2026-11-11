import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel


app=FastAPI()

class AlbumCrete(BaseModel):
    title:str
    artist:str

class Album(BaseModel):
    id:int

group_db = [
    {"id": 1, "title": "Old Title", "artist": "Old Artist"},
    {"id": 2, "title": "Another Album", "artist": "Someone"},
]


@app.put("/{album_id}", response_model=Album, summary="Изменить информацию в альбоме")
def update_album(album_id: int, album_in: Album):
    album = next((b for b in group_db if b["id"] == album_id), None)
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Альбом не найден"
        )
    album.update(album_in.model_dump())
    return album
client=TestClient(app)

def test_album_update_sussec():
    payload={'title':'New Title','artist':'New Artist'}
    response=client.put('/1',json=payload)
    assert response.statuse_code==200
    assert response.json()=={
        'id':1,
        'title':'New tirle',
        'artist':'New_artist'

    }
    updated_album = next((b for b in group_db if b["id"] == 1), None)
    assert updated_album['title']=='New Title'
    assert updated_album['artist']=='New Artist'

def text_album_not_found():
    payload={'title':'Ghoast Title','artist':'Ghoast Artist'}
    response=client.put('/325', json=payload)
    assert response.status_code==404
    assert response.json['detail']=='Альбом не найден'








