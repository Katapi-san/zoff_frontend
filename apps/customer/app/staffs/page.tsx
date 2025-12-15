'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Staff, Tag, fetchAllStaff, fetchTags } from '../../lib/api';
import { getTagStyle, getTagBadgeStyle } from '../../lib/tagUtils';
import { Star, ChevronRight, ChevronDown, ChevronUp } from 'lucide-react';

export default function StaffList() {
    const router = useRouter();
    const [staffs, setStaffs] = useState<Staff[]>([]);
    const [tags, setTags] = useState<Tag[]>([]);
    const [selectedTagIds, setSelectedTagIds] = useState<number[]>([]);

    // State to track expanded categories
    const [expandedCategory, setExpandedCategory] = useState<number | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            console.log("StaffList Component Loaded - v2 (API Centralized)");
            try {
                // Fetch Staff
                const staffData = await fetchAllStaff();

                // Deduplicate staff by display_name to handle duplicates with different IDs
                const uniqueStaffs = Array.from(new Map(staffData.map((s: Staff) => [s.display_name, s])).values());
                setStaffs(uniqueStaffs as Staff[]);

                // Fetch Tags
                const tagsData = await fetchTags();
                setTags(tagsData);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    const toggleTag = (id: number) => {
        setSelectedTagIds(prev =>
            prev.includes(id) ? prev.filter(tagId => tagId !== id) : [...prev, id]
        );
    };

    const toggleCategory = (categoryId: number) => {
        setExpandedCategory(prev => prev === categoryId ? null : categoryId);
    };

    const [searchTerm, setSearchTerm] = useState("");

    // Filter logic: AND (Narrow down) - Staff must have ALL selected tags AND match Name
    const filteredStaffs = staffs.filter(staff => {
        // Tag Filter
        if (selectedTagIds.length > 0) {
            const staffTagIds = (staff.tags || []).map(t => t.id);
            if (!selectedTagIds.every(id => staffTagIds.includes(id))) return false;
        }

        // Name Search Filter
        if (searchTerm) {
            const term = searchTerm.toLowerCase();
            const name = (staff.name || "").toLowerCase();
            const disp = (staff.display_name || "").toLowerCase();
            const store = (staff.store?.name || "").toLowerCase();
            return name.includes(term) || disp.includes(term) || store.includes(term);
        }

        return true;
    });

    // Group Tags
    const categories = [
        { id: 1, title: "技術スキルで選ぶ", tags: tags.filter(t => t.id >= 1 && t.id <= 50), color: "text-blue-600", bgColor: "bg-blue-50", borderColor: "border-blue-200" },
        { id: 2, title: "提案・スタイルで選ぶ", tags: tags.filter(t => t.id >= 51 && t.id <= 100), color: "text-orange-600", bgColor: "bg-orange-50", borderColor: "border-orange-200" },
        { id: 3, title: "シーン・用途で選ぶ", tags: tags.filter(t => t.id >= 101 && t.id <= 200), color: "text-green-600", bgColor: "bg-green-50", borderColor: "border-green-200" },
        { id: 4, title: "趣味・カルチャーで選ぶ", tags: tags.filter(t => t.id >= 201), color: "text-purple-600", bgColor: "bg-purple-50", borderColor: "border-purple-200" },
    ];

    return (
        <main className="min-h-screen bg-gray-50 pb-10">
            <header className="bg-[#00A0E9] text-white p-4 shadow-md sticky top-0 z-10">
                <div className="flex justify-between items-center max-w-md mx-auto">
                    <Link href="/" className="font-bold text-lg">{'< Back'}</Link>
                    <h1 className="text-xl font-bold">Zoff Scope</h1>
                    <div className="w-10"></div>
                </div>
            </header>

            <div className="p-4 max-w-md mx-auto">
                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                    <span className="mr-2">🔍</span> スタッフをタグで探す
                </h2>

                {/* Search Input */}
                <div className="mb-6">
                    <input
                        type="text"
                        placeholder="スタッフ名・店舗名で検索..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full p-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#00A0E9] shadow-sm transition-shadow"
                    />
                </div>

                {/* Categories */}
                <div className="mb-6 space-y-3">
                    {categories.map(cat => {
                        const isExpanded = expandedCategory === cat.id;
                        const activeCount = cat.tags.filter(t => selectedTagIds.includes(t.id)).length;

                        return (
                            <div key={cat.id} className="bg-white rounded-xl overflow-hidden border border-gray-100 shadow-sm">
                                <button
                                    onClick={() => toggleCategory(cat.id)}
                                    className={`w-full flex items-center justify-between p-4 ${isExpanded ? cat.bgColor : 'bg-white hover:bg-gray-50'} transition-colors`}
                                >
                                    <div className="flex items-center gap-2">
                                        <span className={`font-bold ${cat.color}`}>{cat.title}</span>
                                        {activeCount > 0 && (
                                            <span className="bg-gray-800 text-white text-xs font-bold px-2 py-0.5 rounded-full">
                                                {activeCount}
                                            </span>
                                        )}
                                    </div>
                                    {isExpanded ? (
                                        <ChevronUp className={`w-5 h-5 ${cat.color}`} />
                                    ) : (
                                        <ChevronDown className="w-5 h-5 text-gray-400" />
                                    )}
                                </button>

                                {isExpanded && (
                                    <div className={`p-4 border-t ${cat.borderColor} bg-white animate-in slide-in-from-top-2 duration-200`}>
                                        <div className="flex flex-wrap gap-2">
                                            {cat.tags.map(tag => (
                                                <button
                                                    key={tag.id}
                                                    onClick={() => toggleTag(tag.id)}
                                                    className={`px-3 py-1.5 rounded-full text-sm border transition-colors ${getTagStyle(tag.id, selectedTagIds.includes(tag.id))}`}
                                                >
                                                    {tag.name}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>

                <div className="mb-4 text-gray-600 text-sm flex justify-between items-center">
                    <p>{filteredStaffs.length} 名のスタッフが見つかりました</p>
                    {(selectedTagIds.length > 0 || searchTerm) && (
                        <button
                            onClick={() => { setSelectedTagIds([]); setSearchTerm(""); }}
                            className="text-xs text-red-500 underline"
                        >
                            条件をクリア
                        </button>
                    )}
                </div>

                {/* Staff List (Vertical) */}
                {filteredStaffs.length > 0 ? (
                    <div className="space-y-4">
                        {filteredStaffs.map((staff) => (

                            <div
                                key={staff.id}
                                onClick={() => router.push(`/staffs/${staff.id}`)}
                                className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 cursor-pointer hover:bg-gray-50 transition-colors active:scale-[0.99]"
                            >
                                <div className="flex items-center justify-between mb-3">
                                    <div className="flex items-center space-x-4">
                                        <div className="relative flex-shrink-0">
                                            <div className="w-16 h-16 bg-gray-200 rounded-full overflow-hidden border border-gray-100">
                                                {/* eslint-disable-next-line @next/next/no-img-element */}
                                                <img
                                                    src={staff.image_url || "/images/staff/default.jpg"}
                                                    alt={staff.display_name || staff.name}
                                                    className="object-cover w-full h-full"
                                                    onError={(e) => {
                                                        e.currentTarget.src = "/globe.svg";
                                                    }}
                                                />
                                            </div>
                                            <div className="absolute -bottom-1 -right-1 bg-yellow-400 rounded-full p-1 border-2 border-white shadow-sm">
                                                <Star className="w-3 h-3 text-white fill-current" />
                                            </div>
                                        </div>
                                        <div>
                                            <div className="flex items-center gap-2 mb-1">
                                                <h2 className="font-bold text-gray-800 text-lg">{staff.display_name || staff.name}</h2>
                                                <span className="text-[10px] text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded">Zoff {staff.store?.name}</span>
                                            </div>
                                            <p className="text-xs text-gray-500">{staff.role || "スタッフ"}</p>
                                        </div>
                                    </div>
                                    <ChevronRight className="w-5 h-5 text-gray-300" />
                                </div>

                                {/* Tag Area: Independent Row */}
                                <div className="flex flex-wrap gap-1.5 pl-1">
                                    {(staff.tags || []).slice(0, 10).map(tag => (
                                        <span key={tag.id} className={`text-[10px] px-2.5 py-1 rounded-full border ${getTagBadgeStyle(tag.id)}`}>
                                            {tag.name}
                                        </span>
                                    ))}
                                    {(staff.tags || []).length > 10 && (
                                        <span className="text-[10px] text-gray-400 self-center">+{(staff.tags || []).length - 10}</span>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-10 text-gray-500 bg-white rounded-xl">
                        該当するスタッフはいません
                    </div>
                )}
            </div>
        </main>
    );
}
