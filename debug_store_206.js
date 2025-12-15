
async function checkStore206() {
    console.log('Fetching all staff...');
    try {
        const res = await fetch('https://zoff-scope-backend.azurewebsites.net/staffs/?limit=1000');
        const allStaff = await res.json();

        const staff206 = allStaff.filter(s => s.store_id === 206 || (s.store && s.store.id === 206));

        console.log(`Found ${staff206.length} entries for Store 206`);
        staff206.forEach((s, i) => {
            console.log(`[${i}] ID: ${s.id} | Name: ${s.name} | Tags: ${s.tags ? s.tags.length : 0}`);
            if (s.tags) {
                console.log(`   Tags: ${s.tags.map(t => t.name).slice(0, 3).join(', ')}...`);
            }
        });

    } catch (e) {
        console.error("Error:", e);
    }
}

checkStore206();
