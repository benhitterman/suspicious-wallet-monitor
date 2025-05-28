'use client';

import React, { useState, useEffect } from 'react';
import WalletForm from '@/components/WalletForm';
import WalletDetails from '@/components/WalletDetails';
import type { Wallet, Transaction } from '@/types/types';

export default function Home() {
  const [address, setAddress] = useState<string | null>(null);
  const [wallet, setWallet] = useState<Wallet | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleWalletCreated = (newAddress: string) => {
    setAddress(newAddress);
  };

  useEffect(() => {
    if (!address) return;

    setLoading(true);
    setError(null);

    const fetchData = async () => {
      try {
        const walletRes = await fetch(
          `http://localhost:8000/wallets/${address}`
        );
        if (!walletRes.ok) throw new Error('Wallet not found');
        const walletData: Wallet = await walletRes.json();

        const txRes = await fetch(
          `http://localhost:8000/transactions/${address}`
        );
        if (!txRes.ok) throw new Error('Failed to fetch transactions');
        const txData: Transaction[] = await txRes.json();

        setWallet(walletData);
        setTransactions(txData);
      } catch (err: unknown) {
        if (err instanceof Error) setError(err.message);
        else setError('Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [address]);

  return (
    <div className="min-h-screen p-8 bg-gray-50">
      {!wallet && <WalletForm onSubmit={handleWalletCreated} />}

      {loading && <p>Loading wallet data...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {!loading && !error && wallet && (
        <>
          <WalletDetails wallet={wallet} transactions={transactions} />

          {wallet.is_suspicious && (
            <div className="mt-4 p-4 bg-red-100 text-red-800 rounded">
              <p>
                <strong>🚩 Suspicious Wallet</strong>
              </p>
              <p>
                <strong>Risk Level:</strong> High
              </p>
              <p>
                <strong>Reason:</strong> Involved in transactions with known
                malicious addresses
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
