'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import {
    Users,
    Clock,
    Calendar,
    ChevronLeft,
    ChevronRight,
    Search,
    Edit3,
    Settings,
    History,
    Hand,
    ArrowRightLeft,
    CheckCircle2,
    MessageSquare,
    Phone,
    MapPin,
    Smartphone,
    FileText, // Added
    Shield // Added
} from 'lucide-react';

// --- Types ---
type StatusType = 'Check-in' | 'Reservation' | 'Reservation_Nomination';

interface Note {
    id: number;
    content: string;
    date: string;
    author: string;
}

interface Purchase {
    date: string;
    model: string;
    type: string;
}

interface Customer {
    id: number;
    name: string;
    kana: string;
    profile: string; // e.g. "30代男性 会社員 / 東京都在住"
    time: string;
    status: StatusType;
    assignedStaff: string | 'Unassigned';
    isNew: boolean;
    lastVisit?: string;
    vision: {
        date: string;
        r: string;
        l: string;
    };
    ecActivity?: {
        model: string;
        date: string;
        adviceSent: boolean;
        // Search Detail Mock Data
        lensName: string;
        warrantyDate: string;
        price: string;
        prescription: {
            pd: string;
            r: { sph: string; cyl: string; axis: string; add: string; v: string; };
            l: { sph: string; cyl: string; axis: string; add: string; v: string; };
        };
    };
    notes: Note[];
    // HR Interaction Metrics (Mocking real-time state)
    raisedHands: number; // "I want to take this"
    passesRequested: number; // "Help me"
}

// --- Mock Data ---
const MOCK_CUSTOMERS: Customer[] = [
    {
        id: 1,
        name: '山田 太郎',
        kana: 'ヤマダ タロウ',
        profile: '30代男性 会社員 / 東京都在住',
        time: '14:00',
        status: 'Reservation_Nomination',
        assignedStaff: 'あなた',
        isNew: false,
        lastVisit: '2025/11/10',
        vision: {
            date: '2024/11/10',
            r: 'S -3.25',
            l: 'S -3.00'
        },
        ecActivity: {
            model: 'Zoff SMART Skinny',
            date: '2025/11/25',
            adviceSent: false,
            lensName: 'Z-155S(A)',
            warrantyDate: '2026/06/07',
            price: '0円',
            prescription: {
                pd: '61.0',
                r: { sph: '-3.00', cyl: '-0.50', axis: '180', add: '', v: '1.2' },
                l: { sph: '-2.75', cyl: '-0.50', axis: '170', add: '', v: '1.2' }
            }
        },
        notes: [
            { id: 101, content: '前回のフィッティング時に「耳のあたりが痛くなりやすい」との相談あり。テンプルの調整を緩めに設定済み。今回はPC作業用のブルーライトカットを検討中。', date: '2025/11/10', author: 'あなた' }
        ],
        raisedHands: 1,
        passesRequested: 0,
    },
    {
        id: 2,
        name: '佐藤 花子',
        kana: 'サトウ ハナコ',
        profile: '20代女性 学生 / 神奈川県在住',
        time: '14:30',
        status: 'Reservation',
        assignedStaff: 'Unassigned',
        isNew: true,
        vision: { date: '-', r: '-', l: '-' },
        notes: [],
        raisedHands: 3, // Many staff want to take this new customer
        passesRequested: 0,
    },
    {
        id: 3,
        name: '鈴木 一郎',
        kana: 'スズキ イチロウ',
        profile: '50代男性 自営業 / 大阪府在住',
        time: '13:45',
        status: 'Check-in',
        assignedStaff: 'Unassigned',
        isNew: false,
        lastVisit: '2025/10/01',
        vision: { date: '2025/10/01', r: 'S -1.00', l: 'S -1.25' },
        notes: [
            { id: 102, content: '予備のメガネを探している', date: '2025/10/01', author: '田中' }
        ],
        raisedHands: 0,
        passesRequested: 2, // Needs help
    }
];

