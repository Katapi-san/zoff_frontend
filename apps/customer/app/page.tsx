'use client';

import { useState } from 'react';
import QRScanner from '../components/QRScanner';

import { QRCodeCanvas } from 'qrcode.react';

export default function Home() {
  const [scannedResult, setScannedResult] = useState<string | null>(null);

  const handleScan = (data: string) => {
    if (data) {
      setScannedResult(data);
      alert(`QRコードを読み取りました: ${data}`);
      // Here you would typically navigate to the check-in page or API
    }
  };

  const handleDemoScan = () => {
    handleScan('demo_store_checkin_123');
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-20 font-sans">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 text-center sticky top-0 z-10 shadow-md">
        <h1 className="text-xl font-bold tracking-wide">Zoff Scope</h1>
      </header>

      <main className="p-6 max-w-md mx-auto space-y-8">

        {/* Title */}
        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-6">お店にチェックイン</h2>

          {/* Scanner Area */}
          <QRScanner onScan={handleScan} />
        </section>

        {/* Demo Section */}
        <section className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 text-center">
          <h3 className="text-lg font-bold text-gray-800 mb-2">デモ用QRコード</h3>
          <p className="text-gray-500 text-sm mb-6">
            このQRコードをスキャンすると渋谷マークシティ店の情報が表示されます
          </p>

          <div className="flex justify-center mb-6">
            <div className="p-2 bg-white border-4 border-black rounded-lg">
              <QRCodeCanvas
                value="demo_store_checkin_123"
                size={160}
                level={"H"}
              />
            </div>
          </div>

          <button
            onClick={handleDemoScan}
            className="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors shadow-md active:transform active:scale-95"
          >
            QRコードを読み取る（デモ）
          </button>
        </section>

        {scannedResult && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative">
            <strong className="font-bold">スキャン成功!</strong>
            <span className="block sm:inline"> {scannedResult}</span>
          </div>
        )}

      </main>


    </div>
  );
}
