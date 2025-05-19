'use client';

import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface WalletFormProps {
  onSubmit: (address: string) => void;
}

const WalletForm: React.FC<WalletFormProps> = ({ onSubmit }) => {
  const [address, setAddress] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(address);
  };

  return (
    <Card className="max-w-md mx-auto p-4">
      <CardHeader>
        <CardTitle>Enter Wallet Address</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="address">Wallet Address</Label>
            <Input
              id="address"
              type="text"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              required
            />
          </div>
          <Button type="submit" className="w-full">
            Check Wallet
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default WalletForm;
