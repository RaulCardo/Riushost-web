(function () {
  'use strict';
  var T = window.RH_I18N;
  var LANGS = ['es', 'val', 'en', 'fr', 'pt', 'it'];
  var HTML_LANG = { es: 'es', val: 'ca-valencia', en: 'en', fr: 'fr', pt: 'pt', it: 'it' };

  // Same EmailJS account the Hostinger site uses (public client-side keys).
  var EMAILJS = { publicKey: 'nLv6KjhM5OoTyp8r5', service: 'service_ge40s2i', template: 'template_54os28u' };

  var MUNICIPIOS = ['Valencia', 'Alaquàs', 'Alboraya', 'Aldaia', 'Alfafar', 'Algemesí', 'Almussafes', 'Alzira',
    'Benaguasil', 'Benetússer', 'Bétera', 'Burjassot', 'Carlet', 'Catarroja', 'Cheste', 'Chiva', 'Cullera',
    'El Puig de Santa Maria', 'Gandia', 'Godella', "L'Alcúdia", 'La Pobla de Vallbona', 'Llíria', 'Manises',
    'Massamagrell', 'Meliana', 'Mislata', 'Moncada', 'Museros', 'Oliva', 'Ontinyent', 'Paiporta', 'Paterna',
    'Picanya', 'Picassent', 'Puçol', 'Quart de Poblet', 'Requena', 'Riba-roja de Túria', 'Rocafort',
    'Sagunto/Sagunt', 'Sedaví', 'Silla', 'Sueca', 'Tavernes de la Valldigna', 'Torís', 'Torrent', 'Utiel',
    'Vilamarxant', 'Xàtiva', 'Xirivella'];

  var SERVICE_ICONS = ['🏠', '✨', '🔑', '📅', '📈', '🛠️'];
  var BENEFIT_ICONS = ['💶', '⏱️', '🛡️', '🤝'];

  function get(obj, path) {
    return path.split('.').reduce(function (o, k) { return o == null ? o : o[k]; }, obj);
  }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; }
  }

  var current = 'es';

  function render(lang) {
    var t = T[lang] || T.es;
    current = lang;
    document.documentElement.lang = HTML_LANG[lang];

    document.querySelectorAll('[data-i18n]').forEach(function (n) {
      var v = get(t, n.getAttribute('data-i18n'));
      if (typeof v === 'string') n.textContent = v;
    });
    document.querySelectorAll('[data-i18n-ph]').forEach(function (n) {
      var v = get(t, n.getAttribute('data-i18n-ph'));
      if (typeof v === 'string') n.placeholder = v;
    });
    document.querySelectorAll('[data-i18n-aria]').forEach(function (n) {
      var v = get(t, n.getAttribute('data-i18n-aria'));
      if (typeof v === 'string') n.setAttribute('aria-label', v);
    });

    var sg = document.getElementById('servicesGrid');
    sg.textContent = '';
    t.services.items.forEach(function (it, i) {
      var c = el('article', 'card');
      c.appendChild(el('div', 'icon', SERVICE_ICONS[i] || '•'));
      c.appendChild(el('h3', null, it.title));
      c.appendChild(el('p', null, it.description));
      sg.appendChild(c);
    });

    var bg = document.getElementById('benefitsGrid');
    bg.textContent = '';
    t.benefits.items.forEach(function (it, i) {
      var c = el('article', 'card benefit');
      c.appendChild(el('div', 'icon', BENEFIT_ICONS[i] || '•'));
      c.appendChild(el('h3', null, it.title));
      c.appendChild(el('p', null, it.description));
      bg.appendChild(c);
    });

    var loc = document.getElementById('location');
    var locVal = loc.value;
    loc.textContent = '';
    var o0 = el('option', null, t.contact.form.location); o0.value = ''; o0.disabled = true; loc.appendChild(o0);
    MUNICIPIOS.forEach(function (m) { var o = el('option', null, m); o.value = m; loc.appendChild(o); });
    loc.value = locVal || '';

    var pt = document.getElementById('propertyType');
    var ptVal = pt.value;
    pt.textContent = '';
    var p0 = el('option', null, t.contact.form.propertyType); p0.value = ''; p0.disabled = true; pt.appendChild(p0);
    Object.keys(t.contact.form.propertyTypes).forEach(function (k) {
      var o = el('option', null, t.contact.form.propertyTypes[k]); o.value = k; pt.appendChild(o);
    });
    pt.value = ptVal || '';

    document.querySelectorAll('[data-lang]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-lang') === lang ? 'true' : 'false');
    });
    store('rh-lang', lang);
  }

  document.querySelectorAll('[data-lang]').forEach(function (b) {
    b.addEventListener('click', function () { render(b.getAttribute('data-lang')); });
  });

  var menuBtn = document.getElementById('menuBtn');
  var nav = document.getElementById('nav');
  menuBtn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') { nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); }
  });

  var form = document.getElementById('contactForm');
  var status = document.getElementById('formStatus');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var c = (T[current] || T.es).contact;
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var f = new FormData(form);
    var params = {
      to_email: 'info@riushost.com',
      from_name: f.get('nombre'),
      from_email: f.get('email'),
      phone: f.get('phonePrefix') + ' ' + f.get('phoneNumber'),
      municipality: f.get('location'),
      property_type: f.get('propertyType'),
      rooms: f.get('rooms'),
      message: f.get('mensaje') || 'No message provided',
      submission_date: new Date().toLocaleString()
    };
    if (!window.emailjs) {
      status.className = 'status err';
      status.textContent = c.toastConfigErrorTitle + ' ' + c.toastConfigErrorDescription;
      return;
    }
    var btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    window.emailjs.init({ publicKey: EMAILJS.publicKey });
    window.emailjs.send(EMAILJS.service, EMAILJS.template, params).then(function () {
      status.className = 'status ok';
      status.textContent = c.toastSuccessTitle + ' ' + c.toastSuccessDescription;
      form.reset();
      render(current);
    }, function () {
      status.className = 'status err';
      status.textContent = c.toastErrorTitle + ' ' + c.toastErrorDescription;
    }).then(function () { btn.disabled = false; });
  });

  var saved = store('rh-lang');
  var nav0 = (navigator.language || 'es').toLowerCase();
  var guess = nav0.indexOf('ca') === 0 ? 'val' : nav0.slice(0, 2);
  render(LANGS.indexOf(saved) >= 0 ? saved : (LANGS.indexOf(guess) >= 0 ? guess : 'es'));
})();
