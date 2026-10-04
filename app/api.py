from fastapi import APIRouter,Depends,HTTPException
from app.security import auth
from app.domain import IngestRequest,QueryRequest
from app.passport import issue
from app.store import put,all_for_tenant
from app.engine import retrieve
router=APIRouter(prefix="/v1",dependencies=[Depends(auth)])
@router.post("/knowledge")
async def ingest(r:IngestRequest):
 if r.actor.tenant_id!=r.passport.authorization.tenant: raise HTTPException(403,"tenant mismatch")
 p=issue(r.passport); await put(p); return {"object_id":p.object_id,"content_hash":p.content_hash,"signature":p.security.signature}
@router.post("/retrieve")
async def query(r:QueryRequest):
 ps=await all_for_tenant(r.actor.tenant_id); return await retrieve(r.actor,r.query,ps,r.top_k)
