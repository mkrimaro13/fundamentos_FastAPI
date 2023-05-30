from fastapi import Depends, FastAPI, Path, Query, HTTPException, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional

from starlette.requests import Request
from jwtmanager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI( # Creación de la instancia
    title='My First API with FastAPI',
    version='0.0.1',
    description='Just for fun'
)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@admin.com":
             return HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail='invalid credentials')

@app.get('/', tags=['Home'])
def welcome():
    return HTMLResponse('<h1>Hello World</h1>')

class user(BaseModel):
    email:str
    password: str

@app.post('/login', tags=['auth'],status_code= status.HTTP_200_OK)
def login(user: user):
    if user.email == "admin@admin.com" and user.password == "admin":
        token:str=create_token(user.dict())
        return JSONResponse(status_code= status.HTTP_200_OK,content=token)
    else: 
        return JSONResponse(status_code= status.HTTP_401_UNAUTHORIZED,content="Unauthorized, invalid credentials")

class Game(BaseModel):
    # El método "Field" valida los datos que se reciben en el body
    id: int = Field(ge= 1, le=9999)# Optional[int] = None # Valor opcional
    title: str = Field(min_length=1,max_length=50) # Valor por defecto, Mínimo de caracteres y Máximo de caracteres.
    year: int = Field(gt= 1900, le=2023)
    rating: float = Field(gt= 0.0, le=10.0)
    category: str = Field(min_length=3,max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 3,
                "title": "Guild Wars 2",
                "year": 2009,
                "rating": 9.3,
                "category": "Rol"
            }
        }

games = [
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

# GET
@app.get('/games', 
         tags=['Games'], response_model= List[Game], 
         status_code= status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_Games() -> List[Game]:
    return JSONResponse(status_code=status.HTTP_200_OK, content=games)

@app.get('/games/{id}', tags=['Games'], response_model=Game, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_games_by_id(id: int = Path(default = 1,ge = 1, le=2000)) -> Game: # El método 'Path' valida el valor que se pasa por parámetro de ruta
    game = list(filter(lambda x: x['id'] == id, games))
    if game:
        return  JSONResponse(status_code=status.HTTP_200_OK, content=game)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'status_code':404, 'message':"Not Found"})

@app.get('/games/category/', tags=['Games'], response_model= List[Game], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_games_by_category(category: str = Query(min_length= 1, max_length=15)) -> List[Game]:# El método 'Query' valida el valor que se pasa por parámetro Query
    # si no indica en la ruta, FastAPI lo detectará como un parámetro query
    category = [game for game in games if game['category'] == category]
    if category:
        return JSONResponse(status_code=status.HTTP_200_OK, content= category)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'status_code':404, 'message':"Not Found"})

#POST
@app.post('/games/', tags=['Games'], response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def post_Games(game: Game) -> dict:
    games.append(game.dict())
    return JSONResponse(status_code= status.HTTP_201_CREATED,content={"message":"Successful registration"})

#PUT
@app.put('/games/{id}', tags=['Games'], response_model=dict, dependencies=[Depends(JWTBearer())])
def put_Games(id : int, game: Game) -> dict:
    for gm in games:
        if gm['id'] == id:
            gm.update(game)
        return JSONResponse(content={"message":"Successful modification"})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'status_code':404, 'message':"Not Found"})

#DELETE
@app.delete('/games/{id}', tags= ['Games'], response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def delete_game(id: int) -> dict:
    for game in games:
        if game["id"] == id:
            games.remove(game)
            return JSONResponse(content={"message":"Successful removal"})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'status_code':404, 'message':"Not Found"})