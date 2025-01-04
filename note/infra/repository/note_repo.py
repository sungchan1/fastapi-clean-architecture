from note.domain.note import Note
from note.domain.repository.note_repo import INoteRepository


class NoteRepository(INoteRepository):
    def get_notes(self, user_id: str, page: int, items_per_page: int) -> tuple[int, list[Note]]:
        pass

    def find_by_id(self, user_id: str, id: str) -> Note:
        pass

    def save(self, user_id: str, note: Note) -> Note:
        pass

    def update(self, user_id: str, note: Note) -> Note:
        pass

    def delete(self, user_id: str, id: str):
        pass

    def delete_tags(self, user_id: str, id: str):
        pass

    def get_notes_by_tag_name(self, user_id: str, tag_name: str, page: int, items_per_page: int) -> tuple[
        int, list[Note]]:
        pass