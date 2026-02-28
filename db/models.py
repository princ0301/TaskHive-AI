from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import enum

Base = declarative_base()

class JobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ResearchJob(Base):
    __tablename__ = "research_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    topic = Column(String, nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    report = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)