"use client";

import { Store, MapPin, Search, Crown, CreditCard, Home, Users, ClipboardList, PenTool, Hand, Calendar, Bell } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function BottomNav() {

    const pathname = usePathname();


    // Hide on store DASHBOARD pages (singular /store-management), but keep on customer store pages (plural /stores)
    const isStoreDashboard = pathname?.startsWith('/store-management');
    if (isStoreDashboard) return null;

    const isActive = (path: string) => pathname === path;

    return (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 pb-safe z-50">
            <div className="flex justify-around items-center h-16">
                <NavItem href="/" icon={<Home className="w-6 h-6" />} label="トップ" active={isActive('/')} />
                <NavItem href="/stores" icon={<MapPin className="w-6 h-6" />} label="店舗検索" active={isActive('/stores')} />
                <NavItem href="/staffs" icon={<Search className="w-6 h-6" />} label="スタッフ検索" active={isActive('/staffs')} />
                <NavItem href="/member" icon={<CreditCard className="w-6 h-6" />} label="会員証" active={isActive('/member')} />
            </div>
        </div>
    );
}


function NavItem({ icon, label, active = false, href }: { icon: React.ReactNode; label: string; active?: boolean; href?: string }) {
    const content = (
        <div className="flex flex-col items-center justify-center w-full h-full space-y-1">
            <div className={`${active ? 'text-blue-600' : 'text-gray-500'}`}>
                {icon}
            </div>
            <span className={`text-[10px] ${active ? 'text-blue-600 font-bold' : 'text-gray-500'}`}>
                {label}
            </span>
        </div>
    );

    if (href) {
        return (
            <Link href={href} className="w-full h-full flex items-center justify-center">
                {content}
            </Link>
        );
    }

    return (
        <button className="w-full h-full flex items-center justify-center">
            {content}
        </button>
    );
}



export function StoreBottomNav() {
    const pathname = usePathname();
    // Only show on store DASHBOARD pages (singular /store-management)
    const isStoreDashboard = pathname?.startsWith('/store-management');
    if (!isStoreDashboard) return null;

    // Extract store ID
    const match = pathname?.match(/\/store-management\/(\d+)/);
    const storeId = match ? match[1] : '';

    if (!storeId) return null;

    const isActive = (query: string) => {
        if (query === '') return pathname === `/store-management/${storeId}`;
        // Check query params if they exist in window? No, usePathname doesn't include query.
        // We can't easily highlight based on query params here without useSearchParams.
        // But for "Store Top", we check exact path.
        // For others, if pathname includes '/service', we might highlight one of them?
        // Since we can't tell difference between tabs just by path '/service', highlighting might be tricky.
        // But for now, let's just implement links.
        return false;
    };

    // Note: To highlight correctly, we need useSearchParams
    // But since this component is separate, let's just set links. 
    // Highlighting based on tab might require moving this nav INTO the page, OR using Global Layout + SearchParams.

    return (
        <div className="fixed bottom-0 left-0 right-0 bg-slate-900 border-t border-slate-700 pb-safe z-50 text-white">
            <div className="flex justify-around items-center h-16">
                <StoreNavItem
                    href={`/store-management/${storeId}`}
                    icon={<Home className="w-6 h-6" />}
                    label="店舗トップ"
                    active={pathname === `/store-management/${storeId}`}
                />
                <StoreNavItem
                    href={`/store-management/${storeId}/notices`}
                    icon={<Bell className="w-6 h-6" />}
                    label="連絡事項"
                />
                <StoreNavItem
                    href={`/store-management/${storeId}/service?tab=calendar`}
                    icon={<Calendar className="w-6 h-6" />}
                    label="予約状況"
                />
                <StoreNavItem
                    href={`/store-management/${storeId}/service?tab=memo`}
                    icon={<PenTool className="w-6 h-6" />}
                    label="メモ"
                />
            </div>
        </div>
    );
}

function StoreNavItem({ icon, label, active = false, href }: { icon: React.ReactNode; label: string; active?: boolean; href?: string }) {
    return (
        <Link href={href || '#'} className="w-full h-full flex flex-col items-center justify-center space-y-1 hover:bg-white/5 transition-colors">
            <div className={`${active ? 'text-[#00A0E9]' : 'text-gray-400'}`}>
                {icon}
            </div>
            <span className={`text-[10px] ${active ? 'text-[#00A0E9] font-bold' : 'text-gray-400'}`}>
                {label}
            </span>
        </Link>
    );
}
