'use client';

import React from 'react';
import type { Wallet, Transaction } from '@/types/types';

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/card';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

interface WalletDetailsProps {
  wallet: Wallet | null;
  transactions: Transaction[];
}

const WalletDetails: React.FC<WalletDetailsProps> = ({
  wallet,
  transactions,
}) => {
  if (!wallet)
    return (
      <p className="text-center py-6 text-muted-foreground">
        No wallet data to display.
      </p>
    );

  const formatDate = (isoString: string) =>
    new Date(isoString).toLocaleString();

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Wallet Details</CardTitle>
          <CardDescription>
            Summary information about this wallet
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          <p>
            <strong>Address:</strong> {wallet.address}
          </p>
          <p>
            <strong>Owner Name:</strong> {wallet.owner_name || 'Unknown'}
          </p>
          <p>
            <strong>Created At:</strong> {formatDate(wallet.created_at)}
          </p>
        </CardContent>
      </Card>

      <h3 className="text-lg font-semibold">Transactions</h3>

      {transactions.length === 0 ? (
        <p>No transactions found for this wallet.</p>
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Hash</TableHead>
              <TableHead>Timestamp</TableHead>
              <TableHead>Amount</TableHead>
              <TableHead>From</TableHead>
              <TableHead>To</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {transactions.map((tx) => (
              <TableRow key={tx.id} className="hover:bg-muted/50">
                <TableCell className="font-mono text-sm truncate max-w-xs">
                  {tx.tx_hash}
                </TableCell>
                <TableCell>{formatDate(tx.timestamp)}</TableCell>
                <TableCell>{tx.amount}</TableCell>
                <TableCell>{tx.from_address}</TableCell>
                <TableCell>{tx.to_address}</TableCell>
                <TableCell>{tx.status || 'N/A'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
};

export default WalletDetails;
