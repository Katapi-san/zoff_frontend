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

        </div>
    );
}
