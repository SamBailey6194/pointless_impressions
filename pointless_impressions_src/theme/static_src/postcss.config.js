import tailwindcss from '@tailwindcss/postcss';
import autoprefixer from 'autoprefixer';
import postcssHash from 'postcss-hash';

const production = process.env.NODE_ENV === 'production';

export default {
  plugins: [
    tailwindcss,
    autoprefixer,
    production &&
      postcssHash({
        manifest: '../../static/css/manifest.json',
        algorithm: 'md5',
        trim: 8,
      }),
  ].filter(Boolean),
};