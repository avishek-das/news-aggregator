import type { NextConfig } from "next";

// Static export: no SSR, no Next.js API routes.
// All data fetching is client-side via NEXT_PUBLIC_API_URL (FastAPI backend).
// Dynamic routes (e.g. /sources/[id]/edit) require Amplify SPA rewrite:
//   source: /<*>  →  target: /index.html  (status 200)
const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: {
    unoptimized: true, // required for static export
  },
};

export default nextConfig;
