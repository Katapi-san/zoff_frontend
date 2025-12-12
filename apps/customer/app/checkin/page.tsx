"use client";

import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function CheckIn() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);

    const handleCheckIn = () => {
        setLoading(true);
        // Simulate API call
        setTimeout(() => {
            setLoading(false);
            router.push('/staffs');
        }, 1500);
    };

    return (
        <main className="flex min-h-screen flex-col items-center justify-center bg-white p-4">
            <div className="w-full max-w-md text-center">
                <h1 className="text-3xl font-bold text-blue-500 mb-8">Zoff</h1>

                <div className="bg-blue-100 p-8 rounded-2xl shadow-inner mb-8">
                    <p className="text-gray-600 mb-4">Welcome to Zoff Store!</p>
                    <button
                        onClick={handleCheckIn}
                        disabled={loading}
                        className="w-full bg-blue-600 text-white py-4 rounded-xl text-xl font-bold shadow-md hover:bg-blue-700 transition disabled:opacity-50"
                    >
                        {loading ? 'Checking in...' : 'Check-in Here!'}
                    </button>
                </div>
            </div>
        </main>
    );
}
