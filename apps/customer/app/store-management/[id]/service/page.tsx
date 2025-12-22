'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams, useSearchParams } from 'next/navigation';
import {
    Users, Clock, Calendar, ChevronLeft, ChevronRight, Search, Edit3, Settings, History, Hand, ArrowRightLeft, CheckCircle2, MessageSquare, Phone, MapPin, Smartphone, FileText, Shield
} from 'lucide-react';
import { fetchReservations, fetchStaff, fetchStore, Reservation as ApiReservation, Staff, Store } from '../../../../lib/api';

// --- Types ---
type StatusType = 'Check-in' | 'Reservation' | 'Reservation_Nomination';

interface Note {
    id: number;
    content: string;
    date: string;
    author: string;
}

interface ProcessAssignment {
    staffId: number;
    staffName: string;
    staffImage?: string;
}

interface ProcessAssignments {
    reception?: ProcessAssignment | null;
    hearing?: ProcessAssignment | null;
    frameSelection?: ProcessAssignment | null;
    visionTest?: ProcessAssignment | null;
    payment?: ProcessAssignment | null;
    delivery?: ProcessAssignment | null;
    [key: string]: ProcessAssignment | null | undefined;
}

interface Customer {
    id: number;
    name: string;
    kana: string;
    profile: string;
    time: string;
    status: StatusType;
    assignedStaff: string | 'Unassigned';
    serviceMenu: string;
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
    raisedHands: number;
    passesRequested: number;
    preferredTags?: { id: number; name: string; }[];
    processAssignments?: ProcessAssignments;
}

