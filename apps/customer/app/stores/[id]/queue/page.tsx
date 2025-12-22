'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { CheckCircle, Clock, Users } from 'lucide-react';

export default function QueueCompletePage() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const menuId = searchParams.get('menuId');

    // Mock data based on menuId if needed
    const ticketNumber = Math.floor(Math.random() * 899) + 100; // Random 100-999

    return (
        <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6 text-center font-sans">
            <div className="mb-8 animate-in fade-in zoom-in duration-500">
                <CheckCircle className="w-24 h-24 text-green-500 mx-auto" />
            </div>

            <h1 className="text-2xl font-bold text-gray-800 mb-2">受付いたしました</h1>
            <p className="text-gray-500 mb-8">スタッフがお呼びするまで<br />店内でお待ちください。</p>

            <div className="bg-blue-50 rounded-2xl p-8 w-full max-w-sm mb-8 border border-blue-100 shadow-sm relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-2 bg-blue-500"></div>

                <p className="text-sm font-bold text-gray-500 mb-2">受付番号</p>
                <p className="text-6xl font-black text-blue-600 mb-6 tracking-widest">{ticketNumber}</p>

                <div className="flex justify-between items-center border-t border-blue-100 pt-4">
                    <div className="flex items-center gap-2">
                        <Users className="w-5 h-5 text-gray-400" />
                        <div className="text-left">
                            <p className="text-xs text-gray-400 font-bold">待ち組数</p>
                            <p className="font-bold text-gray-700">3組</p>
                        </div>
                    </div>
                    <div className="w-px h-8 bg-blue-200"></div>
                    <div className="flex items-center gap-2">
                        <Clock className="w-5 h-5 text-gray-400" />
                        <div className="text-left">
                            <p className="text-xs text-gray-400 font-bold">予想待ち時間</p>
                            <p className="font-bold text-gray-700">約 15分</p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="space-y-4 w-full max-w-sm">
                <button
                    onClick={() => router.push('/')}
                    className="w-full bg-gray-100 text-gray-600 font-bold py-3 px-6 rounded-xl hover:bg-gray-200 transition"
                >
                    トップへ戻る
                </button>
            </div>
        </div>
    );
}
