from sqlalchemy.dialects.postgresql import TEXT, JSONB, ARRAY
from sqlalchemy.orm import validates, relationship, Mapped, mapped_column, mapped_collection

from db.config import BaseModel


class ContactTable(BaseModel):
    __tablename__ = 'contact'
    
    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(nullable=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
