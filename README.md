# RAGTrust — Zero-Trust Provenance & Knowledge Integrity Runtime

RAGTrust is an independent production-oriented reference implementation for **knowledge-supply-chain security in RAG, GraphRAG, agentic RAG and enterprise search**.

The core premise is simple:

> Retrieved knowledge is untrusted input until its identity, integrity, provenance, authorization and corroboration have been evaluated.

RAGTrust therefore secures the **knowledge plane**, rather than acting as a generic prompt firewall.

## Executive architecture

```text
                    RAGTrust Control Plane
                             |
          +------------------+------------------+
          |                  |                  |
       Identity          Provenance           Policy
          |                  |                  |
       tenant           source lineage      RBAC / ABAC
       principal        content hash        classification
       agent            signatures          trust policy
          +------------------+------------------+
                             |
                      Secure Ingestion
                             |
                      Knowledge Ledger
                             |
          +------------------+------------------+
          |                  |                  |
       Vector DB       Knowledge Graph      Document DB
          +------------------+------------------+
                             |
                    Trust-Aware Retriever
                             |
                     Robust Aggregator
                             |
                    Context Firewall
                             |
                            LLM
```

## Why this project exists

Conventional RAG optimizes relevance. Security-sensitive RAG must additionally answer:

```text
Who created this knowledge?
Where did it come from?
Was it modified?
Which pipeline transformed it?
Which parent objects contributed?
Is the source trusted?
Does independent evidence corroborate it?
Does it contradict established evidence?
Is this principal allowed to retrieve it?
Could this object be poisoned?
```

## Knowledge Passport

Every chunk, graph node and graph edge receives a security identity:

```text
KnowledgePassport {
  object_id
  object_type
  content_hash

  source {
    document
    repository
    author
    organization
    uri
  }

  provenance {
    created_at
    ingested_at
    ingestion_pipeline
    transformations[]
    parent_chunks[]
  }

  security {
    signature
    integrity_verified
    trust_score
    poison_score
    contradiction_score
    source_reputation
    corroboration
  }

  authorization {
    tenant
    classification
    allowed_principals[]
  }
}
```

The passport is separate from semantic content so an embedded instruction cannot rewrite its own trust metadata.

## Knowledge identity

`object_id` is the stable logical identity. `content_hash` binds the current bytes/text. Production systems should additionally version objects rather than overwrite evidence.

## Content integrity

The implementation hashes content and signs the passport envelope. Tampering after issuance causes validation failure.

## Signing

The runnable reference uses HMAC for local simplicity. Production should use asymmetric KMS/HSM-backed signing, key IDs, rotation, verification keys and signed ingestion attestations.

## Source identity

Source metadata captures document, repository, author, organization and URI. Production source identity should be derived from authenticated connectors and SCM/document-system metadata.

## Provenance

Provenance records creation, ingestion pipeline, transformations and parent chunks. This allows downstream claims to retain lineage.

## Transformations

Examples include parsing, OCR, chunking, summarization, translation, entity extraction, graph-edge creation and deduplication.

## Parent lineage

Derived chunks/nodes/edges should point to their parents. A production provenance graph can reconstruct the complete transformation path.

## Knowledge ledger

The ledger stores append-only ingestion events and passport hashes. Mature deployments should add update, revoke, supersede, repair and re-sign events.

## Zero-trust ingestion

Ingestion does not automatically mean trust. It creates an object with explicit evidence and policy state.

## Tenant isolation

Tenant identity is enforced during ingestion and retrieval. Production tenant identity must come from trusted authentication, not request JSON.

## Classification

PUBLIC, INTERNAL, CONFIDENTIAL and RESTRICTED labels enable data-policy enforcement before context reaches the model.

## Allowed principals

Objects can restrict retrieval to exact principals or roles.

## Vector RAG

RAGTrust sits before/around vector retrieval and reranking. Vector similarity remains useful but cannot independently determine trust.

## GraphRAG

Graph nodes and edges are first-class passport-bearing objects.

## Document RAG

Whole documents and chunks can share lineage and signatures.

## Agentic RAG

Agent identity becomes an authorization attribute, while retrieved knowledge remains untrusted context rather than authority.

## SecureRank

Classic retrieval:

```text
rank(d) = similarity(q,d)
```

RAGTrust:

```text
SecureRank =
    α SemanticSimilarity
  + β ProvenanceTrust
  + γ SourceReputation
  + δ Integrity
  + ε Corroboration
  - λ PoisonRisk
```

The reference uses explicit weights in `app/ranking.py`. Production weights should be calibrated using attack and benign corpora.

## Semantic similarity

The runnable implementation uses transparent token overlap so the security architecture runs without an external embedding provider. Replace it with production embeddings/vector search.

## Provenance trust

Trust reflects authenticated source/provenance evidence, not model confidence.

## Source reputation

Reputation is a policy-controlled signal for the source/organization/connector.

## Integrity

Cryptographic integrity confirms that content/passport evidence has not changed since signing.

## Corroboration

Independent evidence supporting the same claim increases robustness.

## Poison risk

Poison risk is an explicit negative term. The reference uses explainable heuristics plus contradiction/provenance penalties.

## Poison detector

A production detector should combine provenance, content classifiers, retrieval anomalies, duplication patterns, source novelty, contradiction, graph anomalies and historical behavior.

## Why poison score cannot be the only control

No classifier is perfect. RAGTrust composes integrity, provenance, authorization, diversity and corroboration rather than relying on one detector.

## Robust aggregation

The baseline aggregator limits dominance by a single organization/source group.

## Source diversity

Ten duplicated documents from one attacker should not count as ten independent confirmations.

## Evidence independence

Production corroboration should model whether evidence sources are actually independent.

## Knowledge Integrity Graph

```text
                       Claim C
                    /     |     \
                   /      |      \
                Doc A   Doc B   Doc C
                  |       |       |
               Author   Author   Author
                  |       |       |
                Org X   Org Y   Org Z
                       |
                 consensus/trust
```

The graph connects claims, documents, authors, organizations, transformations and retrieval events.

## Poison attempt

```text
Established Claim
      ^  ^  ^
      |  |  |
 trusted sources

      ^
      |
new contradictory object
      |
unknown / low-trust source
```

A single low-provenance object should not silently overturn well-corroborated evidence.

## Contradiction detection

The passport includes `contradiction_score`. Production should derive it from claim extraction + NLI/LLM adjudication plus deterministic evidence rules.

## Claim IDs

`metadata.claim_id` groups evidence around a normalized claim.

## Claim normalization

Production systems need entity resolution, canonical predicates, temporal scope and qualifier handling.

## Temporal claims

A newer fact may legitimately contradict an older fact. Contradiction analysis must account for effective dates.

## Knowledge graph integrity monitor

The included monitor detects dangling edges, low-trust edges and high contradiction/inconsistency signals.

## Multi-hop consistency

A GraphRAG answer may rely on several edges. Trust should consider the weakest/most suspicious links and consistency of the path.

## Local graph repair

The reference removes suspicious edges from the retrieved subgraph before context construction.

## Production graph repair

Prefer quarantine/suppression plus evidence-preserving repair records rather than destructive deletion.

## Suspicious node creation

Detect new nodes from unknown sources, abnormal bursts, unusual entity types and privilege-sensitive claims.

## Suspicious edge creation

Detect edges that create surprising high-impact relationships, bridge unrelated clusters or contradict stable evidence.

## Temporal anomaly

Track sudden knowledge changes and compare against trusted update cadence.

## Relationship anomaly

Graph embeddings/statistical topology can identify unusual edges, but anomaly is evidence rather than proof.

## Context Firewall

The final context gate rejects integrity failures, low trust and excessive poison risk before the LLM sees the object.

## Why a context firewall is not a prompt firewall

It operates on knowledge identity, provenance, policy and data integrity, not only text patterns.

## Retrieval authorization

Policy checks happen per knowledge object.

## Secure retrieval pipeline

```text
Query
 -> authenticated principal
 -> tenant-scoped candidate retrieval
 -> object authorization
 -> passport verification
 -> poison assessment
 -> graph integrity
 -> SecureRank
 -> robust/diversity aggregation
 -> context firewall
 -> LLM context
```

## Fail-closed integrity

If a signed object fails integrity verification, it is excluded.

## Revocation

