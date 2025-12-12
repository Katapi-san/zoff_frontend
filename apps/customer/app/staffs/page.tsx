'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { Staff, Tag, fetchAllStaff, fetchTags } from '../../lib/api';

export default function StaffList() {
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

    // Helper to get tag style based on ID
    const getTagStyle = (tagId: number, isSelected: boolean) => {
        if (tagId <= 50) { // Technical - Zoff Blue
            return isSelected
                ? 'bg-zoff-blue/15 border-zoff-blue text-zoff-blue font-bold'
                : 'bg-white border-zoff-blue/30 text-zoff-blue hover:bg-zoff-blue/5';
        } else if (tagId <= 100) { // Proposal - Zoff Orange
            return isSelected
                ? 'bg-zoff-orange/15 border-zoff-orange text-zoff-orange font-bold'
                : 'bg-white border-zoff-orange/30 text-zoff-orange hover:bg-zoff-orange/5';
        } else if (tagId <= 200) { // Scene - Zoff Green
            return isSelected
                ? 'bg-zoff-green/15 border-zoff-green text-zoff-green font-bold'
                : 'bg-white border-zoff-green/30 text-zoff-green hover:bg-zoff-green/5';
        } else { // Hobby - Zoff Purple
            return isSelected
                ? 'bg-zoff-purple/15 border-zoff-purple text-zoff-purple font-bold'
                : 'bg-white border-zoff-purple/30 text-zoff-purple hover:bg-zoff-purple/5';
        }
    };

    const getTagBadgeStyle = (tagId: number) => {
        if (tagId <= 50) return 'bg-zoff-blue/10 border-zoff-blue/20 text-zoff-blue';
        if (tagId <= 100) return 'bg-zoff-orange/10 border-zoff-orange/20 text-zoff-orange';
        if (tagId <= 200) return 'bg-zoff-green/10 border-zoff-green/20 text-zoff-green';
        return 'bg-zoff-purple/10 border-zoff-purple/20 text-zoff-purple';
    };

    // Group Tags
    const technicalTags = tags.filter(t => t.id >= 1 && t.id <= 50);
    const proposalTags = tags.filter(t => t.id >= 51 && t.id <= 100);
    const sceneTags = tags.filter(t => t.id >= 101 && t.id <= 200);
    const hobbyTags = tags.filter(t => t.id >= 201);

    const renderTagSection = (title: string, tags: Tag[], titleColor: string) => (
        <div>
            <h3 className={`font-bold mb-2 ${titleColor}`}>{title}</h3>
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
            <header className="bg-blue-600 text-white p-4 shadow-md sticky top-0 z-10">
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
                    {renderTagSection("技術スキルで選ぶ", technicalTags, "text-zoff-blue")}
                    {renderTagSection("提案・スタイルで選ぶ", proposalTags, "text-zoff-orange")}
                    {renderTagSection("シーン・用途で選ぶ", sceneTags, "text-zoff-green")}
                    {renderTagSection("趣味・カルチャーで選ぶ", hobbyTags, "text-zoff-purple")}
                </div>

                <div className="mb-2 text-gray-600 text-sm">
                    {selectedTagIds.length > 0 ? (
                        <p>{filteredStaffs.length} 名のスタッフが見つかりました</p>
                    ) : (
                        <p>全スタッフ表示中</p>
                    )}
                </div>

                {/* Staff Grid */}
                {filteredStaffs.length > 0 ? (
                    <div className="grid grid-cols-2 gap-4">
                        {filteredStaffs.map((staff) => (
                            <div key={staff.id} className="bg-white p-4 rounded-xl shadow-sm flex flex-col items-center">
                                <div className="w-24 h-24 mb-3 relative rounded-full overflow-hidden bg-gray-200">
                                    {/* eslint-disable-next-line @next/next/no-img-element */}
                                    <img
                                        src={staff.image_url || "/images/staff/default.jpg"}
                                        alt={staff.display_name || staff.name}
                                        className="object-cover w-full h-full"
                                        onError={(e) => {
                                            e.currentTarget.src = "/globe.svg"; // Fallback
                                        }}
                                    />
                                </div>
                                <h2 className="font-bold text-gray-800 text-center">{staff.display_name || staff.name}</h2>
                                <p className="text-xs text-gray-600 mb-1">{staff.store?.name}</p>
                                <p className="text-xs text-gray-500 mb-2">{staff.role}</p>

                                <div className="flex flex-wrap gap-1 justify-center">
                                    {(staff.tags || []).slice(0, 5).map(tag => ( // Limit displayed tags
                                        <span key={tag.id} className={`text-[10px] px-2 py-1 rounded-full border ${getTagBadgeStyle(tag.id)}`}>
                                            {tag.name}
                                        </span>
                                    ))}
                                    {(staff.tags || []).length > 5 && (
                                        <span className="text-[10px] text-gray-400">+{(staff.tags || []).length - 5}</span>
                                    )}
                                </div>
                                <Link
                                    href={`/reservation/staff/${staff.id}`}
                                    className="mt-4 w-full bg-blue-600 text-white text-xs font-bold py-2 rounded-lg text-center hover:bg-blue-700 transition-colors shadow-sm active:scale-95"
                                >
                                    このスタッフを指名して予約
                                </Link>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-10 text-gray-500">
                        該当するスタッフはいません
                    </div>
                )}
            </div>
        </main>
    );
}
