"use client";

import { useState, useEffect } from "react";
import { Store, fetchStores, fetchStoreStaff, Staff } from "../lib/api";
import { Star } from "lucide-react";
import { useRouter } from "next/navigation";

const REGION_MAPPING: { [key: string]: string[] } = {
    "北海道": ["北海道"],
    "東北": ["青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県"],
    "関東": ["東京都", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "神奈川県"],
    "甲信越": ["新潟県", "山梨県", "長野県"],
    "北陸": ["富山県", "石川県", "福井県"],
    "東海": ["岐阜県", "静岡県", "愛知県", "三重県"],
    "近畿": ["滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県"],
    "中国": ["鳥取県", "島根県", "岡山県", "広島県", "山口県"],
    "四国": ["徳島県", "香川県", "愛媛県", "高知県"],
    "九州": ["福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県"],
    "沖縄": ["沖縄県"],
};

export default function StoreSearch() {
    const router = useRouter();
    const [stores, setStores] = useState<Store[]>([]);
    const [cities, setCities] = useState<string[]>([]);

    const [selectedRegion, setSelectedRegion] = useState<string>("");
    const [selectedPrefecture, setSelectedPrefecture] = useState<string>("");
    const [selectedCity, setSelectedCity] = useState<string>("");
    const [selectedStore, setSelectedStore] = useState<Store | null>(null);
    const [storeStaff, setStoreStaff] = useState<Staff[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadStores();
    }, []);

    async function loadStores() {
        try {
            const data = await fetchStores();
            setStores(data);
        } catch (e) {
            console.error(e);
        }
    }

    useEffect(() => {
        setSelectedPrefecture("");
        setSelectedCity("");
    }, [selectedRegion]);

    useEffect(() => {
        if (selectedPrefecture) {
            const filteredCities = Array.from(new Set(
                stores.filter(s => s.prefecture === selectedPrefecture).map(s => s.city)
            )).filter(Boolean);
            setCities(filteredCities);
            setSelectedCity("");
        } else {
            setCities([]);
        }
    }, [selectedPrefecture, stores]);

    useEffect(() => {
        if (selectedStore) {
            fetchStaff(selectedStore.id);
        }
    }, [selectedStore]);

    async function fetchStaff(storeId: number) {
        setLoading(true);
        try {
            const staff = await fetchStoreStaff(storeId);
            setStoreStaff(staff);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    }

    const filteredStores = stores.filter(s => {
        if (selectedRegion && REGION_MAPPING[selectedRegion]) {
            if (!REGION_MAPPING[selectedRegion].includes(s.prefecture)) return false;
        }
        if (selectedPrefecture && s.prefecture !== selectedPrefecture) return false;
        if (selectedCity && s.city !== selectedCity) return false;
        return true;
    });

    const availablePrefectures = selectedRegion ? REGION_MAPPING[selectedRegion] : [];

    if (selectedStore) {
        return (
            <div className="p-4">
                <button
                    onClick={() => setSelectedStore(null)}
                    className="mb-4 text-blue-600 text-sm flex items-center font-bold"
                >
                    &lt; 店舗一覧に戻る
                </button>

                <div className="bg-white rounded-xl p-6 shadow-sm mb-6 border border-gray-100">
                    <h2 className="text-xl font-bold text-gray-800 mb-2">Zoff {selectedStore.name}</h2>
                    <p className="text-gray-500 text-sm mb-4">{selectedStore.address}</p>
                    <div className="flex space-x-2">
                        {selectedStore.phone_number && (
                            <a href={`tel:${selectedStore.phone_number}`} className="bg-blue-50 text-blue-600 px-3 py-1 rounded text-sm font-bold">
                                📞 電話する
                            </a>
                        )}
                        <a
                            href={`https://www.google.com/maps/search/?api=1&query=Zoff ${selectedStore.name}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="bg-gray-100 text-gray-600 px-3 py-1 rounded text-sm font-bold"
                        >
                            📍 地図を見る
                        </a>
                    </div>
                </div>

                <h3 className="font-bold text-gray-800 mb-4 text-lg">只今の出勤スタッフ</h3>

                <div className="space-y-4">
                    {loading ? (
                        <p className="text-center text-gray-400">読み込み中...</p>
                    ) : storeStaff.length === 0 ? (
                        <p className="text-gray-400 text-center py-8 bg-gray-50 rounded-xl">出勤スタッフ情報はありません</p>
                    ) : (
                        storeStaff.map(staff => (
                            <div key={staff.id} className="border rounded-xl p-4 shadow-sm flex items-center justify-between bg-white">
                                <div className="flex items-center space-x-4">
                                    <div className="relative">
                                        <div className="w-14 h-14 bg-gray-200 rounded-full overflow-hidden border border-gray-100">
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
                                        <h3 className="font-bold text-gray-800 text-lg">{staff.display_name || staff.name}</h3>
                                        <div className="flex flex-wrap gap-1 mt-1">
                                            {staff.tags && staff.tags.slice(0, 3).map((t: any) => (
                                                <span key={t.id} className="bg-blue-50 text-blue-600 text-xs px-2 py-0.5 rounded font-bold">
                                                    {t.name}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                                <button
                                    onClick={() => router.push(`/reservation/staff/${staff.id}`)}
                                    className="border border-blue-600 text-blue-600 px-4 py-1.5 rounded-full text-sm font-bold hover:bg-blue-50 transition-colors"
                                >
                                    詳細
                                </button>
                            </div>
                        ))
                    )}
                </div>
            </div>
        );
    }

    return (
        <div className="p-4 max-w-md mx-auto bg-white min-h-screen pb-20">
            <h1 className="text-xl font-bold mb-4 text-gray-800">店舗を探す</h1>

            <div className="space-y-4 mb-6 bg-gray-50 p-4 rounded-xl">
                <select
                    className="w-full p-3 border border-gray-200 rounded-lg bg-white text-gray-700 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                    value={selectedRegion}
                    onChange={(e) => setSelectedRegion(e.target.value)}
                >
                    <option value="">地方を選択</option>
                    {Object.keys(REGION_MAPPING).map(r => (
                        <option key={r} value={r}>{r}</option>
                    ))}
                </select>

                <select
                    className="w-full p-3 border border-gray-200 rounded-lg bg-white text-gray-700 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none disabled:bg-gray-100 disabled:text-gray-400"
                    value={selectedPrefecture}
                    onChange={(e) => setSelectedPrefecture(e.target.value)}
                    disabled={!selectedRegion}
                >
                    <option value="">都道府県を選択</option>
                    {availablePrefectures.map(p => (
                        <option key={p} value={p}>{p}</option>
                    ))}
                </select>

                <select
                    className="w-full p-3 border border-gray-200 rounded-lg bg-white text-gray-700 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none disabled:bg-gray-100 disabled:text-gray-400"
                    value={selectedCity}
                    onChange={(e) => setSelectedCity(e.target.value)}
                    disabled={!selectedPrefecture}
                >
                    <option value="">市区町村を選択</option>
                    {cities.map(c => (
                        <option key={c} value={c}>{c}</option>
                    ))}
                </select>
            </div>

            <div className="space-y-4">
                {filteredStores.map(store => (
                    <div key={store.id} className="border border-gray-100 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow bg-white">
                        <h2 className="font-bold text-lg mb-1 text-gray-800">Zoff {store.name}</h2>
                        <p className="text-sm text-gray-500 mb-2">{store.address}</p>
                        <div className="flex flex-wrap gap-2 mb-4">
                            {store.opening_hours && (
                                <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                                    🕒 {store.opening_hours.split('\n')[0]}...
                                </span>
                            )}
                        </div>
                        <button
                            className="w-full bg-blue-600 text-white py-2.5 rounded-lg font-bold hover:bg-blue-700 transition-colors shadow-sm active:transform active:scale-95"
                            onClick={() => setSelectedStore(store)}
                        >
                            店舗を選択
                        </button>
                    </div>
                ))}
                {selectedPrefecture && filteredStores.length === 0 && (
                    <div className="text-center py-10">
                        <p className="text-gray-400">店舗が見つかりませんでした。</p>
                    </div>
                )}
                {!selectedPrefecture && (
                    <div className="text-center py-10">
                        <p className="text-gray-400">地域・都道府県を選択してください</p>
                    </div>
                )}
            </div>
        </div>
    );
}