Production ledger should support object/source/key revocation and fast cache invalidation.

## Supersession

New versions should supersede old versions without erasing forensic history.

## Connector trust

Connectors should authenticate to the ingestion plane and attest source identity.

## Ingestion pipeline identity

Every transformation service should have workload identity and sign/attest its output.

## Supply-chain analogy

```text
Software supply chain:
source -> build -> artifact -> signature -> verification -> deploy

Knowledge supply chain:
source -> ingest -> transform -> chunk/graph -> passport -> verify -> retrieve
```

## Sigstore analogy

RAGTrust borrows the conceptual idea of verifiable provenance/signatures, but this implementation is independent and does not claim Sigstore compatibility.

## Policy model

The runnable reference enforces tenant and principal/role access. Production expands to ABAC: purpose, geography, classification, legal hold, project, user clearance and agent risk.

## Context confidentiality

A semantically relevant document is not retrievable if policy forbids it.

## Retrieval poisoning

Attackers may inject highly query-relevant documents. SecureRank prevents similarity from being the only objective.

## Index poisoning

Monitor unusual insert/update volume, embedding-neighborhood capture and source concentration.

## Knowledge-base compromise

A compromised trusted source is harder; use signatures, connector identity, change review, corroboration and anomaly history.

## Insider threat

Author identity is evidence, not absolute trust. High-impact claims can require independent corroboration.

## Sybil sources

Many fake sources can simulate consensus. Reputation and source independence must be identity-aware.

## Citation laundering

A poisoned document may cite trusted sources incorrectly. Verify claims/evidence relationships instead of trusting citation strings.

## Retrieval-time provenance

Return passport metadata with every candidate so downstream systems can explain why context was accepted.

## Answer-time citations

The answer layer should cite the actual accepted knowledge objects and preserve passport IDs.

## Model isolation

The LLM cannot modify trust score, authorization or signature fields.

## Agent isolation

Agents can request ingestion/retrieval but cannot self-certify trusted knowledge.

## Administrative separation

Knowledge-security administrators, source owners and application developers should have separate roles.

## Audit

Record ingestion, signature, policy, retrieval, block, repair, revocation and administrative events.

## Observability

Metrics should cover ingestion volume, integrity failures, poison blocks, contradiction rate, low-trust retrieval, source concentration, graph repair and retrieval latency.

## Security metrics

```text
poison attack success rate
benign answer accuracy
retrieval recall
false-positive block rate
integrity failure rate
corroboration coverage
source diversity
graph inconsistency rate
time to revoke poisoned knowledge
```

## Evaluation

Maintain clean and poisoned corpora, targeted poisoning, query-specific poisoning, graph poisoning, source-Sybil attacks and compromised trusted-source scenarios.

## Golden queries

CI should replay security-sensitive queries against known clean/poisoned knowledge.

## Counterfactual evaluation

Replay historical retrievals against proposed ranking/policy changes.

## Shadow mode

New poison detectors and ranking weights can run without blocking before enforcement.

## Canary

Enable active filtering for a subset of tenants/workloads.

## Rollback

Version ranking, detector, policy and trust-model bundles.

## Applications

### Enterprise search
Prevent untrusted or unauthorized content from dominating employee answers.

### Coding RAG
Attach passports to source files, issues, documentation and dependency intelligence.

### Security copilots
Require strong provenance for remediation guidance and vulnerability facts.

### Financial research
Preserve source identity, publication time and corroboration.

### Legal RAG
Track document authority, jurisdiction, version and access policy.

### Healthcare knowledge systems
Track source lineage and strict classification/authorization.

### Customer support
Separate approved product policy from community/untrusted content.

### GraphRAG
Protect nodes, edges and multi-hop reasoning paths.

### Agent memory
Passport persistent memories so externally derived memories retain provenance/trust.

### Multi-agent systems
Carry knowledge passports across agents without converting context into authority.

## API

```text
GET  /health
POST /v1/knowledge
POST /v1/retrieve
```

## Docker run

```bash
unzip ragtrust-zero-trust-provenance-runtime.zip
cd ragtrust-zero-trust-provenance-runtime
cp .env.example .env
docker compose up --build -d
docker compose ps
curl http://localhost:8000/health
```

## Ingest example

```bash
curl -X POST http://localhost:8000/v1/knowledge \
  -H 'x-api-key: change-me' \
  -H 'Content-Type: application/json' \
  --data-binary @examples/ingest.json
```

## Retrieve example

```bash
curl -X POST http://localhost:8000/v1/retrieve \
  -H 'x-api-key: change-me' \
  -H 'Content-Type: application/json' \
  --data-binary @examples/query.json
```

## Host development

```bash
docker compose up -d postgres
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
# Change DATABASE_URL hostname from postgres to localhost.
uvicorn app.main:app --reload
```

## Tests

```bash
python -m pytest -q
ruff check .
```

## Database inspection

```bash
docker compose exec postgres psql -U postgres -d ragtrust
```

```sql
SELECT object_id, tenant, object_type, secure_hash FROM knowledge_objects;
SELECT object_id, event_type, event_hash FROM knowledge_ledger;
```

## Shutdown

```bash
docker compose down
```

## Kubernetes starter

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/api.yaml
kubectl get pods -n ragtrust
```

## Code map

```text
app/domain.py            Knowledge Passport and API contracts
app/crypto.py            canonical hashing + local signing
app/passport.py          passport issuance/verification
app/policy.py            tenant/principal authorization
app/poison.py            baseline poison-risk detector
app/ranking.py           SecureRank
app/aggregator.py        source-diverse robust aggregation
app/graph_integrity.py   GraphRAG integrity + local repair
app/context_firewall.py  final context admission
app/models.py            knowledge objects + ledger
app/store.py             durable persistence
app/engine.py            secure retrieval pipeline
app/api.py               ingestion/retrieval endpoints
```

## `passport.py`

Issues content hashes and signatures. Verification fails if content or signed metadata is modified.

## `policy.py`

Prevents cross-tenant and unauthorized principal retrieval.

## `poison.py`

Implements an explainable baseline. It is intentionally not represented as a complete research-grade poison classifier.

## `ranking.py`

Implements the weighted SecureRank formula and exposes component scores.

## `aggregator.py`

Implements a diversity-aware baseline so one organization cannot flood the final context with unlimited copies.

## `graph_integrity.py`

Inspects graph edges and removes suspicious edges from the retrieved subgraph.

## `context_firewall.py`

Enforces minimum trust, integrity and poison-risk constraints.

## `engine.py`

```text
authorize
 -> verify passport
 -> graph repair
 -> poison assessment
 -> SecureRank
 -> robust aggregation
 -> context firewall
 -> context
```

## Threat model

Knowledge poisoning, targeted retrieval poisoning, index poisoning, graph node/edge poisoning, malicious connector, compromised source, malicious insider, source Sybil, citation laundering, unauthorized retrieval, cross-tenant leakage, tampered chunks and poisoned persistent memory.

## Security invariants

```text
semantic relevance != trust
retrieval != authorization
model confidence != integrity
citation string != provenance
many copies != independent corroboration
memory != trusted knowledge
graph edge != verified fact
```

## Incident response

1. Identify poisoned object/source.
2. Revoke/quarantine passports.
3. Stop new retrieval.
4. Search ledger for descendants.
5. Identify affected graph paths and answers.
6. Repair/supersede knowledge.
7. Rotate compromised connector/signing identity.
8. Replay golden queries.
9. Restore progressively.

## Production architecture

```text
Authenticated Connectors
 -> Ingestion Gateway
 -> Malware/DLP/Content Inspection
 -> Provenance Service
 -> KMS Signing Service
 -> Append-only Knowledge Ledger
 -> Vector/Graph/Document Stores
 -> Retrieval Gateway
 -> Policy PDP
 -> Passport Verifier
 -> Poison/Contradiction Services
 -> SecureRank
 -> Robust Aggregator
 -> Context Firewall
 -> LLM/Agent
 -> Retrieval Audit
