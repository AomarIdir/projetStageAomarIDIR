/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')({
        charts: true,
    }),
    // ... other plugins
  ],
}

