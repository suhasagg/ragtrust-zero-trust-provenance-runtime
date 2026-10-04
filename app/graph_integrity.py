def inspect_subgraph(passports):
 findings=[]
 nodes={p.object_id:p for p in passports}
 for p in passports:
  if p.object_type=="graph_edge":
   src=p.metadata.get("src"); dst=p.metadata.get("dst")
   if src not in nodes or dst not in nodes: findings.append({"object_id":p.object_id,"rule":"DANGLING_EDGE"})
   if p.security.trust_score<.3: findings.append({"object_id":p.object_id,"rule":"LOW_TRUST_EDGE"})
   if p.security.contradiction_score>.7: findings.append({"object_id":p.object_id,"rule":"MULTIHOP_INCONSISTENCY"})
 return findings
def repair(passports,findings):
 bad={x["object_id"] for x in findings if x["rule"] in {"LOW_TRUST_EDGE","MULTIHOP_INCONSISTENCY","DANGLING_EDGE"}}
 return [p for p in passports if p.object_id not in bad]
