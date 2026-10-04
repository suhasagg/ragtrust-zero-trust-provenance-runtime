from app.domain import Identity,KnowledgePassport
def authorized(actor:Identity,p:KnowledgePassport):
 if actor.tenant_id!=p.authorization.tenant: return False,"TENANT_MISMATCH"
 if p.authorization.allowed_principals and actor.principal_id not in p.authorization.allowed_principals and not set(actor.roles)&{"admin","knowledge_reader"}:
  return False,"PRINCIPAL_NOT_ALLOWED"
 return True,"AUTHORIZED"
