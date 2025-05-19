from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Wallet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address: str = Field(index=True, unique=True)
    owner_name: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tx_hash: str = Field(index=True, unique=True)
    wallet_address: str = Field(index=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    amount: float
    from_address: str
    to_address: str
    status: Optional[str] = None