from app.domain import KnowledgePassport
from app.crypto import content_hash,sign,verify
def signing_payload(p):
 d=p.model_dump(); d["security"]["signature"]=""; return d
def issue(p:KnowledgePassport):
 p.content_hash=content_hash(p.content); p.security.integrity_verified=True
 p.security.signature=sign(signing_payload(p)); return p
def validate(p):
 return p.content_hash==content_hash(p.content) and verify(signing_payload(p),p.security.signature)
