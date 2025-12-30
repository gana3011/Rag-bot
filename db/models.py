from db.database import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

class Document(Base):
    __tablename__ = "documents"
    document_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    status = Column(String, nullable=False, default="UPLOADED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())