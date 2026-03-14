from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from tv_show import Show, ShowRequest

show_router = APIRouter()

show_list = []
global_id = 0


@show_router.get("")
async def get_all_shows() -> list[Show]:
    return show_list


@show_router.post("", status_code=201)
async def create_new_show(tv_show: ShowRequest) -> Show:
    global global_id  # important, so that this variable will have value and tracked for every request
    global_id += 1
    new_show = Show(id=global_id, title=tv_show.title, desc=tv_show.desc, season = tv_show.season, episode = tv_show.episode)
    show_list.append(new_show)
    return new_show


@show_router.put("/{id}")
async def edit_show_by_id(
    id: Annotated[int, Path(gt=0, le=1000)], tv_show: ShowRequest
) -> Show:
    for x in show_list:
        if x.id == id:
            x.title = tv_show.title
            x.desc = tv_show.desc
            x.season = tv_show.season
            x.episode = tv_show.episode
            return x

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"TV Show with ID = {id} is not found.",
    )


@show_router.get("/{id}")
async def get_show_by_id(id: Annotated[int, Path(gt=0, le=1000)]) -> Show:
    for show in show_list:
        if show.id == id:
            return show

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"TV Show with ID = {id} is not found.",
    )


@show_router.delete("/{id}")
async def delete_show_by_id(
    id: Annotated[int, Path(title="The ID of the item", gt=0, le=1000)],
) -> dict:
    for index in range(len(show_list)):
        show = show_list[index]
        if show.id == id:
            show_list.pop(index)
            return {"msg": f"The TV Show {show.title} with ID = {id} is deleted."}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with ID = {id} is not found",
    )
