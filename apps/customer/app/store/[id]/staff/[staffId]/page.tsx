'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { ChevronLeft, Star, MessageCircle, TrendingUp, Award, Shirt, Palette, User, Glasses } from 'lucide-react';
import { fetchStaff, Staff } from '../../../../../lib/api';

// Simple Gauge Component using SVG
const Gauge = ({ score }: { score: number }) => {
    // Score 0-100
    // Gauge covers 180 degrees (half circle)
    const radius = 80;
    const stroke = 20;
    const normalizedRadius = radius - stroke * 2;
    const circumference = normalizedRadius * 2 * Math.PI; // Full circle
    // We only want half circle logic, but keeping it simple:
    // Actually full circle path, visually cut off or use dasharray
    // strokeDasharray = circumference + ' ' + circumference
    // offset = circumference - percent / 100 * circumference

    // Simpler visual: Semidoughnut
    // Using CSS transforms or just a simple colored arc
    // Angle: -90deg to +90deg (180deg range)
    // score 0 -> -90deg, score 100 -> 90deg
    const rotation = -90 + (score / 100) * 180;

    return (
        <div className="relative w-48 h-32 flex justify-center items-end bg-white overflow-hidden">
            {/* Background Arc */}
            <div className="absolute w-40 h-40 rounded-full border-[20px] border-gray-200 top-4 box-border border-b-0 border-l-0 border-r-0" style={{ clipPath: 'polygon(0 0, 100% 0, 100% 50%, 0 50%)', borderRadius: '50%' }}></div>
            {/* We can hack a gauge with simple CSS rotation of a half-circle? */}
            {/* Let's use a simpler approach: SVG */}
            <svg width="200" height="110" viewBox="0 0 200 110">
                {/* Background Track */}
                <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#E5E7EB" strokeWidth="20" strokeLinecap="round" />

                {/* Colored Track - Segmented in image (blue/green/yellow/red) */}
                {/* Simplified to gradient or segments */}
                <path d="M 20 100 A 80 80 0 0 1 60 44" fill="none" stroke="#3B82F6" strokeWidth="20" strokeLinecap="butt" /> {/* Blue */}
                <path d="M 62 42 A 80 80 0 0 1 110 24" fill="none" stroke="#10B981" strokeWidth="20" strokeLinecap="butt" /> {/* Green */}
                <path d="M 112 24 A 80 80 0 0 1 180 100" fill="none" stroke="#F59E0B" strokeWidth="20" strokeLinecap="round" /> {/* Yellow/Orange */}

                {/* Needle */}
                {/* Center at 100, 100. Length 70. Angle based on score */}
                {/* 0 = 180deg (left), 50 = 270deg (up), 100 = 360deg (right) basically */}
                {/* Math: rad = (180 + score/100 * 180) * PI / 180 */}
                <line
                    x1="100" y1="100"
                    x2={100 + 70 * Math.cos(Math.PI + (score / 100) * Math.PI)}
                    y2={100 + 70 * Math.sin(Math.PI + (score / 100) * Math.PI)}
                    stroke="#4B5563" strokeWidth="4"
                    markerEnd="url(#arrowhead)"
                />
                <circle cx="100" cy="100" r="5" fill="#4B5563" />
            </svg>
            <div className="absolute bottom-0 text-center">
                <p className="text-xs text-gray-500 font-bold tracking-widest mb-1">SCOPE SCORE</p>
                {/* <p className="text-3xl font-black text-gray-800">{score}</p> */}
            </div>
        </div>
    );
};

