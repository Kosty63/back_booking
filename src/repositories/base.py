from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel


class BaseRepository:
    """
    Базовый класс репозитория
    """

    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **filter_by):
        """
        Функция по получению все записей сущности БД
        :param args:
        :param kwargs:
        :return: all records model
        """
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, *args, **filter_by):
        """
        Функция по получению одной записи переданной модели
        :param args:
        :param kwargs:
        :return: one record model
        """
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        """
        Функция по добавлению записи в БД
        :param data:
        :return: one record model
        """
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False,  **filter_by) -> None:
        stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
