import fastapi
app = fastapi.FastAPI()

@app.get("/")
def hello_world():
    return "Hello, world!"
