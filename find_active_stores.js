
// Use native fetch
async function findStoresWithStaff() {
    console.log('Fetching all staff...');
    try {
        const res = await fetch('https://zoff-scope-backend.azurewebsites.net/staffs/?limit=1000');
        const staff = await res.json();

        console.log(`Total staff found: ${staff.length}`);

        // Count staff per store
        const storeCounts = {};
        const storeNames = {};

        staff.forEach(s => {
            const id = s.store_id || (s.store ? s.store.id : null);
            const name = s.store ? s.store.name : 'Unknown';
            if (id) {
                storeCounts[id] = (storeCounts[id] || 0) + 1;
                storeNames[id] = name;
            }
        });

        console.log('\n--- Stores with Staff ---');
        // Sort by count descending
        const sortedStores = Object.entries(storeCounts)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 20); // Top 20

        sortedStores.forEach(([id, count]) => {
            console.log(`Store ID: ${id} | Name: ${storeNames[id]} | Staff Count: ${count}`);
            console.log(`URL: https://zoff-scope-frontend.azurewebsites.net/stores/${id}`);
        });

        if (sortedStores.length === 0) {
            console.log('No stores found with staff.');
        }

    } catch (e) {
        console.error("Error:", e);
    }
}

findStoresWithStaff();
