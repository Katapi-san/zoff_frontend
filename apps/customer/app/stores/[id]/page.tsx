'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Store, Staff, fetchStore, fetchAllStaff } from '../../../lib/api';
import { getTagBadgeStyle } from '../../../lib/tagUtils';
import { Star, ChevronRight, MapPin, ChevronLeft } from 'lucide-react';
import Link from 'next/link';

export default function StoreDetailPage() {
    const params = useParams();
    const router = useRouter();
    const [store, setStore] = useState<Store | null>(null);
    const [staffList, setStaffList] = useState<Staff[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            if (params.id) {

                try {
                    const storeId = Number(params.id);
                    // Use fetchAllStaff and filter client-side to ensure reliability
                    const [storeData, allStaffData] = await Promise.all([
                        fetchStore(storeId),
                        fetchAllStaff()
                    ]);
                    setStore(storeData);



                    // Filter staff by store_id or store.id with robust type casting
                    const storeStaff = allStaffData.filter(staff => {
                        const staffStoreId = staff.store_id ? Number(staff.store_id) : null;
                        const nestedStoreId = staff.store && staff.store.id ? Number(staff.store.id) : null;
                        return staffStoreId === storeId || nestedStoreId === storeId;
                    });


                    console.log(`Store ${storeId}: Found ${storeStaff.length} staff from ${allStaffData.length} total records.`);


                    // Aggressive Deduplication & Merge Logic
                    // The backend seems to return multiple rows for the same staff with split tags.
                    // We group by Name and Merge tags.
                    const mergedStaffMap = new Map<string, Staff>();

                    storeStaff.forEach(s => {
                        const key = s.name; // Group by name
                        if (!mergedStaffMap.has(key)) {
                            // Initialize with a clone of tags to allow mutation
                            mergedStaffMap.set(key, { ...s, tags: s.tags ? [...s.tags] : [] });
                        } else {
                            const existing = mergedStaffMap.get(key)!;
                            // Merge tags: Add only new ones
                            if (s.tags) {
                                const existingTagIds = new Set((existing.tags || []).map(t => t.id));
                                s.tags.forEach(t => {
                                    if (!existingTagIds.has(t.id)) {
                                        existing.tags!.push(t);
                                        existingTagIds.add(t.id);
                                    }
                                });
                            }
                            // Merge fields: Fill in missing image_url if current has one and existing doesn't
                            if (!existing.image_url && s.image_url) {
                                existing.image_url = s.image_url;
                            }
                        }
                    });

                    const uniqueStoreStaff = Array.from(mergedStaffMap.values());

                    console.log(`Merged ${storeStaff.length} raw entries into ${uniqueStoreStaff.length} unique profiles.`);
                    setStaffList(uniqueStoreStaff);

                    console.log(`Final Unique Staff: ${uniqueStoreStaff.length}`);
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

    if (loading) return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-gray-500">読み込み中...</div>;
    if (!store) return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-gray-500">店舗が見つかりません</div>;

    return (
        <div className="bg-gray-100 min-h-screen pb-20">
            <header className="bg-blue-600 text-white p-4 text-center font-bold text-lg sticky top-0 z-10 flex items-center justify-center relative shadow-sm">
                <button
                    onClick={() => router.push('/stores')}
                    className="absolute left-4 p-1 hover:bg-blue-700 rounded transition-colors"
                >
                    <ChevronLeft className="w-6 h-6" />
                </button>
                Zoff Scope
            </header>

            <main className="p-4 max-w-md mx-auto">
                <div className="bg-white rounded-xl p-6 shadow-sm mb-6 border border-gray-100">
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

                <h3 className="font-bold text-gray-800 mb-4 text-lg flex items-center gap-2">
                    <div className="w-1 h-6 bg-blue-600 rounded-full"></div>
                    只今の出勤スタッフ
                </h3>

                <div className="space-y-4">
                    {staffList.length === 0 ? (
                        <p className="text-gray-400 text-center py-8 bg-white rounded-xl border border-gray-100">出勤スタッフ情報はありません</p>
                    ) : (

                        staffList.map((staff, index) => (
                            <div
                                key={`${staff.id}-${index}`}
                                onClick={() => router.push(`/staffs/${staff.id}`)}
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
            </main>
        </div>
    );
}
