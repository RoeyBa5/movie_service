from dataclasses import dataclass

import dataclasses_json


@dataclasses_json.dataclass_json
@dataclass
class Movie:
    Title: str
    Year: str
    imdbID: str
    Type: str
    Poster: str
