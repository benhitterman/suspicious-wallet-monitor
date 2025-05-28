# Wallet Suspicion Checker

A full-stack application that allows users to input a wallet address and receive information on its activity, including transaction history and potential suspicion flags. Built with **FastAPI** (Python backend), **PostgreSQL** for database interactions, and **Next.js** with **Tailwind CSS** for the frontend.
<img width="1497" alt="Screenshot 2025-05-18 at 10 42 44 PM" src="https://github.com/user-attachments/assets/7e4cb256-ba43-4fa2-a4dc-6c131b4525f2" />

## Features

- View wallets
- View recent transactions for a wallet
- Flagged wallets as suspicious
- FastAPI backend with auto-generated docs
- Type-safe and responsive frontend

---

## Tech Stack

**Backend:**

- Python 3
- FastAPI
- SQLModel
- PostgreSQL
- CORS middleware

**Frontend:**

- Next.js (React)
- TypeScript
- Tailwind CSS
- ShadCN UI

---

## Environment Setup

### PostgreSQL Database

Ensure you have PostgreSQL installed and a database named `walletdb` created:

```bash
psql postgres
CREATE DATABASE walletdb;
\q
```

### `.env` File

In your backend/ directory, create a `.env` file with the following content:

```env
DATABASE_URL=postgresql://your_username@localhost:5432/walletdb
```

---

## Running Locally

### 1. Clone the repo and run virtual environment

```bash
git clone https://github.com/benhitterman/suspicious-wallet-monitor.git
python3 -m venv venv

# For Linux/macOS:
source venv/bin/activate

# For Windows:
venv\Scripts\activate
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload # Runs on http://localhost:8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev # Runs on http://localhost:3000
```

---

## API Endpoints

Test the API interactively on http://localhost:8000/docs

### `POST /wallets/`

Create a new wallet

```json
{
  "address": "0x123...",
  "owner_name": "Alice"
}
```

### `GET /wallets/{address}`

Get wallet by address

### `GET /wallets/`

Get all wallets

### `POST /transactions/`

Add a new transaction

```json
{
  "tx_hash": "abc123...",
  "wallet_address": "0x123...",
  "amount": 100,
  "from_address": "0x123...",
  "to_address": "0xabc...",
  "status": "confirmed"
}
```

Add new suspicious transaction

```json
{
  "tx_hash": "abc123...",
  "wallet_address": "0x123...",
  "amount": 100,
  "from_address": "0x123...",
  "to_address": "0x123malicious",
  "status": "confirmed"
}
```

### `GET /transactions/{wallet_address}`

Get transactions for a given wallet

### `GET /wallets/{address}/suspicious`

Check if a wallet is flagged for suspicious activity

### `DELETE /wallets/{address}/`

Delete wallet by address

### `GET /transactions/{tx_hash}`

Delete transaction by hash

---

## Suspicious Wallet Logic

Flagged address are hardcoded:

```python
MALICIOUS_ADDRESSES = {
    "0x123malicious",
    "0x456scam",
    "0x789fraud",
}
```
