"use client";

import { Store, MapPin, Search, Crown, CreditCard } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function BottomNav() {
    const pathname = usePathname();

    const isActive = (path: string) => pathname === path;

    return (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 pb-safe z-50">
            <div className="flex justify-around items-center h-16">
                <NavItem href="/" icon={<Store className="w-6 h-6" />} label="チェックイン" active={isActive('/')} />
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