export default function StoreServiceMode() {
    const params = useParams();
    const [activeTab, setActiveTab] = useState<'list' | 'history' | 'memo' | 'settings'>('list');
    const [viewMode, setViewMode] = useState<'list' | 'detail' | 'order_detail'>('list');
    const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);
    const [filterMyCustomers, setFilterMyCustomers] = useState(false);

    // Interactions
    const [interactionStats, setInteractionStats] = useState<{ raised: number, passed: number }>({ raised: 12, passed: 5 });

    const handleCustomerClick = (customer: Customer) => {
        setSelectedCustomer(customer);
        setViewMode('detail');
    };

    const handleBack = () => {
        if (viewMode === 'order_detail') {
            setViewMode('detail');
        } else {
            setViewMode('list');
            setSelectedCustomer(null);
        }
    };

    const handleRaiseHand = () => {
        alert('「手を挙げました！」\n積極性が評価されました (+1 Point)');
        setInteractionStats(prev => ({ ...prev, raised: prev.raised + 1 }));
    };

    const handlePassRequest = () => {
        alert('「パス（ヘルプ）を出しました」\nチームワーク連携が記録されました');
        setInteractionStats(prev => ({ ...prev, passed: prev.passed + 1 }));
    };

    // Filter Logic
    const displayCustomers = filterMyCustomers
        ? MOCK_CUSTOMERS.filter(c => c.assignedStaff === 'あなた')
        : MOCK_CUSTOMERS;

    return (
        <div className="min-h-screen bg-gray-50 font-sans text-gray-800 pb-20 relative">

            {/* --- Header --- */}
            <header className="fixed top-0 left-0 right-0 bg-[#00A0E9] text-white p-4 shadow-md z-30 h-16 flex items-center justify-between">
                {viewMode !== 'list' ? (
                    <button onClick={handleBack} className="flex items-center text-sm font-bold">
                        <ChevronLeft className="w-5 h-5 mr-1" />
                        戻る
                    </button>
                ) : (
                    <h1 className="text-lg font-bold">Scope Studio App</h1>
                )}

                {/* Global Stats / Notification */}
                <div className="flex items-center gap-3">
                    <div className="flex flex-col items-end text-[10px] leading-tight opacity-90">
                        <span>Hands: {interactionStats.raised}</span>
                        <span>Passes: {interactionStats.passed}</span>
                    </div>
                    <div className="bg-white text-[#00A0E9] rounded-full px-2 py-0.5 text-xs font-bold shadow">
                        3件
                    </div>
                </div>
            </header>

            {/* --- Main Content --- */}
            <main className="pt-20 px-4">

                {viewMode === 'list' && (
                    <div className="space-y-4">
                        {/* Filter Toggle */}
                        <div className="flex justify-end mb-2">
                            <button
                                onClick={() => setFilterMyCustomers(!filterMyCustomers)}
                                className={`text-xs px-3 py-1 rounded-full border ${filterMyCustomers ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-500 border-blue-200'}`}
                            >
                                {filterMyCustomers ? '自分の指名のみ' : '全員を表示'}
                            </button>
                        </div>

                        {displayCustomers.map(customer => (
                            <div
                                key={customer.id}
                                onClick={() => handleCustomerClick(customer)}
                                className="bg-white rounded-xl shadow-sm border border-blue-200 overflow-hidden active:scale-[0.99] transition-transform"
                            >
                                <div className="p-4 border-b border-blue-100 flex justify-between items-start">
                                    <div>
                                        <div className="flex items-center gap-2 mb-1">
                                            <span className="text-sm font-bold text-gray-500">{customer.time}</span>
                                            <span className={`text-xs px-2 py-0.5 rounded font-bold 
                                                ${customer.status === 'Reservation_Nomination' ? 'bg-blue-50 text-blue-700' :
                                                    customer.status === 'Reservation' ? 'bg-gray-100 text-gray-600' :
                                                        'bg-green-100 text-green-700'}`}>
                                                {customer.status === 'Reservation_Nomination' ? '予約 (指名)' :
                                                    customer.status === 'Reservation' ? '予約' : '来店中'}
                                            </span>
                                        </div>
                                        <h2 className="text-xl font-bold text-blue-900">{customer.name} <span className="text-sm font-normal text-gray-400">様</span></h2>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-xs text-blue-500 font-bold mb-1">
                                            {customer.assignedStaff === 'あなた' ? '担当: あなた' :
                                                customer.isNew ? '新規' : ''}
                                        </p>
                                    </div>
                                </div>
                                <div className="px-4 py-2 bg-blue-50/30 flex justify-between items-center text-xs text-gray-500">
                                    <span>{customer.profile}</span>
                                    <ChevronRight className="w-4 h-4 text-blue-300" />
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {viewMode === 'detail' && selectedCustomer && (
                    <div className="space-y-6 pb-24">
                        {/* Basic Info Card */}
                        <div className="bg-white rounded-xl shadow-sm border border-blue-200 p-5">
                            <div className="flex justify-between items-start mb-2">
                                <div>
                                    <h2 className="text-2xl font-bold text-blue-900">{selectedCustomer.name} <span className="text-lg font-normal">様</span></h2>
                                    <p className="text-sm text-gray-500 mt-1">{selectedCustomer.profile}</p>
                                </div>
                                <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded font-bold">
                                    {selectedCustomer.status === 'Check-in' ? '来店中' : '予約'}
                                </span>
                            </div>
                        </div>

                        {/* Interaction Actions (The "Raise Hand / Pass" Feature) */}
                        <div className="grid grid-cols-2 gap-4">
                            <button
                                onClick={handleRaiseHand}
                                className="bg-white border-2 border-[#FF9200] text-[#FF9200] rounded-xl p-3 flex flex-col items-center justify-center gap-1 active:bg-orange-50 transition-colors"
                            >
                                <Hand className="w-6 h-6" />
                                <span className="text-xs font-bold">手を挙げる (Join)</span>
                            </button>
                            <button
                                onClick={handlePassRequest}
                                className="bg-white border-2 border-[#5CC035] text-[#5CC035] rounded-xl p-3 flex flex-col items-center justify-center gap-1 active:bg-green-50 transition-colors"
                            >
                                <ArrowRightLeft className="w-6 h-6" />
                                <span className="text-xs font-bold">パス / Help</span>
                            </button>
                        </div>

                        {/* Vision Data */}
                        <div className="bg-white rounded-xl shadow-sm border border-blue-200 overflow-hidden">
                            <div className="bg-blue-50/50 px-4 py-3 border-b border-blue-100 flex justify-between items-center">
                                <h3 className="font-bold text-sm text-blue-800">VISION DATA</h3>
                                <span className="text-xs text-gray-400">最新: {selectedCustomer.vision.date}</span>
                            </div>
                            <div className="p-4 space-y-3">
                                <div className="flex items-center justify-between border-b border-blue-100 pb-2">
                                    <span className="font-bold text-xl text-gray-400 w-8">R</span>
                                    <span className="font-bold text-gray-800">{selectedCustomer.vision.r}</span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <span className="font-bold text-xl text-gray-400 w-8">L</span>
                                    <span className="font-bold text-gray-800">{selectedCustomer.vision.l}</span>
                                </div>
                            </div>
                        </div>

                        {/* EC Activity */}
                        {selectedCustomer.ecActivity && (
                            <div className="bg-white rounded-xl shadow-sm border-2 border-[#00A0E9] overflow-hidden">
                                <div className="px-4 py-3 bg-blue-50 border-b border-blue-100 flex items-center gap-2">
                                    <Smartphone className="w-4 h-4 text-blue-500" />
                                    <h3 className="font-bold text-sm text-blue-600">EC ACTIVITY (購入履歴)</h3>
                                </div>
                                <div className="p-4">
                                    <p className="text-xs text-gray-600 mb-3">お客様がECサイトで商品を購入しました。来店時にフィッティングの具合を確認してください。</p>
                                    <div className="bg-gray-100 rounded-lg p-3 flex items-center gap-4 mb-4">
                                        <div className="w-12 h-8 bg-gray-300 rounded flex-shrink-0"></div>
                                        <div>
                                            <p className="text-sm font-bold text-gray-800">{selectedCustomer.ecActivity.model}</p>
                                            <p className="text-xs text-gray-500">購入日: {selectedCustomer.ecActivity.date}</p>
                                        </div>
                                    </div>
                                    <button
                                        onClick={() => setViewMode('order_detail')}
                                        className="w-full bg-[#00A0E9] text-white font-bold py-3 rounded-lg shadow-sm active:bg-blue-600"
                                    >
                                        購入履歴詳細を見る
                                    </button>
                                </div>
                            </div>
                        )}

                        {/* Staff Memo (Read Only) */}
                        <div className="bg-white rounded-xl shadow-sm border border-blue-200">
                            <div className="bg-blue-50/50 px-4 py-3 border-b border-blue-100">
                                <h3 className="font-bold text-sm text-blue-800">STAFF MEMO (History)</h3>
                            </div>
                            <div className="p-4 space-y-4">
                                {selectedCustomer.notes.length > 0 ? selectedCustomer.notes.map(note => (
                                    <div key={note.id} className="text-sm text-gray-700">
                                        <p className="mb-1 leading-relaxed">{note.content}</p>
                                        <p className="text-xs text-gray-400 text-right">- {note.author} ({note.date})</p>
                                    </div>
                                )) : (
                                    <p className="text-sm text-gray-400">メモはありません</p>
                                )}
                            </div>
                        </div>

                    </div>
                )}

                {viewMode === 'order_detail' && selectedCustomer && selectedCustomer.ecActivity && (
                    <div className="bg-white min-h-[80vh] pb-24">
                        <div className="text-center py-4 border-b border-blue-200">
                            <h2 className="text-[#00A0E9] font-bold text-xl italic">Zoff</h2>
                        </div>

                        {/* Lens Info */}
                        <div className="p-4">
                            <h3 className="text-[#00A0E9] font-bold text-lg text-center mb-4">レンズ</h3>

                            <div className="mb-6">
                                <div className="text-sm text-gray-600 mb-1">レンズ(R) : {selectedCustomer.ecActivity.lensName}</div>
                                <div className="text-sm text-gray-600 mb-2">保証期間 : {selectedCustomer.ecActivity.warrantyDate}</div>
                                <div className="bg-gray-50 p-3 flex justify-between items-center rounded text-sm mb-4">
                                    <span>合計金額</span>
                                    <span>{selectedCustomer.ecActivity.price}</span>
                                </div>

                                <div className="text-sm text-gray-600 mb-1">レンズ(L) : {selectedCustomer.ecActivity.lensName}</div>
                                <div className="text-sm text-gray-600 mb-2">保証期間 : {selectedCustomer.ecActivity.warrantyDate}</div>
                                <div className="bg-gray-50 p-3 flex justify-between items-center rounded text-sm">
                                    <span>合計金額</span>
                                    <span>{selectedCustomer.ecActivity.price}</span>
                                </div>
                            </div>

                            <hr className="border-blue-100 my-6" />

                            {/* Warranty */}
                            <h3 className="text-[#00A0E9] font-bold text-lg text-center mb-4">保証内容</h3>
                            <div className="bg-gray-50 p-4 rounded text-sm text-gray-700 mb-4">
                                <p>フレーム・サングラス・パッケージ商品保証</p>
                                <p>レンズ度数保証</p>
                            </div>
                            <div className="text-center mb-8">
                                <button className="text-[#00A0E9] text-sm hover:underline">詳細な保証内容はこちら</button>
                            </div>

                            <hr className="border-blue-100 my-6" />

                            {/* Degree Check */}
                            <h3 className="text-[#00A0E9] font-bold text-lg text-center mb-4">度数確認</h3>
                            <div className="border border-blue-200 rounded overflow-hidden text-center text-sm">
                                <div className="grid grid-cols-3 border-b border-blue-200 bg-gray-50 font-bold text-gray-600">
                                    <div className="py-2 border-r border-blue-200"></div>
                                    <div className="py-2 border-r border-blue-200">R (右目)</div>
                                    <div className="py-2">L (左目)</div>
                                </div>
                                <div className="grid grid-cols-3 border-b border-blue-200">
                                    <div className="py-2 border-r border-blue-200 bg-gray-50 font-medium">PD</div>
                                    <div className="py-2 col-span-2">{selectedCustomer.ecActivity.prescription.pd}</div>
                                </div>
                                {[
                                    { label: 'SPH', r: selectedCustomer.ecActivity.prescription.r.sph, l: selectedCustomer.ecActivity.prescription.l.sph },
                                    { label: 'CYL', r: selectedCustomer.ecActivity.prescription.r.cyl, l: selectedCustomer.ecActivity.prescription.l.cyl },
                                    { label: 'AXIS', r: selectedCustomer.ecActivity.prescription.r.axis, l: selectedCustomer.ecActivity.prescription.l.axis },
                                    { label: 'ADD', r: selectedCustomer.ecActivity.prescription.r.add, l: selectedCustomer.ecActivity.prescription.l.add },
                                ].map(row => (
                                    <div key={row.label} className="grid grid-cols-3 border-b border-blue-200">
                                        <div className="py-2 border-r border-blue-200 bg-gray-50 font-medium">{row.label}</div>
                                        <div className="py-2 border-r border-blue-200">{row.r}</div>
                                        <div className="py-2">{row.l}</div>
                                    </div>
                                ))}
                                <div className="grid grid-cols-3">
                                    <div className="py-2 border-r border-blue-200 bg-gray-50 font-medium">V</div>
                                    <div className="py-2 col-span-2">
                                        {selectedCustomer.ecActivity.prescription.r.v} R=L
                                    </div>
                                </div>
                            </div>

                            <div className="mt-8 text-center">
                                <h3 className="text-[#00A0E9] font-bold text-lg mb-2">取扱説明書について</h3>
                                <p className="text-xs text-gray-600 text-left mb-4 leading-relaxed">
                                    環境保全活動の推進のため、ご注文商品への取扱説明書の別添は行っておりません。<br />
                                    ご注文商品の取扱説明書は、以下のリンクからご確認いただけます。
                                </p>
                                <button className="text-[#00A0E9] text-sm hover:underline mb-8">取扱説明書はこちら</button>

                                <button onClick={() => setViewMode('detail')} className="border border-[#00A0E9] text-[#00A0E9] rounded-full px-8 py-3 w-full font-bold mb-4">
                                    前のページに戻る
                                </button>
                                <button onClick={() => setViewMode('list')} className="bg-[#00A0E9] text-white rounded-full px-8 py-3 w-full font-bold">
                                    マイページTOPへ
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                {/* --- Memo Entry View --- */}
                {activeTab === 'memo' && (
                    <div className="bg-white rounded-xl shadow-lg border border-blue-200 p-6 min-h-[400px]">
                        <h2 className="text-lg font-bold text-blue-800 mb-4 flex items-center gap-2">
                            <Edit3 className="w-5 h-5" /> メモ記入
                        </h2>
                        <div className="mb-4">
                            <label className="block text-xs font-bold text-gray-500 mb-1">お客様ID / 名前</label>
                            <div className="flex gap-2">
                                <input type="text" placeholder="ID or Name search" className="flex-1 border border-blue-200 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none" />
                                <button className="bg-blue-50 p-2 rounded-lg text-blue-600"><Search className="w-4 h-4" /></button>
                            </div>
                        </div>
                        <div className="mb-4">
                            <label className="block text-xs font-bold text-gray-500 mb-1">メモ内容</label>
                            <textarea
                                className="w-full h-40 border border-blue-200 rounded-lg p-3 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none"
                                placeholder="接客内容や気付いた点を記入してください..."
                            ></textarea>
                        </div>
                        <button className="w-full bg-[#00A0E9] text-white font-bold py-3 rounded-lg shadow-md active:bg-blue-600 transition-colors">
                            保存する (Save)
                        </button>
                        <p className="text-xs text-gray-400 mt-2 text-center">※ どのお客様のメモでも記入可能です</p>
                    </div>
                )}

            </main>

            {/* --- Bottom Navigation --- */}
            <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-blue-200 h-16 flex justify-around items-center z-40 pb-safe">
                <button
                    onClick={() => { setActiveTab('list'); setViewMode('list'); }}
                    className={`flex flex-col items-center justify-center w-full h-full ${activeTab === 'list' ? 'text-[#00A0E9]' : 'text-gray-400'}`}
                >
                    <Users className="w-6 h-6 mb-1" />
                    <span className="text-[10px] font-bold">指名リスト</span>
                </button>
                <button
                    onClick={() => setActiveTab('history')}
                    className={`flex flex-col items-center justify-center w-full h-full ${activeTab === 'history' ? 'text-[#00A0E9]' : 'text-gray-400'}`}
                >
                    <History className="w-6 h-6 mb-1" />
                    <span className="text-[10px] font-bold">接客履歴</span>
                </button>
                <button
                    onClick={() => setActiveTab('memo')}
                    className={`flex flex-col items-center justify-center w-full h-full ${activeTab === 'memo' ? 'text-[#00A0E9]' : 'text-gray-400'}`}
                >
                    <Edit3 className="w-6 h-6 mb-1" />
                    <span className="text-[10px] font-bold">メモ記入</span>
                </button>
                <button
                    onClick={() => setActiveTab('settings')}
                    className={`flex flex-col items-center justify-center w-full h-full ${activeTab === 'settings' ? 'text-[#00A0E9]' : 'text-gray-400'}`}
                >
                    <Settings className="w-6 h-6 mb-1" />
                    <span className="text-[10px] font-bold">設定</span>
                </button>
            </nav>
        </div>
    );
}
