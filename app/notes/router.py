from datetime import date
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import TypeAdapter


from app.notes.dao import NotesDAO
from app.users.dependencies import get_current_user
from app.notes.schemas import SNote
from app.tasks.tasks import send_reminder

router = APIRouter(
    prefix="/notes",
    tags=["Заметки"]
)


# получаем все заметки из базы данных и в будущем отображаем их на страничке
@router.get("")
async def get_notes():
    notes = await NotesDAO.find_all()

    return notes

@router.get("/{note_id}")
@cache(expire=20)
async def get_note_by_id(note_id: int):
    note = await NotesDAO.find_one_or_none(id=note_id)
    if note is None:
        return "Ошибочка вышла"
    
    return note

@router.post("/create_note")
async def create_note(note: str, deadline: date, user = Depends(get_current_user)) -> None:
    new_note = await NotesDAO.add(user_id=user.id, note=note, deadline=str(deadline))
    new_note_dict = TypeAdapter(SNote).validate_python(new_note).model_dump()
    
    send_reminder.delay(new_note_dict, user.email)