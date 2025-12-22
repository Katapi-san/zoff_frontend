'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { Staff, fetchStaff } from '../../../lib/api';
import { getTagBadgeStyle, getTagActiveStyle } from '../../../lib/tagUtils';
import { Star, ChevronLeft, MapPin, BadgeCheck } from 'lucide-react';

export default function StaffProfilePage() {
    const params = useParams();
    const router = useRouter();
    const searchParams = useSearchParams();
    const menuId = searchParams.get('menuId');
    const [staff, setStaff] = useState<Staff | null>(null);
    const [loading, setLoading] = useState(true);
    const [selectedTags, setSelectedTags] = useState<number[]>([]);

    const toggleTag = (tagId: number) => {
        setSelectedTags(prev =>
            prev.includes(tagId)
                ? prev.filter(id => id !== tagId)
                : [...prev, tagId]
        );
    };

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
        <main className="min-h-screen bg-gray-50 pb-40 font-sans text-gray-800">
            {/* Header / Navigation */}
            <div className="fixed top-0 left-0 right-0 z-20 flex items-center p-4 bg-transparent via-transparent to-transparent">
                <button
                    onClick={() => router.back()}
                    className="w-10 h-10 bg-white/80 backdrop-blur-sm rounded-full flex items-center justify-center shadow-sm hover:bg-white transition-colors"
                >
                    <ChevronLeft className="w-6 h-6 text-gray-700" />
                </button>
            </div>


            {/* New Compact Header Section */}
            <div className="pt-20 px-5 pb-6 bg-white border-b border-gray-100">
                <div className="flex gap-4">
                    {/* Left: Photo */}
                    <div className="shrink-0 w-20 h-28 rounded-lg overflow-hidden shadow-md border border-gray-100">
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img
                            src={staff.image_url || "/images/staff/default.jpg"}
                            alt={staff.display_name || staff.name}
                            className="w-full h-full object-cover"
                            onError={(e) => { e.currentTarget.src = "/globe.svg"; }}
                        />
                    </div>

                    {/* Right: Info */}
                    <div className="flex-1 flex flex-col justify-center">
                        <div className="flex items-center gap-2 mb-1">
                            <h1 className="text-xl font-bold text-gray-900">{staff.display_name || staff.name}</h1>
                            <span className="bg-yellow-100 text-yellow-700 text-[10px] px-2 py-0.5 rounded-full font-bold flex items-center gap-1 border border-yellow-200">
                                <Star className="w-3 h-3 fill-current" /> 95
                            </span>
                        </div>
                        <p className="text-sm text-gray-500 font-medium tracking-wide mb-1">スタッフ</p>
                        <p className="text-xs text-gray-400 flex items-center gap-1">
                            <MapPin className="w-3 h-3" /> Zoff {staff.store?.name}
                        </p>

                        {/* Social / Extra Info Placeholders like reference */}
                        <div className="flex gap-2 mt-3">
                            <span className="text-[10px] bg-gray-100 text-gray-500 px-2 py-1 rounded"># {staff.role || "販売スタッフ"}</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Profile Content Body */}
            <div className="relative px-5 pt-6">
                <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">


                    {/* Tags */}
                    <div className="mb-8 text-center p-6 border-2 border-[#00A0E9] rounded-2xl bg-blue-50/30">
                        <p className="text-sm font-bold text-gray-700 mb-4">気に入ったタグにチェックしてください</p>
                        <div className="flex flex-wrap gap-2 justify-center">
                            {staff.tags?.map(tag => {
                                const isSelected = selectedTags.includes(tag.id);
                                return (
                                    <button
                                        key={tag.id}
                                        onClick={() => toggleTag(tag.id)}
                                        className={`px-3 py-1.5 rounded-full text-xs font-bold border transition-colors ${isSelected
                                            ? getTagActiveStyle(tag.id)
                                            : `${getTagBadgeStyle(tag.id)} hover:opacity-80`
                                            }`}
                                    >
                                        #{tag.name}
                                        {isSelected && <span className="ml-1 inline-block">✓</span>}
                                    </button>
                                );
                            })}
                        </div>
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
                                    <p>{staff.name === 'とんとん' ? '東京都出身' : '神奈川県出身 | 販売歴6年目'}</p>
                                </div>
                            </div>

                            <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100 text-gray-700">
                                <p className="whitespace-pre-wrap">
                                    {staff.introduction ||
                                        `「メガネ選びをもっと楽しく、ハッピーに！」をモットーに接客しています。
                                    似合うメガネがわからない、という方はぜひご相談ください。
                                    顔タイプ診断やパーソナルカラーに基づいた提案が得意です👓✨`}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Fixed Bottom Button - Raised to bottom-16 to clear BottomNav */}
            <div className="fixed bottom-16 left-0 right-0 p-4 bg-white/90 backdrop-blur-sm border-t border-gray-100 shadow-[0_-5px_20px_rgba(0,0,0,0.05)] z-40">
                <Link
                    href={`/reservation/staff/${staff.id}?tags=${selectedTags.join(',')}&menuId=${menuId || ''}`}
                    className="block w-full max-w-md mx-auto bg-[#00A0E9] text-white font-bold py-4 rounded-xl text-center shadow-lg shadow-blue-200 hover:bg-[#008bc9] transition-all active:scale-[0.98]"
                >
                    このスタッフを指名して予約
                </Link>
            </div>
        </main>
    );
}
