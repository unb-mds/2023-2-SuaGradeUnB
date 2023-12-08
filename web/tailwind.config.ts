import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      fontFamily: {
        sans: ['var(--font-poppins)'],
      },
      colors: {
        primary: '#13AF5E',
        secondary: '#4080F4',
        snow: {
          primary: '#F6F6F6',
          secondary: '#E9E9E9',
          tertiary: '#D9D9D9',
        }
      },
      screens: {
        flat: {
          raw: '(max-height: 365px)'
        }
      }
    },
  },
  plugins: [],
};
export default config;
