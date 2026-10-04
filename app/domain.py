from pydantic import BaseModel,Field
from typing import Literal,Any
class Identity(BaseModel):
 tenant_id:str; principal_id:str; kind:Literal["human","agent","service"]; roles:list[str]=Field(default_factory=list)
class Source(BaseModel):
 document:str; repository:str|None=None; author:str|None=None; organization:str|None=None; uri:str|None=None
class Provenance(BaseModel):
 created_at:str; ingested_at:str; ingestion_pipeline:str; transformations:list[str]=Field(default_factory=list)
 parent_chunks:list[str]=Field(default_factory=list)
class Security(BaseModel):
 signature:str=""; integrity_verified:bool=False; trust_score:float=0.5
 poison_score:float=0.0; contradiction_score:float=0.0; source_reputation:float=0.5; corroboration:float=0.0
class Authorization(BaseModel):
 tenant:str; classification:Literal["PUBLIC","INTERNAL","CONFIDENTIAL","RESTRICTED"]="INTERNAL"
 allowed_principals:list[str]=Field(default_factory=list)
class KnowledgePassport(BaseModel):
 object_id:str; object_type:Literal["chunk","graph_node","graph_edge"]; content:str; content_hash:str=""
 source:Source; provenance:Provenance; security:Security; authorization:Authorization; metadata:dict[str,Any]=Field(default_factory=dict)
class IngestRequest(BaseModel):
 actor:Identity; passport:KnowledgePassport
class QueryRequest(BaseModel):
 actor:Identity; query:str; top_k:int=5
class Candidate(BaseModel):
 object_id:str; content:str; semantic_similarity:float; secure_rank:float; reasons:list[str]; passport:KnowledgePassport
class QueryResponse(BaseModel):
 query:str; candidates:list[Candidate]; context:list[str]; blocked:list[str]; integrity_summary:dict[str,Any]
