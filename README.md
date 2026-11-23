# riushost.com

Web estática de RiusHost, publicada con GitHub Pages en https://riushost.com.

## Cómo está hecha

Las páginas HTML se generan con un script de Python, sin dependencias:

```
python3 src/build.py
```

- `src/i18n.json`: todos los textos en 7 idiomas (es, val, en, fr, pt, it, de), incluidas las preguntas frecuentes.
- `src/site.json`: email, teléfono y datos legales (titular, NIF, dirección).
- `src/legal/*.md`: textos de aviso legal, privacidad y cookies (en castellano).
- `src/build.py`: genera `/index.html` (castellano), `/val/`, `/en/`, `/fr/`, `/pt/`, `/it/`, `/de/`, las páginas legales y `sitemap.xml`.

Para cambiar un texto: editar `src/i18n.json` (o `src/legal/`), ejecutar el script y subir también los HTML generados.

## Recursos

- `assets/styles.css`, `assets/main.js`: estilos, menú móvil y envío del formulario con EmailJS.
- `assets/fonts/`: fuente Inter servida desde la propia web (licencia OFL en `LICENSE-Inter.txt`).
- `assets/vendor/emailjs-4.4.1.min.js`: librería de EmailJS servida desde la propia web.
- `assets/hero.jpg`: foto de portada (vista aérea de València, Egor Kunovsky en Pexels; licencia Pexels).
- `CNAME`: dominio personalizado de GitHub Pages.
