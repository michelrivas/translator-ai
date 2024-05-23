from sqlalchemy import Column, String, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TranslationText(Base):
    """
    Model to store a translation text
    """
    __tablename__ = 'translation_texts'

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=text("(gen_random_uuid())"))
    translations = relationship('Translation', backref='translation_text')
    status = Column(Enum('pending', 'completed', name='status_types'), nullable=False, default='pending')
    text = Column(String, nullable=False)


class Translation(Base):
    """
    Model to store translations of the related text into a specific language
    """
    __tablename__ = 'translations'

    id = Column(Integer, primary_key=True)
    text_id = Column(UUID(as_uuid=True), ForeignKey('translation_texts.uuid'))
    language = Column(String, nullable=False)
    text = Column(String, nullable=True)
    error = Column(String, nullable=True)
