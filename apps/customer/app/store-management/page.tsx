'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Store, MapPin, ChevronRight, Search } from 'lucide-react';
import { fetchStores, Store as StoreType } from '../../lib/api';

export default function StoreSelectPage() {
    const [stores, setStores] = useState<StoreType[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const loadStores = async () => {
            try {
                // Assuming fetchStores can be called without args or I'll filter client side
                const data = await fetchStores();
                setStores(data);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        loadStores();
    }, []);

    const filteredStores = stores.filter(store =>
        store.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (store.address && store.address.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    return (

        <div className="min-h-screen bg-slate-100 font-sans text-gray-800">
            <header className="bg-slate-800 border-b border-gray-700 p-4 sticky top-0 z-10 flex justify-between items-center shadow-lg">
                <div className="flex items-center gap-2">
                    <div className="bg-white/10 p-2 rounded-lg text-white backdrop-blur-sm">
                        <Store className="w-6 h-6 text-[#00A0E9]" />
                    </div>
                    <h1 className="text-xl font-bold text-white tracking-wide">
                        Zoff Scope <span className="text-[#00A0E9]">Store</span>
                    </h1>
                </div>
            </header>

            <main className="p-6 max-w-2xl mx-auto">
                <div className="mb-6">
                    <h2 className="text-2xl font-bold text-gray-800 mb-2">店舗を選択してください</h2>
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                        <input
                            type="text"
                            placeholder="店舗名・住所で検索"
                            className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>

                {loading ? (
                    <div className="text-center py-10 text-gray-500">読み込み中...</div>
                ) : (
                    <div className="space-y-3">
                        {filteredStores.map(store => (
                            <Link
                                key={store.id}
                                href={`/store-management/${store.id}`}
                                className="block bg-white p-4 rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-blue-400 transition-all group"
                            >
                                <div className="flex justify-between items-center">
                                    <div>
                                        <h3 className="font-bold text-lg text-gray-800 group-hover:text-blue-600">{store.name}</h3>
                                        <p className="text-sm text-gray-500 flex items-center mt-1">
                                            <MapPin className="w-4 h-4 mr-1" />
                                            {store.address || '住所情報なし'}
                                        </p>
                                    </div>
                                    <ChevronRight className="text-gray-300 group-hover:text-blue-500" />
                                </div>
                            </Link>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}
