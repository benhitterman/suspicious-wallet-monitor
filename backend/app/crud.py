from typing import Optional, List
from sqlmodel import Session, select, delete
from .models import Wallet, Transaction
from .database import engine

MALICIOUS_ADDRESSES = {
    "0x123malicious",
    "0x456scam",
    "0x789fraud",
}

def create_wallet(wallet: Wallet) -> Wallet:
    with Session(engine) as session:
        session.add(wallet)
        session.commit()
        session.refresh(wallet)
        return wallet # returns wallet with DB auto-generated ID

def get_wallet_by_address(address: str, session: Optional[Session] = None) -> Optional[Wallet]:
    close_session = False
    if session is None:
        session = Session(engine)
        close_session = True

    statement = select(Wallet).where(Wallet.address == address)
    result = session.exec(statement).first()

    if close_session:
        session.close()

    return result
    
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

        flag_wallet_if_suspicious(transaction.wallet_address, session)
        flag_wallet_if_suspicious(transaction.to_address, session)

        return transaction

def get_transactions_by_wallet(address: str) -> List[Transaction]:
    with Session(engine) as session:
        statement = select(Transaction).where(Transaction.wallet_address == address).order_by(Transaction.timestamp.desc())
        results = session.exec(statement)
        return results.all()

def get_transaction_by_hash(tx_hash: str, session: Optional[Session] = None) -> Optional[Transaction]:
    close_session = False
    if session is None:
        session = Session(engine)
        close_session = True

    statement = select(Transaction).where(Transaction.tx_hash == tx_hash)
    result = session.exec(statement)
    transaction = result.first()

    if close_session:
        session.close()

    return transaction
    
def delete_wallet(address: str) -> bool:
    with Session(engine) as session:
        wallet = get_wallet_by_address(address)
        if not wallet:
            return False
        
        session.exec(delete(Transaction).where(Transaction.wallet_address == address))
        session.delete(wallet)
        session.commit()
        return True

def delete_transaction(tx_hash: str) -> bool:
    with Session(engine) as session:
        transaction = get_transaction_by_hash(tx_hash, session)
        if not transaction:
            return False

        session.delete(transaction)
        session.commit()
        return True
    
def flag_wallet_if_suspicious(wallet_address: str, session: Session) -> None:
    statement = select(Transaction).where(
        (Transaction.wallet_address == wallet_address) |
        (Transaction.to_address == wallet_address)
    )
    results = session.exec(statement).all()

    for tx in results:
        if tx.wallet_address in MALICIOUS_ADDRESSES or tx.to_address in MALICIOUS_ADDRESSES:
            wallet = get_wallet_by_address(wallet_address, session)
            if wallet and not wallet.is_suspicious:
                wallet.is_suspicious = True
                session.add(wallet)
                session.commit()
                session.refresh(wallet)
            return  # No need to continue once marked