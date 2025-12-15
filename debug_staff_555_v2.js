
// Use native fetch (Node 18+)
async function checkStaff() {
    console.log('Fetching all staff...');
    try {
        const res = await fetch('https://zoff-scope-backend.azurewebsites.net/staffs/?limit=1000');
        const staff = await res.json();

        console.log(`Total staff found: ${staff.length}`);

        const store555Staff = staff.filter(s => s.store_id === 555 || (s.store && s.store.id === 555));
        console.log(`Staff for Store 555: ${store555Staff.length}`);

        if (store555Staff.length > 0) {
            console.log('Sample Staff:', JSON.stringify(store555Staff[0], null, 2));
        } else {
            console.log('No staff found for store 555.');
            if (staff.length > 0) {
                const sample = staff[0];
                console.log(`Sample data check: ID=${sample.id}, StoreID=${sample.store_id}, Store=${JSON.stringify(sample.store)}`);
            }
        }
    } catch (e) {
        console.error("Error:", e);
    }
}

checkStaff();
