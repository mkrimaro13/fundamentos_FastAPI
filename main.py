from fastapi import FastAPI

app = FastAPI()
app.title = 'My First API with FastAPI'
app.version = '0.0.1'

@app.get('/', tags=['home'])
def message():
    return "Hi!"