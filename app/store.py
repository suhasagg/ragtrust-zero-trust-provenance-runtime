from sqlalchemy import select
from app.db import Session
from app.models import KnowledgeObject,LedgerEvent
from app.domain import KnowledgePassport
from app.crypto import digest
async def put(p):
 d=p.model_dump(); eh=digest({"event":"INGEST","passport":d})
 async with Session.begin() as s:
  s.add(KnowledgeObject(object_id=p.object_id,tenant=p.authorization.tenant,object_type=p.object_type,content=p.content,passport=d,secure_hash=p.content_hash))
  s.add(LedgerEvent(object_id=p.object_id,event_type="INGEST",event_hash=eh,payload={"passport_hash":digest(d)}))
async def all_for_tenant(tenant):
 async with Session() as s:
  rows=(await s.execute(select(KnowledgeObject).where(KnowledgeObject.tenant==tenant))).scalars().all()
  return [KnowledgePassport.model_validate(x.passport) for x in rows]
