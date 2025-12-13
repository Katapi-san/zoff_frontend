'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Staff, Tag, fetchAllStaff, fetchTags } from '../../lib/api';
import { getTagStyle, getTagBadgeStyle, getTagTitleColor } from '../../lib/tagUtils';
import { Star, ChevronRight } from 'lucide-react';

export default function StaffList() {
    const router = useRouter();
    const [staffs, setStaffs] = useState<Staff[]>([]);
    const [tags, setTags] = useState<Tag[]>([]);
    const [selectedTagIds, setSelectedTagIds] = useState<number[]>([]);

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

    // Filter logic: AND (Narrow down) - Staff must have ALL selected tags
    const filteredStaffs = staffs.filter(staff => {
        if (selectedTagIds.length === 0) return true;
        const staffTagIds = (staff.tags || []).map(t => t.id);
        return selectedTagIds.every(id => staffTagIds.includes(id));
    });

    // Group Tags
    const technicalTags = tags.filter(t => t.id >= 1 && t.id <= 50);
    const proposalTags = tags.filter(t => t.id >= 51 && t.id <= 100);
    const sceneTags = tags.filter(t => t.id >= 101 && t.id <= 200);
    const hobbyTags = tags.filter(t => t.id >= 201);

    const renderTagSection = (title: string, tags: Tag[], titleId: number) => (
        <div>
            <h3 className={`font-bold mb-2 ${getTagTitleColor(titleId)}`}>{title}</h3>
            <div className="flex flex-wrap gap-2">
                {tags.map(tag => (
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
    );

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

                {/* Tag Filters */}
                <div className="mb-8 space-y-6">
                    {renderTagSection("技術スキルで選ぶ", technicalTags, 1)}
                    {renderTagSection("提案・スタイルで選ぶ", proposalTags, 51)}
                    {renderTagSection("シーン・用途で選ぶ", sceneTags, 101)}
                    {renderTagSection("趣味・カルチャーで選ぶ", hobbyTags, 201)}
                </div>

                <div className="mb-2 text-gray-600 text-sm">
                    {selectedTagIds.length > 0 ? (
                        <p>{filteredStaffs.length} 名のスタッフが見つかりました</p>
                    ) : (
                        <p>全スタッフ表示中</p>
                    )}
                </div>

                {/* Staff List (Vertical) */}
                {filteredStaffs.length > 0 ? (
                    <div className="space-y-4">
                        {filteredStaffs.map((staff) => (
                            <div
                                key={staff.id}
                                onClick={() => router.push(`/staffs/${staff.id}`)}
                                className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between cursor-pointer hover:bg-gray-50 transition-colors active:scale-[0.99]"
                            >
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
                                        <div className="flex items-center gap-2">
                                            <h2 className="font-bold text-gray-800 text-lg">{staff.display_name || staff.name}</h2>
                                            <span className="text-[10px] text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded">Zoff {staff.store?.name}</span>
                                        </div>
                                        <p className="text-xs text-gray-500 mb-1.5">{staff.role || "スタッフ"}</p>

                                        <div className="flex flex-wrap gap-1">
                                            {(staff.tags || []).slice(0, 3).map(tag => (
                                                <span key={tag.id} className={`text-[10px] px-2 py-0.5 rounded-full border ${getTagBadgeStyle(tag.id)}`}>
                                                    #{tag.name}
                                                </span>
                                            ))}
                                            {(staff.tags || []).length > 3 && (
                                                <span className="text-[10px] text-gray-400 self-center">+{(staff.tags || []).length - 3}</span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                                <ChevronRight className="w-5 h-5 text-gray-300" />
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
