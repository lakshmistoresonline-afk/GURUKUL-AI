const isProd = process.env.NODE_ENV === 'production';

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: isProd ? 'export' : undefined,
  images: {
    unoptimized: true,
    remotePatterns: [
      { protocol: 'https', hostname: 'api.dicebear.com' },
      { protocol: 'https', hostname: 'img.youtube.com' },
    ],
  },
  reactStrictMode: true,
  swcMinify: false,
};

export default nextConfig;
