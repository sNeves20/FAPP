from pydantic import BaseModel
from uuid import uuid4
from typing import Optional, List


class StockBase(BaseModel):
    ticker: str
    average_buy: float
    quantity: float


class FinancialInfo(BaseModel):
    static_expenses: list
    recursive_expenses: list
    savings: list
    income_streams: list


class UserBase(BaseModel):
    username: str
    password: str


class UserData(UserBase):
    financial_info: Optional[FinancialInfo]