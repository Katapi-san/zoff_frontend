/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
    env: {
        NEXT_PUBLIC_API_BASE_URL: "https://zoff-scope-backend.azurewebsites.net",
    },
};

export default nextConfig;