```

## Streaming ingestion

At scale use Kafka/PubSub-style eventing, idempotent ingestion IDs and transactional outbox patterns.

## Vector database integration

Adapters should retrieve semantic candidates, then RAGTrust applies security filtering/reranking. Security metadata should be stored separately/authoritatively as well as indexed for performance.

## Graph database integration

Neo4j/JanusGraph/managed graph adapters can expose retrieved subgraphs while the passport ledger remains authoritative.

## Document database integration

Store source documents and immutable versions in object/document storage.

## KMS

Production passport signing uses KMS/HSM asymmetric keys, key rotation, key IDs and verification caching.

## Workload identity

Connectors and transformation services authenticate using cloud workload identity or SPIFFE/SPIRE-like identities.

## OPA/Cedar/IAM

External policy engines can evaluate retrieval ABAC and data policy.

## DLP

DLP/classification can label sensitive knowledge before indexing.

## Migrations

Replace development `create_all` with Alembic.

## High availability

Stateless retrieval gateways scale horizontally. Ledger and policy dependencies require HA and tested failover.

## Multi-region

Keep knowledge and security metadata in allowed regions; replicate trust roots/policies carefully.

## Cache safety

Cache passport verification and policy results only with bounded TTL and revocation invalidation.

## Revocation service

Distribute source/object/key revocations rapidly to retrieval gateways.

## Rate limiting

Limit ingestion, mutation, retrieval and administrative operations by tenant/principal.

## Supply-chain hardening

Pin dependencies, generate SBOMs, scan/sign containers and enforce trusted images.

## Production readiness boundary

### Implemented and runnable

- typed Knowledge Passport;
- content hashing;
- signed passport envelope;
- tenant/principal retrieval policy;
- append-only ingestion ledger foundation;
- poison-risk baseline;
- SecureRank;
- source-diversity robust aggregation;
- graph-edge integrity checks;
- local subgraph repair;
- context firewall;
- PostgreSQL persistence;
- FastAPI;
- Docker;
- Kubernetes starter;
- tests.

### Enterprise integrations still required

- OIDC/workload identity;
- trusted tenant derivation;
- asymmetric KMS/HSM signing;
- connector attestations;
- immutable/versioned knowledge ledger;
- vector DB adapter;
- graph DB adapter;
- document/object-store adapter;
- production embedding/reranker;
- robust poison classifier ensemble;
- NLI/claim contradiction service;
- independent-source/corroboration graph;
- OPA/Cedar/IAM ABAC;
- DLP;
- revocation service;
- OpenTelemetry/Prometheus;
- SIEM;
- Alembic;
- Kafka/outbox;
- Redis/cache;
- Helm/HPA/PDB/NetworkPolicy;
- multi-region/residency;
- comprehensive adversarial evaluation.

## Why this boundary is explicit

A professional security reference should not claim that HMAC signing, lexical similarity or heuristic poisoning detection is equivalent to a fully deployed enterprise trust infrastructure. The repository implements the architecture and core security mechanics while keeping external production integrations explicit.

## Production implementation roadmap

```text
1 OIDC + workload identity
2 KMS asymmetric passport signing
3 immutable versioned ledger
4 authenticated connector attestations
5 vector/graph/document adapters
6 production embeddings/reranking
7 claim extraction + contradiction graph
8 independent-source corroboration
9 poison detector ensemble
10 OPA/Cedar ABAC + DLP
11 revocation/cache invalidation
12 Kafka/outbox + OTel/SIEM
13 hardened K8s/Helm
14 attack corpus + load/chaos
15 multi-region/residency
```

## Principal design review questions

What is the trust root? Can an ingester self-assign trust? How is source identity authenticated? How do transformations preserve provenance? How do you detect compromised trusted sources? How do you prevent source Sybils from manufacturing consensus? How do you distinguish legitimate temporal updates from contradictions? How are graph edges verified? How quickly can poisoned knowledge be revoked? Can cached retrieval bypass revocation? How are historical answers traced to exact knowledge versions?

## Research positioning

RAGTrust combines:

```text
knowledge identity
+
cryptographic integrity
+
provenance lineage
+
retrieval authorization
+
trust-aware ranking
+
source diversity
+
corroboration
+
poison-risk scoring
+
GraphRAG integrity
+
context admission
+
knowledge ledger
```

The central research question is:

> Can RAG systems treat enterprise knowledge like a software supply chain—giving every retrieved object a verifiable identity, provenance and policy envelope, then making retrieval robust to malicious or corrupted knowledge rather than merely filtering prompts?

## References

1. ToxicRAG, arXiv:2609.11082 (2026) — recent work on targeted RAG poisoning.
2. PRA-RAG, Findings of ACL 2026 — robust aggregation against corrupted retrieved content.
3. RAGShield, arXiv:2604.00387 (2026) — provenance-oriented RAG defense direction.
4. HoG-GRAG, ACL 2026 Short Papers — poisoning-induced inconsistency detection and local repair for multi-hop GraphRAG.
5. Sigstore documentation — conceptual precedent for signed provenance and artifact verification.
6. NIST SP 800-207 — Zero Trust Architecture.
7. in-toto / SLSA — conceptual precedents for supply-chain provenance and attestations.

These references motivate the architecture. RAGTrust is independent code and does not claim to reproduce any author's or vendor's internal implementation.

## Final invariant

```text
KNOWLEDGE IS INPUT, NOT AUTHORITY.

Before retrieved content reaches an LLM:

authenticate its source,
verify its integrity,
preserve its lineage,
enforce its data policy,
measure its trust,
check contradictions,
seek independent corroboration,
penalize poison risk,
repair suspicious graph structure,
and record the decision.
```

# Comprehensive Principal / Staff Engineering Manual

## Part I — System intent

### 1. Problem statement

Modern RAG security cannot be reduced to scanning the user prompt. The knowledge corpus itself is an attack surface. An attacker can introduce documents, chunks, graph nodes, graph edges, persistent memories, connector records, transformed summaries or highly query-relevant content that influences downstream reasoning.

RAGTrust therefore treats knowledge as a supply chain.

```text
Source
  ↓
Connector
  ↓
Ingestion
  ↓
Transformation
  ↓
Chunk / Node / Edge
  ↓
Index
  ↓
Retrieval
  ↓
Aggregation
  ↓
Context
  ↓
Model / Agent
```

A security decision is attached to every stage rather than only the final prompt.

### 2. Security objective

For every knowledge object reaching an LLM, RAGTrust should be able to answer:

```text
WHAT is this object?
WHO created or supplied it?
WHERE did it originate?
WHEN was it created and ingested?
HOW was it transformed?
WHICH parent objects contributed?
HAS its content changed?
WHO signed/attested it?
WHICH tenant owns it?
WHO may retrieve it?
HOW trustworthy is its provenance?
DO independent sources corroborate it?
DO trusted sources contradict it?
DOES its graph position look anomalous?
WHY was it admitted into context?
```

### 3. Core invariant

```text
KNOWLEDGE VISIBILITY != KNOWLEDGE TRUST
KNOWLEDGE TRUST      != RETRIEVAL AUTHORIZATION
RETRIEVAL            != EXECUTION AUTHORITY
```

### 4. Control-plane / data-plane split

The control plane manages source identities, trust policy, signing roots, authorization, revocation and detector/ranking versions. The data plane ingests, verifies, retrieves, reranks and admits knowledge.

### 5. Trust boundaries

```text
UNTRUSTED:
 public web
 email
 user uploads
 third-party connectors
 model-generated summaries
 external tool output

CONDITIONALLY TRUSTED:
 enterprise repositories
 approved document systems
 authenticated authors
 signed transformation services

HIGHER ASSURANCE:
 cryptographically attested source
 reviewed policy repository
 controlled pipeline
 corroborated evidence

NEVER ABSOLUTELY TRUSTED:
 semantic content itself
