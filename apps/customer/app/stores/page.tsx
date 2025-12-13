import StoreSearch from "../../components/StoreSearch";


export default function StoresPage() {
    return (
        <div className="bg-gray-100 min-h-screen pb-20">
            <header className="bg-blue-600 text-white p-4 text-center font-bold text-lg sticky top-0 z-10">
                Zoff Scope
            </header>
            <main>
                <StoreSearch />
            </main>
            <footer className="text-center text-[10px] text-gray-300 py-2">
                v20251213-1945-NOBUILD
            </footer>
        </div>
    );
}
