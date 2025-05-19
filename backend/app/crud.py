from typing import Optional, List
from sqlmodel import Session, select
from .models import Wallet, Transaction
from .database import engine

def create_wallet(wallet: Wallet) -> Wallet:
    with Session(engine) as session:
        session.add(wallet)
        session.commit()
        session.refresh(wallet)
        return wallet # returns wallet with DB auto-generated fiels like ID

def get_wallet_by_address(address: str) -> Optional[Wallet]:
    with Session(engine) as session:
        statement = select(Wallet).where(Wallet.address == address)
        results = session.exec(statement)
        return results.first()
    
def get_all_wallets() -> List[Wallet]:
    with Session(engine) as session:
        statement = select(Wallet)
        results = session.exec(statement)
        return results.all()
    
def create_transaction(transaction: Transaction) -> Transaction:
    with Session(engine) as session:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction

def get_transactions_by_wallet(address: str) -> List[Transaction]:
    with Session(engine) as session:
        statement = select(Transaction).where(Transaction.wallet_address == address).order_by(Transaction.timestamp.desc())
        results = session.exec(statement)
        return results.all()

def get_transaction_by_hash(tx_hash: str) -> Optional[Transaction]:
    with Session(engine) as session:
        statement = select(Transaction).where(Transaction.tx_hash == tx_hash)
        result = session.exec(statement)
        return result.first()