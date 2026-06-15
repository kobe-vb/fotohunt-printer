from dataclasses import dataclass

@dataclass(frozen=True)
class Element:
    text: str
    likes: int


@dataclass(frozen=True)
class Task:
    location: Element
    pose: Element
    object: Element
    extras: tuple[Element, ...]
    
    @property
    def likes(self) -> int:
        return (
            self.location.likes +
            self.pose.likes +
            self.object.likes
        )
    
    @property
    def bonus_likes(self) -> int:
        return sum(extra.likes for extra in self.extras)