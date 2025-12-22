'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Store, MapPin, ChevronRight, Search } from 'lucide-react';
import { fetchStores, Store as StoreType } from '../../lib/api';
import { REGIONS } from '../../lib/constants';



export default function StoreSelectPage() {
    const [stores, setStores] = useState<StoreType[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedRegion, setSelectedRegion] = useState<string | null>(null);
    const [selectedPrefecture, setSelectedPrefecture] = useState<string | null>(null);

    useEffect(() => {
        const loadStores = async () => {
            try {
                const data = await fetchStores();
                // Deduplicate stores by name to handle API duplicates
                const uniqueStores = Array.from(new Map(data.map(store => [store.name, store])).values());
                setStores(uniqueStores);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        loadStores();
    }, []);

    const filteredStores = stores.filter(store => {
        const matchesSearch = store.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (store.address && store.address.toLowerCase().includes(searchTerm.toLowerCase()));

        let matchesRegion = true;
        if (selectedPrefecture) {
            matchesRegion = (store.prefecture === selectedPrefecture) ||
                (store.address && store.address.includes(selectedPrefecture));
        } else if (selectedRegion) {
            matchesRegion = REGIONS[selectedRegion].some(pref =>
                (store.prefecture && store.prefecture.includes(pref)) ||
                (store.address && store.address.includes(pref))
            );
        }

        return matchesSearch && matchesRegion;
    });

    return (
        <div className="min-h-screen bg-gray-50 font-sans text-gray-800 pb-20">
            <header className="bg-[#00A0E9] text-white p-4 text-center font-bold text-lg sticky top-0 z-10 shadow-sm">
                Zoff Scope
            </header>

            <main className="p-4 max-w-md mx-auto">
                <div className="mb-6">
                    <h2 className="text-xl font-bold text-gray-800 mb-2">店舗を探す</h2>

                    {/* Region Filter */}
                    <div className="mb-4">
                        {/* Region Filter */}
                        <div className="overflow-x-auto pb-2 mb-2">
                            <div className="flex space-x-2 whitespace-nowrap">
                                <button
                                    onClick={() => {
                                        setSelectedRegion(null);
                                        setSelectedPrefecture(null);
                                    }}
                                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${selectedRegion === null
                                        ? 'bg-[#00A0E9] text-white'
                                        : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
                                        }`}
                                >
                                    全て
                                </button>
                                {Object.keys(REGIONS).map(region => (
                                    <button
                                        key={region}
                                        onClick={() => {
                                            if (region === selectedRegion) {
                                                setSelectedRegion(null);
                                                setSelectedPrefecture(null);
                                            } else {
                                                setSelectedRegion(region);
                                                setSelectedPrefecture(null);
                                            }
                                        }}
                                        className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${selectedRegion === region
                                            ? 'bg-[#00A0E9] text-white'
                                            : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
                                            }`}
                                    >
                                        {region}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* Prefecture Filter (shown when region is selected) */}
                        {selectedRegion && (
                            <div className="overflow-x-auto pb-2">
                                <div className="flex space-x-2 whitespace-nowrap">
                                    <button
                                        onClick={() => setSelectedPrefecture(null)}
                                        className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${selectedPrefecture === null
                                            ? 'bg-slate-600 text-white'
                                            : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
                                            }`}
                                    >
                                        全域
                                    </button>
                                    {REGIONS[selectedRegion].map(pref => (
                                        <button
                                            key={pref}
                                            onClick={() => setSelectedPrefecture(pref === selectedPrefecture ? null : pref)}
                                            className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${selectedPrefecture === pref
                                                ? 'bg-slate-600 text-white'
                                                : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
                                                }`}
                                        >
                                            {pref}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="relative mb-4">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                        <input
                            type="text"
                            placeholder="店舗名・住所で検索"
                            className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[#00A0E9] shadow-sm"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>

                    {/* Store Count */}
                    <div className="text-right text-sm text-gray-500 font-medium">
                        {loading ? '...' : `${filteredStores.length}店舗 見つかりました`}
                    </div>
                </div>

                {loading ? (
                    <div className="text-center py-10 text-gray-500">読み込み中...</div>
                ) : (
                    <div className="space-y-3">
                        {filteredStores.map(store => (
                            <Link
                                key={store.id}
                                href={`/stores/${store.id}`}
                                className="block bg-white p-4 rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-[#00A0E9] transition-all group"
                            >
                                <div className="flex justify-between items-center">
                                    <div>
                                        <h3 className="font-bold text-lg text-gray-800 group-hover:text-[#00A0E9]">Zoff {store.name}</h3>
                                        <p className="text-sm text-gray-500 flex items-center mt-1">
                                            <MapPin className="w-4 h-4 mr-1" />
                                            {store.address || '住所情報なし'}
                                        </p>
                                    </div>
                                    <ChevronRight className="text-gray-300 group-hover:text-[#00A0E9]" />
                                </div>
                            </Link>
                        ))}
                        {filteredStores.length === 0 && (
                            <div className="text-center py-10 text-gray-500">
                                条件に一致する店舗が見つかりませんでした。
                            </div>
                        )}
                    </div>
                )}
            </main>
        </div>
    );
}
