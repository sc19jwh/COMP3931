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
            slideInLeft: {
              '0%': { transform: 'translateX(-100%)' },
              '100%': { transform: 'translateX(0)' },
            },
            slideInRight: {
              '0%': { transform: 'translateX(100%)' },
              '100%': { transform: 'translateX(0)' },
            },
          },
          animation: {
            fadeIn: 'fadeIn 0.2s',
            fadeInMedium: 'fadeIn 0.5s',
            fadeInLong: 'fadeIn 1.0s',
            fadeInExtraLong: 'fadeIn 1.5s',
            zoomIn: 'zoomIn 0.2s',
            zoomInMedium: 'zoomIn 0.5s',
            zoomInLong: 'zoomIn 1.0s',
            zoomInExtraLong: 'zoomIn 1.5s',
            slideInLeft: 'slideInLeft 1.0s',
            slideInRight: 'slideInRight 1.0s',
          }
        }
    },
    variants: {},
    plugins: [],
}
