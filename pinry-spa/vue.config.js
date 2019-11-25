module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000/',
        changeOrigin: true,
        ws: true,
      },
      '/static/media': {
        target: 'http://localhost:8000/',
        changeOrigin: true,
      },
    },
  },
};
