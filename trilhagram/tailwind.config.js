/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
      extend: {
        fontFamily: {
            cursiva: ['"Imperial Script"', 'cursive'],
            calsans: ['"Cal Sans"', 'sans-serif']
          }
      },
    },
    plugins: [],
  }