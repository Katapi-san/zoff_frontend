'use client';

import React, { useEffect, useState, Suspense } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { CheckCircle } from 'lucide-react';
import liff from '@line/liff';

interface Profile {
    userId: string;
    displayName: string;
    pictureUrl?: string;
    statusMessage?: string;
}

function ReservationCompleteContent() {
    const searchParams = useSearchParams();
    const staffName = searchParams.get('staffName');
    const storeName = searchParams.get('storeName');
    const date = searchParams.get('date');
    const time = searchParams.get('time');
    const menuName = searchParams.get('menuName');

    const [profile, setProfile] = useState<Profile | null>(null);

    useEffect(() => {
        const initializeLiff = async () => {
            // Avoid LIFF init on external browsers to prevent console warnings
            const isLineApp = /Line/i.test(navigator.userAgent);
            if (!isLineApp) return;

            try {
                // APIからLIFF IDを取得
                const res = await fetch('/api/liff-id');
                const data = await res.json();
                const runtimeLiffId = data.liffId;

                if (!runtimeLiffId) {
                    console.warn('LIFF_ID is not defined in runtime environment.');
                    return;
                }

                // LIFF初期化
                await liff.init({ liffId: runtimeLiffId });

                if (liff.isLoggedIn()) {
                    const userProfile = await liff.getProfile();
                    setProfile(userProfile);
                }
            } catch (e) {
                console.error('LIFF Initialization failed', e);
            }
        };

        initializeLiff();
    }, []);

    return (
        <div className="min-h-screen bg-white flex flex-col items-center justify-center px-6 pt-12 pb-32 text-center">
            <div className="mb-6">
                <CheckCircle className="w-24 h-24 text-green-500" />
            </div>

            <h1 className="text-2xl font-bold text-gray-800 mb-4">ご予約ありがとうございました</h1>

            {/* LINEプロフィール表示エリア */}
            {profile && (
                <div className="flex flex-col items-center mb-6">
                    {profile.pictureUrl && (
                        <img
                            src={profile.pictureUrl}
                            alt={profile.displayName}
                            className="w-16 h-16 rounded-full border-2 border-gray-100 mb-2"
                        />
                    )}
                    <p className="text-gray-700 font-bold">{profile.displayName} 様</p>
                </div>
            )}

            <p className="text-gray-600 mb-8">
                以下の内容で予約を承りました。<br />
                当日お会いできるのを楽しみにしております。
            </p>

            <div className="bg-gray-50 rounded-xl p-6 w-full max-w-sm mb-8 text-left border border-gray-100 shadow-sm">
                <div className="mb-4">
                    <p className="text-xs text-gray-500 mb-1">予約メニュー</p>
                    <p className="font-bold text-lg text-gray-800">{menuName || 'メニュー未選択'}</p>
                </div>
                <div className="mb-4">
                    <p className="text-xs text-gray-500 mb-1">指名スタッフ</p>
                    <p className="font-bold text-lg text-gray-800">{staffName} さん</p>
                </div>
                <div className="mb-4">
                    <p className="text-xs text-gray-500 mb-1">ご来店日時</p>
                    <p className="font-bold text-lg text-gray-800">
                        {date && `12月${date}日`} {time}
                    </p>
                </div>
                <div>
                    <p className="text-xs text-gray-500 mb-1">店舗</p>
                    <p className="font-bold text-gray-800">{storeName || 'Zoff 店舗'}</p>
                </div>
            </div>

            <Link
                href="/"
                className="bg-blue-600 text-white font-bold py-3 px-10 rounded-full hover:bg-blue-700 transition shadow-md w-full max-w-sm"
            >
                トップに戻る
            </Link>
        </div>
    );
}

export default function ReservationCompletePage() {
    return (
        <Suspense fallback={<div className="min-h-screen flex items-center justify-center">Loading...</div>}>
            <ReservationCompleteContent />
        </Suspense>
    );
}
