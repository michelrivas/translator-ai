from uuid import UUID

from typing import Optional
from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    """
    Model to validate a translate request
    """
    text: str
    languages: list[str] = Field(..., min_items=1)


class TranslationResult(BaseModel):
    """
    Model to return a translation result
    """
    language: str
    text: Optional[str] = None

    class Config:
        from_attributes = True


class Translation(BaseModel):
    """
    Model to return a translation object
    """
    uuid: UUID
    text: str
    status: str
    translations: list[TranslationResult] = []

    class Config:
        from_attributes = True
