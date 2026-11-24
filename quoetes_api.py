
from fastapi import FastAPI

app = FastAPI(title="Welcome To Quotes API")
QUOTES = [
{"text": "Simple is better than complex."},
{"author": "The Zen of Python"},
{"text": "Python for beginners"},
{ "author": "No one"}
]
new_quote = {"Harav": "teaching data"}

@app.post("/posted")
def posted():
    QUOTES.append(new_quote)
    return QUOTES

@app.get("/quotes")
def get_quotes():
    return QUOTES

@app.get("/quotes/count")
def get_count():
    count = 0
    for q in QUOTES:
        count += 1
    return {"count": 4}

@app.get("/quotes/{number}")
def get_one_quote(number:int):
    if number > len(QUOTES):
        return {"Hey dude": "your index is out of range"}
    return QUOTES[number]

@app.delete("/deleting")
def delete():
    QUOTES.pop()
    return QUOTES


@app.put("/updating")
def updating():
    QUOTES[-1] = {"J.K. Rolling": "very successfull"}
    return QUOTES