```

## Part II — Knowledge Passport internals

### 6. Passport as security identity

The Knowledge Passport is analogous to an artifact manifest plus provenance attestation plus retrieval-policy envelope.

### 7. `object_id`

Logical identity of a chunk, graph node or graph edge.

### 8. `object_type`

Allows security policy to distinguish chunks from graph structure.

### 9. `content`

The content is intentionally separate from security metadata.

### 10. `content_hash`

SHA-256 binds the passport to exact content.

### 11. `source.document`

Identifies the originating source document.

### 12. `source.repository`

Identifies repository/collection when available.

### 13. `source.author`

Captures author identity as evidence, not automatic trust.

### 14. `source.organization`

Enables source reputation and independence analysis.

### 15. `source.uri`

Allows evidence navigation and connector-specific source identity.

### 16. `created_at`

When the source content was created.

### 17. `ingested_at`

When RAGTrust accepted the object.

### 18. `ingestion_pipeline`

Identifies the transformation pipeline/version.

### 19. `transformations[]`

Records operations such as parsing, OCR, chunking, summarization, extraction and graph construction.

### 20. `parent_chunks[]`

Preserves derivation relationships.

### 21. `signature`

Cryptographic evidence over canonical passport metadata.

### 22. `integrity_verified`

Runtime result of signature/hash verification.

### 23. `trust_score`

Policy/evidence-derived source/provenance trust.

### 24. `poison_score`

Estimated probability/risk that the object is maliciously constructed to manipulate retrieval or downstream reasoning.

### 25. `contradiction_score`

Measures conflict with established evidence.

### 26. `source_reputation`

Historical/policy reputation of the authenticated source.

### 27. `corroboration`

Evidence that independent trusted sources support the claim.

### 28. `authorization.tenant`

Knowledge belongs to a tenant/security domain.

### 29. `classification`

PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED.

### 30. `allowed_principals[]`

Fine-grained object-level retrieval authorization.

## Part III — Cryptographic integrity and provenance

### 31. Canonical serialization

Signatures require deterministic serialization so equivalent metadata produces identical bytes.

### 32. Hash verification

Retrieval recomputes the content hash before context admission.

### 33. Signature verification

The reference signs the passport envelope with HMAC for local operation.

### 34. Production signer

```text
Ingestion Service
      ↓ workload identity
KMS / HSM
      ↓
asymmetric signature
      ↓
Knowledge Passport
      ↓
verification key / JWKS-like trust root
```

### 35. Key IDs

Production passports should carry signing key ID and algorithm.

### 36. Rotation

Old verification keys remain available for historical evidence while compromised keys can be revoked.

### 37. Connector attestation

Authenticated connectors should attest source system, source object ID, version and acquisition time.

### 38. Transformation attestation

Every trusted transformation can append an attestation:

```text
input hashes
transformer identity
software version
parameters
output hashes
timestamp
signature
```

### 39. Provenance DAG

```text
Original Document
   ├── Chunk A
   │    └── Summary A
   ├── Chunk B
   │    └── Entity Node
   └── Chunk C
        └── Graph Edge
```

### 40. Lineage query

A production API should answer: "Show every ancestor that contributed to this retrieved object."

## Part IV — Knowledge Ledger

### 41. Purpose

The ledger provides durable evidence of knowledge lifecycle changes.

### 42. Ingestion event

Records object/passport hash at acceptance.

### 43. Update event

Records new immutable version rather than silently overwriting history.

### 44. Supersede event

Marks a previous object version as no longer preferred.

### 45. Revoke event

Prevents retrieval of a compromised object/source/key.

### 46. Repair event

Records graph/claim repair and evidence.

### 47. Re-sign event

Records migration to a new trust root.

### 48. Append-only model

Security events should not be destructively rewritten.

### 49. WORM export

Critical ledger checkpoints can be exported to immutable object storage.

### 50. Merkle/checkpoint evolution

At scale, batches can be Merkle-rooted and externally anchored.

## Part V — Secure ingestion

### 51. Ingestion authentication

Only authenticated connectors/services should ingest enterprise knowledge.

### 52. Tenant derivation

Production derives tenant from authenticated identity.

### 53. Source allowlists

High-assurance corpora can restrict approved repositories/domains/connectors.

### 54. Malware inspection

Attachments should pass conventional malware scanning before parsing.

### 55. DLP/classification

Classification is assigned before indexing.

### 56. Content normalization

Normalize encodings and formats without destroying evidence.

### 57. Parser isolation

Run document parsers in constrained sandboxes.

### 58. Chunking

Every chunk inherits source lineage and transformation evidence.

### 59. Graph extraction

Every derived node/edge points to supporting chunks.

### 60. Duplicate detection

Exact and near-duplicate detection prevents flooding.

### 61. Source concentration

Monitor sudden domination by one source/organization.

### 62. Quarantine ingestion

Suspicious objects can be stored but excluded from production retrieval.

## Part VI — SecureRank in depth

### 63. Ranking formula

```text
SecureRank(d,q) =
  α * semantic_similarity(q,d)
+ β * provenance_trust(d)
+ γ * source_reputation(d)
+ δ * integrity(d)
+ ε * corroboration(d)
- λ * poison_risk(d)
```

### 64. Why additive ranking

The reference keeps the score interpretable. Production can use constrained learned-to-rank models while preserving hard gates.

### 65. Hard gate vs soft score

Authorization and failed integrity are hard gates. Trust/reputation/corroboration can be ranking features.

### 66. Semantic similarity

Relevant content still matters; security should not make retrieval useless.

### 67. Trust weighting

A low-trust highly relevant object should compete poorly against corroborated high-trust evidence.

### 68. Integrity weighting

Valid signature/hash adds evidence but does not prove factual truth.

### 69. Corroboration weighting

Independent corroboration makes targeted one-source poisoning harder.

### 70. Poison penalty

Poison risk explicitly reduces rank.

### 71. Weight calibration

Use clean/poisoned evaluation sets; optimize security and answer utility jointly.

### 72. Query sensitivity

Security-sensitive queries can require stronger trust/corroboration thresholds.

### 73. Domain sensitivity

Finance, production operations, legal and healthcare can use stricter profiles.

### 74. Explainability

Return component scores so investigators understand why an object ranked.

## Part VII — Poisoning defenses

### 75. Targeted poisoning

Attacker creates content optimized for a particular query/target answer.

### 76. Retrieval capture

A poisoned document can exploit embedding similarity to enter top-k.

### 77. Poison instruction patterns

Lexical instruction patterns are useful signals but not complete defenses.

### 78. Source novelty

A previously unseen source making a high-impact claim increases risk.

### 79. Duplicate flooding

Many copies should not create artificial consensus.

### 80. Query-specific anomaly

Monitor objects that suddenly dominate a narrow query family.

### 81. Embedding neighborhood capture

Detect abnormal source concentration around sensitive query embeddings.

### 82. Trusted-source compromise

Signatures prove source/identity, not that a trusted author was uncompromised.

### 83. Insider poisoning

Require independent corroboration for high-impact claims.

### 84. Poisoned summaries

Derived summaries retain parent lineage and cannot become more trusted than evidence permits.

### 85. Poisoned memory

Persistent memory receives the same passport/provenance treatment.

## Part VIII — Robust aggregation

### 86. Motivation

The model should not receive a context where one attacker supplies every supporting item.

### 87. Organization cap

The reference limits repeated contribution from one organization.

### 88. Domain cap

Production can cap by source domain/repository/author cluster.

### 89. Independence graph

Sources with shared origin should not count as independent evidence.

### 90. Consensus

Consensus should combine agreement plus source independence.

### 91. Outlier suppression

Low-trust contradictory outliers can be excluded or presented as disputed.

### 92. Minority truth

Do not equate majority with truth. Trusted authoritative sources may legitimately update consensus.

### 93. Authority policy

Domain-specific authority rules can identify official sources.

## Part IX — Knowledge Integrity Graph

### 94. Graph schema

```text
Claim
Document
Chunk
Author
Organization
Repository
Connector
Transformation
GraphNode
GraphEdge
Retrieval
Answer
```

### 95. Evidence edge

`Chunk -> SUPPORTS -> Claim`

### 96. Contradiction edge

`Chunk -> CONTRADICTS -> Claim`

### 97. Authorship edge

`Author -> CREATED -> Document`

### 98. Organization edge

`Author -> MEMBER_OF -> Organization`

### 99. Derivation edge

`DerivedObject -> DERIVED_FROM -> Parent`

### 100. Retrieval edge

`Query -> RETRIEVED -> KnowledgeObject`

### 101. Answer lineage

`Answer -> GROUNDED_IN -> KnowledgeObject`

### 102. Claim trust

Trust is derived from evidence, provenance, authority, independence, freshness and contradiction.

### 103. Evidence consensus

```text
Claim
 ├─ trusted independent evidence A
 ├─ trusted independent evidence B
 ├─ trusted independent evidence C
 └─ low-trust contradictory source X
