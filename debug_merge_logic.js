
async function debugMergeLogic() {
    console.log('Fetching all staff...');
    try {
        const res = await fetch('https://zoff-scope-backend.azurewebsites.net/staffs/?limit=1000');
        const allStaffData = await res.json();

        const testStoreIds = [347, 176, 206]; // 347: data missing?, 176: data exists, 206: data exists

        testStoreIds.forEach(storeId => {
            console.log(`\n--- Testing Store ID: ${storeId} ---`);

            // 1. Filter
            const storeStaff = allStaffData.filter(staff => {
                const staffStoreId = staff.store_id ? Number(staff.store_id) : null;
                const nestedStoreId = staff.store && staff.store.id ? Number(staff.store.id) : null;
                return staffStoreId === storeId || nestedStoreId === storeId;
            });
            console.log(`Raw filtered count: ${storeStaff.length}`);

            // 2. Merge Logic (Current Code)
            const mergedStaffMap = new Map();
            storeStaff.forEach(s => {
                const key = s.name;
                // console.log(`Processing: ${s.name} (ID: ${s.id})`); // Debug log

                if (!key) {
                    console.warn(`!! Staff with ID ${s.id} has no name!`);
                    return;
                }

                if (!mergedStaffMap.has(key)) {
                    mergedStaffMap.set(key, { ...s, tags: s.tags ? [...s.tags] : [] });
                } else {
                    const existing = mergedStaffMap.get(key);
                    if (s.tags) {
                        const existingTagIds = new Set((existing.tags || []).map(t => t.id));
                        s.tags.forEach(t => {
                            if (!existingTagIds.has(t.id)) {
                                existing.tags.push(t);
                                existingTagIds.add(t.id);
                            }
                        });
                    }
                    if (!existing.image_url && s.image_url) {
                        existing.image_url = s.image_url;
                    }
                }
            });

            const uniqueStoreStaff = Array.from(mergedStaffMap.values());
            console.log(`Merged count: ${uniqueStoreStaff.length}`);

            if (uniqueStoreStaff.length > 0) {
                console.log('Sample names:', uniqueStoreStaff.map(s => s.name).join(', '));
            } else {
                console.log('(No staff to display)');
            }
        });

    } catch (e) {
        console.error("Error:", e);
    }
}

debugMergeLogic();
