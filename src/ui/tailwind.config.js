/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      'coral': {
        DEFAULT: '#FF4D6D',
        hover: '#CC1A3A'
      },

      'background': {
        DEFAULT: '#141414',
        alt: '#111111'
      },
      'text-color': '#f5f5f5',
      'accent-1': '#1C1C1C',
      'accent-2': '#BDBDBD'
    },
    fontFamily: {
      'maven': ['Maven Pro', 'sans-serif']
    },
    extend: {
      gridTemplateColumns: {
        'displayColumns': "repeat(12, 1fr)"
      },
      gridTemplateRows: {
        'mainSplit': "repeat(8, 1fr)",
        'overviewRows': "repeat(6, 1fr)"
      },

    },
  },
  plugins: [],
};