```

### 104. Blast radius

If source X is revoked, graph traversal identifies affected chunks, claims, retrievals and answers.

## Part X — GraphRAG security

### 105. Graph poisoning

Attackers can add malicious nodes/edges that alter multi-hop reasoning.

### 106. Dangling edges

Edges referring to missing nodes are integrity anomalies.

### 107. Low-trust edges

Edges derived from weak provenance can be excluded.

### 108. Contradictory edges

Relationships conflicting with strong evidence require review/repair.

### 109. Temporal anomaly

A sudden relationship update may be legitimate or malicious.

### 110. Topological anomaly

Unexpected bridges between clusters are useful signals.

### 111. Multi-hop path trust

A path's reliability depends on each contributing edge and source.

### 112. Weakest-link policy

High-impact conclusions can require a minimum trust for every path edge.

### 113. Path diversity

Prefer conclusions supported by multiple independent paths.

### 114. Local repair

Remove/quarantine suspicious edges from the retrieved subgraph.

### 115. Evidence-preserving repair

Do not delete forensic history.

### 116. Recompute

After repair, recompute candidate paths and answer context.

## Part XI — Context Firewall

### 117. Role

The firewall is the last deterministic admission gate before model context.

### 118. Integrity gate

Invalid integrity => reject.

### 119. Trust gate

Trust below configured threshold => reject.

### 120. Poison gate

Poison risk above threshold => reject.

### 121. Classification gate

Production adds user/agent clearance and purpose.

### 122. Contradiction policy

High contradiction may require disputed-context presentation or human review.

### 123. Context budget

Security-aware selection operates within token budgets.

### 124. Provenance metadata

Downstream generation should receive compact source IDs and evidence metadata.

## Part XII — Authorization

### 125. Identity tuple

```text
tenant
principal
principal kind
roles
purpose
agent/workload identity
```

### 126. RBAC

Roles provide coarse-grained access.

### 127. ABAC

Attributes include classification, project, region, purpose, source and legal restrictions.

### 128. Purpose limitation

Knowledge can be allowed for support but not model training, for example.

### 129. Agent identity

Agent permissions may be narrower than the human's.

### 130. No privilege laundering

A downstream agent cannot retrieve knowledge merely because an upstream agent saw it.

### 131. Cross-tenant isolation

Tenant mismatch is a hard deny.

### 132. Row/object policy

Every object is independently evaluated.

## Part XIII — Agentic RAG

### 133. Retrieval tool

Expose RAGTrust as the only approved enterprise knowledge retrieval tool.

### 134. Agent cannot bypass passports

Direct vector DB access should be denied to application agents.

### 135. Agent-to-agent transfer

Knowledge Passport IDs and provenance travel with messages.

### 136. Memory write

Persisted memory inherits provenance of source context.

### 137. Memory read

Retrieved memory is evaluated like other knowledge.

### 138. Tool results

Tool output can be ingested as ephemeral passport-bearing knowledge.

### 139. Planning

A model may decide what to search; deterministic security decides what context is admissible.

## Part XIV — Enterprise applications

### 140. Enterprise search

Protect employee search from poisoned or unauthorized documents.

### 141. Software engineering

Secure repository docs, issues, code intelligence and dependency knowledge.

### 142. SRE

Require authoritative runbooks and corroboration for destructive production guidance.

### 143. Security operations

Preserve provenance for threat intelligence and remediation knowledge.

### 144. Finance

Track publication, issuer, analyst/source identity and time-sensitive contradictions.

### 145. Legal

Track jurisdiction, authority, effective date and document version.

### 146. Healthcare

Apply strict provenance/classification and approved-source policy.

### 147. Customer support

Prioritize signed product policy over forum/community content.

### 148. News

Track source/author lineage, temporal claims and corroboration.

### 149. Government

Use classification, compartment and authoritative-source controls.

### 150. Research assistants

Make source diversity and contradiction explicit.

## Part XV — API walkthrough

### 151. Health

```bash
curl http://localhost:8000/health
```

### 152. Ingestion

```bash
curl -X POST http://localhost:8000/v1/knowledge \
  -H 'x-api-key: change-me' \
  -H 'Content-Type: application/json' \
  --data-binary @examples/ingest.json
```

### 153. Retrieval

```bash
curl -X POST http://localhost:8000/v1/retrieve \
  -H 'x-api-key: change-me' \
  -H 'Content-Type: application/json' \
  --data-binary @examples/query.json
```

### 154. Expected retrieval response

The response includes candidates, SecureRank, semantic similarity, reasons, accepted context, blocked objects and graph-integrity summary.

## Part XVI — Complete run instructions

### 155. Prerequisites

```text
Docker + Docker Compose
or
Python 3.11+
PostgreSQL 16+
```

### 156. Docker quick start

```bash
unzip ragtrust-zero-trust-provenance-runtime-comprehensive.zip
cd ragtrust-zero-trust-provenance-runtime
cp .env.example .env
docker compose up --build -d
```

### 157. Verify services

```bash
docker compose ps
curl http://localhost:8000/health
```

### 158. Ingest sample

```bash
curl -X POST http://localhost:8000/v1/knowledge \
  -H 'x-api-key: change-me' \
  -H 'Content-Type: application/json' \
  --data-binary @examples/ingest.json
```

### 159. Query sample

```bash
curl -X POST http://localhost:8000/v1/retrieve \
  -H 'x-api-key: change-me' \
  -H 'Content-Type: application/json' \
  --data-binary @examples/query.json
```

### 160. View logs

```bash
docker compose logs -f api
docker compose logs -f postgres
```

### 161. Inspect database

```bash
docker compose exec postgres psql -U postgres -d ragtrust
```

```sql
SELECT object_id, tenant, object_type, secure_hash
FROM knowledge_objects;

SELECT object_id, event_type, event_hash, created_at
FROM knowledge_ledger
ORDER BY created_at;
```

### 162. Stop

```bash
docker compose down
```

### 163. Delete local volumes

```bash
docker compose down -v
```

Only use the latter when local data should be destroyed.

### 164. Native Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 165. Start PostgreSQL only

```bash
docker compose up -d postgres
```

### 166. Configure local DB

Change the database hostname in `DATABASE_URL` from `postgres` to `localhost`.

### 167. Start API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 168. Run tests

```bash
python -m pytest -q
```

### 169. Lint

```bash
ruff check .
```

### 170. Compile

```bash
python -m compileall -q app tests
```

## Part XVII — Kubernetes

### 171. Starter deployment

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/api.yaml
kubectl get pods -n ragtrust
```

### 172. Production additions

Add Service, Ingress/Gateway, ConfigMap, Secret/external secret provider, ServiceAccount/workload identity, HPA, PDB, NetworkPolicy, topology spread, resource requests/limits and probes.

### 173. Managed database

Production should use HA managed PostgreSQL or equivalent.

### 174. Pod identity

Use cloud workload identity rather than static API keys.

### 175. Network policy

Only ingestion/retrieval gateways should reach required stores and policy/signing services.

## Part XVIII — Code-level walkthrough

### 176. `app/config.py`

Loads runtime configuration through Pydantic Settings.

### 177. `app/domain.py`

Defines the security contracts. Typed passports prevent arbitrary dictionaries from silently becoming trusted metadata.

### 178. `app/crypto.py`

Provides canonical JSON hashing, content SHA-256 and local HMAC signing.

### 179. `app/passport.py`

`issue()` binds content hash, marks integrity and signs the envelope. `validate()` recomputes content hash and signature.

### 180. `app/policy.py`

Enforces tenant and principal/role retrieval policy.

### 181. `app/poison.py`

Computes a transparent baseline poison score using suspicious instruction patterns, weak provenance and contradiction evidence.

### 182. `app/ranking.py`

Computes semantic similarity and SecureRank.

### 183. `app/aggregator.py`

Implements organization diversity limits.

### 184. `app/graph_integrity.py`

Detects dangling, low-trust and inconsistent graph edges and locally removes them.

### 185. `app/context_firewall.py`

Applies final integrity/trust/poison thresholds.

### 186. `app/models.py`

Stores knowledge objects and append-only ledger events.

### 187. `app/store.py`

Persists passports and ledger events transactionally.

### 188. `app/engine.py`

Coordinates the retrieval security pipeline.

### 189. `app/security.py`

Provides local API-key authentication. This is intentionally a development/reference boundary.

### 190. `app/api.py`

