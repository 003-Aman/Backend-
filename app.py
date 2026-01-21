from fastapi import FastAPI

app = FastAPI()

notes =[]
next_id=1

@app.get("/notes")
def get_notes():
    return notes