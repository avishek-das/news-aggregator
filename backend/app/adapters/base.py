from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class RawItem:
    title: str
    url: str
    excerpt: str
    published_at: datetime | None
    category: str
    is_paywalled: bool = False
    raw_metadata: dict = field(default_factory=dict, compare=False, hash=False)


class SourceAdapter(ABC):
    def __init__(self, source_id: str, fetch_config: dict) -> None:
        self.source_id = source_id
        self.fetch_config = fetch_config

    @abstractmethod
    async def fetch(self) -> list[RawItem]:
        ...
