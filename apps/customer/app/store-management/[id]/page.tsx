'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Users, Eye, ArrowRight, UserCircle } from 'lucide-react';
import { fetchStoreStaff, Staff } from '../../../lib/api';

export default function StoreDashboard() {
    const params = useParams(); // params.id is store id
    const [staffList, setStaffList] = useState<Staff[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!params.id) return;
        const loadStaff = async () => {
            try {
                const data = await fetchStoreStaff(Number(params.id));
                setStaffList(data);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        loadStaff();
    }, [params.id]);

    return (

        <div className="min-h-screen bg-slate-100 font-sans text-gray-800">
            <header className="bg-slate-800 border-b border-gray-700 p-4 sticky top-0 z-10 flex justify-between items-center shadow-lg">

                <div className="flex items-center gap-2">
                    <Link href="/store-management" className="text-gray-400 hover:text-white font-bold text-sm transition-colors">← 店舗選択</Link>
                    <span className="text-gray-600">|</span>
                    <h1 className="text-lg font-bold text-white tracking-wide">店舗ダッシュボード (v5)</h1>
                </div>
            </header>

            <main className="p-6 max-w-4xl mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                    {/* Service Mode Card */}
                    <Link
                        href={`/store-management/${params.id}/service`}
                        className="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1 flex flex-col justify-between h-48"
                    >
                        <div>
                            <Eye className="w-10 h-10 mb-4 opacity-80" />
                            <h2 className="text-2xl font-bold">Service Mode</h2>
                            <p className="text-blue-100 mt-1">接客・カルテ・視力データ確認</p>
                        </div>
                        <div className="flex justify-end">
                            <span className="bg-white/20 px-4 py-2 rounded-full text-sm font-bold flex items-center backdrop-blur-sm">
                                開く <ArrowRight className="w-4 h-4 ml-1" />
                            </span>
                        </div>
                    </Link>

                    {/* Other potential dashboard items */}
                    <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm flex flex-col justify-center items-center text-gray-400">
                        <span className="text-sm">本日の予約数</span>
                        <span className="text-4xl font-bold text-gray-700">12</span>
                    </div>
                </div>

                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                    <Users className="w-5 h-5 mr-2 text-blue-600" />
                    所属スタッフ一覧
                </h2>

                {loading ? (
                    <div className="text-center py-10 text-gray-500">読み込み中...</div>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                        {staffList.map(staff => (
                            <Link
                                key={staff.id}
                                href={`/store-management/${params.id}/staff/${staff.id}`}
                                className="bg-white p-4 rounded-xl border border-[#00A0E9] shadow-sm hover:shadow-md transition-all flex items-center gap-4 group"
                            >
                                <div className="w-16 h-16 rounded-full overflow-hidden bg-gray-100 flex-shrink-0 border border-gray-100">
                                    {/* eslint-disable-next-line @next/next/no-img-element */}
                                    <img
                                        src={staff.image_url || "/images/staff/default.jpg"}
                                        alt={staff.display_name}
                                        className="w-full h-full object-cover group-hover:scale-110 transition-transform"
                                        onError={(e) => { e.currentTarget.src = "/globe.svg"; }}
                                    />
                                </div>
                                <div className="flex-1 min-w-0">

                                    <h3 className="font-bold text-gray-800 truncate">{staff.display_name}</h3>
                                    <p className="text-xs text-gray-500 mb-1">{staff.role || 'Staff'}</p>
                                    <div className="flex flex-wrap gap-1 mt-1">
                                        {/* Mock Tags matching image */}
                                        <span className="text-[10px] bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full border border-blue-200">#フィッティング</span>
                                        <span className="text-[10px] bg-orange-50 text-orange-600 px-2 py-0.5 rounded-full border border-orange-200">#色彩検定</span>
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}
