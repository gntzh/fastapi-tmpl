from sqlalchemy import Column, ForeignKey, types
from sqlalchemy.orm import relationship

from src.libs.sa.timezone import TZDateTime
from src.libs.sa.uuid import UUID
from src.utils import utcnow

from .mapper import Base
from .user import User


class Item(Base):
    id = Column(types.Integer, primary_key=True, autoincrement=True)
    created_at = Column(TZDateTime, nullable=False, default=utcnow)
    title = Column(types.String(40), nullable=False)
    description = Column(types.String(200))
    owner_id = Column(UUID, ForeignKey("user.id"), nullable=False)

    owner: User = relationship("User")
