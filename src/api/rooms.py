from fastapi import APIRouter, Query, HTTPException

from src.schemas.rooms import SRoomsAdd, SRoomsAddRequest, SRoomsEditPUTCHRequest, SRoomsEditPUTCH
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository

router = APIRouter(
    prefix="/hotel",
    tags=["Комнаты"],
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int | None = None,
        page: int | None = Query(1, ge=1),
        per_page: int | None = Query(None, ge=1, lt=10),
):
    """
    Ручка для получения всех номер одного отеля
    :param hotel_id:
    :param page:
    :param per_page:
    :return: Список номеров
    """
    per_page = per_page or 5

    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            limit=per_page,
            offset=per_page * (page - 1)
        )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    """
    Ручка для получения одного номера
    :param hotel_id:
    :param room_id:
    :return: Номер
    """
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, rooms_data: SRoomsAddRequest):
    """
    Ручка для создания номера
    :param hotel_id:
    :param rooms_data:
    :return:
    """
    _room = SRoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).add(_room)
        await session.commit()
        return {"status": "ok"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_all_param_room(hotel_id: int, room_id: int, rooms_data: SRoomsAddRequest):
    """
    Ручка для редактирование всех полей номера
    :param hotel_id:
    :param room_id:
    :param rooms_data:
    :return:
    """
    _room = SRoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if room:
            await RoomsRepository(session).edit(_room, id=room_id)
            await session.commit()
            return {"status": "ok"}

        raise HTTPException(status_code=404, detail="Room not found")


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_one_param_room(hotel_id: int, room_id: int, rooms_data: SRoomsEditPUTCHRequest):
    """
    Ручка для редактирование одного или более полей номера
    :param hotel_id:
    :param room_id:
    :param rooms_data:
    :return:
    """
    _room = SRoomsEditPUTCH(hotel_id=hotel_id, **rooms_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if room:
            await RoomsRepository(session).edit(_room, exclude_unset=True, id=room_id, hotel_id=hotel_id)
            await session.commit()
            return {"status": "ok"}

        raise HTTPException(status_code=404, detail="Room not found")


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    """
    Ручка для удаления номера
    :param hotel_id:
    :param room_id:
    :return:
    """
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if room:
            await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
            await session.commit()
            return {"status": "ok"}

        raise HTTPException(status_code=404, detail="Room not found")
