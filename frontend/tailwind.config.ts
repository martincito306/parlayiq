import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#080B12",
        panel: "#111827",
        panelHover: "#161F33",
        borderDark: "#243041",
        accentGreen: "#10B981",
        accentCyan: "#06B6D4",
        accentAmber: "#F59E0B",
        accentRed: "#EF4444",
        textPrimary: "#F8FAFC",
        textSecondary: "#94A3B8",
      },
    },
  },
  plugins: [],
};
export default config;
