'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Html5Qrcode } from 'html5-qrcode';
import { Camera, X } from 'lucide-react';
import { QRCodeSVG } from 'qrcode.react';

export default function CheckInPage() {
    const router = useRouter();
    const [isScanning, setIsScanning] = useState(false);
    const scannerRef = useRef<Html5Qrcode | null>(null);

    // デモ用URL（固定）
    const demoUrl = "https://zoff-scope-frontend.azurewebsites.net/stores/1";

    useEffect(() => {
        // コンポーネントのアンマウント時にクリーンアップ
        return () => {
            if (scannerRef.current) {
                try {
                    if (scannerRef.current.isScanning) {
                        try {
                            // @ts-ignore
                            scannerRef.current.stop();
                        } catch (ignore) { }
                    }
                    try {
                        // @ts-ignore
                        scannerRef.current.clear();
                    } catch (ignore) { }
                } catch (e) {
                    // 同期エラーもキャッチ
                    console.error(e);
                }
            }
        };
    }, []);

    const startScan = async () => {
        setIsScanning(true);

        // 要素が表示されるのを少しだけ待つ（Reactのレンダリング待ち）
        // iOSでもPromise内でのユーザーアクション起因とみなされる範囲内であることを期待
        await new Promise(r => setTimeout(r, 100));

        try {
            const html5QrCode = new Html5Qrcode("reader");
            scannerRef.current = html5QrCode;

            await html5QrCode.start(
                { facingMode: "environment" },
                {
                    fps: 10,
                    qrbox: { width: 250, height: 250 },
                    aspectRatio: 1.0,
                    disableFlip: false,
                },
                onScanSuccess,
                onScanFailure
            );
        } catch (err) {
            console.error("Failed to start scanner", err);
            setIsScanning(false);
            alert("カメラの起動に失敗しました。ブラウザのカメラ権限設定を確認してください。\n" + err);
        }
    };

    const stopScan = async () => {
        if (scannerRef.current) {
            try {
                if (scannerRef.current.isScanning) {
                    await scannerRef.current.stop();
                }
                // clear() はDOMを削除してしまうことがあるため、stop()だけに留めるか注意が必要だが
                // 次回new Html5Qrcodeするときのためにclearもしておく
                await scannerRef.current.clear();
            } catch (error) {
                console.error("Failed to stop scanner", error);
            }
        }
        setIsScanning(false);
    };

    const onScanSuccess = (decodedText: string, decodedResult: any) => {
        console.log(`Code matched = ${decodedText}`, decodedResult);

        // スキャン成功したら即停止
        stopScan().then(() => {
            if (decodedText.includes('/stores/')) {
                try {
                    const url = new URL(decodedText);
                    const path = decodedText.split('azurewebsites.net')[1] || url.pathname;
                    router.push(url.pathname);
                } catch (e) {
                    if (decodedText.startsWith('/')) {
                        router.push(decodedText);
                    } else {
                        window.location.href = decodedText;
                    }
                }
            } else {
                alert(`読み取ったQRコード: ${decodedText}\n店舗のQRコードではありません。`);
            }
        });
    };

    const onScanFailure = (error: any) => {
        // console.warn(`Code scan error = ${error}`);
    };

    return (
        <div className="bg-gray-100 min-h-screen pb-20">
            <header className="bg-blue-600 text-white p-4 text-center font-bold text-lg sticky top-0 z-10">
                Zoff Scope
            </header>

            <main className="p-4 max-w-md mx-auto">
                <h1 className="text-2xl font-bold text-gray-800 mb-6 text-center">お店にチェックイン</h1>

                <div className="bg-white rounded-2xl p-6 shadow-sm mb-6 border border-gray-100 min-h-[400px] relative overflow-hidden">
                    {/* スキャナー領域 */}
                    {!isScanning ? (
                        <div
                            onClick={startScan}
                            className="absolute inset-0 m-6 flex flex-col items-center justify-center bg-blue-50 border-2 border-dashed border-blue-300 rounded-xl cursor-pointer hover:bg-blue-100 transition-colors group z-10"
                        >
                            <div className="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform">
                                <Camera className="w-10 h-10 text-white" />
                            </div>
                            <p className="text-blue-600 font-bold text-lg">QRコードをスキャン</p>
                            <p className="text-blue-400 text-sm">(タップしてカメラ起動)</p>
                        </div>
                    ) : (
                        <button
                            onClick={stopScan}
                            className="absolute top-8 right-8 z-20 bg-white/80 p-2 rounded-full shadow-md hover:bg-white"
                        >
                            <X className="w-6 h-6 text-gray-700" />
                        </button>
                    )}

                    {/* リーダー本体 */}
                    <div id="reader" className={`w-full h-full rounded-xl overflow-hidden bg-black ${!isScanning ? 'invisible' : ''}`}></div>

                    {isScanning && (
                        <p className="text-center text-xs text-gray-400 mt-2 absolute bottom-8 left-0 right-0 z-10 pointer-events-none">
                            QRコードを枠内に合わせてください
                        </p>
                    )}
                </div>

                <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 text-center">
                    <h2 className="text-lg font-bold text-gray-800 mb-2">デモ用QRコード</h2>
                    <p className="text-gray-500 text-sm mb-4">
                        このQRコードをスキャンすると<br />店舗情報の動作確認ができます。
                    </p>
                    <div className="flex justify-center mb-2 bg-gray-50 p-4 rounded-xl border border-dotted border-gray-300 inline-block">
                        <QRCodeSVG value={demoUrl} size={150} />
                    </div>
                    <p className="text-xs text-blue-500 break-all font-mono mt-2">{demoUrl}</p>
                </div>
            </main>
        </div>
    );
}
