from dataclasses import dataclass
from typing import Dict

@dataclass
class SearchResult:
    id: str
    score: float
    content: str
    metadata: Dict
    
    def __post_init__(self):
        if self.score < 0 or self.score > 1:
            raise ValueError("Score must be between 0 and 1")