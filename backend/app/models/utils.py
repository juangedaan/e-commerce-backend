from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr

class TimestampMixin:
    """Adds created_at and updated_at timestamp columns to models."""
    
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now())
    
    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), onupdate=func.now())

