from uuid import UUID

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from src.translator.database import get_db
from src.translator.schemas import TranslationRequest
from src.translator.service import translate_service, get_translated_text_service, trigger_translation_service


router = APIRouter()


@router.post("/translate", tags=["translate"])
async def translate(
        translation_item: TranslationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """
    Receives a request to translate a text into multiple languages
    :param translation_item:
    :param background_tasks:
    :param db:
    :return:
    """
    response = await translate_service(translation_item, background_tasks, db)
    return response


@router.post("/translate/{uuid}/trigger", tags=["translate"])
async def trigger_translate(uuid: UUID, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Receives a request to manually trigger a stored translation request
    Used in case a translation has to be retried
    :param uuid:
    :param background_tasks:
    :param db:
    :return:
    """
    response = await trigger_translation_service(uuid, background_tasks, db)
    return response


@router.get("/translate/{uuid}", tags=["translate"])
async def get_translations(uuid: UUID, db: Session = Depends(get_db)):
    """
    Returns a translation of a text into all the available languages
    If the translation is in progress it will include the progress
    :param uuid:
    :param db:
    :return:
    """
    response = await get_translated_text_service(uuid, db)
    return response
