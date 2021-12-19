"""This is were the several Schemas for 
Pydantic modules should be placed"""

from pydantic import BaseModel
from typing import Optional


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


class BrokerUser(UserBase):
    broker_name: str


class SavingsBody(BaseModel):
    location: Optional[str]
    amount: float
    action: str
