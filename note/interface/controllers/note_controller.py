from dataclasses import asdict
from datetime import datetime
from http.client import responses
from typing import Annotated

from cffi.model import const_voidp_type
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from common.auth import CurrentUser, get_current_user
from containers import Container
from note.application.note_service import NoteService

router = APIRouter(prefix="/notes")

class NoteResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    memo_date: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class CreateNoteBody(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1)
    memo_date: str = Field(min_length=8, max_length=8)
    tags: list[str] | None = Field(default=None, min_length=1, max_length=32)

class GetNotesResponse(BaseModel):
    total_count: int
    page: int
    notes: list[NoteResponse]

class UpdateNoteBody(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=64)
    content: str | None = Field(default=None, min_length=1)
    memo_date: str | None = Field(default=None, min_length=8, max_length=8)
    tags: list[str] | None = Field(default=None)


@router.post("", status_code=201, response_model=NoteResponse)
@inject
def create_note(current_user: Annotated[CurrentUser, Depends(get_current_user)],
                body: CreateNoteBody,
                note_service: NoteService = Depends(Provide[Container.note_service])):
    note = note_service.create_note(
        user_id = current_user.id,
        title=body.title,
        content=body.content,
        memo_date=body.memo_date,
        tag_names=body.tags if body.tags else [],
    )

    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})
    return response

@router.get("", response_model=GetNotesResponse)
@inject
def get_notes(
        page: int=1,
        items_per_page: int =10,
        current_user: CurrentUser = Depends(get_current_user),
        note_service: NoteService = Depends(Provide[Container.user_service])
):
    total_count, notes = note_service.get_notes(
        user_id = current_user.id,
        page=page,
        items_per_page=items_per_page,
    )
    res_notes = []
    for note in notes:
        note_dict = asdict(note)
        note_dict.update({"tags": [tag.name for tag in note.tags]})
        res_notes.append(note_dict)

    return {
        "total_count": total_count,
        "page": page,
        "notes": res_notes,
    }


@router.get("/{id}", response_model=NoteResponse)
@inject
def get_note(
        id: str,
        current_user: Annotated[CurrentUser, Depends(get_current_user())],
        note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.get_note(
        user_id=current_user.id,
        id=id,
    )
    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})

    return response


@router.put("/{id}", response_model=NoteResponse)
@inject
def update_note(
    id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user())],
        body: UpdateNoteBody,
        note_service: NoteService = Depends(Provide[Container.note_service])

):
    note = note_service.update_note(
        user_id=current_user.id,
        id=id,
        title=body.title,
        content=body.content,
        memo_date=body.memo_date,
        tag_names=body.tags
    )

    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})
    return response


@router.delete("/{id}", status_code=204)