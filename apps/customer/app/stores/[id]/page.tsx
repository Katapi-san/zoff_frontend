'use client';

import { useEffect, useState, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Store, Staff, fetchStore, fetchStoreStaff } from '../../../lib/api';
import { getTagBadgeStyle } from '../../../lib/tagUtils';
import { Star, ChevronRight, MapPin, ChevronLeft } from 'lucide-react';
import Link from 'next/link';

export default function StoreDetailPage() {
    const params = useParams();
    const router = useRouter();
    const [store, setStore] = useState<Store | null>(null);
    const [staffList, setStaffList] = useState<Staff[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedMenuId, setSelectedMenuId] = useState<number | null>(null);
    const [nominationType, setNominationType] = useState<'none' | 'nominated' | null>(null);
    const staffListRef = useRef<HTMLDivElement>(null); // Ref for scrolling
    const nominationSectionRef = useRef<HTMLDivElement>(null); // Ref for scrolling to nomination choice

    const MENU_ITEMS = [
        { id: 1, name: 'メガネの作成・相談', duration: 60 },
        { id: 2, name: 'レンズ交換', duration: 30 },
        { id: 3, name: '調整・メンテナンス', duration: 15 },
    ];

    const handleNoNomination = () => {
        if (!selectedMenuId) {
            alert('メニューを選択してください');
            return;
        }
        router.push(`/stores/${params.id}/queue?menuId=${selectedMenuId}`);
    };

    const handleNomination = () => {
        if (!selectedMenuId) {
            alert('メニューを選択してください');
            return;
        }
        setNominationType('nominated');
    };

    // Auto-scroll to nomination section when menu is selected
    useEffect(() => {
        if (selectedMenuId && nominationSectionRef.current) {
            // Use setTimeout to allow UI update
            setTimeout(() => {
                nominationSectionRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
        }
    }, [selectedMenuId]);

    useEffect(() => {
        const loadData = async () => {
            if (params.id) {
                try {
                    const storeId = Number(params.id);
                    // Use fetchStoreStaff to reduce payload size for mobile devices
                    const [storeData, storeStaffData] = await Promise.all([
                        fetchStore(storeId),
                        fetchStoreStaff(storeId)
                    ]);
                    setStore(storeData);

                    // API returns filtered staff, so we use it directly
                    const storeStaff = storeStaffData;

                    // Deduplication logic
                    const mergedStaffMap = new Map<string, Staff>();
                    storeStaff.forEach(s => {
                        const key = s.name;
                        if (!mergedStaffMap.has(key)) {
                            mergedStaffMap.set(key, { ...s, tags: s.tags ? [...s.tags] : [] });
                        } else {
                            const existing = mergedStaffMap.get(key)!;
                            if (s.tags) {
                                const existingTagIds = new Set((existing.tags || []).map(t => t.id));
                                s.tags.forEach(t => {
                                    if (!existingTagIds.has(t.id)) {
                                        existing.tags!.push(t);
                                        existingTagIds.add(t.id);
                                    }
                                });
                            }
                            if (!existing.image_url && s.image_url) {
                                existing.image_url = s.image_url;
                            }
                        }
                    });

                    const uniqueStoreStaff = Array.from(mergedStaffMap.values());
                    setStaffList(uniqueStoreStaff);
                } catch (error) {
                    console.error('Failed to fetch data:', error);
                } finally {
                    setLoading(false);
                }
            }
        };
        loadData();
    }, [params.id]);

    useEffect(() => {
        if (nominationType === 'nominated' && staffListRef.current) {
            // Use setTimeout to ensure the DOM has updated
            setTimeout(() => {
                staffListRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 150);
        }
    }, [nominationType]);

    if (loading) return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-gray-500">読み込み中...</div>;
    if (!store) return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-gray-500">店舗が見つかりません</div>;

    return (
        <div className="bg-gray-100 min-h-screen pb-32">
            <header className="bg-blue-600 text-white p-4 text-center font-bold text-lg sticky top-0 z-10 flex items-center justify-center relative shadow-sm">
                <button
                    onClick={() => router.push('/stores')}
                    className="absolute left-4 p-1 hover:bg-blue-700 rounded transition-colors"
                >
                    <ChevronLeft className="w-6 h-6" />
                </button>
                Zoff Scope
            </header>

            <main className="p-4 max-w-md mx-auto space-y-6">
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                    <h2 className="text-xl font-bold text-gray-800 mb-2">Zoff {store.name}</h2>
                    <p className="text-gray-500 text-sm mb-4 flex items-start gap-1">
                        <MapPin className="w-4 h-4 mt-0.5 shrink-0" />
                        {store.address}
                    </p>
                    <div className="flex space-x-2">
                        {store.phone_number && (
                            <a href={`tel:${store.phone_number}`} className="bg-blue-50 text-blue-600 px-3 py-1.5 rounded-lg text-sm font-bold flex items-center gap-1 hover:bg-blue-100 transition-colors">
                                📞 電話する
                            </a>
                        )}
                        <a
                            href={`https://www.google.com/maps/search/?api=1&query=Zoff ${store.name}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="bg-gray-100 text-gray-600 px-3 py-1.5 rounded-lg text-sm font-bold flex items-center gap-1 hover:bg-gray-200 transition-colors"
                        >
                            📍 地図を見る
                        </a>
                    </div>
                </div>

                {/* Section 1: Menu Selection */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <h3 className="font-bold text-gray-800 mb-4 text-lg flex items-center gap-2">
                        <span className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">1</span>
                        ご希望のメニュー
                    </h3>
                    <div className="space-y-3">
                        {MENU_ITEMS.map(item => (
                            <button
                                key={item.id}
                                onClick={() => setSelectedMenuId(item.id)}
                                className={`w-full flex justify-between items-center p-4 rounded-xl border transition-all ${selectedMenuId === item.id
                                    ? 'border-blue-500 bg-blue-50 ring-1 ring-blue-500'
                                    : 'border-gray-200 hover:bg-gray-50'
                                    }`}
                            >
                                <span className="font-medium text-gray-700">{item.name}</span>
                                <span className="bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded font-medium">{item.duration}分</span>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Section 2: Nomination Choice */}
                <div ref={nominationSectionRef} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 scroll-mt-24">
                    <h3 className="font-bold text-gray-800 mb-4 text-lg flex items-center gap-2">
                        <span className={`w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold text-white transition-colors ${selectedMenuId ? 'bg-blue-600' : 'bg-gray-300'}`}>2</span>
                        スタッフ指名
                    </h3>

                    <div className="space-y-3">
                        {/* A: No Nomination */}
                        <button
                            onClick={handleNoNomination}
                            disabled={!selectedMenuId}
                            className={`w-full p-4 rounded-xl border-2 transition-all text-left relative overflow-hidden group ${!selectedMenuId
                                ? 'border-gray-100 bg-gray-50 opacity-60 cursor-not-allowed'
                                : 'border-green-500 bg-white hover:bg-green-50'
                                }`}
                        >
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-white shrink-0 ${!selectedMenuId ? 'bg-gray-300' : 'bg-green-500'}`}>A</div>
                                    <div>
                                        <p className="font-bold text-gray-800">指名なし (最短)</p>
                                        <p className="text-xs text-gray-500">空いているスタッフが対応します</p>
                                    </div>
                                </div>
                                <div className={`flex items-center gap-1 text-sm font-bold ${!selectedMenuId ? 'text-gray-400' : 'text-green-600'}`}>
                                    <span className={`w-3 h-3 rounded-full ${!selectedMenuId ? 'bg-gray-300' : 'bg-green-500'}`}></span>
                                    5分待ち
                                </div>
                            </div>
                        </button>

                        {/* B: With Nomination */}
                        <button
                            onClick={handleNomination}
                            disabled={!selectedMenuId}
                            className={`w-full p-4 rounded-xl border-2 transition-all text-left relative overflow-hidden group ${!selectedMenuId
                                ? 'border-gray-100 bg-gray-50 opacity-60 cursor-not-allowed'
                                : nominationType === 'nominated'
                                    ? 'border-orange-500 bg-orange-50 ring-2 ring-orange-200'
                                    : 'border-orange-400 bg-white hover:bg-orange-50'
                                }`}
                        >
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-white shrink-0 ${!selectedMenuId ? 'bg-gray-300' : 'bg-orange-500'}`}>B</div>
                                    <div>
                                        <p className="font-bold text-gray-800">スタッフ指名</p>
                                        <p className="text-xs text-gray-500">一覧からスタッフを選択します</p>
                                    </div>
                                </div>
                                <div className={`flex items-center gap-1 text-sm font-bold ${!selectedMenuId ? 'text-gray-400' : 'text-orange-600'}`}>
                                    <span className={`w-3 h-3 rounded-full ${!selectedMenuId ? 'bg-gray-300' : 'bg-orange-500'}`}></span>
                                    40分待ち
                                </div>
                            </div>
                            {/* Annotation */}
                            <p className="text-[10px] text-gray-400 text-right mt-1">※注釈あり</p>
                        </button>
                    </div>
                </div>

                {/* Section 3: Staff List (Conditional) */}
                {nominationType === 'nominated' && (
                    <div ref={staffListRef} className="scroll-mt-24 space-y-2">
                        <h3 className="font-bold text-gray-800 mb-4 text-lg flex items-center gap-2">
                            <span className="w-1 h-6 bg-blue-600 rounded-full"></span>
                            只今の出勤スタッフ
                        </h3>

                        <div className="space-y-4">
                            {staffList.length === 0 ? (
                                <p className="text-gray-400 text-center py-8 bg-white rounded-xl border border-gray-100">出勤スタッフ情報はありません</p>
                            ) : (
                                staffList.map((staff, index) => (
                                    <div
                                        key={`${staff.id}-${index}`}
                                        onClick={() => router.push(`/staffs/${staff.id}?menuId=${selectedMenuId}`)}
                                        className="border border-[#00A0E9] rounded-xl p-4 shadow-sm bg-white cursor-pointer hover:bg-gray-50 transition-colors active:scale-[0.99]"
                                    >
                                        <div className="flex items-center justify-between mb-3">
                                            <div className="flex items-center space-x-4">
                                                <div className="relative flex-shrink-0">
                                                    <div className="w-16 h-16 bg-gray-200 rounded-full overflow-hidden border border-gray-100">
                                                        {/* eslint-disable-next-line @next/next/no-img-element */}
                                                        {staff.image_url ? (
                                                            <img src={staff.image_url} alt={staff.display_name || staff.name} className="w-full h-full object-cover" />
                                                        ) : (
                                                            <div className="w-full h-full bg-gray-300 flex items-center justify-center text-gray-500 text-xs">No Img</div>
                                                        )}
                                                    </div>
                                                    <div className="absolute -bottom-1 -right-1 bg-yellow-400 rounded-full p-1 border-2 border-white shadow-sm">
                                                        <Star className="w-3 h-3 text-white fill-current" />
                                                    </div>
                                                </div>
                                                <div>
                                                    <div className="flex items-center gap-2 mb-1">
                                                        <h3 className="font-bold text-gray-800 text-lg">{staff.display_name || staff.name}</h3>
                                                        {/* Show store name as requested */}
                                                        <span className="text-[10px] text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded">Zoff {store.name}</span>
                                                    </div>
                                                    <p className="text-xs text-gray-500">{staff.role || "スタッフ"}</p>
                                                </div>
                                            </div>
                                            <ChevronRight className="w-5 h-5 text-gray-300" />
                                        </div>

                                        {/* Tag Area: Independent Row, up to 10 tags */}
                                        <div className="flex flex-wrap gap-1.5 pl-1 border-t border-gray-50 pt-2 mt-1">
                                            {staff.tags && staff.tags.slice(0, 10).map((t: any) => (
                                                <span key={t.id} className={`text-[10px] px-2.5 py-1 rounded-full border ${getTagBadgeStyle(t.id)}`}>
                                                    {t.name}
                                                </span>
                                            ))}
                                            {(staff.tags || []).length > 10 && (
                                                <span className="text-[10px] text-gray-400 self-center">+{(staff.tags || []).length - 10}</span>
                                            )}
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}
