export interface Wallet {
  id?: number;
  address: string;
  owner_name?: string;
  created_at: string;
}

export interface Transaction {
  id?: number;
  tx_hash: string;
  wallet_address: string;
  timestamp: string;
  amount: number;
  from_address: string;
  to_address: string;
  status?: string;
}

export interface SuspiciousInfo {
  address: string;
  isFlagged: boolean;
  riskLevel: string;
  reason: string;
}