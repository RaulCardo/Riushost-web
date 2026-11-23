# riushost.com (versión estática)

Web estática (HTML + CSS + JS, sin build) que replica la web de Hostinger Horizons.

- `index.html`: estructura de la página (una sola página con secciones).
- `assets/i18n.js`: todos los textos en 6 idiomas (es, val, en, fr, pt, it), extraídos de la web original.
- `assets/main.js`: cambio de idioma, menú móvil y envío del formulario con EmailJS (mismas claves que la web actual).
- `assets/styles.css`: estilos.
- `assets/hero.jpg`: FALTA. Foto de portada (Torres de Serrano / Turia). Descargarla de la web actual antes de cancelar Hostinger.

Para editar un texto: cambiarlo en `assets/i18n.js` en cada idioma.
Para publicar: subir esta carpeta tal cual a Cloudflare Pages / Netlify / GitHub Pages (sin comando de build).
