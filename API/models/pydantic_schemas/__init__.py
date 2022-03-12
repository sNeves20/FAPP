"""This is were the several Schemas for
Pydantic modules should be placed"""
# Disabaling Pylint errors
# pylint: disable=R0903
# pylint: disable=E0611
from typing import Optional
from pydantic import BaseModel


class StockBase(BaseModel):
    """Base representation of the Stock class"""

    ticker: str
    average_buy: float
    quantity: float


class FinancialInfo(BaseModel):
    """Model that  represents the financial information"""

    static_expenses: list
    recursive_expenses: list
    savings: list
    income_streams: list


class UserBase(BaseModel):
    """Model that represents a basic user"""

    username: str
    password: str


class UserData(UserBase):
    """Model that represents a user with financial information"""

    financial_info: Optional[FinancialInfo]


class BrokerUser(UserBase):
    """MOdel that represents a user with brokers information"""

    broker_name: str


class SavingsBody(BaseModel):
    """Model that representes the savings information"""

    location: Optional[str]
    amount: float
    action: str
