"use client";

import { ChevronRight } from "lucide-react";

export default function MemberPage() {
    return (
        <div className="min-h-screen bg-white pb-20">
            <header className="bg-white border-b p-4 text-center sticky top-0 z-10">
                <h1 className="text-lg font-bold text-blue-600">会員証</h1>
            </header>

            <div className="p-4 bg-gray-50 min-h-[calc(100vh-60px)]">
                {/* Member Card */}
                <div className="bg-blue-600 rounded-2xl p-6 text-white shadow-lg mb-6 relative overflow-hidden">
                    <div className="flex justify-between items-start mb-8">
                        <div>
                            <p className="text-blue-100 text-sm mb-1">Zoff Scope Member</p>
                            <h2 className="text-2xl font-bold tracking-wide">TARO YAMADA</h2>
                        </div>
                        <div className="border border-white/50 rounded-full px-3 py-1 text-xs">
                            Regular
                        </div>
                    </div>

                    <div className="bg-white rounded-lg p-4 text-center">
                        <p className="text-gray-800 font-mono text-xl tracking-widest">1234 5678 9012</p>
                    </div>
                </div>

                {/* Menu List */}
                <div className="bg-white rounded-xl shadow-sm overflow-hidden">
                    <MenuItem label="購入履歴" />
                    <div className="border-t border-gray-100"></div>
                    <MenuItem label="視力・処方箋データ" />
                    <div className="border-t border-gray-100"></div>
                    <MenuItem label="お気に入りスタッフ" />
                </div>
            </div>
        </div>
    );
}

function MenuItem({ label }: { label: string }) {
    return (
        <div className="flex justify-between items-center p-4 hover:bg-gray-50 cursor-pointer">
            <span className="text-gray-800">{label}</span>
            <ChevronRight className="w-5 h-5 text-gray-300" />
        </div>
    );
}
