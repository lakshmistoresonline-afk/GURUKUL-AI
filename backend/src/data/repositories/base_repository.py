from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import TypeVar, Generic, Type, List, Optional

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: str) -> Optional[T]:
        return await self.session.get(self.model, id)

    async def list(self) -> List[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
