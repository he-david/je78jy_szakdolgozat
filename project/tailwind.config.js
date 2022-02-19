module.exports = {
  mode: 'jit',
  content: [
    './templates/**/*.html',
    './templates/*.html',
    './**/templates/**/*.html',
    './**/templates/*.html'
  ],
  darkMode: 'media', // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}