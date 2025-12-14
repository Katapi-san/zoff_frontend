'use client';

import { QRCodeSVG } from 'qrcode.react';
import { ChevronLeft } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function MemberPage() {
    const router = useRouter();
    // メンバーシップID（ダミー）
    const memberId = "ZOFF-MEMBER-123456789";

    return (
        <div className="bg-gray-100 min-h-screen pb-20">
            <header className="bg-blue-600 text-white p-4 text-center font-bold text-lg sticky top-0 z-10 flex items-center justify-center relative">
                <button
                    onClick={() => router.push('/')}
                    className="absolute left-4 p-1 hover:bg-blue-700 rounded"
                >
                    <ChevronLeft className="w-6 h-6" />
                </button>
                Zoff Scope
            </header>

            <main className="p-6 max-w-md mx-auto">
                <h1 className="text-2xl font-bold text-gray-800 mb-6 text-center">会員証</h1>

                <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 flex flex-col items-center">
                    <div className="mb-2 text-gray-500 font-bold">Zoff Scope Member</div>
                    <div className="mb-6 text-2xl font-bold text-[#00A0E9]">YAMADA TARO</div>

                    <div className="bg-white p-4 border-4 border-gray-800 rounded-xl mb-6">
                        <QRCodeSVG value={memberId} size={200} />
                    </div>

                    <p className="text-gray-400 text-sm break-all font-mono">{memberId}</p>
                    <p className="text-xs text-gray-400 mt-4 text-center">
                        店舗でこの会員証をご提示ください。<br />
                        ポイントやお買い上げ履歴が確認できます。
                    </p>
                </div>
            </main>
        </div>
    );
}
