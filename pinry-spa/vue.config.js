module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true,
        ws: true,
      },
      '/media': {
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true,
      },
      '/static/js/': {
        target: 'http://127.0.0.1:8000/',
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
