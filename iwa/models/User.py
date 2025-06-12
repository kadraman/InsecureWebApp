"""
        InsecureWebApp - an insecure Python/Flask Web application

        Copyright (C) 2024-2025  Kevin A. Lee (kadraman)

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    email: str
    password: str
    date_created: datetime
    first_name: str
    last_name: str
    phone: str
    city: str
    state: str
    zip: str
    country: str
    role: str
    enabled: bool
    otp_enabled: bool
    otp_secret: str