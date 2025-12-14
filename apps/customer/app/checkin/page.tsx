'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Html5QrcodeScanner } from 'html5-qrcode';
import { Camera } from 'lucide-react';
import { QRCodeSVG } from 'qrcode.react';

export default function CheckInPage() {
    const router = useRouter();
    const [isScanning, setIsScanning] = useState(false);
    const scannerRef = useRef<Html5QrcodeScanner | null>(null);

    // デモ用URL（固定）
    const demoUrl = "https://zoff-scope-frontend.azurewebsites.net/stores/1";

    useEffect(() => {
        // コンポーネントのアンマウント時にクリーンアップ
        return () => {
            if (scannerRef.current) {
                scannerRef.current.clear().catch(console.error);
            }
        };
    }, []);

    const startScan = () => {
        setIsScanning(true);
        // DOM要素のレンダリングを待つために少し遅延させる
        setTimeout(() => {
            try {
                // html5-qrcodeの設定
                const scanner = new Html5QrcodeScanner(
                    "reader",
                    {
                        fps: 10,
                        qrbox: { width: 250, height: 250 },
                        aspectRatio: 1.0,
                        disableFlip: false,
                        showTorchButtonIfSupported: true,
                        rememberLastUsedCamera: true
                    },
                    /* verbose= */ false
                );
                scannerRef.current = scanner;

                scanner.render(onScanSuccess, onScanFailure);
            } catch (err) {
                console.error("Failed to start scanner", err);
                setIsScanning(false);
                alert("カメラの起動に失敗しました。権限設定を確認してください。");
            }
        }, 100);
    };

    const stopScan = async () => {
        if (scannerRef.current) {
            try {
                await scannerRef.current.clear();
                setIsScanning(false);
            } catch (error) {
                console.error("Failed to clear scanner", error);
            }
        }
    };

    const onScanSuccess = (decodedText: string, decodedResult: any) => {
        // スキャン成功時の処理
        console.log(`Code matched = ${decodedText}`, decodedResult);

        if (scannerRef.current) {
            scannerRef.current.clear().then(() => {
                setIsScanning(false);

                // URLかどうか検証し、アプリ内の店舗ページか確認
                // https://.../stores/123 の形式を想定
                if (decodedText.includes('/stores/')) {
                    try {
                        const url = new URL(decodedText);
                        // 同じドメイン内ならパス遷移、外部ならURL検証が必要だが、ここではシンプルにパスを取得
                        // 開発環境と本番環境でドメインが違う場合も考慮し、パス部分だけ抽出して遷移が安全
                        const path = decodedText.split('azurewebsites.net')[1] || url.pathname;
                        // 単純にパスとしてrouter.pushできるか確認。
                        // URLオブジェクトにしてpathnameを取得するのが一番確実。
                        router.push(url.pathname);
                    } catch (e) {
                        // URLパース失敗時などはそのまま遷移してみる（相対パスの場合など）
                        if (decodedText.startsWith('/')) {
                            router.push(decodedText);
                        } else {
                            window.location.href = decodedText;
                        }
                    }
                } else {
                    alert(`読み取ったQRコード: ${decodedText}\n店舗のQRコードではありません。`);
                }
            }).catch(console.error);
        }
    };

    const onScanFailure = (error: any) => {
        // スキャン中の軽微なエラーは無視（フレームごとに呼ばれるため）
    };

    return (
        <div className="bg-gray-100 min-h-screen pb-20">
            <header className="bg-blue-600 text-white p-4 text-center font-bold text-lg sticky top-0 z-10">
                Zoff Scope
            </header>

            <main className="p-4 max-w-md mx-auto">
                <h1 className="text-2xl font-bold text-gray-800 mb-6 text-center">お店にチェックイン</h1>

                <div className="bg-white rounded-2xl p-6 shadow-sm mb-6 border border-gray-100 min-h-[400px]">
                    {!isScanning ? (
                        <div
                            onClick={startScan}
                            className="w-full h-80 bg-blue-50 border-2 border-dashed border-blue-300 rounded-xl flex flex-col items-center justify-center cursor-pointer hover:bg-blue-100 transition-colors group"
                        >
                            <div className="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform">
                                <Camera className="w-10 h-10 text-white" />
                            </div>
                            <p className="text-blue-600 font-bold text-lg">QRコードをスキャン</p>
                            <p className="text-blue-400 text-sm">(タップしてカメラ起動)</p>
                        </div>
                    ) : (
                        <div className="flex flex-col h-full">
                            <div id="reader" className="overflow-hidden rounded-xl bg-black"></div>
                            <p className="text-center text-xs text-gray-400 mt-2">カメラへのアクセスを許可してください</p>
                            <button
                                onClick={stopScan}
                                className="w-full mt-4 bg-gray-200 text-gray-700 py-3 rounded-xl font-bold hover:bg-gray-300"
                            >
                                中止する
                            </button>
                        </div>
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
