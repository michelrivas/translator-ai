
import asyncio
import logging

from sqlalchemy.orm import Session

from src.translator.external_service import translate_external_api
from src.translator.models import TranslationText, Translation

logger = logging.getLogger(__name__)


async def process_translation(translation: Translation, translation_text: str, db: Session):
    """
    Wrapper task used to call the external translation API and update the translation in the database
    :param translation:
    :param translation_text:
    :param db:
    :return:
    """
    try:
        translation.text = await translate_external_api(translation_text, translation.language)
        translation.error = None
    except Exception as e:
        translation.error = str(e)
        logger.error(str(e))
    finally:
        db.commit()


async def translate_task(translation_text_id: str, db: Session):
    """
    Background task to process all the translations asynchronously
    :param translation_text_id:
    :param db:
    :return:
    """
    # Retrieve the TranslationText object from the database
    translation_text = db.get(TranslationText, translation_text_id)

    # Check if the translation_text exists
    if not translation_text:
        logger.info(f'No TranslationText found with id: {translation_text_id}')
        return

    # Create translation tasks for each language in the languages list
    # Execute all tasks concurrently and handle results
    async with asyncio.TaskGroup() as tg:
        for translation in translation_text.translations:
            tg.create_task(process_translation(translation, translation_text.text, db))

    translation_texts_updated = [tr.text is not None for tr in translation_text.translations]

    if all(translation_texts_updated):
        translation_text.status = 'completed'

    # Commit all changes (updated translations and updated status) at once
    db.commit()
