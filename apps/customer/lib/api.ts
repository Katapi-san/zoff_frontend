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
    const res = await fetch(`${API_BASE_URL}/staffs/`, {
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