export default function StoreServiceMode() {
    const params = useParams();
    const searchParams = useSearchParams();

    const [activeTab, setActiveTab] = useState<'list' | 'reservation' | 'history' | 'memo' | 'calendar' | 'settings'>('list');
    const [viewMode, setViewMode] = useState<'list' | 'detail' | 'order_detail'>('list');
    const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);
    const [filterMyCustomers, setFilterMyCustomers] = useState(false);

    // Data State
    const [reservations, setReservations] = useState<ApiReservation[]>([]);
    const [loading, setLoading] = useState(true);
    const [loggedInStaff, setLoggedInStaff] = useState<Staff | null>(null);
    const [allStaff, setAllStaff] = useState<Staff[]>([]);
    const [store, setStore] = useState<Store | null>(null);

    // Process Assignment Local State
    const [processUpdates, setProcessUpdates] = useState<{ [customerId: number]: ProcessAssignments }>({});
    const [selectedProcess, setSelectedProcess] = useState<{
        customerId: number;
        customerName: string;
        processKey: string;
        processLabel: string;
    } | null>(null);
    const [showStaffSelector, setShowStaffSelector] = useState(false);

    useEffect(() => {
        const tab = searchParams.get('tab');
        if (tab && ['list', 'reservation', 'memo', 'calendar'].includes(tab)) {
            setActiveTab(tab as any);
            if (tab !== 'memo' && tab !== 'calendar') setViewMode('list');
        }
    }, [searchParams]);

    // Fetch Reservations
    useEffect(() => {
        if (!params.id) return;
        const loadReservations = async () => {
            try {
                // Fetch for current month range to support calendar and list
                // Fixed date range for demo: 2025-12-01 to 2025-12-31
                const data = await fetchReservations(Number(params.id), undefined, '2025-12-01', '2025-12-31');
                setReservations(data);
            } catch (e) {
                console.error("Failed to load reservations", e);
            } finally {
                setLoading(false);
            }
        };
        loadReservations();
    }, [params.id]);

    // Fetch Store Info
    useEffect(() => {
        if (!params.id) return;
        const loadStore = async () => {
            try {
                const data = await fetchStore(Number(params.id));
                setStore(data);
            } catch (e) {
                console.error("Failed to load store", e);
            }
        };
        loadStore();
    }, [params.id]);

    // Fetch Staff Info
    useEffect(() => {
        const staffId = searchParams.get('staffId');
        if (!staffId) return;

        const loadStaff = async () => {
            try {
                const staff = await fetchStaff(Number(staffId));
                setLoggedInStaff(staff);

                // For demo, create mock staff list (in production, fetch from API)
                const mockStaff: Staff[] = [
                    staff,
                    { id: 2, name: 'スタッフB', display_name: 'スタッフB', role: 'スタッフ', image_url: null, store_id: Number(params.id), tags: [] },
                    { id: 3, name: 'スタッフC', display_name: 'スタッフC', role: 'スタッフ', image_url: null, store_id: Number(params.id), tags: [] },
                ];
                setAllStaff(mockStaff);
            } catch (e) {
                console.error("Failed to load staff", e);
            }
        };
        loadStaff();
    }, [searchParams, params.id]);

    // Map API Data to UI Customers
    const mapReservationToCustomer = (res: ApiReservation): Customer => {
        const c = res.customer;
        const ph = c?.purchase_histories?.[0]; // Latest purchase

        let status: StatusType = 'Reservation';
        if (res.status === 'Check-in') status = 'Check-in';
        if (res.staff_id) status = 'Reservation_Nomination';

        const timeStr = new Date(res.reservation_time).toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' });

        // Default assignments logic
        // If nominated (store_id has value), assign Hearing, Frame, Vision to that staff
        let assignments: ProcessAssignments = {
            reception: null,
            hearing: null,
            frameSelection: null,
            visionTest: null,
            payment: null,
            delivery: null
        };

        if (res.staff) {
            const assignedStaffObj: ProcessAssignment = {
                staffId: res.staff.id,
                staffName: res.staff.display_name || res.staff.name,
                staffImage: res.staff.image_url
            };
            assignments.hearing = assignedStaffObj;
            assignments.frameSelection = assignedStaffObj;
            assignments.visionTest = assignedStaffObj;
        }

        // Merge local updates
        const customerId = c?.id || 0;
        if (processUpdates[customerId]) {
            assignments = { ...assignments, ...processUpdates[customerId] };
        }

        return {
            id: c?.id || 0,
            name: c?.name || 'Unknown',
            kana: c?.kana || '',
            profile: c?.profile || 'No Profile',
            time: timeStr,
            status: status,
            assignedStaff: res.staff?.display_name || res.staff?.name || (res.staff_id ? 'Assigned' : 'Unassigned'),
            serviceMenu: res.memo || 'メガネ作成・調整', // Use memo or default
            isNew: false, // Mock
            preferredTags: (c as any)?.preferred_tags?.map((pt: any) => ({ id: pt.tag?.id || 0, name: pt.tag?.name || '' })) || [],
            processAssignments: assignments,
            vision: {
                date: ph?.purchase_date || '-',
                r: ph?.prescription_r_sph ? `S ${ph.prescription_r_sph}` : '-',
                l: ph?.prescription_l_sph ? `S ${ph.prescription_l_sph}` : '-'
            },
            ecActivity: ph ? {
                model: ph.frame_model || 'Unknown Frame',
                date: ph.purchase_date || '-',
                adviceSent: false,
                lensName: ph.lens_r || 'Standard Lens',
                warrantyDate: '2026/12/31', // Mock
                price: '¥8,800',
                prescription: {
                    pd: ph.prescription_pd?.toString() || '60',
                    r: { sph: ph.prescription_r_sph?.toString() || '0', cyl: ph.prescription_r_cyl?.toString() || '0', axis: ph.prescription_r_axis?.toString() || '0', add: '', v: '1.0' },
                    l: { sph: ph.prescription_l_sph?.toString() || '0', cyl: ph.prescription_l_cyl?.toString() || '0', axis: ph.prescription_l_axis?.toString() || '0', add: '', v: '1.0' }
                }
            } : undefined,
            notes: (c as any).notes || [],
            raisedHands: 0,
            passesRequested: 0
        };
    };


    const handleProcessClick = (customer: Customer, processKey: string, processLabel: string) => {
        setSelectedProcess({
            customerId: customer.id,
            customerName: customer.name,
            processKey,
            processLabel
        });
        setShowStaffSelector(false);
    };

    const handleAssignSelf = () => {
        if (!selectedProcess || !loggedInStaff) return;
        const { customerId, processKey } = selectedProcess;

        setProcessUpdates(prev => ({
            ...prev,
            [customerId]: {
                ...prev[customerId],
                [processKey]: {
                    staffId: loggedInStaff.id,
                    staffName: loggedInStaff.display_name || loggedInStaff.name,
                    staffImage: loggedInStaff.image_url
                }
            }
        }));
        setSelectedProcess(null);
    };

    const handleAssignOther = (staff: Staff) => {
        if (!selectedProcess) return;
        const { customerId, processKey } = selectedProcess;

        setProcessUpdates(prev => ({
            ...prev,
            [customerId]: {
                ...prev[customerId],
                [processKey]: {
                    staffId: staff.id,
                    staffName: staff.display_name || staff.name,
                    staffImage: staff.image_url
                }
            }
        }));
        setSelectedProcess(null);
        setShowStaffSelector(false);
    };

    // Filter Logic
    // Mock "Today" as 2025-12-17 for demo
    const TODAY_STR = '2025-12-17';

    const todaysReservations = reservations.filter(r => {
        const d = new Date(r.reservation_time).toISOString().split('T')[0];
        return d === TODAY_STR;
    });

    let displayCustomers = todaysReservations.map(mapReservationToCustomer);

    // Sort by reservation time (ascending)
    displayCustomers.sort((a, b) => {
        const timeA = a.time.split(':').map(Number);
        const timeB = b.time.split(':').map(Number);
        return (timeA[0] * 60 + timeA[1]) - (timeB[0] * 60 + timeB[1]);
    });

    // 1. Tab Filter
    if (activeTab === 'reservation') {
        displayCustomers = displayCustomers.filter(c => c.status.includes('Reservation'));
    }

    // 2. My Customers Filter
    if (filterMyCustomers) {
        // Simple mock filter
    }

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

    return (
        <div className="min-h-screen bg-gray-50 font-sans text-gray-800 pb-20 relative">

            {/* --- Header --- */}
            {/* --- Header --- */}
            <header className="fixed top-0 left-0 right-0 bg-[#00A0E9] text-white shadow-md z-30 h-16 grid grid-cols-3 items-center px-4 relative">

                {/* Left: Store Name & Staff Info / Back Button */}
                <div className="flex items-center justify-start h-full overflow-hidden">
                    {viewMode !== 'list' ? (
                        <button onClick={handleBack} className="flex items-center text-sm font-bold bg-white/10 px-3 py-1.5 rounded-full hover:bg-white/20 transition-colors">
                            <ChevronLeft className="w-5 h-5 mr-1" />
                            戻る
                        </button>
                    ) : (
                        <div className="flex items-center gap-4 w-full">
                            {/* Store Name - New Requirement */}
                            {store && (
                                <h2 className="text-xl font-bold tracking-tight whitespace-nowrap truncate max-w-[400px]">{store.name}</h2>
                            )}

                            {/* Staff Info */}
                            {loggedInStaff ? (
                                <div className="flex items-center gap-2 bg-white/10 pl-1 pr-3 py-1 rounded-full border border-white/20 shrink-0">
                                    <div className="w-9 h-9 rounded-full overflow-hidden bg-white/20 border border-white/50 shrink-0">
                                        {/* eslint-disable-next-line @next/next/no-img-element */}
                                        <img
                                            src={loggedInStaff.image_url || "/globe.svg"}
                                            alt={loggedInStaff.display_name || loggedInStaff.name}
                                            className="w-full h-full object-cover"
                                            onError={(e) => { e.currentTarget.src = "/globe.svg"; }}
                                        />
                                    </div>
                                    <div className="flex flex-col leading-none pr-1">
                                        <span className="text-[9px] opacity-80 mb-0.5">担当</span>
                                        <span className="text-sm font-bold whitespace-nowrap">{loggedInStaff.display_name || loggedInStaff.name}</span>
                                    </div>
                                </div>
                            ) : (
                                <div className="text-sm opacity-80">担当: 未選択</div>
                            )}
                        </div>
                    )}
                </div>

                {/* Center: App Title */}
                <div className="flex items-center justify-center">
                    <h1 className="text-xl font-bold tracking-wider whitespace-nowrap">Scope Studio App</h1>
                </div>

                {/* Right: Stats */}
                <div className="flex items-center justify-end gap-3">
                    <div className="flex flex-col items-end text-[10px] leading-tight opacity-90 hidden sm:flex">
                        <span>Hands: {interactionStats.raised}</span>
                        <span>Passes: {interactionStats.passed}</span>
                    </div>
                    <div className="bg-white text-[#00A0E9] rounded-full px-3 py-1 text-sm font-bold shadow min-w-[3rem] text-center">
                        {displayCustomers.length}件
                    </div>
                </div>

                {/* Secret Admin Link (Clickable overlay on right side if needed, or kept separate) */}
                {/* Currently maintained as absolute but z-index adjusted to not block other interactions unless specifically targeted */}
                <a
                    href="/"
                    className="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-red-500 opacity-0 cursor-pointer"
                    aria-label="Go to Customer App"
                ></a>
            </header>

            {/* --- Main Content --- */}
            <main className="pt-20 px-4">

                {viewMode === 'list' && (
                    <div className="space-y-4">
                        {/* Filter Toggle */}
                        <div className="flex justify-end gap-2 mb-2">
                            <button
                                onClick={() => setFilterMyCustomers(false)}
                                className={`text-xs px-4 py-2 rounded-full border font-bold transition-all ${!filterMyCustomers ? 'bg-blue-600 text-white border-blue-600 shadow-md' : 'bg-white text-gray-400 border-gray-200'}`}
                            >
                                全員を表示
                            </button>
                            <button
                                onClick={() => setFilterMyCustomers(true)}
                                className={`text-xs px-4 py-2 rounded-full border font-bold transition-all ${filterMyCustomers ? 'bg-blue-600 text-white border-blue-600 shadow-md' : 'bg-white text-gray-400 border-gray-200'}`}
                            >
                                自分の指名のみ表示
                            </button>
                        </div>

                        {displayCustomers.length > 0 ? displayCustomers.map(customer => (
                            <div
                                key={customer.id}
                                onClick={() => handleCustomerClick(customer)}
                                className="bg-white rounded-xl shadow-sm border border-blue-200 overflow-hidden active:scale-[0.99] transition-transform flex"
                            >
                                {/* Time Column */}
                                <div className="bg-blue-50 w-24 flex flex-col items-center justify-center border-r border-blue-100 p-2 shrink-0">
                                    <span className="text-2xl font-black text-blue-900 tracking-tighter">{customer.time}</span>
                                    <span className={`text-[10px] px-2 py-0.5 rounded font-bold mt-1 whitespace-nowrap
                                        ${customer.status === 'Reservation_Nomination' ? 'bg-blue-100 text-blue-700' :
                                            customer.status === 'Reservation' ? 'bg-gray-200 text-gray-600' :
                                                'bg-green-100 text-green-700'}`}>
                                        {customer.status === 'Reservation_Nomination' ? '指名予約' :
                                            customer.status === 'Reservation' ? '通常予約' : '来店中'}
                                    </span>
                                </div>

                                {/* Info Column */}
                                <div className="flex-1 p-3 flex flex-col justify-between">
                                    <div>
                                        <div className="flex justify-between items-start mb-1">
                                            <h2 className="text-lg font-bold text-gray-800 leading-tight">
                                                {customer.name} <span className="text-xs font-normal text-gray-400">様</span>
                                            </h2>
                                            {customer.assignedStaff === 'あなた' && (
                                                <span className="text-[10px] bg-red-100 text-red-600 px-2 py-0.5 rounded-full font-bold">担当</span>
                                            )}
                                        </div>
                                        <p className="text-sm font-bold text-[#00A0E9] mb-1">
                                            {customer.serviceMenu}
                                        </p>
                                        {/* Preferred Tags */}
                                        {customer.preferredTags && customer.preferredTags.length > 0 && (
                                            <div className="flex flex-wrap gap-1 mt-1 mb-2">
                                                {customer.preferredTags.slice(0, 3).map(tag => (
                                                    <span key={tag.id} className="text-[9px] px-1.5 py-0.5 rounded-full bg-purple-50 text-purple-600 border border-purple-200">
                                                        {tag.name}
                                                    </span>
                                                ))}
                                                {customer.preferredTags.length > 3 && (
                                                    <span className="text-[9px] text-gray-400">+{customer.preferredTags.length - 3}</span>
                                                )}
                                            </div>
                                        )}

                                        {/* Service Process Flow - New Requirement */}
                                        <div className="flex items-center justify-between mt-3 bg-gray-50 rounded-lg p-2 border border-gray-100 overflow-x-auto">
                                            {[
                                                { key: 'reception', label: '受付' },
                                                { key: 'hearing', label: 'ヒアリング' },
                                                { key: 'frameSelection', label: 'フレーム' },
                                                { key: 'visionTest', label: '視力検査' },
                                                { key: 'payment', label: '支払い' },
                                                { key: 'delivery', label: 'お渡し' },
                                            ].map((proc, idx) => {
                                                const assignment = (customer.processAssignments as any)?.[proc.key];
                                                return (
                                                    <div key={proc.key} className="flex flex-col items-center min-w-[3rem] relative">
                                                        <div className="mb-1 text-[8px] text-gray-500 font-bold whitespace-nowrap">{proc.label}</div>
                                                        <button
                                                            onClick={(e) => {
                                                                e.stopPropagation();
                                                                handleProcessClick(customer, proc.key, proc.label);
                                                            }}
                                                            className="w-8 h-8 rounded-full border border-gray-200 bg-white flex items-center justify-center overflow-hidden hover:border-blue-400 hover:ring-2 hover:ring-blue-100 transition-all relative group z-10"
                                                        >
                                                            {assignment ? (
                                                                <img
                                                                    src={assignment.staffImage || "/globe.svg"}
                                                                    alt={assignment.staffName}
                                                                    className="w-full h-full object-cover"
                                                                    onError={(e) => { e.currentTarget.src = "/globe.svg"; }}
                                                                />
                                                            ) : (
                                                                <span className="text-gray-300 text-xs font-bold">+</span>
                                                            )}
                                                            {/* Tooltip on hover */}
                                                            {assignment && (
                                                                <div className="absolute bottom-full mb-1 left-1/2 -translate-x-1/2 bg-black/80 text-white text-[9px] px-1.5 py-0.5 rounded whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none z-10">
                                                                    {assignment.staffName}
                                                                </div>
                                                            )}
                                                        </button>
                                                        {idx < 5 && (
                                                            <div className="absolute top-1/2 -right-3 w-4 h-[1px] bg-gray-200 mt-2" />
                                                        )}
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>
                                    <div className="flex justify-between items-center mt-2 border-t border-gray-100 pt-2 text-xs text-gray-400">
                                        <span>{customer.profile}</span>
                                        {customer.isNew && <span className="text-green-600 font-bold bg-green-50 px-2 rounded">新規</span>}
                                    </div>
                                </div>
                                <div className="w-8 flex items-center justify-center bg-gray-50/50">
                                    <ChevronRight className="w-5 h-5 text-gray-300" />
                                </div>
                            </div>
                        )) : (
                            <div className="text-center py-10 text-gray-400 bg-white rounded-xl">本日の予約はありません</div>
                        )}
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

                        {/* Interaction Actions */}
                        <div className="grid grid-cols-3 gap-2">
                            <button
                                onClick={handleRaiseHand}
                                className="bg-white border-2 border-[#00A0E9] text-[#00A0E9] rounded-xl p-3 flex flex-col items-center justify-center gap-1 active:bg-blue-50 transition-colors"
                            >
                                <Hand className="w-6 h-6" />
                                <span className="text-xs font-bold">引き受ける</span>
                            </button>
                            <button
                                onClick={() => alert('スタッフ分担機能')}
                                className="bg-white border-2 border-purple-500 text-purple-600 rounded-xl p-3 flex flex-col items-center justify-center gap-1 active:bg-purple-50 transition-colors"
                            >
                                <Users className="w-6 h-6" />
                                <span className="text-xs font-bold">スタッフで分担する</span>
                            </button>
                            <button
                                onClick={handlePassRequest}
                                className="bg-white border-2 border-[#FF9200] text-[#FF9200] rounded-xl p-3 flex flex-col items-center justify-center gap-1 active:bg-orange-50 transition-colors"
                            >
                                <ArrowRightLeft className="w-6 h-6" />
                                <span className="text-xs font-bold">ほかのスタッフに任せる</span>
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

                {/* --- Calendar View --- */}
                {activeTab === 'calendar' && (
                    <div className="bg-white rounded-xl shadow-sm border border-blue-200 p-4 min-h-[500px]">
                        <h2 className="text-lg font-bold text-blue-800 mb-4 flex items-center gap-2">
                            <Calendar className="w-5 h-5" /> 予約状況 (2025年12月)
                        </h2>

                        {/* Calendar Grid */}
                        <div className="grid grid-cols-7 gap-1 text-center mb-2">
                            {['日', '月', '火', '水', '木', '金', '土'].map((day, i) => (
                                <div key={i} className={`text-xs font-bold py-1 ${i === 0 ? 'text-red-500' : i === 6 ? 'text-blue-500' : 'text-gray-500'}`}>
                                    {day}
                                </div>
                            ))}
                        </div>
                        <div className="grid grid-cols-7 gap-1">
                            {/* December 2025 starts on Monday (1st) */}
                            {Array.from({ length: 35 }).map((_, i) => {
                                const offset = 1; // Dec 1 is Monday
                                const day = i - offset + 1;
                                const isCurrentMonth = day > 0 && day <= 31;

                                // Find reservations for this day
                                const dayReservations = isCurrentMonth ? reservations.filter(r => {
                                    const d = new Date(r.reservation_time);
                                    return d.getDate() === day && d.getMonth() === 11; // Dec 2025
                                }) : [];

                                const hasReservation = dayReservations.length > 0;

                                return (
                                    <div key={i} className={`aspect-square border border-gray-100 rounded flex flex-col items-center justify-start py-1 relative ${isCurrentMonth ? 'bg-white' : 'bg-gray-50'}`}>
                                        <span className={`text-sm ${!isCurrentMonth ? 'text-gray-300' : 'text-gray-700'}`}>
                                            {day > 0 && day <= 31 ? day : ''}
                                        </span>
                                        {hasReservation && isCurrentMonth && (
                                            <div className="mt-1 flex flex-col items-center gap-0.5 w-full px-1">
                                                <div className="w-full bg-blue-100 text-blue-700 text-[8px] px-0.5 truncate text-center rounded">
                                                    {dayReservations.length}件
                                                </div>
                                                {dayReservations.slice(0, 1).map((r, idx) => (
                                                    <div key={idx} className="w-full bg-green-50 text-green-700 text-[8px] px-0.5 truncate text-center rounded">
                                                        {r.staff?.name || '担当'}
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                        </div>

                        <div className="mt-6 border-t border-gray-100 pt-4">
                            <h3 className="text-sm font-bold text-gray-700 mb-2">今後の予約 (リスト)</h3>
                            <div className="space-y-2">
                                {reservations
                                    .filter(r => new Date(r.reservation_time) >= new Date(2025, 11, 17)) // From 17th
                                    .sort((a, b) => new Date(a.reservation_time).getTime() - new Date(b.reservation_time).getTime())
                                    .slice(0, 5) // Show top 5
                                    .map((r, idx) => (
                                        <div key={idx} className="flex items-center text-sm p-2 bg-white rounded border border-gray-200">
                                            <div className="w-12 font-bold text-blue-700">{new Date(r.reservation_time).getDate()}日</div>
                                            <div className="w-12 text-gray-500">{new Date(r.reservation_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                                            <div className="flex-1 font-bold">{r.customer?.name} 様</div>
                                            <div className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">担当: {r.staff?.name || '-'}</div>
                                        </div>
                                    ))}
                                {reservations.length === 0 && <p className="text-sm text-gray-500">予約はありません</p>}
                            </div>
                        </div>
                    </div>
                )}

            </main>
        </div>
    );
}

