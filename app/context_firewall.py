from app.config import settings
def allow_context(candidate):
 p=candidate.passport
 if not p.security.integrity_verified: return False,"INTEGRITY_UNVERIFIED"
 if p.security.trust_score<settings.min_trust_score: return False,"LOW_TRUST"
 if p.security.poison_score>settings.max_poison_score: return False,"POISON_RISK"
 return True,"PASS"
