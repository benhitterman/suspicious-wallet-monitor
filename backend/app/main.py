from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .models import Wallet, Transaction
from .database import engine, create_db_and_tables
from .crud import create_wallet, get_wallet_by_address, get_all_wallets, create_transaction, get_transactions_by_wallet, get_transaction_by_hash

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

flagged_wallets = {
    '0x123...': {"isFlagged": True, "riskLevel": "High", "reason": "Associated with phishing scams"},
}

@app.post("/wallets/", response_model=Wallet)
def create_wallet_endpoint(wallet: Wallet):
    db_wallet = get_wallet_by_address(wallet.address)
    if db_wallet:
        raise HTTPException(status_code=400, detail="Wallet already exists")
    return create_wallet(wallet)

@app.get("/wallets/{address}", response_model=Wallet)
def get_wallet_endpoint(address: str):
    wallet = get_wallet_by_address(address)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@app.get("/wallets/", response_model=list[Wallet])
def get_wallets_endpoint():
    return get_all_wallets()

@app.post("/transactions/", response_model=Transaction)
def create_transaction_endpoint(transaction: Transaction):
    existing_tx = get_transaction_by_hash(transaction.tx_hash)
    if existing_tx:
        raise HTTPException(status_code=400, detail="Transaction already exists")
    return create_transaction(transaction)

@app.get("/transactions/{wallet_address}", response_model=list[Transaction])
def get_transactions_for_wallet(wallet_address: str):
    return get_transactions_by_wallet(wallet_address)

@app.get("/wallets/{address}/suspicious")
def check_wallet_suspicious(address: str):
    address_lower = address.lower()
    info = flagged_wallets.get(address_lower, {
        "isFlagged": False,
        "riskLevel": "Low",
        "reason": "No suspicious activity detected",
    })
    return JSONResponse(content={"address": address, **info})