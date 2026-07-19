"""
type Extra = { text: string; likes: number };

type TaskRecord = {
  id: string;
  sequence_number: number;
  // location/pose/object zijn null als opdracht_text is ingevuld (en vice versa)
  location_text: string | null;
  location_likes: number | null;
  pose_text: string | null;
  pose_likes: number | null;
  object_text: string | null;
  object_likes: number | null;
  opdracht_text: string | null;
  opdracht_likes: number | null;
  extras: Extra[];
};
"""


from pydantic import BaseModel

from models.models import TaskRecord


class Extra(BaseModel):
    text: str
    likes: int

class TaskResponse(BaseModel):
    id: str
    sequence_number: int
    location_text: str | None
    location_likes: int | None
    pose_text: str | None
    pose_likes: int | None
    object_text: str | None
    object_likes: int | None
    special_task_text: str | None
    special_task_likes: int | None
    extras: list[Extra]
    photo_url: str | None
    is_stolen: bool
    multiplier: float
    
    @property
    def likes(self) -> int:
        if self.special_task_text is not None:
            return self.special_task_likes or 0
        return (self.location_likes or 0) + (self.pose_likes or 0) + (self.object_likes or 0)
    
    @property
    def bonus_likes(self) -> int:
        return sum(extra.likes for extra in self.extras)

    @classmethod
    def from_record(cls, r: TaskRecord) -> "TaskResponse":
        return cls(**r.model_dump(exclude={"extras_json"}), extras=r.extras)


class TeamHistoryResponse(BaseModel):
    id: str
    name: str
    tasks: list[TaskResponse]
    
class TaskPage(BaseModel):
    items: list[TaskResponse]
    next_offset: int | None