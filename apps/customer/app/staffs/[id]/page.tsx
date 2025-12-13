'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { Staff, fetchStaff } from '../../../lib/api';
import { getTagBadgeStyle } from '../../../lib/tagUtils';
import { Star, ChevronLeft, MapPin, BadgeCheck } from 'lucide-react';

export default function StaffProfilePage() {
    const params = useParams();
    const router = useRouter();
    const [staff, setStaff] = useState<Staff | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadStaff = async () => {
            if (params.id) {
                try {
                    const data = await fetchStaff(Number(params.id));
                    setStaff(data);
                } catch (error) {
                    console.error('Failed to fetch staff:', error);
                } finally {
                    setLoading(false);
                }
            }
        };
        loadStaff();
    }, [params.id]);

    if (loading) return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-gray-500">読み込み中...</div>;
    if (!staff) return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-gray-500">スタッフが見つかりません</div>;

    return (
        <main className="min-h-screen bg-gray-50 pb-24 font-sans text-gray-800">
            {/* Header / Navigation */}
            <div className="fixed top-0 left-0 right-0 z-20 flex justify-between items-center p-4 bg-transparent via-transparent to-transparent">
                <button
                    onClick={() => router.back()}
                    className="w-10 h-10 bg-white/80 backdrop-blur-sm rounded-full flex items-center justify-center shadow-sm hover:bg-white transition-colors"
                >
                    <ChevronLeft className="w-6 h-6 text-gray-700" />
                </button>
            </div>

            {/* Hero Image Section */}
            <div className="relative w-full aspect-[3/4] bg-gray-200">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                    src={staff.image_url || "/images/staff/default.jpg"}
                    alt={staff.display_name || staff.name}
                    className="w-full h-full object-cover"
                    onError={(e) => { e.currentTarget.src = "/globe.svg"; }}
                />
                <div className="absolute inset-x-0 bottom-0 h-32 bg-gradient-to-t from-white to-transparent" />
            </div>

            {/* Profile Content */}
            <div className="relative px-5 -mt-10">
                <div className="bg-white rounded-2xl p-6 shadow-xl border border-gray-100">
                    {/* Name & Role */}
                    <div className="text-center mb-6">
                        <div className="flex items-center justify-center gap-2 mb-1">
                            <h1 className="text-2xl font-bold text-gray-900">{staff.display_name || staff.name}</h1>
                            <span className="bg-yellow-100 text-yellow-700 text-[10px] px-2 py-0.5 rounded-full font-bold flex items-center gap-1 border border-yellow-200">
                                <Star className="w-3 h-3 fill-current" /> 95
                            </span>
                        </div>
                        <p className="text-sm text-gray-500 font-medium tracking-wide">スタッフ</p>
                        <p className="text-xs text-gray-400 mt-1 flex items-center justify-center gap-1">
                            <MapPin className="w-3 h-3" /> Zoff {staff.store?.name}
                        </p>
                    </div>

                    {/* Tags */}
                    <div className="flex flex-wrap gap-2 justify-center mb-8">
                        {staff.tags?.map(tag => (
                            <span key={tag.id} className={`px-3 py-1.5 rounded-full text-xs font-bold border ${getTagBadgeStyle(tag.id)}`}>
                                #{tag.name}
                            </span>
                        ))}
                    </div>

                    {/* Personal Content Section */}
                    <div className="border-t border-gray-100 pt-6">
                        <div className="flex items-center gap-2 mb-4">
                            <div className="w-1 h-6 bg-[#00A0E9] rounded-full"></div>
                            <h2 className="text-lg font-bold text-gray-800">Personal Content</h2>
                        </div>

                        <div className="space-y-4 text-sm text-gray-600 leading-relaxed">
                            <div className="flex items-start gap-3">
                                <BadgeCheck className="w-5 h-5 text-[#00A0E9] shrink-0 mt-0.5" />
                                <div>
                                    <p className="font-bold text-gray-700 mb-1">基本情報</p>
                                    <p>神奈川県出身 | 販売歴6年目</p>
                                </div>
                            </div>

                            <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100 text-gray-700">
                                <p>
                                    「メガネ選びをもっと楽しく、ハッピーに！」をモットーに接客しています。
                                    似合うメガネがわからない、という方はぜひご相談ください。
                                    顔タイプ診断やパーソナルカラーに基づいた提案が得意です👓✨
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Fixed Bottom Button */}
            <div className="fixed bottom-0 left-0 right-0 p-4 bg-white border-t border-gray-100 shadow-[0_-5px_20px_rgba(0,0,0,0.05)]">
                <Link
                    href={`/reservation/staff/${staff.id}`}
                    className="block w-full max-w-md mx-auto bg-[#00A0E9] text-white font-bold py-4 rounded-xl text-center shadow-lg shadow-blue-200 hover:bg-[#008bc9] transition-all active:scale-[0.98]"
                >
                    このスタッフを指名して予約
                </Link>
            </div>
        </main>
    );
}
