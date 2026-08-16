from typing import Any,Literal
from pydantic import BaseModel,Field
class ZeusDecision(BaseModel):
 response:str
 category:Literal['HOME','CODING','LINEAR','GITHUB','SYSTEM','NETWORK','GENERAL','UNKNOWN']
 action:str
 target:Literal['LOCAL','BACKLOG','RTX_3090','CLARIFY','NONE']
 risk_level:int=Field(ge=0,le=3)
 tool:Literal['none','ha_read','ha_light']='none'
 arguments:dict[str,Any]={}
class HomeEntityQuery(BaseModel):
    domain: str | None = None
    device_classes: list[str] = []
    states: list[str] = []
    name_terms: list[str] = []
    requested_state_label: str | None = None 
