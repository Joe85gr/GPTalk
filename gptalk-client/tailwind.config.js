/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    colors: {
      transparent: 'transparent',
      "main": '#343541',
    },
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ]
}
