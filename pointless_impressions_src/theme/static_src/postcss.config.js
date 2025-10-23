const production = process.env.NODE_ENV === 'production';

module.exports = {
  plugins: [
    require('@tailwindcss/postcss'),
    require('autoprefixer'),
    production &&
      require('postcss-hash')({
        manifest: '../../static/css/manifest.json',
        algorithm: 'md5',
        trim: 8,
      }),
  ].filter(Boolean),
};