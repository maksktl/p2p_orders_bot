from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class OrderFullDto:
    id: UUID
    external_id: str
    username: str
    source: str
    asset: str
    fiat: str
    price: float
    trade_type: str
    limit_lower: float
    limit_upper: float
    capital: float
    pay_type: List[str]
