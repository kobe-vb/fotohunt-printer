"""
type Extra = { text: string; likes: number };

type TaskRecord = {
  id: string;
  sequence_number: number;
  location_text: string;
  location_likes: number;
  pose_text: string;
  pose_likes: number;
  object_text: string;
  object_likes: number;
  extras: Extra[];
};
"""

from typing import Optional

from pydantic import BaseModel

from models.models import TaskRecord


class Extra(BaseModel):
    text: str
    likes: int

class TaskResponse(BaseModel):
    id: str
    sequence_number: int
    location_text: str
    location_likes: int
    pose_text: str
    pose_likes: int
    object_text: str
    object_likes: int
    extras: list[Extra]
    photo_url: str | None
    
    @property
    def likes(self) -> int:
        return self.location_likes + self.pose_likes + self.object_likes
    
    @property
    def bonus_likes(self) -> int:
        return sum(extra.likes for extra in self.extras)

    @classmethod
    def from_record(cls, r: TaskRecord) -> "TaskResponse":
        return cls(**r.model_dump(exclude={"extras_json"}), extras=r.extras)
  