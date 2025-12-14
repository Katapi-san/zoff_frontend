'use client';

import { useState, useEffect } from 'react';
import { Store, fetchStores } from '../../lib/api';
import { QRCodeSVG } from 'qrcode.react';

// Reusing Region mapping for consistency
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

export default function QrGeneratorPage() {
    const [stores, setStores] = useState<Store[]>([]);
    const [selectedRegion, setSelectedRegion] = useState<string>("");
    const [selectedPrefecture, setSelectedPrefecture] = useState<string>("");
    const [selectedStore, setSelectedStore] = useState<Store | null>(null);

    useEffect(() => {
        async function loadStores() {
            try {
                const data = await fetchStores();
                setStores(data);
            } catch (e) {
                console.error(e);
            }
        }
        loadStores();
    }, []);

    // Filter logic
    const availablePrefectures = selectedRegion ? REGION_MAPPING[selectedRegion] : [];

    const filteredStores = stores.filter(s => {
        if (selectedRegion && REGION_MAPPING[selectedRegion]) {
            if (!REGION_MAPPING[selectedRegion].includes(s.prefecture)) return false;
        }
        if (selectedPrefecture && s.prefecture !== selectedPrefecture) return false;
        return true;
    });

    const qrUrl = selectedStore ? `https://zoff-scope-frontend.azurewebsites.net/stores/${selectedStore.id}` : "";

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col items-center p-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">店舗QRコード発行</h1>

            <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-2xl border border-gray-100">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                    <div>
                        <label className="block text-sm font-bold text-gray-700 mb-2">地方</label>
                        <select
                            className="w-full p-3 border border-gray-200 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none"
                            value={selectedRegion}
                            onChange={(e) => {
                                setSelectedRegion(e.target.value);
                                setSelectedPrefecture("");
                                setSelectedStore(null);
                            }}
                        >
                            <option value="">選択してください</option>
                            {Object.keys(REGION_MAPPING).map(r => (
                                <option key={r} value={r}>{r}</option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-bold text-gray-700 mb-2">都道府県</label>
                        <select
                            className="w-full p-3 border border-gray-200 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none disabled:opacity-50"
                            value={selectedPrefecture}
                            onChange={(e) => {
                                setSelectedPrefecture(e.target.value);
                                setSelectedStore(null);
                            }}
                            disabled={!selectedRegion}
                        >
                            <option value="">選択してください</option>
                            {availablePrefectures.map(p => (
                                <option key={p} value={p}>{p}</option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="mb-8">
                    <label className="block text-sm font-bold text-gray-700 mb-2">店舗選択</label>
                    <select
                        className="w-full p-3 border border-gray-200 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none disabled:opacity-50"
                        value={selectedStore ? selectedStore.id : ""}
                        onChange={(e) => {
                            const storeId = Number(e.target.value);
                            const store = stores.find(s => s.id === storeId);
                            setSelectedStore(store || null);
                        }}
                        disabled={!selectedPrefecture}
                    >
                        <option value="">店舗を選択してください</option>
                        {filteredStores.map(store => (
                            <option key={store.id} value={store.id}>Zoff {store.name}</option>
                        ))}
                    </select>
                </div>

                {selectedStore && (
                    <div className="flex flex-col items-center justify-center p-8 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-300">
                        <div className="bg-white p-4 rounded-xl shadow-sm mb-4">
                            <QRCodeSVG
                                value={qrUrl}
                                size={250}
                                level={"H"}
                                includeMargin={true}
                            />
                        </div>
                        <h2 className="text-xl font-bold text-gray-800 mb-2">Zoff {selectedStore.name}</h2>
                        <a href={qrUrl} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline text-sm break-all font-mono">
                            {qrUrl}
                        </a>
                        <p className="mt-4 text-sm text-gray-500">
                            このQRコードを読み取ると、店舗のスタッフ一覧ページに直接アクセスします。
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
