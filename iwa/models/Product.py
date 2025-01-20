from dataclasses import dataclass

@dataclass
class Product:
    id: int
    code: str
    name: str
    summary: str
    description: str
    image: str
    price: float
    on_sale: bool
    sale_price: float
    in_stock: bool
    time_to_stock: int
    rating: int
    available: bool