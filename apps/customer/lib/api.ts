// Hardcoded to ensure HTTPS is used and avoid Mixed Content errors
const API_BASE_URL = "https://zoff-scope-backend.azurewebsites.net";

export interface Tag {
    id: number;
    name: string;
    type: string;
}

export interface Store {
    id: number;
    name: string;
    prefecture: string;
    city: string;
    address?: string;
    congestion_url?: string;
    opening_hours?: string;
    phone_number?: string;
    remarks?: string;
}

export interface Staff {
    id: number;
    name: string;
    display_name?: string;
    role?: string;
    store_id: number;
    image_url?: string;
    introduction?: string;
    tags?: Tag[];
    store?: Store;
}

export async function fetchStores(prefecture?: string, city?: string): Promise<Store[]> {
    // Debug logging to verify code version
    console.log(`[API] Fetching stores from: ${API_BASE_URL}/stores/`);

    const params = new URLSearchParams();
    if (prefecture) params.append("prefecture", prefecture);
    if (city) params.append("city", city);
    // Cache busting
    params.append("_t", Date.now().toString());

    // Add trailing slash to prevent backend from redirecting to HTTP (307)
    const res = await fetch(`${API_BASE_URL}/stores/?${params.toString()}`, {
        cache: "no-store",
    });

    if (!res.ok) {
        throw new Error("Failed to fetch stores");
    }

    return res.json();
}

export async function fetchStoreStaff(storeId: number): Promise<Staff[]> {
    const res = await fetch(`${API_BASE_URL}/stores/${storeId}/staff`, {
        cache: "no-store",
    });

    if (!res.ok) {
        throw new Error("Failed to fetch staff");
    }

    return res.json();
}

export async function fetchAllStaff(): Promise<Staff[]> {
    // Adding limit=1000 to ensure we search across ALL staff, not just the first page
    const res = await fetch(`${API_BASE_URL}/staffs/?limit=1000`, {
        cache: "no-store",
    });

    if (!res.ok) {
        throw new Error("Failed to fetch all staff");
    }

    return res.json();
}

export async function fetchTags(limit: number = 1000): Promise<Tag[]> {
    const res = await fetch(`${API_BASE_URL}/tags/?limit=${limit}`, {
        cache: "no-store",
    });

    if (!res.ok) {
        throw new Error("Failed to fetch tags");
    }

    return res.json();
}

export async function fetchStaff(id: number | string): Promise<Staff> {
    const res = await fetch(`${API_BASE_URL}/staffs/${id}`, {
        cache: "no-store",
    });

    if (!res.ok) {
        throw new Error("Failed to fetch staff");
    }

    return res.json();
}

export async function fetchStore(id: number | string): Promise<Store> {
    const res = await fetch(`${API_BASE_URL}/stores/${id}`, {
        cache: "no-store",
    });

    if (!res.ok) {
        throw new Error("Failed to fetch store");
    }

    // ... existing fetchStore ...
    return res.json();
}

// --- Reservation & Customer Interfaces ---

export interface PurchaseHistory {
    id: number;
    purchase_date: string;
    frame_model?: string;
    lens_r?: string;
    lens_l?: string;
    warranty_info?: string;
    prescription_pd?: number;
    prescription_r_sph?: number;
    prescription_r_cyl?: number;
    prescription_r_axis?: number;
    prescription_l_sph?: number;
    prescription_l_cyl?: number;
    prescription_l_axis?: number;
}

export interface CustomerPreferredTag {
    tag: Tag;
}

export interface Customer {
    id: number;
    name?: string;
    kana?: string;
    gender?: string;
    age?: number;
    profile?: string;
    image_url?: string;
    purchase_histories?: PurchaseHistory[];
    preferred_tags?: CustomerPreferredTag[];
}

export interface Reservation {
    id: number;
    store_id: number;
    customer_id: number;
    staff_id?: number;
    reservation_time: string; // ISO datetime
    status: string;
    memo?: string;
    customer?: Customer;
    staff?: Staff;
}

export async function fetchReservations(storeId: number, date?: string, start_date?: string, end_date?: string): Promise<Reservation[]> {
    const params = new URLSearchParams();
    params.append('store_id', storeId.toString());
    if (date) params.append('date', date);
    if (start_date) params.append('start_date', start_date);
    if (end_date) params.append('end_date', end_date);
    params.append("_t", Date.now().toString());

    // Fix: Ensure we are using correct endpoint prefix if needed. Backend router is /reservations
    const res = await fetch(`${API_BASE_URL}/reservations/?${params.toString()}`, {
        cache: "no-store",
    });

    if (!res.ok) {
        throw new Error("Failed to fetch reservations");
    }

    return res.json();
}
