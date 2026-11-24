from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_server():
    return {"message": "hello from my first server!"}


@app.post("/posting_here")
def post_some(word="how"):
    return {"post": "this message"}



