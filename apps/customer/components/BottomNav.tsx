"use client";

import { Store, MapPin, Search, Crown, CreditCard, Home } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function BottomNav() {

    const pathname = usePathname();

    // Hide on store pages which have their own nav
    if (pathname?.startsWith('/store')) return null;

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

import { Users, ClipboardList, PenTool, Hand } from 'lucide-react';

export function StoreBottomNav() {
    const pathname = usePathname();
    const isActive = (path: string) => pathname?.includes(path);

    // Only show on store pages
    if (!pathname?.startsWith('/store')) return null;

    return (
        <div className="fixed bottom-0 left-0 right-0 bg-slate-900 border-t border-slate-700 pb-safe z-50 text-white">
            <div className="flex justify-around items-center h-16">
                <StoreNavItem href="#" icon={<Users className="w-6 h-6" />} label="顧客リスト" active={true} />
                <StoreNavItem href="#" icon={<ClipboardList className="w-6 h-6" />} label="カルテ" />
                <StoreNavItem href="#" icon={<PenTool className="w-6 h-6" />} label="メモ" />
                <StoreNavItem href="#" icon={<Hand className="w-6 h-6" />} label="HR" />
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
