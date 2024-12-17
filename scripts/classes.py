from dataclasses import dataclass


@dataclass
class Scan:
    name: str
    data: str
    num_keys: int
    num_points: int
    num_valid_points: int


@dataclass
class Observable:
    search_key: str
    label: str
    key: str
    dimension: str
    
