// http://localhost:8080/
// https://pin.lapo.it/
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'https://pin.lapo.it/',
        changeOrigin: true,
        ws: true,
      },
      '/media': {
        target: 'https://pin.lapo.it/',
        changeOrigin: true,
      },
      '/static/js/': {
        target: 'https://pin.lapo.it/',
        changeOrigin: true,
      },
    },
  },
  pwa: {
    name: 'Pinry Mobile',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'black',
    // configure the workbox plugin
    workboxPluginMode: 'GenerateSW',
    iconPaths: {
      favicon32: 'favicon.png',
      favicon16: 'favicon.png',
      appleTouchIcon: 'favicon.png',
      // FIXME(winkidney): Add svg file for safari
      // maskIcon: 'img/icons/safari-pinned-tab.svg',
      msTileImage: 'favicon.png',
    },
  },
};
