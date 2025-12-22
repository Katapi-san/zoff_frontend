'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';
import { ChevronLeft, Bell, AlertCircle, Calendar, Clock } from 'lucide-react';
import Link from 'next/link';

interface Notice {
    id: number;
    title: string;
    content: string;
    priority: 'high' | 'medium' | 'low';
    date: string;
    category: 'store' | 'staff' | 'system' | 'customer';
}

export default function NoticesPage() {
    const params = useParams();

    // サンプルの連絡事項データ
    const [notices] = useState<Notice[]>([
        {
            id: 1,
            title: '新商品入荷のお知らせ',
            content: '春夏新作フレームが本日入荷しました。トレンドカラーの展示をお願いします。',
            priority: 'high',
            date: '2025-12-17 09:00',
            category: 'store'
        },
        {
            id: 2,
            title: '営業時間変更',
            content: '12/25-12/31は年末営業となり、営業時間が11:00-20:00に変更となります。',
            priority: 'high',
            date: '2025-12-16 14:30',
            category: 'store'
        },
        {
            id: 3,
            title: 'システムメンテナンス',
            content: '本日22:00-23:00までPOSシステムのメンテナンスを実施します。',
            priority: 'medium',
            date: '2025-12-17 08:00',
            category: 'system'
        },
        {
            id: 4,
            title: 'スタッフミーティング',
            content: '明日18:00からスタッフミーティングを実施します。参加必須です。',
            priority: 'medium',
            date: '2025-12-16 17:00',
            category: 'staff'
        },
        {
            id: 5,
            title: '顧客満足度調査',
            content: '今月の顧客満足度調査の結果が公開されました。店長までご確認ください。',
            priority: 'low',
            date: '2025-12-15 10:00',
            category: 'customer'
        },
    ]);

    const getPriorityStyle = (priority: string) => {
        switch (priority) {
            case 'high':
                return 'bg-red-50 border-red-200 text-red-700';
            case 'medium':
                return 'bg-orange-50 border-orange-200 text-orange-700';
            case 'low':
                return 'bg-blue-50 border-blue-200 text-blue-700';
            default:
                return 'bg-gray-50 border-gray-200 text-gray-700';
        }
    };

    const getPriorityLabel = (priority: string) => {
        switch (priority) {
            case 'high':
                return '重要';
            case 'medium':
                return '通常';
            case 'low':
                return '参考';
            default:
                return '';
        }
    };

    const getCategoryIcon = (category: string) => {
        switch (category) {
            case 'store':
                return '🏪';
            case 'staff':
                return '👥';
            case 'system':
                return '⚙️';
            case 'customer':
                return '😊';
            default:
                return '📢';
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 font-sans">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 p-6 sticky top-0 z-10 shadow-sm">
                <div className="max-w-4xl mx-auto flex items-center gap-4">
                    <Link
                        href={`/store-management/${params.id}`}
                        className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm font-semibold flex items-center"
                    >
                        <ChevronLeft className="w-4 h-4 mr-2" />
                        戻る
                    </Link>
                    <div className="flex items-center gap-3 flex-1">
                        <Bell className="w-6 h-6 text-blue-600" />
                        <h1 className="text-2xl font-bold text-gray-800">連絡事項</h1>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="p-6 max-w-4xl mx-auto">
                {/* Summary Stats */}
                <div className="grid grid-cols-3 gap-4 mb-6">
                    <div className="bg-white rounded-xl p-4 text-center shadow-sm border border-red-100">
                        <div className="text-3xl font-bold text-red-600 mb-1">
                            {notices.filter(n => n.priority === 'high').length}
                        </div>
                        <div className="text-xs text-gray-500">重要</div>
                    </div>
                    <div className="bg-white rounded-xl p-4 text-center shadow-sm border border-orange-100">
                        <div className="text-3xl font-bold text-orange-600 mb-1">
                            {notices.filter(n => n.priority === 'medium').length}
                        </div>
                        <div className="text-xs text-gray-500">通常</div>
                    </div>
                    <div className="bg-white rounded-xl p-4 text-center shadow-sm border border-blue-100">
                        <div className="text-3xl font-bold text-blue-600 mb-1">
                            {notices.filter(n => n.priority === 'low').length}
                        </div>
                        <div className="text-xs text-gray-500">参考</div>
                    </div>
                </div>

                {/* Notices List */}
                <div className="space-y-4">
                    {notices.map(notice => (
                        <div
                            key={notice.id}
                            className={`rounded-xl p-5 border-2 ${getPriorityStyle(notice.priority)} shadow-sm hover:shadow-md transition-shadow`}
                        >
                            <div className="flex items-start justify-between mb-3">
                                <div className="flex items-center gap-2">
                                    <span className="text-2xl">{getCategoryIcon(notice.category)}</span>
                                    <div>
                                        <h3 className="font-bold text-lg text-gray-800">{notice.title}</h3>
                                        <div className="flex items-center gap-2 mt-1">
                                            <span className={`text-xs px-2 py-1 rounded-full font-bold border ${getPriorityStyle(notice.priority)}`}>
                                                {getPriorityLabel(notice.priority)}
                                            </span>
                                            <span className="text-xs text-gray-500 flex items-center gap-1">
                                                <Clock className="w-3 h-3" />
                                                {notice.date}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <p className="text-gray-700 leading-relaxed">
                                {notice.content}
                            </p>
                        </div>
                    ))}
                </div>

                {/* Empty State */}
                {notices.length === 0 && (
                    <div className="text-center py-20">
                        <Bell className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <p className="text-gray-500">新しい連絡事項はありません</p>
                    </div>
                )}
            </main>
        </div>
    );
}
