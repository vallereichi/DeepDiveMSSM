from dataclasses import dataclass
import pandas as pd


@dataclass
class Scan:
    name: str
    data: pd.DataFrame
    plr: list
    num_keys: int
    num_points: int
    num_valid_points: int


@dataclass
class Observable:
    search_key: str
    label: str
    key: str
    dimension: str
    