Exposes ingestion and retrieval APIs.

### 191. `app/main.py`

Bootstraps FastAPI and development schema creation.

## Part XIX — Production data architecture

### 192. Vector adapter

```text
Query
 -> vector candidate IDs
 -> authoritative passport lookup
 -> security gates
 -> SecureRank
```

### 193. Graph adapter

```text
Graph query
 -> subgraph
 -> passport verification per node/edge
 -> path integrity
 -> local repair
```

### 194. Document adapter

Original immutable source documents should remain addressable for forensic reconstruction.

### 195. Metadata authority

Do not make the vector database the only authoritative store of security metadata.

### 196. Cache

Verification/policy caches require bounded TTL and revocation-aware invalidation.

## Part XX — Observability

### 197. Suggested metrics

```text
ragtrust_ingest_total
ragtrust_integrity_failures_total
ragtrust_poison_blocks_total
ragtrust_policy_denies_total
ragtrust_graph_repairs_total
ragtrust_retrieval_latency_seconds
ragtrust_source_concentration
ragtrust_contradictions_total
ragtrust_revocation_lag_seconds
```

### 198. Tracing

Trace query -> candidate retrieval -> passport verification -> policy -> ranking -> context admission.

### 199. Audit correlation

Every answer should be traceable to exact knowledge object versions.

### 200. Alerting

Alert on signature failures, source bursts, high poison rates, cross-tenant attempts, abnormal graph repair and revocation lag.

## Part XXI — Reliability

### 201. Fail closed

Integrity-critical verification failure should exclude the object.

### 202. Policy outage

High-sensitivity retrieval should fail closed if authorization cannot be established.

### 203. Detector outage

Use deterministic integrity/authorization controls and configured conservative behavior.

### 204. Ledger outage

Do not silently accept security-critical ingestion without durable evidence.

### 205. Revocation outage

Use local signed revocation snapshots and bounded TTL.

### 206. Vector DB outage

Security correctness should not degrade into bypass; retrieval can fail safely.

## Part XXII — Scaling

### 207. Partitioning

Partition knowledge/security state by tenant and corpus.

### 208. Ingestion stream

Use Kafka/PubSub with idempotency keys and outbox.

### 209. Retrieval latency

Parallelize passport fetch/verification and cache safe immutable evidence.

### 210. Signature verification cache

Cache verification by passport hash + key ID.

### 211. Batch verification

Batch KMS/trust-root operations where appropriate.

### 212. Graph scale

Retrieve bounded subgraphs and run integrity checks on the relevant neighborhood.

## Part XXIII — Evaluation framework

### 213. Clean corpus

Measures utility and false positives.

### 214. Poison corpus

Contains malicious knowledge designed to alter target answers.

### 215. Targeted attacks

Evaluate one/few poisoned objects targeting specific queries.

### 216. Source-Sybil attacks

Create multiple apparently independent malicious sources.

### 217. Trusted-source compromise

Test malicious updates from an otherwise trusted identity.

### 218. Graph poisoning

Inject nodes/edges affecting multi-hop answers.

### 219. Temporal updates

Ensure legitimate fresh facts can supersede old consensus.

### 220. Metrics

```text
Attack Success Rate
Answer Accuracy
Retrieval Recall
Poisoned Context Rate
False Positive Block Rate
Source Diversity
Corroboration Coverage
Graph Repair Precision
Graph Repair Recall
Revocation Latency
p95 Retrieval Latency
```

### 221. Security/utility frontier

A useful system minimizes attack success without destroying clean answer accuracy.

### 222. Regression gates

Every detector/ranking/policy change replays the golden suite.

## Part XXIV — Red-team scenarios

### 223. One-document target poison

Create one highly query-relevant malicious object.

### 224. Duplicate flood

Create many copies from the same source family.

### 225. Cross-source Sybil

Create fake independent organizations.

### 226. Poisoned graph edge

Insert a relationship that redirects a multi-hop answer.

### 227. Compromised connector

Submit validly authenticated but malicious content.

### 228. Signature tampering

Modify content after signing.

### 229. Authorization bypass

Attempt cross-tenant retrieval.

### 230. Poisoned transformation

Compromise summarizer/entity extractor.

### 231. Citation laundering

Reference a trusted source while asserting unsupported content.

### 232. Memory persistence

Inject malicious content and persist it as agent memory.

## Part XXV — Incident response

### 233. Detect

Identify suspicious object/source/path.

### 234. Contain

Revoke/quarantine object/source/signing key.

### 235. Trace

Traverse descendants, graph paths, retrievals and answers.

### 236. Assess blast radius

Identify users/agents/answers exposed.

### 237. Repair

Supersede poisoned objects and repair graph structure.

### 238. Rotate

Rotate compromised connector/workload/signing identity.

### 239. Replay

Replay affected golden/production-safe queries.

### 240. Restore

Progressively restore source after verification.

## Part XXVI — Production security hardening

### 241. OIDC

Human/admin APIs use enterprise OIDC/SSO.

### 242. Workload identity

Services/connectors use cloud workload identity or SPIFFE/SPIRE-style identity.

### 243. KMS/HSM

Passport signing keys stay outside application memory.

### 244. Secret management

Use managed secret stores and short-lived credentials.

### 245. Database TLS

Require TLS and least-privilege database roles.

### 246. Container security

Non-root, read-only root filesystem, dropped capabilities and signed images.

### 247. SBOM

Generate SBOM for every release.

### 248. Dependency scanning

Continuously scan dependencies/images.

### 249. Admission control

Only verified images deploy.

### 250. Network segmentation

Separate ingestion, retrieval, signing, policy and data stores.

## Part XXVII — Production roadmap

### 251. Phase 1 — Identity and cryptography

OIDC/workload identity, trusted tenant, KMS signing, key rotation.

### 252. Phase 2 — Real stores

Vector, graph, object/document adapters.

### 253. Phase 3 — Knowledge integrity intelligence

Claim extraction, contradiction, corroboration, source independence.

### 254. Phase 4 — Advanced poisoning detection

Ensemble classifiers, retrieval anomaly, source concentration, embedding-neighborhood attacks.

### 255. Phase 5 — Policy and DLP

OPA/Cedar/IAM + classification + purpose limitation.

### 256. Phase 6 — Operations

Revocation, Kafka/outbox, OTel, SIEM, Alembic, rate limiting.

### 257. Phase 7 — Platform hardening

Helm, HPA, PDB, NetworkPolicy, multi-region, residency, DR.

### 258. Phase 8 — Evaluation

Attack corpus, red-team automation, load, chaos and security/utility regression gates.

## Part XXVIII — Principal-level tradeoffs

### 259. Why not trust signatures alone?

A signed malicious document is still malicious.

### 260. Why not trust reputation alone?

Trusted sources can be compromised.

### 261. Why not trust consensus alone?

Attackers can create Sybils and duplicated evidence.

### 262. Why not use only a poison classifier?

Classifiers can be evaded and have false positives.

### 263. Why not use only similarity?

Similarity is precisely what targeted poisoning exploits.

### 264. Why preserve contradictory evidence?

Disagreement may represent legitimate temporal or domain differences and is useful for forensics.

### 265. Why separate hard gates and ranking?

Authorization/integrity are correctness constraints; trust/relevance are selection objectives.

### 266. Why retain lineage after summarization?

Transformation can distort or poison meaning.

### 267. Why secure graph edges independently?

GraphRAG reasoning may depend on one malicious edge.

### 268. Why make revocation first class?

Knowledge that was safe yesterday can become known-compromised today.

## Part XXIX — Production readiness matrix

```text
Capability                         Repository   Enterprise target
Knowledge Passport                 implemented implemented
Content hashing                    implemented implemented
Passport signing                   HMAC         KMS/HSM asymmetric
Integrity verification             implemented implemented
Tenant policy                      implemented trusted identity
Principal policy                   baseline    RBAC/ABAC/PDP
Knowledge ledger                   baseline    immutable/versioned
Poison detector                    baseline    ensemble
SecureRank                         implemented calibrated
Robust aggregation                 baseline    source-independence graph
Contradiction                      signal      claim/NLI service
Corroboration                      signal      evidence graph
Graph integrity                    baseline    advanced graph analytics
Local graph repair                 implemented evidence-preserving workflow
Context firewall                   implemented policy profiles
Vector DB                          adapter TODO production adapter
Graph DB                           adapter TODO production adapter
Document store                     adapter TODO production adapter
KMS                                TODO         required
OIDC/workload identity             TODO         required
DLP                                TODO         required
Revocation distribution            TODO         required
Streaming/outbox                   TODO         required
OTel/SIEM                          TODO         required
Alembic                            TODO         required
Multi-region                       design       deployment-specific
```

