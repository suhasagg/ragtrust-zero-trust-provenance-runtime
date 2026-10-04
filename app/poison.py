import re
from app.domain import KnowledgePassport
PATTERNS=[r"ignore (all|previous)",r"system prompt",r"override (the )?(instructions|policy)",r"exfiltrat",r"send .*secret"]
def assess(p:KnowledgePassport):
 text=p.content.lower()
 lexical=min(1.0,sum(bool(re.search(x,text)) for x in PATTERNS)*0.28)
 provenance_penalty=0.25 if not p.source.author and not p.source.organization else 0.0
 contradiction=p.security.contradiction_score
 return min(1.0,max(p.security.poison_score,lexical+provenance_penalty+0.25*contradiction))
