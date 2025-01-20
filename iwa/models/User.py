from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    password: str
    date_created: datetime
    first_name: str
    last_name: str
    email: str
    phone: str
    city: str
    state: str
    zip: str
    country: str
    role: str
    enable: bool