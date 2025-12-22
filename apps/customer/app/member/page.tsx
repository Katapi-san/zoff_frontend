'use client';

import { useEffect, useState } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { ChevronLeft } from 'lucide-react';
import { useRouter } from 'next/navigation';
import liff from '@line/liff';

// 環境変数からLIFF IDを取得、設定されていない場合は空文字列
const LIFF_ID = process.env.NEXT_PUBLIC_LIFF_ID || '';

interface Profile {
    userId: string;
    displayName: string;
    pictureUrl?: string;
    statusMessage?: string;
}

export default function MemberPage() {
    const router = useRouter();
    const [profile, setProfile] = useState<Profile | null>(null);
    const [error, setError] = useState<string>('');
    const [loading, setLoading] = useState(false); // 初期化はfalseにして必要なときだけロード表示

    const initializeLiff = async () => {
        setLoading(true);
        setError(''); // Clear previous errors
        try {
            // STEP 1: APIからLIFF IDを取得（ランタイム設定を取得）
            const res = await fetch('/api/liff-id', { cache: 'no-store' }); // Ensure fresh fetch
            if (!res.ok) throw new Error(`API Error: ${res.status}`);

            const data = await res.json();
            const runtimeLiffId = data.liffId;

            console.log('LIFF ID fetched:', runtimeLiffId); // Debug Log

            if (!runtimeLiffId) {
                console.warn('LIFF_ID is not defined in runtime environment.');
                setError('LIFF IDが設定されていません。システム管理者に連絡してください。(Env missing)');
                setLoading(false);
                return;
            }

            // STEP 2: LIFF初期化
            // 既に初期化されている場合はスキップするチェックを入れると安全だが、SDK仕様では再initはエラーにはならないこともあるが、念のため
            // しかしliff.idがないのでチェックできない。そのままinitする。
            await liff.init({ liffId: runtimeLiffId });

            if (!liff.isLoggedIn()) {
                // iPhoneのSafariなどで確実に元のページに戻るためにredirectUriを明示
                liff.login({ redirectUri: window.location.href });
            } else {
                const userProfile = await liff.getProfile();
                setProfile(userProfile);
            }
        } catch (e: any) {
            console.error('LIFF Initialization failed', e);
            // エラーの詳細を表示
            setError(`LINE認証エラー: ${e.message || JSON.stringify(e)}`);
        } finally {
            setLoading(false);
        }
    };



    useEffect(() => {
        // ページロード時に自動的にLIFF初期化＆ログインチェック
        initializeLiff();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // 会員ID生成（LINE IDがあればそれを利用、なければダミー）
    const memberId = profile ? `ZOFF-${profile.userId.substring(0, 8).toUpperCase()}` : "Guest";

    if (loading) {
        return (
            <div className="bg-gray-100 min-h-screen flex flex-col items-center justify-center p-4">
                <div className="bg-white p-8 rounded-2xl shadow-sm max-w-sm w-full text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent mx-auto mb-4"></div>
                    <p className="text-gray-500 font-bold">読み込み中...</p>
                    <p className="text-xs text-gray-400 mt-2">LINEアカウントを確認しています</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-gray-100 min-h-screen p-6 flex flex-col items-center justify-center">
                <div className="bg-white p-6 rounded-xl shadow-md text-center max-w-sm">
                    <h2 className="text-red-500 font-bold mb-2">エラーが発生しました</h2>
                    <p className="text-gray-700 text-sm">{error}</p>
                    <button
                        onClick={() => router.push('/')}
                        className="mt-4 px-4 py-2 bg-gray-200 rounded text-gray-700 hover:bg-gray-300"
                    >
                        トップに戻る
                    </button>
                </div>
            </div>
        );
    }

    if (!profile) {
        return (
            <div className="bg-gray-100 min-h-screen flex flex-col items-center justify-center p-4">
                <div className="bg-white p-8 rounded-2xl shadow-sm max-w-sm w-full text-center">
                    <h1 className="text-xl font-bold mb-6 text-gray-800">会員証作成</h1>
                    <p className="mb-6 text-gray-600 text-sm">
                        会員証を表示するには、<br />LINEアカウントでのログインが必要です。
                    </p>
                    <button
                        onClick={() => initializeLiff()}
                        disabled={loading}
                        className="w-full bg-[#06C755] text-white font-bold py-3 px-4 rounded-lg shadow hover:bg-[#05b34c] transition duration-200 flex items-center justify-center gap-2"
                    >
                        {loading ? '処理中...' : 'LINEでログインして会員証を作る'}
                    </button>
                    {/* 開発中のため戻るボタンも設置 */}
                    <button
                        onClick={() => router.push('/')}
                        className="mt-4 text-xs text-gray-400 underline"
                    >
                        トップに戻る
                    </button>
                </div>
            </div>
        );
    }

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

                    {/* プロフィール画像があれば表示 */}
                    {profile.pictureUrl && (
                        <img
                            src={profile.pictureUrl}
                            alt={profile.displayName}
                            className="w-16 h-16 rounded-full mb-2 border-2 border-gray-100"
                        />
                    )}

                    <div className="mb-6 text-2xl font-bold text-[#00A0E9] text-center">
                        {profile.displayName} 様
                    </div>

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
