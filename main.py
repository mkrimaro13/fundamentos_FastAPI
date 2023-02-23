from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = 'My First API with FastAPI'
app.version = '0.0.1'

class Game(BaseModel):
    # El método "Field" valida los datos que se reciben en el body
    id: int = Field(gt= 1, le=9999)# Optional[int] = None # Valor opcional
    title: str = Field(min_length=5,max_length=15) # Valor por defecto, Mínimo de caracteres y Máximo de caracteres.
    year: int = Field(gt= 1900, le=2023)
    rating: float = Field(gt= 0.0, le=10.0)
    category: str = Field(min_length=3,max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 9999,
                "title": "Guild Wars 2",
                "year": 2009,
                "rating": 9.3,
                "category": "Rol"
            }
        }

@app.get('/', tags=['Home'])
def message():
    # return "Hi!"
    return HTMLResponse('<h1>Hello World</h1>')

games =[
    {
        'id': 1,
        'title': 'Nier Automata',
        'year': '2017',
        'rating': 9,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Dead Cells',
        'year': '2022',
        'rating': 8.9,
        'category': 'Aventura'    
    } 
]
@app.get('/games', tags=['Games'], response_model= list[Game])
def get_Games() -> list[Game]:
    return JSONResponse(content=games)

@app.get('/games/{id}', tags=['Games'], response_model=Game)
def get_games_by_id(id: int = Path(default = 1,ge = 1, le=2000)) -> Game: # El método 'Path' valida el valor que se pasa por parámetro de ruta
    game = list(filter(lambda x: x['id'] == id, games))
    if game is not None:
        return JSONResponse(content=game)
    return  JSONResponse(content=[])


@app.get('/games/', tags=['Games'], response_model= list[Game])
def get_games_by_category(category: str = Query(min_length= 3, max_length=15)) -> list[Game]:# El método 'Query' valida el valor que se pasa por parámetro Query
    # si no indica en la ruta, FastAPI lo detectará como un parámetro query
    # category = list(filter(lambda x: x['category'] == category, games))
    category = [game for game in games if game['category'] == category]
    if category is not None:
        return JSONResponse(content= category)
    return  JSONResponse(content=[])

@app.post('/games/', tags=['Games'], response_model=dict)
def create_Games(game: Game) -> dict:
    games.append(game.dict())
    return JSONResponse(content={"message":"Successful registration"})

@app.put('/games/{id}', tags=['Games'], response_model=dict)
def put_Games(id : int, game: Game) -> dict:
    for gm in games:
        if gm['id'] == id:
            gm.update(game)
    return JSONResponse(content={"message":"Successful modification"})

@app.delete('/games/{id}', tags= ['Games'], response_model=dict)
def delete_game(id: int) -> dict:
    for game in games:
        if game["id"] == id:
            games.remove(game)
            return JSONResponse(content={"message":"Successful removal"})