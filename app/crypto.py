import hashlib,hmac,json
from app.config import settings
def canonical(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def digest(x): return hashlib.sha256(canonical(x)).hexdigest()
def content_hash(s): return hashlib.sha256(s.encode()).hexdigest()
def sign(payload): return hmac.new(settings.api_key.encode(),canonical(payload),hashlib.sha256).hexdigest()
def verify(payload,sig): return hmac.compare_digest(sign(payload),sig)
