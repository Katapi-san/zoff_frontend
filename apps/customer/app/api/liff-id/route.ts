import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
    // Azureの環境変数からLIFF IDを取得する
    // NEXT_PUBLIC_LIFF_ID または LIFF_ID を参照
    const liffId = process.env.NEXT_PUBLIC_LIFF_ID || process.env.LIFF_ID || '';

    return NextResponse.json({ liffId });
}
