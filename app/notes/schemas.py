from pydantic import BaseModel

class SNote(BaseModel):
    id: int
    user_id: int
    note: str
    deadline: str
    
    class Config:
        from_attributes=True