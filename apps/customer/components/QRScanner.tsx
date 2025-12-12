'use client';

import { useEffect, useRef, useState } from 'react';
import { Html5Qrcode, Html5QrcodeSupportedFormats } from 'html5-qrcode';
import { Camera } from 'lucide-react';

interface QRScannerProps {
    onScan: (decodedText: string) => void;
}

export default function QRScanner({ onScan }: QRScannerProps) {
    const [isScanning, setIsScanning] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const scannerRef = useRef<Html5Qrcode | null>(null);
    const scannerId = 'reader';

    useEffect(() => {
        // Cleanup on unmount
        return () => {
            if (scannerRef.current) {
                scannerRef.current.stop().catch((err) => console.error('Failed to stop scanner', err));
            }
        };
    }, []);

    const startScanning = async () => {
        setError(null);
        try {
            const html5QrCode = new Html5Qrcode(scannerId);
            scannerRef.current = html5QrCode;

            await html5QrCode.start(
                { facingMode: 'environment' },
                {
                    fps: 10,
                    qrbox: { width: 250, height: 250 },
                    aspectRatio: 1.0,
                },
                (decodedText) => {
                    onScan(decodedText);
                    stopScanning();
                },
                (errorMessage) => {
                    // parse error, ignore it.
                }
            );
            setIsScanning(true);
        } catch (err) {
            console.error('Error starting scanner:', err);
            setError('カメラの起動に失敗しました。権限を確認してください。');
            setIsScanning(false);
        }
    };

    const stopScanning = async () => {
        if (scannerRef.current) {
            try {
                await scannerRef.current.stop();
                scannerRef.current = null;
                setIsScanning(false);
            } catch (err) {
                console.error('Failed to stop scanner', err);
            }
        }
    };

    return (
        <div className="w-full max-w-sm mx-auto">
            <div
                className="relative border-2 border-dashed border-blue-300 rounded-3xl bg-blue-50 overflow-hidden aspect-square flex flex-col items-center justify-center cursor-pointer hover:bg-blue-100 transition-colors"
                onClick={!isScanning ? startScanning : undefined}
            >
                {!isScanning ? (
                    <div className="flex flex-col items-center justify-center p-6 text-center">
                        <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mb-4 shadow-lg">
                            <Camera className="w-10 h-10 text-white" />
                        </div>
                        <p className="text-gray-500 font-medium">QRコードをスキャン</p>
                        <p className="text-gray-400 text-sm mt-1">(タップしてカメラ起動)</p>
                        {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
                    </div>
                ) : (
                    <div id={scannerId} className="w-full h-full" />
                )}

                {isScanning && (
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            stopScanning();
                        }}
                        className="absolute bottom-4 bg-white/80 text-gray-700 px-4 py-2 rounded-full text-sm font-medium shadow-sm hover:bg-white"
                    >
                        キャンセル
                    </button>
                )}
            </div>
        </div>
    );
}