## Part XXX — Explanation

### 269. 

> RAGTrust is a zero-trust knowledge-supply-chain security runtime for RAG and GraphRAG. Every chunk, node and edge receives a signed Knowledge Passport carrying source identity, content integrity, provenance, trust, poisoning, contradiction, corroboration and authorization metadata. Retrieval combines hard authorization/integrity gates with security-aware ranking, source-diverse aggregation, GraphRAG integrity checks and a final context firewall.

### 270. What makes it different from a RAG firewall?

A generic firewall primarily inspects prompts/content. RAGTrust secures knowledge identity, lineage, authorization, integrity, evidence consensus and graph structure across ingestion and retrieval.

### 271. What makes it a distributed-systems problem?

It requires identity, signing, immutable/versioned state, revocation propagation, caches, heterogeneous stores, graph traversal, stream processing, multi-region policy and low-latency retrieval.

### 272. What makes it a security problem?

The system assumes knowledge sources, transformations, indexes and retrieved context can be malicious or compromised.

### 273. What makes it an AI problem?

Semantic retrieval, poisoning, contradiction, claim extraction, corroboration and GraphRAG reasoning require AI-aware evaluation.

## Part XXXI — Research extensions

### 274. Provenance-conditioned retrieval

Learn ranking models constrained by cryptographic provenance.

### 275. Claim-level passports

Issue passports to normalized claims rather than only chunks.

### 276. Evidence independence scoring

Infer common origin to defeat consensus Sybils.

### 277. Temporal truth graphs

Model claims as valid over intervals.

### 278. Cross-modal passports

Extend to images, audio, video and multimodal embeddings.

### 279. Federated RAGTrust

Verify knowledge across organizations without centralizing all data.

### 280. Privacy-preserving corroboration

Use secure attestations to establish corroboration without revealing restricted documents.

### 281. Answer passport

Generate a final answer manifest containing exact knowledge versions, policy and model/ranking versions.

### 282. Continuous knowledge red teaming

Automatically generate poisoning campaigns and replay security-sensitive queries.

## Part XXXII — Final architecture

```text
AUTHENTICATED SOURCE
        |
        v
CONNECTOR / WORKLOAD ID
        |
        v
INGESTION GATEWAY
        |
        +--> malware / DLP / classification
        |
        v
PROVENANCE SERVICE
        |
        +--> source identity
        +--> transformation lineage
        +--> parent hashes
        |
        v
KMS SIGNER
        |
        v
KNOWLEDGE PASSPORT
        |
        v
APPEND-ONLY KNOWLEDGE LEDGER
        |
        +----------+-----------+
        |          |           |
      Vector      Graph      Document
       Store       Store       Store
        +----------+-----------+
                   |
                   v
          RETRIEVAL GATEWAY
                   |
          +--------+--------+
          |                 |
      Policy PDP      Passport Verify
          |                 |
          +--------+--------+
                   |
                   v
        Poison / Contradiction
                   |
                   v
          Graph Integrity
                   |
                   v
             SecureRank
                   |
                   v
        Robust Aggregation
                   |
                   v
          Context Firewall
                   |
                   v
             LLM / Agent
                   |
                   v
         Answer + Evidence IDs
                   |
                   v
              Audit Graph
```

## Part XXXIII — Final engineering rule

```text
DO NOT ASK ONLY:
"Is this document relevant?"

ASK:
"Is it relevant?"
"Is it authorized?"
"Is it intact?"
"Where did it come from?"
"How was it transformed?"
"Who signed it?"
"Who else corroborates it?"
"What contradicts it?"
"Is its graph structure plausible?"
"Could it be poisoned?"
"Can we revoke it?"
"Can we explain why it was retrieved?"
```

That is the zero-trust knowledge model RAGTrust is designed to demonstrate.

## Research Foundations & Citations

RAGTrust is an **independent engineering and research reference implementation**. Its architecture is motivated by recent work on RAG knowledge poisoning, provenance verification, robust retrieval, GraphRAG integrity, zero-trust architecture, and software-supply-chain provenance.

RAGTrust does **not** reproduce the implementation of any cited research project. Instead, it combines several emerging ideas into a unified production-oriented architecture:

```text
Knowledge Identity
        +
Cryptographic Integrity
        +
Provenance Lineage
        +
Retrieval Authorization
        +
Trust-Aware Ranking
        +
Poison-Risk Detection
        +
Evidence Corroboration
        +
Robust Aggregation
        +
GraphRAG Integrity
        +
Context Admission
        +
Knowledge Ledger
```

---

### [1] ToxicRAG — Single-Shot Knowledge Poisoning

**Haozhe Lu, Jiaqi Li, Xinyuan Zhu, Xiang Li.**  
*ToxicRAG: Compromising Retrieval-Augmented Generation Systems via Single-Shot Knowledge Poisoning Attacks.*  
arXiv:2609.11082, 2026.

ToxicRAG demonstrates that RAG poisoning does not necessarily require a large collection of obviously malicious documents. The work studies a **one-document-per-target** poisoning strategy in which misinformation is presented as a plausible knowledge update.

The paper reports attack-success rates between **0.61 and 0.91** across its twelve evaluated dataset/model combinations.

#### RAGTrust relevance

This motivates moving beyond:

```text
query
   ↓
semantic similarity
   ↓
top-k
```

toward:

```text
query
   ↓
semantic candidates
   ↓
source identity
   ↓
provenance
   ↓
integrity
   ↓
corroboration
   ↓
poison risk
   ↓
SecureRank
```

RAGTrust therefore treats **semantic relevance as insufficient evidence of trustworthiness**.

---

### [2] RAGShield — Provenance-Verified RAG Defense

**KrishnaSaiReddy Patil.**  
*RAGShield: Provenance-Verified Defense-in-Depth Against Knowledge Base Poisoning in Government Retrieval-Augmented Generation Systems.*  
arXiv:2604.00387, 2026.

RAGShield explicitly observes that knowledge-base poisoning has structural similarities to **software supply-chain attacks** and proposes provenance-oriented defenses including document attestation, trust-weighted retrieval, taint tracking, contradiction detection, and auditable citations.

#### RAGTrust relevance

This research strongly motivates RAGTrust's knowledge-supply-chain model:

```text
Software Supply Chain

Source
  ↓
Build
  ↓
Artifact
  ↓
Signature
  ↓
Verification
  ↓
Deployment


RAGTrust Knowledge Supply Chain

Source
  ↓
Ingestion
  ↓
Transformation
  ↓
Chunk / Node / Edge
  ↓
Knowledge Passport
  ↓
Verification
  ↓
Retrieval
```

RAGTrust extends this architectural direction with:

```text
Knowledge Passport
Knowledge Ledger
Knowledge Integrity Graph
SecureRank
Source-independent corroboration
GraphRAG integrity monitoring
Retrieval authorization
Context Firewall
```

---

### [3] HoG-GRAG — GraphRAG Knowledge-Poisoning Defense

**Havva Alizadeh Noughabi, Fattane Zarrinkalam, Ali Dehghantanha.**  
*Defense Against Knowledge Poisoning Attack on GraphRAG.*  
Proceedings of ACL 2026, Volume 2: Short Papers, pp. 555–563.

HoG-GRAG studies the additional poisoning surface created by GraphRAG, where malicious knowledge can introduce spurious entities and relationships into a knowledge graph.

The proposed defense monitors multi-hop retrieval for poisoning-induced inconsistencies and performs **local repair of the retrieved subgraph**.

#### RAGTrust relevance

This motivates RAGTrust's:

```text
Graph Integrity Monitor
        │
        ├── suspicious nodes
        ├── suspicious edges
        ├── dangling edges
        ├── low-trust edges
        ├── temporal anomalies
        ├── relationship anomalies
        └── multi-hop inconsistencies
                    ↓
             Local Graph Repair
```

Every RAGTrust graph node and edge can additionally carry its own Knowledge Passport.

---

