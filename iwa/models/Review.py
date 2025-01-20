from dataclasses import dataclass
from datetime import datetime

@dataclass
class Review:
    id: int
    product_id: int
    user_id: int
    review_date: datetime
    comment: str
    rating: int
    visible: bool