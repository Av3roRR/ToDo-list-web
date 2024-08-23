from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker

class BaseDAO:
    model = None
    
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
        
            return result.mappings().one_or_none()
    
    @classmethod
    async def find_one_or_none(cls, **kwargs):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(query)

            return result.mappings().one_or_none()
        
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            
            return result.scalars().all()
        
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)

            result = await session.execute(query)
            await session.commit()
            return result.scalar()
        
    @classmethod
    async def update(cls, id: int, field: str, data):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == id).values({field: data}).returning(cls.model)
            
            if query is not None:
                updated = await session.execute(query)
                await session.commit()
                
                return updated
            else:
                return None
            
    @classmethod
    async def delete(cls, id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == id)
            if query is not None:
                await session.execute(query)
                await session.commit()
            