### [4] PoisonedRAG — Knowledge Corruption Attacks

**Wei Zou, Runpeng Geng, Binghui Wang, Jinyuan Jia.**  
*PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models.*  
34th USENIX Security Symposium, 2025, pp. 3827–3844.

PoisonedRAG established knowledge-base corruption as a significant RAG attack surface and demonstrated that attackers can manipulate external retrieval knowledge to influence generated answers.

#### RAGTrust relevance

RAGTrust treats the external corpus as a security boundary:

```text
External Knowledge
       │
       ▼
NOT automatically trusted
       │
       ▼
Identity
Integrity
Provenance
Authorization
Poison Analysis
Corroboration
       │
       ▼
Context Admission
```

---

### [5] Zero Trust Architecture

**NIST Special Publication 800-207.**  
*Zero Trust Architecture.*

Zero Trust replaces implicit trust based on network or system location with explicit identity, policy, and resource-level authorization.

#### RAGTrust relevance

RAGTrust applies a similar principle to knowledge:

```text
Never trust knowledge merely because:

it exists in the vector database
it came from the knowledge graph
it was retrieved at rank #1
it has high embedding similarity
it was previously used by another agent
it appears authoritative
```

Instead:

```text
VERIFY
   identity
   integrity
   provenance
   authorization
   trust
   corroboration
   contradiction
```

before context admission.

---

### [6] Sigstore — Artifact Signing and Verification

**Sigstore Project.**  
Software-signing and transparency infrastructure.

Sigstore provides an important conceptual precedent for associating software artifacts with verifiable identity and integrity evidence.

#### RAGTrust relevance

RAGTrust applies an analogous concept to AI knowledge objects:

```text
Software Artifact
       ↓
signature
       ↓
verification


Knowledge Object
       ↓
Knowledge Passport
       ↓
signature + provenance
       ↓
verification
```

RAGTrust is **not a Sigstore implementation** and does not claim protocol compatibility.

---

### [7] in-toto — Supply-Chain Attestations

**in-toto Project.**  
*A framework to secure the integrity of software supply chains.*

in-toto provides a model for recording and verifying the steps through which an artifact passes.

#### RAGTrust relevance

A knowledge object may similarly pass through:

```text
Source Document
      ↓
Parser
      ↓
OCR
      ↓
Chunker
      ↓
Summarizer
      ↓
Entity Extractor
      ↓
Graph Builder
      ↓
Retriever
```

RAGTrust therefore preserves transformation lineage rather than trusting only the final chunk.

---

### [8] SLSA — Supply-Chain Levels for Software Artifacts

**Supply-chain Levels for Software Artifacts (SLSA).**

SLSA provides another important precedent for provenance, trusted build pipelines, and verifiable artifact production.

#### RAGTrust relevance

RAGTrust adapts the architectural idea to knowledge:

```text
Authenticated Source
        ↓
Attested Ingestion
        ↓
Attested Transformation
        ↓
Signed Knowledge Object
        ↓
Verified Retrieval
```

---

## Research → RAGTrust Architecture Mapping

| Research direction | RAGTrust subsystem |
|---|---|
| Knowledge poisoning | Poison Risk Engine |
| Single-document targeted poisoning | SecureRank + corroboration |
| Corpus corruption | Secure Ingestion |
| Provenance verification | Knowledge Passport |
| Supply-chain security | Knowledge Ledger |
| Trust-weighted retrieval | SecureRank |
| Contradiction detection | Knowledge Integrity Graph |
| Source independence | Robust Aggregator |
| GraphRAG poisoning | Graph Integrity Monitor |
| Multi-hop inconsistency | Graph path validation |
| Local graph repair | Graph repair layer |
| Zero Trust | Per-object authorization |
| Artifact signing | Passport signatures |
| Transformation provenance | Provenance DAG |
| Supply-chain attestations | Transformation attestations |
| Persistent-memory poisoning | Passport-bearing memory |

---

## How the Research Fits Together

The cited work exposes different pieces of the same larger security problem:

```text
PoisonedRAG
     │
     └── Knowledge corruption is an attack surface
                    │
                    ▼
               ToxicRAG
                    │
     └── Very small poisoning footprints can matter
                    │
                    ▼
               RAGShield
                    │
     └── Provenance and supply-chain defenses
                    │
                    ▼
               HoG-GRAG
                    │
     └── Graph structure itself must be protected
                    │
                    ▼
                 RAGTrust
                    │
     ├── Knowledge Passport
     ├── Knowledge Ledger
     ├── SecureRank
     ├── Corroboration
     ├── Knowledge Integrity Graph
     ├── Graph Integrity Monitor
     ├── Local Graph Repair
     ├── Retrieval Authorization
     └── Context Firewall
```

---

## RAGTrust Research Positioning

RAGTrust explores a broader systems-security question:

> **What would RAG look like if enterprise knowledge were treated as a cryptographically identifiable, policy-controlled, provenance-carrying supply chain rather than an implicitly trusted collection of embeddings?**

The resulting security model is:

```text
Semantic Relevance
        +
Knowledge Identity
        +
Cryptographic Integrity
        +
Source Provenance
        +
Transformation Lineage
        +
Retrieval Authorization
        +
Source Reputation
        +
Independent Corroboration
        +
Contradiction Analysis
        +
Poison Risk
        +
Graph Integrity
        ↓
Secure Context
```

---

## Citation Disclaimer

RAGTrust is an **independent open engineering reference implementation**.

The papers and projects cited above provide research motivation and architectural context.

Citation does **not** imply:

- affiliation with the authors;
- endorsement by the cited organizations;
- reproduction of proprietary systems;
- implementation equivalence;
- compatibility certification;
- that RAGTrust is the official implementation of any cited paper.

Where RAGTrust combines provenance, authorization, trust-aware retrieval, knowledge integrity graphs, graph repair, cryptographic passports, and context admission into one architecture, that combination represents the design of this project rather than a claim that any single cited work implements the complete architecture.

---

## References

**[1]** Haozhe Lu, Jiaqi Li, Xinyuan Zhu, and Xiang Li.  
*ToxicRAG: Compromising Retrieval-Augmented Generation Systems via Single-Shot Knowledge Poisoning Attacks.*  
arXiv:2609.11082, 2026.

**[2]** KrishnaSaiReddy Patil.  
*RAGShield: Provenance-Verified Defense-in-Depth Against Knowledge Base Poisoning in Government Retrieval-Augmented Generation Systems.*  
arXiv:2604.00387, 2026.

**[3]** Havva Alizadeh Noughabi, Fattane Zarrinkalam, and Ali Dehghantanha.  
*Defense Against Knowledge Poisoning Attack on GraphRAG.*  
Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics, Volume 2: Short Papers, pp. 555–563, 2026.  
DOI: `10.18653/v1/2026.acl-short.47`

**[4]** Wei Zou, Runpeng Geng, Binghui Wang, and Jinyuan Jia.  
*PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models.*  
34th USENIX Security Symposium, pp. 3827–3844, 2025.

**[5]** National Institute of Standards and Technology.  
*Zero Trust Architecture.*  
NIST Special Publication 800-207.

**[6]** Sigstore Project.  
*Sigstore Documentation — Software Signing and Verification.*

**[7]** in-toto Project.  
*in-toto: A Framework to Secure the Integrity of Software Supply Chains.*

**[8]** SLSA.  
*Supply-chain Levels for Software Artifacts.*

---

## Recommended Citation for RAGTrust

If you use or discuss this repository in engineering work, presentations, research prototypes, or architecture discussions:

```bibtex
@software{ragtrust2026,
  title  = {RAGTrust: Zero-Trust Provenance and Knowledge Integrity Runtime},
  year   = {2026},
  type   = {AI Security Reference Implementation},
  note   = {Zero-trust knowledge provenance, integrity, secure retrieval,
            robust aggregation, GraphRAG security, and knowledge-supply-chain architecture}
}
```

---

## Final Research Principle

```text
RELEVANCE IS NOT TRUST.
RETRIEVAL IS NOT AUTHORIZATION.
A SIGNATURE IS NOT TRUTH.
POPULARITY IS NOT CORROBORATION.
A GRAPH EDGE IS NOT A VERIFIED FACT.

Knowledge entering an AI system should carry
identity, integrity, provenance, policy and evidence.
```
