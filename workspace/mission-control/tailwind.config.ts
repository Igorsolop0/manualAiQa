import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Linear-like dark theme colors
        background: {
          DEFAULT: "#08080A",
          hover: "#131316",
          elevated: "#1C1C1F",
        },
        border: {
          DEFAULT: "#2A2A2D",
          focus: "#6B7280",
        },
        text: {
          primary: "#F3F4F6",
          secondary: "#9CA3AF",
          muted: "#6B7280",
        },
        accent: {
          blue: "#5E6AD2",
          purple: "#A78BFA",
          green: "#34D399",
          red: "#F87171",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
        mono: ["JetBrains Mono", "Menlo", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
