import uvicorn
import json

from fastapi import FastAPI, Request
from utils.database import execute_query_json 
from controllers.PokRcontroller import insert_pokemon_r, update_pokemon_r, select_pokemon_request, get_all_request, delete_pokemon_request
from models.PokeRequest import PokeRequest
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def add_cors_header(request: Request, exc: Exception):
    return JSONResponse(
        content={"detail": str(exc)},
        status_code=500,
        headers={"Access-Control-Allow-Origin": "*"}
    )

@app.get("/")
async def read_root():
    query = "SELECT * FROM proyecto2pok.messages"
    result = await execute_query_json(query)
    result_dict = json.loads(result)
    return result_dict

@app.get("/version")
async def get_version():
    return {"version": "0.3.0"}

@app.post("/api/request")
async def create_request(poke_request: PokeRequest):
   return await insert_pokemon_r(poke_request)

@app.put("/api/request")
async def update_request(poke_request: PokeRequest):
   return await update_pokemon_r(poke_request)

@app.get("/api/request/{request_id}")
async def select_request(request_id: int):
    return await select_pokemon_request(request_id)

@app.get("/api/request")
async def select_all_request():
    return await get_all_request()

@app.delete("/api/report/{report_id}")
async def delete_request(report_id: int):
    return await delete_pokemon_request(report_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000) 
    
    