from app.domain import Candidate,QueryResponse
from app.passport import validate
from app.policy import authorized
from app.ranking import secure_rank
from app.aggregator import robust_filter
from app.context_firewall import allow_context
from app.graph_integrity import inspect_subgraph,repair
async def retrieve(actor,query,passports,top_k):
 blocked=[]; cs=[]; graph_findings=inspect_subgraph(passports); clean=repair(passports,graph_findings)
 for p in clean:
  ok,why=authorized(actor,p)
  if not ok: blocked.append(f"{p.object_id}:{why}"); continue
  p.security.integrity_verified=validate(p)
  score,sem,poison=secure_rank(query,p); p.security.poison_score=poison
  reasons=[f"semantic={sem:.3f}",f"trust={p.security.trust_score:.3f}",f"poison={poison:.3f}",f"integrity={p.security.integrity_verified}"]
  c=Candidate(object_id=p.object_id,content=p.content,semantic_similarity=sem,secure_rank=score,reasons=reasons,passport=p)
  allowed,reason=allow_context(c)
  if allowed: cs.append(c)
  else: blocked.append(f"{p.object_id}:{reason}")
 cs=robust_filter(cs)[:top_k]
 return QueryResponse(query=query,candidates=cs,context=[c.content for c in cs],blocked=blocked,
  integrity_summary={"graph_findings":graph_findings,"returned":len(cs),"blocked":len(blocked)})
