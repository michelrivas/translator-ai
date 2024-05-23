from typing import Optional
from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload

from src.translator.tasks import translate_task
from src.translator.models import TranslationText, Translation
from src.translator.schemas import TranslationRequest


async def translate_service(request: TranslationRequest, background_tasks: BackgroundTasks, db: Session) -> str:
    """
    Main translate service.
    Stores the translation data in the database and triggers a background task to process it
    :param request:
    :param background_tasks:
    :param db:
    :return:
    """
    translation_text = TranslationText(text=request.text)

    db.add(translation_text)
    db.flush()  # This will generate the UUID and keep it in the session

    for language in request.languages:
        translation = Translation(text_id=translation_text.uuid, language=language)
        db.add(translation)

    db.commit()  # Commit changes to the database

    background_tasks.add_task(translate_task, translation_text.uuid, db)

    return translation_text.uuid


async def trigger_translation_service(uuid: UUID, background_tasks: BackgroundTasks, db: Session) -> str:
    """
    Service to trigger a stored translation which is not completed (in case of errors)
    :param uuid:
    :param background_tasks:
    :param db:
    :return:
    """
    try:
        translation_text = (
            db.query(TranslationText)
            .options(joinedload(TranslationText.translations))
            .filter(TranslationText.uuid == uuid, TranslationText.status == "pending")
            .one()
        )
        background_tasks.add_task(translate_task, translation_text.uuid, db)
        return "Translation task triggered"
    except NoResultFound:
        return "No record found with given UUID or the status is not pending"


def calculate_translation_progress(translation_text: TranslationText) -> int:
    """
    Calculates the completion progress of a translation
    The progress is calculated based on the number of languages translated out of the total
    :param translation_text:
    :return:
    """
    try:
        total_translations = len(translation_text.translations)
        completed_translations = len([tr for tr in translation_text.translations if tr.text is not None])
        progress = (completed_translations / total_translations) * 100 if total_translations > 0 else 0
        return int(progress)
    except NoResultFound:
        return 0


async def get_translated_text_service(uuid: UUID, db: Session) -> Optional[TranslationText]:
    """
    Retrieves a translation from the database
    If the translation is not completed, then it calculates the progress of completion
    :param uuid:
    :param db:
    :return:
    """
    try:
        translation_text = (
            db.query(TranslationText)
            .options(joinedload(TranslationText.translations))
            .filter(TranslationText.uuid == uuid)
            .one()
        )
        if translation_text.status != "completed":
            progress = calculate_translation_progress(translation_text)
            translation_text.progress = f"In progress: {progress}"
        return translation_text
    except NoResultFound:
        return None
