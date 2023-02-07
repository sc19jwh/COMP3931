module.exports = {
    future: {
      removeDeprecatedGapUtilities: true,
      purgeLayersByDefault: true,
    },
    purge: {
        enabled: false, //true for production build
        content: [
            '**/templates/*.html',
            '**/templates/**/*html'
        ]
    },
    theme: {
        extend: {
          colors: {
            custom: {"50":"#5F9595", "100": "#4C7777"}
          }
        }
    },
    variants: {},
    plugins: [],
}
