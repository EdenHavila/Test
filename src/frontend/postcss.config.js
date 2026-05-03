module.exports = {
  plugins: [
    require('postcss-import'),           // Résout les @import
    require('postcss-prefixwrap')('.mon-bootstrap'), // Encapsule tout le CSS dans .mon-bootstrap
    require('autoprefixer')              // Compatibilité navigateurs
  ]
}
