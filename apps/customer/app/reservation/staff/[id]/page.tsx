'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { ChevronLeft, MapPin } from 'lucide-react';

import { fetchStaff, Staff, Tag, Store } from '../../../../lib/api';

// Interfaces (Reuse from staff details) - REMOVED LOCALS to use shared types

// Mock Menu Data
const MENU_ITEMS = [
    { id: 1, name: 'メガネの作成・相談', duration: 60 },
    { id: 2, name: 'レンズ交換', duration: 30 },
    { id: 3, name: '調整・メンテナンス', duration: 15 },
];

// Mock Date Data
const DATES = [
    { day: '火', date: 10 },
    { day: '水', date: 11 },
    { day: '木', date: 12 },
    { day: '金', date: 13 },
    { day: '土', date: 14 },
    { day: '日', date: 15 },
];

// Mock Time Slots
const TIME_SLOTS = [
    "10:00", "11:00", "12:00", "13:00", "14:00",
    "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"
];

export default function StaffReservationPage() {
    const params = useParams(); // params.id
    const router = useRouter();
    const [staff, setStaff] = useState<Staff | null>(null);
    const [selectedMenuId, setSelectedMenuId] = useState<number | null>(null);
    const [selectedDate, setSelectedDate] = useState<number | null>(null);
    const [selectedTime, setSelectedTime] = useState<string | null>(null);

    useEffect(() => {
        if (!params.id) return;
        const loadStaff = async () => {
            try {
                const data = await fetchStaff(params.id as string);
                setStaff(data);
            } catch (e) {
                console.error("Failed to fetch staff", e);
            }
        };
        loadStaff();
    }, [params.id]);

    // Reset time when date changes
    useEffect(() => {
        setSelectedTime(null);
    }, [selectedDate]);

    if (!staff) return <div className="p-10 text-center text-gray-500">読み込み中...</div>;

    const selectedMenu = MENU_ITEMS.find(m => m.id === selectedMenuId);

    const handleReservation = () => {
        if (!staff || !selectedDate || !selectedTime) return;

        const query = new URLSearchParams({
            staffName: staff.display_name || '',
            date: selectedDate.toString(),
            time: selectedTime
        });

        router.push(`/reservation/complete?${query.toString()}`);
    };

    return (
        <div className="min-h-screen bg-gray-50 pb-32 font-sans">
            {/* Header */}
            <header className="bg-white border-b p-4 text-center sticky top-0 z-10 grid grid-cols-3 items-center">
                <button onClick={() => router.back()} className="text-blue-600 justify-self-start p-1 hover:bg-gray-50 rounded-full transition-colors">
                    <ChevronLeft size={28} strokeWidth={2.5} />
                </button>
                <h1 className="text-lg font-bold text-gray-800">指名予約</h1>
                <div></div>
            </header>

            <div className="p-4 max-w-md mx-auto space-y-6">
                {/* Staff Card */}
                <div className="bg-white p-4 rounded-xl shadow-sm flex items-start border-l-4 border-blue-600 relative overflow-hidden">
                    <div className="w-16 h-16 mr-4 rounded-full overflow-hidden bg-gray-200 flex-shrink-0 border border-gray-100">
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img
                            src={staff.image_url || "/images/staff/default.jpg"}
                            alt={staff.display_name}
                            className="object-cover w-full h-full"
                            onError={(e) => {
                                e.currentTarget.src = "/globe.svg";
                            }}
                        />
                    </div>
                    <div>
                        <h2 className="font-bold text-lg mb-1">{staff.display_name} <span className="text-sm font-normal text-gray-500">さんを指名中</span></h2>
                        <div className="flex items-center text-gray-500 text-sm mb-2">
                            <MapPin size={14} className="mr-1" />
                            {staff.store?.name || "店舗未設定"}
                        </div>
                        <div className="flex flex-wrap gap-1">
                            {(staff.tags || []).slice(0, 3).map(tag => (
                                <span key={tag.id} className="text-xs text-blue-500">#{tag.name}</span>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Section 1: Menu */}
                <div className="bg-white p-6 rounded-2xl shadow-sm">
                    <h3 className="font-bold text-lg mb-4 flex items-center text-gray-800">
                        <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm mr-2 font-bold">1</span>
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

                {/* Section 2: Date Selection */}
                <div className="bg-white p-6 rounded-2xl shadow-sm">
                    <h3 className="font-bold text-lg mb-4 flex items-center text-gray-800">
                        <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm mr-2 font-bold">2</span>
                        日時選択
                    </h3>
                    <div className="flex space-x-3 overflow-x-auto pb-4 scrollbar-hide -mx-2 px-2">
                        {DATES.map((d, i) => (
                            <button
                                key={i}
                                onClick={() => setSelectedDate(d.date)}
                                className={`flex-shrink-0 w-16 h-20 rounded-xl border flex flex-col items-center justify-center transition-all ${selectedDate === d.date
                                    ? 'bg-blue-600 text-white border-blue-600 shadow-xl transform scale-105'
                                    : 'border-gray-200 text-gray-700 hover:bg-gray-50 hover:border-gray-300'
                                    }`}
                            >
                                <span className={`text-sm mb-1 font-medium ${selectedDate === d.date ? 'text-blue-100' : 'text-gray-500'}`}>{d.day}</span>
                                <span className="text-2xl font-bold">{d.date}</span>
                            </button>
                        ))}
                        <button className="flex-shrink-0 w-16 h-20 rounded-xl border border-gray-200 border-dashed text-gray-400 flex items-center justify-center text-2xl hover:bg-gray-50">
                            +
                        </button>
                    </div>

                    {/* Time Grid - Only show if date is selected */}
                    {selectedDate && (
                        <div className="mt-6 pt-6 border-t border-gray-100 animate-in fade-in slide-in-from-top-4 duration-300">
                            <h4 className="font-bold text-gray-700 mb-3 text-sm">時間を選択してください</h4>
                            <div className="grid grid-cols-3 gap-3">
                                {TIME_SLOTS.map((time) => (
                                    <button
                                        key={time}
                                        onClick={() => setSelectedTime(time)}
                                        className={`py-2 px-1 rounded-lg text-sm font-bold border transition-all ${selectedTime === time
                                            ? 'bg-blue-600 text-white border-blue-600 shadow-md'
                                            : 'bg-white border-gray-200 text-gray-600 hover:border-blue-300 hover:text-blue-500'
                                            }`}
                                    >
                                        {time}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Sticky Footer */}
            <div className="fixed bottom-0 left-0 right-0 bg-white border-t p-4 shadow-[0_-5px_10px_rgba(0,0,0,0.05)] z-[60]">
                <div className="max-w-md mx-auto flex items-center justify-between">
                    <div>
                        <div className="text-gray-500 text-sm font-medium">
                            {selectedDate && selectedTime ? `12月${selectedDate}日(火) ${selectedTime}` : '日時未選択'}
                        </div>
                        <div className={`font-bold transition-all ${selectedMenu ? 'text-blue-600 text-md' : 'text-blue-500 text-sm animate-pulse'}`}>
                            {selectedMenu ? selectedMenu.name : 'メニューを選択してください'}
                        </div>
                    </div>
                    <button
                        disabled={!selectedMenu || !selectedDate || !selectedTime}
                        className={`px-8 py-3 rounded-full font-bold text-white shadow-lg transition-all transform ${(!selectedMenu || !selectedDate || !selectedTime)
                            ? 'bg-blue-300 cursor-not-allowed'
                            : 'bg-blue-600 hover:bg-blue-700 active:scale-95 shadow-blue-200'
                            }`}
                        onClick={handleReservation}
                    >
                        予約する
                    </button>
                </div>
            </div>
        </div>
    );
}
