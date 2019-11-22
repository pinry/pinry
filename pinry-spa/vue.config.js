module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000/',
        changeOrigin: true,
        ws: true,
        pathRewrite: {
          '^/api': '',
        },
      },
    },
  },
};
