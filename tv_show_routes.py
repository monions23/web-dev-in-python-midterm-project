from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, logger, status
from tv_show import Show, ShowRequest

show_router = APIRouter()


@show_router.get("")
async def get_all_shows() -> list[Show]:
    show_list = await Show.find_all().to_list()
    return show_list


@show_router.post("", status_code=201)
async def create_new_show(tv_show: ShowRequest) -> Show:
    tv_show = Show(**tv_show.model_dump())
    await tv_show.insert()
    return tv_show


@show_router.put("/{id}")
async def edit_show_by_id(
    id: str, tv_show: ShowRequest
) -> Show:
    show = await Show.get(id)
    show = Show(**show.model_dump())
    if not show:
        raise HTTPException(status_code=404, detail="Show not found in database")

    update_data = tv_show.model_dump(exclude_unset=True)
    await show.update({"$set": update_data})

    updated_item = await Show.get(id)

    return updated_item


@show_router.get("/{id}")
async def get_show_by_id(id: str) -> Show:
    show = await Show.get(id)
    if not show:
        raise HTTPException(status_code=404, detail="Show not found in database")
    return show


@show_router.delete("/{id}")
async def delete_show_by_id(
    id: str,
) -> dict:
    show = await Show.get(id)
    if not show:
        raise HTTPException(status_code=404, detail="Show not found in database")
    await show.delete()
    return {"msg": f"The TV Show {show.title} has been deleted successfully."}
