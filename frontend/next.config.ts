import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable experimental features for better development experience
  experimental: {
    // Enable turbopack for faster builds in development
    turbo: {
      // Enable hot reloading for all file types
      rules: {
        "*.{js,jsx,ts,tsx}": {
          loaders: ["swc-loader"],
          as: "*.js",
        },
      },
    },
  },
  // Disable type checking during build for faster hot reload
  typescript: {
    ignoreBuildErrors: false,
  },
  // Enable webpack hot module replacement
  webpack: (config, { dev }) => {
    if (dev) {
      // Enable hot module replacement
      config.optimization = {
        ...config.optimization,
        moduleIds: 'named',
      };
    }
    return config;
  },
};

export default nextConfig;
