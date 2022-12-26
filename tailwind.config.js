module.exports = {
  future: {
      removeDeprecatedGapUtilities: true,
      purgeLayersByDefault: true,
  },
  purge: {
      enabled: false, //true for production build
      content: [
          '**/templates/*.html'
      ]
  },
  theme: {
      extend: {},
  },
  variants: {},
  plugins: [],
}