export default function StaffMyPage() {
    const params = useParams();
    const [staff, setStaff] = useState<Staff | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!params.staffId) return;
        const load = async () => {
            try {
                const data = await fetchStaff(params.staffId as string);
                setStaff(data);
            } catch (e) { console.error(e); }
            finally { setLoading(false); }
        };
        load();
    }, [params.staffId]);

    if (!staff && !loading) return <div>Staff not found</div>;

    // Mock Data for Dashboard
    const scopeScore = 78;
    const nextRankProgress = 60;
    const myTags = [
        { name: 'Fitting Pro', icon: <Shirt size={14} />, color: 'bg-pink-100 text-pink-700' },
        { name: 'Color Master', icon: <Palette size={14} />, color: 'bg-orange-100 text-orange-700' },
        { name: 'Zoff Star', icon: <Star size={14} />, color: 'bg-green-100 text-green-700' },
        { name: '色彩検定', icon: <Award size={14} />, color: 'bg-blue-100 text-blue-700' },
        { name: 'Trend Setter', icon: <TrendingUp size={14} />, color: 'bg-purple-100 text-purple-700' },
        { name: 'Insurance Ace', icon: <User size={14} />, color: 'bg-yellow-100 text-yellow-700' },
    ];

    const messages = [
        { id: 1, user: '20代 女性', content: 'とても親身になって相談に乗ってくれました。似合うメガネが見つかりました！', date: '2023/12/10', rating: 5 },
        { id: 2, user: '40代 男性', content: 'フィッティングがとても丁寧で、掛け心地が最高です。', date: '2023/12/05', rating: 5 },
        { id: 3, user: '30代 女性', content: '知識が豊富で、レンズの選び方も分かりやすかった。', date: '2023/11/28', rating: 4 },
    ];

    return (
        <div className="min-h-screen bg-gray-100 font-sans pb-10">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 px-4 py-3 sticky top-0 z-10 flex items-center justify-between shadow-sm">
                <div className="flex items-center gap-2">
                    <Link href={`/store/${params.id}`} className="p-2 rounded-full hover:bg-gray-100 text-gray-500 transition-colors">
                        <ChevronLeft size={24} />
                    </Link>
                    <h1 className="text-lg font-bold text-gray-800">My Page</h1>
                </div>
                {staff && (
                    <div className="w-8 h-8 rounded-full overflow-hidden border border-gray-200">
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img src={staff.image_url || "/images/staff/default.jpg"} alt="me" className="w-full h-full object-cover" />
                    </div>
                )}
            </header>

            <main className="max-w-md mx-auto p-4 space-y-6">

                {/* Score Card */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 flex flex-col items-center relative overflow-hidden">
                    <div className="absolute top-0 w-full h-2 bg-gradient-to-r from-blue-400 via-green-400 to-yellow-400"></div>

                    <h2 className="text-gray-500 font-bold text-sm mb-2">CURRENT SCORE</h2>
                    <Gauge score={scopeScore} />

                    <div className="text-center mt-[-20px] mb-6">
                        <span className="text-4xl font-black text-gray-800 tracking-tighter">{scopeScore}</span>
                        <span className="text-sm text-gray-400 ml-1">/ 100</span>
                    </div>

                    <div className="w-full">
                        <div className="flex justify-between text-xs font-bold text-gray-400 mb-1">
                            <span>Path to next rank</span>
                            <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                        </div>
                        <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                            <div className="h-full bg-blue-500 rounded-full" style={{ width: `${nextRankProgress}%` }}></div>
                        </div>
                    </div>
                </div>

                {/* My Tags */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-5">
                    <h3 className="text-center font-bold text-gray-700 mb-4 border-b border-gray-100 pb-2">My Tags</h3>
                    <div className="grid grid-cols-2 gap-3">
                        {/* Combine API tags with mock badges if needed, or just use mock for display */}
                        {myTags.map((tag, i) => (
                            <div key={i} className={`flex items-center gap-2 px-3 py-2 rounded-lg border border-transparent ${tag.color} bg-opacity-50`}>
                                <div className="p-1 bg-white rounded-full bg-opacity-60">
                                    {tag.icon}
                                </div>
                                <span className="text-xs font-bold whitespace-nowrap overflow-hidden text-ellipsis">{tag.name}</span>
                            </div>
                        ))}
                    </div>
                    {/* Add actual staff tags */}
                    {staff?.tags && staff.tags.length > 0 && (
                        <div className="mt-2 pt-2 border-t border-gray-100 grid grid-cols-2 gap-3">
                            {staff.tags.map(t => (
                                <div key={t.id} className="flex items-center gap-2 px-3 py-2 rounded-lg border border-gray-100 bg-gray-50 text-gray-600">
                                    <span className="text-xs font-bold"># {t.name}</span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Customer Voices */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-5">
                    <h3 className="text-center font-bold text-gray-700 mb-4 flex items-center justify-center gap-2">
                        <MessageCircle className="w-5 h-5 text-blue-500" />
                        Customer Voices
                    </h3>
                    <div className="space-y-4">
                        {messages.map(msg => (
                            <div key={msg.id} className="border-b border-gray-100 pb-4 last:border-0 last:pb-0">
                                <div className="flex justify-between items-start mb-1">
                                    <div className="flex items-center gap-2">
                                        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-xs font-bold text-gray-500">
                                            User
                                        </div>
                                        <div>
                                            <p className="text-xs font-bold text-gray-700">{msg.user}</p>
                                            <p className="text-[10px] text-gray-400">{msg.date}</p>
                                        </div>
                                    </div>
                                    <div className="flex text-yellow-400">
                                        {[...Array(5)].map((_, i) => (
                                            <Star key={i} size={12} fill={i < msg.rating ? "currentColor" : "none"} className={i < msg.rating ? "" : "text-gray-300"} />
                                        ))}
                                    </div>
                                </div>
                                <div className="bg-blue-50 p-3 rounded-lg rounded-tl-none mt-2 relative">
                                    <p className="text-sm text-gray-700 leading-snug">{msg.content}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

            </main>
        </div>
    );
}
