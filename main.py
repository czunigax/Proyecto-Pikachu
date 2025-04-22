import uvicorn
from fastapi import FastAPI
from utils.database import execute_query_json 

app = FastAPI()


@app.get("/version")
def read_root():
    return {"version": "0.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)