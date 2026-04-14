import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: '#0b0f0e',
        'bg-2': '#111816',
        ink: '#f4f1ea',
        muted: '#9aa19d',
        line: '#1f2a27',
        accent: '#c8ff4d',
        'accent-soft': '#e8ffb0',
        card: '#131a18',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Fraunces', 'Georgia', 'serif'],
      },
    },
  },
  plugins: [],
};
export default config;
