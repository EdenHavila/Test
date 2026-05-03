// Importer Alpine.js et HTMX globalement
import Alpine from 'alpinejs'
import htmx from 'htmx.org'

window.Alpine = Alpine
Alpine.start()

window.htmx = htmx;

// Tu peux ajouter ton code JS personnalisé ici
console.log("Django + Alpine + HTMX ready!")
