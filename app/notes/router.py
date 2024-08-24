from fastapi import APIRouter

from app.notes.dao import NotesDAO

router = APIRouter(
    prefix="/notes",
    tags=["Заметки"]
)


# получаем все заметки из базы данных и в будущем отображаем их на страничке
@router.get("")
async def get_notes():
    notes = await NotesDAO.find_all()

    return notes



"""
В будущем добавлю чтобы была проверка на user и искала в БД
find_all(user_id=user.id, id=note_id)
а входные данные
async def get_note_by_id(note_id: int, user=Depends(get_current_user))
"""
@router.get("/{note_id}")
async def get_note_by_id(note_id: int):
    note = await NotesDAO.find_one_or_none(id=note_id)
    if note is None:
        return "Ошибочка вышла"
    
    return note