import re,math
from app.domain import KnowledgePassport
from app.poison import assess
def tokens(s): return set(re.findall(r"[a-z0-9_]+",s.lower()))
def similarity(q,d):
 a,b=tokens(q),tokens(d)
 return len(a&b)/math.sqrt(max(1,len(a))*max(1,len(b)))
def secure_rank(q,p:KnowledgePassport):
 sem=similarity(q,p.content); poison=assess(p)
 score=(.45*sem+.18*p.security.trust_score+.10*p.security.source_reputation+
        .10*(1.0 if p.security.integrity_verified else 0.0)+.17*p.security.corroboration-.30*poison)
 return max(-1,min(1,score)),sem,poison
