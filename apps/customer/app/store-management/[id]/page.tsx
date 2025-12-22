'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Users, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { fetchStoreStaff, fetchStore, Staff, Store } from '../../../lib/api';
import { getTagBadgeStyle } from '../../../lib/tagUtils';

export default function StaffSelectionPage() {
    const params = useParams();
    const router = useRouter();
    const [staffList, setStaffList] = useState<Staff[]>([]);
    const [store, setStore] = useState<Store | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!params.id) return;

        const loadData = async () => {
            try {
                const [staffData, storeData] = await Promise.all([
                    fetchStoreStaff(Number(params.id)),
                    fetchStore(Number(params.id))
                ]);
                setStaffList(staffData);
                setStore(storeData);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        loadData();
    }, [params.id]);

    const handleStaffSelect = (staffId: number) => {
        // スタッフを選択したら、サービスモード画面に遷移
        router.push(`/store-management/${params.id}/service?staffId=${staffId}`);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 font-sans text-gray-800">
            <header className="bg-white border-b border-gray-200 p-6 sticky top-0 z-10 shadow-sm">
                <div className="max-w-6xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <Link
                            href="/store-management"
                            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm font-semibold flex items-center"
                        >
                            <ArrowLeft className="w-4 h-4 mr-2" />
                            店舗選択に戻る
                        </Link>
                    </div>

                    {store && (
                        <div className="text-right">
                            <p className="text-sm text-gray-500 mb-1">店舗ダッシュボード</p>
                            <h1 className="text-2xl font-bold text-gray-800">{store.name}</h1>
                        </div>
                    )}
                </div>
            </header>

            <main className="p-6 max-w-6xl mx-auto">
                {/* ヘッダーセクション */}
                <div className="text-center mb-12 mt-8">
                    <div className="inline-flex items-center justify-center w-20 h-20 bg-blue-500 rounded-full mb-6 shadow-lg">
                        <Users className="w-10 h-10 text-white" />
                    </div>
                    <h2 className="text-4xl font-bold text-gray-800 mb-3">
                        担当スタッフを選択してください
                    </h2>
                    <p className="text-gray-600 text-lg">
                        あなたの名前をタップしてログインします
                    </p>
                </div>

                {loading ? (
                    <div className="text-center py-20">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
                        <p className="mt-4 text-gray-500">読み込み中...</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                        {staffList.map(staff => (
                            <button
                                key={staff.id}
                                onClick={() => handleStaffSelect(staff.id)}
                                className="bg-white p-6 rounded-2xl border-2 border-gray-200 shadow-sm hover:shadow-xl hover:border-blue-500 hover:-translate-y-1 transition-all group"
                            >
                                {/* スタッフ画像 */}
                                <div className="w-24 h-24 mx-auto rounded-full overflow-hidden bg-gradient-to-br from-blue-100 to-blue-200 mb-4 border-4 border-white shadow-md group-hover:shadow-lg transition-shadow">
                                    {/* eslint-disable-next-line @next/next/no-img-element */}
                                    <img
                                        src={staff.image_url || "/images/staff/default.jpg"}
                                        alt={staff.display_name}
                                        className="w-full h-full object-cover group-hover:scale-110 transition-transform"
                                        onError={(e) => { e.currentTarget.src = "/globe.svg"; }}
                                    />
                                </div>

                                {/* スタッフ名 */}
                                <h3 className="font-bold text-xl text-gray-800 mb-1 truncate">
                                    {staff.display_name}
                                </h3>

                                {/* 役職 */}
                                <p className="text-sm text-gray-500 mb-3">
                                    {staff.role || 'スタッフ'}
                                </p>

                                {/* タグ */}
                                <div className="flex flex-wrap gap-1.5 justify-center min-h-[60px]">
                                    {(staff.tags || []).slice(0, 6).map(tag => (
                                        <span
                                            key={tag.id}
                                            className={`text-[10px] px-2 py-1 rounded-full border ${getTagBadgeStyle(tag.id)}`}
                                        >
                                            {tag.name}
                                        </span>
                                    ))}
                                    {(staff.tags || []).length > 6 && (
                                        <span className="text-[10px] text-gray-400 self-center">
                                            +{(staff.tags || []).length - 6}
                                        </span>
                                    )}
                                </div>

                                {/* ホバー時の選択インジケーター */}
                                <div className="mt-4 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <span className="inline-block bg-blue-500 text-white text-sm font-bold px-4 py-2 rounded-full">
                                        選択
                                    </span>
                                </div>
                            </button>
                        ))}
                    </div>
                )}

                {/* スタッフがいない場合 */}
                {!loading && staffList.length === 0 && (
                    <div className="text-center py-20">
                        <div className="inline-flex items-center justify-center w-20 h-20 bg-gray-100 rounded-full mb-4">
                            <Users className="w-10 h-10 text-gray-400" />
                        </div>
                        <p className="text-gray-500 text-lg">この店舗にはスタッフが登録されていません</p>
                    </div>
                )}
            </main>
        </div>
    );
}
