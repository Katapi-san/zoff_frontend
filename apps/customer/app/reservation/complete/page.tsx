
import React from 'react';
import Link from 'next/link';
import { CheckCircle } from 'lucide-react';

export const dynamic = 'force-dynamic';

type Props = {
    searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}

export default async function ReservationCompletePage({ searchParams }: Props) {
    const params = await searchParams;
    const staffName = params.staffName as string;
    const date = params.date as string;
    const time = params.time as string;

    return (
        <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6 text-center">
            <div className="mb-6">
                <CheckCircle className="w-24 h-24 text-green-500" />
            </div>

            <h1 className="text-2xl font-bold text-gray-800 mb-4">ご予約ありがとうございました</h1>

            <p className="text-gray-600 mb-8">
                以下の内容で予約を承りました。<br />
                当日お会いできるのを楽しみにしております。
            </p>

            <div className="bg-gray-50 rounded-xl p-6 w-full max-w-sm mb-8 text-left border border-gray-100 shadow-sm">
                <div className="mb-4">
                    <p className="text-xs text-gray-500 mb-1">指名スタッフ</p>
                    <p className="font-bold text-lg text-gray-800">{staffName} さん</p>
                </div>
                <div className="mb-4">
                    <p className="text-xs text-gray-500 mb-1">ご来店日時</p>
                    <p className="font-bold text-lg text-gray-800">
                        {date && `12月${date}日`} {time}
                    </p>
                </div>
                <div>
                    <p className="text-xs text-gray-500 mb-1">店舗</p>
                    <p className="font-bold text-gray-800">Zoff 原宿店</p>
                </div>
            </div>

            <Link
                href="/"
                className="bg-blue-600 text-white font-bold py-3 px-10 rounded-full hover:bg-blue-700 transition shadow-md w-full max-w-sm"
            >
                トップに戻る
            </Link>
        </div>
    );
}
