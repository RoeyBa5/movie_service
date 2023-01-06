from dataclasses import dataclass, field
from typing import List, Optional

import dataclasses_json
from dataclasses_json import config

from api.models.base import Movie


def int_decoder(value: str) -> Optional[int]:
    return int(value) if value else None


@dataclasses_json.dataclass_json
@dataclass
class SearchMovies:
    Response: bool = field(metadata=config(decoder=bool))
    totalResults: Optional[int] = field(metadata=config(decoder=int_decoder), default=None)
    Search: Optional[List[Movie]] = None
    Error: Optional[str] = None
