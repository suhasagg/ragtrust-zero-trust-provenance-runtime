import uuid
from datetime import datetime
from sqlalchemy import String,DateTime,Float
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.sql import func
from app.db import Base
class KnowledgeObject(Base):
 __tablename__="knowledge_objects"
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
 object_id:Mapped[str]=mapped_column(String(256),unique=True,index=True); tenant:Mapped[str]=mapped_column(String(128),index=True)
 object_type:Mapped[str]=mapped_column(String(32)); content:Mapped[str]=mapped_column(String)
 passport:Mapped[dict]=mapped_column(JSONB); secure_hash:Mapped[str]=mapped_column(String(64))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
class LedgerEvent(Base):
 __tablename__="knowledge_ledger"
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
 object_id:Mapped[str]=mapped_column(String(256),index=True); event_type:Mapped[str]=mapped_column(String(64))
 event_hash:Mapped[str]=mapped_column(String(64),unique=True); payload:Mapped[dict]=mapped_column(JSONB)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
