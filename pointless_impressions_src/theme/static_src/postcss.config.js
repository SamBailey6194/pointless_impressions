module.exports = {
  plugins: [
    require('@tailwindcss/postcss'),
    require('autoprefixer'),
    require('postcss-hash')({
      manifest: '../../static/css/manifest.json',
      algorithm: 'md5',
      trim: 8
    })
  ]
};