(function () {
  'use strict';

  // Same EmailJS account the Hostinger site used (public client-side keys).
  var EMAILJS = { publicKey: 'nLv6KjhM5OoTyp8r5', service: 'service_ge40s2i', template: 'template_54os28u' };

  // Solid header after scrolling past the hero top
  var bar = document.getElementById('top');
  function onScroll() { if (bar) bar.classList.toggle('scrolled', window.scrollY > 40); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  var menuBtn = document.getElementById('menuBtn');
  var nav = document.getElementById('nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Contact form
  var form = document.getElementById('contactForm');
  if (!form) return;
  var status = document.getElementById('formStatus');
  var M = {};
  try { M = JSON.parse(document.getElementById('rh-msgs').textContent); } catch (e) { M = {}; }

  function show(ok, title, text) {
    status.className = 'status ' + (ok ? 'ok' : 'err');
    status.textContent = (title ? title + ' ' : '') + (text || '');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var consent = document.getElementById('f-consent');
    if (consent && !consent.checked) { show(false, '', M.consentError); consent.focus(); return; }
    if (!form.checkValidity()) { form.reportValidity(); return; }
    if (!window.emailjs) { show(false, M.toastConfigErrorTitle, M.toastConfigErrorDescription); return; }

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
      language: document.documentElement.lang,
      submission_date: new Date().toLocaleString()
    };
    var btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    window.emailjs.init({ publicKey: EMAILJS.publicKey });
    window.emailjs.send(EMAILJS.service, EMAILJS.template, params).then(function () {
      show(true, M.toastSuccessTitle, M.toastSuccessDescription);
      form.reset();
    }, function () {
      show(false, M.toastErrorTitle, M.toastErrorDescription);
    }).then(function () { btn.disabled = false; });
  });
})();
