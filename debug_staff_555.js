
const fetch = require('node-fetch');

async function checkStaff() {
    console.log('Fetching all staff...');
    const res = await fetch('https://zoff-scope-backend.azurewebsites.net/staffs/?limit=1000');
    const staff = await res.json();

    console.log(`Total staff found: ${staff.length}`);

    const store555Staff = staff.filter(s => s.store_id === 555 || (s.store && s.store.id === 555));
    console.log(`Staff for Store 555: ${store555Staff.length}`);

    if (store555Staff.length > 0) {
        console.log('Sample Staff:', JSON.stringify(store555Staff[0], null, 2));
    } else {
        console.log('No staff found for store 555.');
        // Check finding ANY staff to ensure logic works
        const anyStoreId = staff[0].store_id;
        console.log(`Logic check: Found ${staff.filter(s => s.store_id === anyStoreId).length} staff for store ${anyStoreId}`);
    }
}

checkStaff();
