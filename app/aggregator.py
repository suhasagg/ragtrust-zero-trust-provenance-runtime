from collections import defaultdict
def corroboration_groups(passports):
 groups=defaultdict(list)
 for p in passports:
  claim=str(p.metadata.get("claim_id",p.object_id)); groups[claim].append(p)
 return groups
def robust_filter(candidates):
 # diversity-aware baseline: do not let many copies from one organization dominate.
 seen={}; out=[]
 for c in sorted(candidates,key=lambda x:x.secure_rank,reverse=True):
  org=c.passport.source.organization or "unknown"
  if seen.get(org,0)>=2: continue
  seen[org]=seen.get(org,0)+1; out.append(c)
 return out
