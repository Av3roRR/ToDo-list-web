from app.dao.base import BaseDAO
from app.notes.models import Notes

class NotesDAO(BaseDAO):
    model=Notes