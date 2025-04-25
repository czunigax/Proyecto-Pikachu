import json
import logging

from fastapi import HTTPException, status
from models.PokeRequest import PokeRequest  
from utils.database import execute_query_json   
from utils.AQueue import AQueue  
from utils.ABlob import ABlob  # Asegúrate de que la ruta sea correcta       

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def select_pokemon_request(id : int) :
    try:  
        query = "select * from proyecto2pok.requests where id = ?"
        params = (id,)
        result = await execute_query_json(query, params)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        logger.error(f"Error updating Pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# En update_pokemon_r (corrigiendo también el typo):
async def update_pokemon_r(poke_request: PokeRequest) -> dict:
    try:
        query = "exec proyecto2pok.update_poke_request ? ? ?"
        
        if not poke_request.url:  # Corregido de pokemon_request a poke_request
            poke_request.url = ""
        
        params = (poke_request.id, poke_request.status, poke_request.url)
        result = await execute_query_json(query, params, needs_commit=True)  # Cambiado de db.execute
        return json.loads(result)
            
    except Exception as e:
        logger.error(f"Error updating Pokemon: {e}")
        raise HTTPException(status_code=500, detail="Error updating Pokemon")
    

# En insert_pokemon_r:
async def insert_pokemon_r(poke_request: PokeRequest) -> dict:
    try:
        query = "exec proyecto2pok.createpokrequest ?"
        params = (poke_request.pokemon_type,)
        result = await execute_query_json(query, params, needs_commit=True)  # Cambiado de db.execute
        await AQueue().insert_message(result)
        return json.loads(result)
    except Exception as e:
        logger.error(f"Error inserting Pokemon: {e}")
        raise HTTPException(status_code=500, detail="Error inserting Pokemon")
    
async def get_all_request() -> dict:
    query = """
        select 
            r.id as ReportId
            , s.description as Status
            , r.type as PokemonType
            , r.url 
            , r.created 
            , r.updated
        from proyecto2pok.requests r 
        inner join proyecto2pok.status s 
        on r.id_status = s.id 
    """
    result = await execute_query_json( query  )
    result_dict = json.loads(result)
    blob = ABlob()
    for record in result_dict:
        id = record['ReportId']
        record['url'] = f"{record['url']}?{blob.generate_sas(id)}"
    return result_dict
   
async def delete_pokemon_request(poke_request_id: int) -> dict:
    try:
        #  Intentamos eliminar primero el blob
        blob = ABlob()
        blob_response = blob.delete_blob(poke_request_id)

        if not blob_response["success"]:
            # Si falla, no hacemos nada más
            return [{
                "message": " No se eliminó el reporte en la base de datos porque falló la eliminación del blob.",
                "blob_deletion": blob_response
            }]
        
        #  Si el blob fue eliminado correctamente, eliminamos en la base de datos
        query = "exec pokequeue.delete_poke_request ?"
        params = (poke_request_id,)
        result = await execute_query_json(query, params, True)

        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            result = []

        #  Adjuntamos al resultado de la base la info del blob
        if result:
            result[0]["blob_deletion"] = blob_response

        return result

    except Exception as e:
        logger.error(f"Error deleting Pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")    