import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/lib/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/hooks/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#050a14",
          900: "#0a1628",
          800: "#0f2040",
          700: "#1a3358",
          600: "#1e3a6e",
          500: "#2a4f8f",
        },
        accent: {
          blue: "#3b82f6",
          cyan: "#06b6d4",
        },
        verdict: {
          true: "#22c55e",
          false: "#ef4444",
          unverified: "#f59e0b",
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
};

export default config;