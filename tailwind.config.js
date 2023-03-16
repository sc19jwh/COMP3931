module.exports = {
    future: {
      removeDeprecatedGapUtilities: true,
      purgeLayersByDefault: true,
    },
    purge: {
        enabled: false, //true for production build
        content: [
            '**/templates/*.html',
            '**/templates/**/*.html'
        ]
    },
    theme: {
        extend: {
          colors: {
            custom: {"50":"#5F9595", "100": "#4C7777"},
            disabled: {"50":"#5F9595"}
          },
          keyframes: {
            fadeIn: {
              '0%': { opacity: 0 },
              '100%': { opacity: 1 },
            },
            zoomIn: {
              '0%': { transform: 'scale(0.9)' },
              '100%': { transform: 'scale(1)' },
            },
          },
          animation: {
            fadeIn: 'fadeIn 0.2s',
            zoomIn: 'zoomIn 0.2s',
          }
        }
    },
    variants: {},
    plugins: [],
}
