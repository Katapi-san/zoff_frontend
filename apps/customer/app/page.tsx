'use client';

import Link from 'next/link';
import { Camera, CreditCard, ShoppingBag, UserCog, Search, MapPin } from 'lucide-react';

export default function Home() {
  const menuItems = [
    { name: 'チェックイン', icon: <Camera className="w-10 h-10 mb-2 text-[#00A0E9]" />, href: '/checkin' },
    { name: '会員証', icon: <CreditCard className="w-10 h-10 mb-2 text-[#00A0E9]" />, href: '/member' }, // Placeholder
    { name: '店舗検索', icon: <MapPin className="w-10 h-10 mb-2 text-[#00A0E9]" />, href: '/stores' },
    { name: 'スタッフ検索', icon: <Search className="w-10 h-10 mb-2 text-[#00A0E9]" />, href: '/staffs' }, // Assuming staffs listing page is here
    { name: '購入履歴', icon: <ShoppingBag className="w-10 h-10 mb-2 text-[#00A0E9]" />, href: '#' }, // Placeholder
    { name: '登録情報編集', icon: <UserCog className="w-10 h-10 mb-2 text-[#00A0E9]" />, href: '#' }, // Placeholder
  ];

  return (
    <div className="bg-gray-50 min-h-screen pb-20 font-sans">
      <header className="bg-blue-600 text-white p-4 text-center font-bold text-lg sticky top-0 z-10">
        ホーム
      </header>

      <main className="p-4 max-w-md mx-auto pt-10">
        {/* Logo Section */}
        <div className="text-center mb-10">
          <h1 className="text-5xl font-bold text-gray-800 tracking-tight" style={{ fontFamily: 'Inter, sans-serif' }}>
            Zoff Scope <span className="block text-4xl mt-2 font-normal">Studio</span>
          </h1>
        </div>

        {/* My Page Title */}
        <div className="text-center mb-6">
          <h2 className="text-[#00A0E9] font-bold text-xl">マイページ</h2>
        </div>

        {/* Menu Grid */}
        <div className="grid grid-cols-3 gap-4">
          {menuItems.map((item, index) => (
            <Link
              key={index}
              href={item.href}
              className="bg-white flex flex-col items-center justify-center p-4 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow aspect-square active:scale-95"
            >
              {item.icon}
              <span className="text-xs font-bold text-[#00A0E9] text-center">{item.name}</span>
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}
