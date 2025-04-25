from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PokeRequest(BaseModel):
    id:Optional [int] = Field(None,ge =1, description="ID de Pokemon")
    pokemon_type: Optional[str] = Field(default=None, description="Tipo de Pokemon",pattern=r"^[a-zA-Z0-9]+$")
    url: Optional[str] = Field(default=None, description="URL de Peticion",pattern=r"^(https?://[^\s]+)$")
    status: Optional[str] = Field(default=None, description="Estado de Peticion",pattern=r"^(sent|completed|failed|inprogress)$")
    
    