#!/usr/bin/env python3
"""Genera la web estática de riushost.com.

Uso:  python3 src/build.py
Lee src/i18n.json (textos de cada idioma) y src/site.json (datos de contacto y legales)
y escribe los HTML en la raíz del repositorio: /, /val/, /en/, /fr/, /pt/, /it/, /de/,
/aviso-legal/, /privacidad/, /cookies/ y sitemap.xml.
"""
import datetime
import json
import os
from html import escape as esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

T = json.load(open(os.path.join(SRC, "i18n.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SRC, "site.json"), encoding="utf-8"))
LANGS = list(T.keys())  # el primero (es) va en la raíz
HTML_LANG = {"es": "es", "val": "ca-ES-valencia", "en": "en", "fr": "fr", "pt": "pt", "it": "it", "de": "de"}
HREFLANG = {"es": "es", "val": "ca", "en": "en", "fr": "fr", "pt": "pt", "it": "it", "de": "de"}
OG_LOCALE = {"es": "es_ES", "val": "ca_ES", "en": "en_GB", "fr": "fr_FR", "pt": "pt_PT", "it": "it_IT", "de": "de_DE"}
TODAY = datetime.date.today().isoformat()
LANG_SHORT = {"es": "ES", "val": "VAL", "en": "EN", "fr": "FR", "pt": "PT", "it": "IT", "de": "DE"}

MUNICIPIOS = ["Valencia", "Alaquàs", "Alboraya", "Aldaia", "Alfafar", "Algemesí", "Almussafes", "Alzira",
              "Benaguasil", "Benetússer", "Bétera", "Burjassot", "Carlet", "Catarroja", "Cheste", "Chiva", "Cullera",
              "El Puig de Santa Maria", "Gandia", "Godella", "L'Alcúdia", "La Pobla de Vallbona", "Llíria", "Manises",
              "Massamagrell", "Meliana", "Mislata", "Moncada", "Museros", "Oliva", "Ontinyent", "Paiporta", "Paterna",
              "Picanya", "Picassent", "Puçol", "Quart de Poblet", "Requena", "Riba-roja de Túria", "Rocafort",
              "Sagunto/Sagunt", "Sedaví", "Silla", "Sueca", "Tavernes de la Valldigna", "Torís", "Torrent", "Utiel",
              "Vilamarxant", "Xàtiva", "Xirivella"]
PREFIXES = [("+34", "Spain (+34)"), ("+33", "France (+33)"), ("+351", "Portugal (+351)"), ("+39", "Italy (+39)"),
            ("+44", "United Kingdom (+44)"), ("+49", "Germany (+49)"), ("+41", "Switzerland (+41)"),
            ("+43", "Austria (+43)"), ("+1", "United States (+1)"), ("+376", "Andorra (+376)")]
DEFAULT_PREFIX = {"fr": "+33", "pt": "+351", "it": "+39", "en": "+44", "de": "+49"}

SERVICE_ICONS = ["🏠", "✨", "🔑", "📅", "📈", "🛠️"]
BENEFIT_ICONS = ["💶", "⏱️", "🛡️", "🤝"]


def path_for(lang):
    return "/" if lang == LANGS[0] else f"/{lang}/"


def write(rel, content):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def head(lang, title, description, canonical, alternates=True, noindex=False):
    t = T[lang]
    alt = ""
    if alternates:
        alt = "\n".join(
            f'  <link rel="alternate" hreflang="{HREFLANG[l]}" href="{S["domain"]}{path_for(l)}" />' for l in LANGS)
        alt += f'\n  <link rel="alternate" hreflang="x-default" href="{S["domain"]}/" />'
    robots = '\n  <meta name="robots" content="noindex" />' if noindex else ""
    return f"""<!doctype html>
<html lang="{HTML_LANG[lang]}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />{robots}
  <link rel="canonical" href="{S['domain']}{canonical}" />
{alt}
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:url" content="{S['domain']}{canonical}" />
  <meta property="og:site_name" content="RiusHost" />
  <meta property="og:locale" content="{OG_LOCALE[lang]}" />
  <meta property="og:image" content="{S['domain']}/assets/og-image.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="theme-color" content="#0f172a" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="preload" href="/assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="/assets/styles.css" />
"""


def lang_switch(current, target_path_fn):
    t = T[current]
    btns = "\n".join(
        f'      <a href="{target_path_fn(l)}" hreflang="{HREFLANG[l]}" lang="{HTML_LANG[l]}" title="{esc(T[l]["langName"])}"'
        f'{" aria-current=\"true\"" if l == current else ""}>{LANG_SHORT[l]}</a>' for l in LANGS)
    return f"""    <nav class="langs" aria-label="{esc(t['header']['changeLanguage'])}">
{btns}
    </nav>"""


def topbar(lang, home, solid=False, nav=True):
    t = T[lang]
    links = ""
    if nav:
        links = f"""    <nav class="nav" id="nav" aria-label="Menu">
      <a href="{home}#servicios">{esc(t['header']['services'])}</a>
      <a href="{home}#como-funciona">{esc(t['header']['how'])}</a>
      <a href="{home}#faq">{esc(t['header']['faq'])}</a>
      <a href="{home}#contacto">{esc(t['header']['contact'])}</a>
      <div class="nav-langs">{"".join(f'<a href="{path_for(l)}" hreflang="{HREFLANG[l]}" lang="{HTML_LANG[l]}"' + (' aria-current="true"' if l == lang else '') + f'>{LANG_SHORT[l]}</a>' for l in LANGS)}</div>
    </nav>"""
    menu_btn = """    <button class="menu-btn" id="menuBtn" aria-controls="nav" aria-expanded="false" aria-label="Menu">
      <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    </button>""" if nav else ""
    return f"""  <header class="topbar{' solid' if solid else ''}" id="top">
    <a class="brand" href="{home}" aria-label="RiusHost">
      <svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path d="M2 6c2-1.5 4-1.5 6 0s4 1.5 6 0 4-1.5 6 0M2 12c2-1.5 4-1.5 6 0s4 1.5 6 0 4-1.5 6 0M2 18c2-1.5 4-1.5 6 0s4 1.5 6 0 4-1.5 6 0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      <span>RiusHost</span>
    </a>
{links}
{lang_switch(lang, path_for) if nav else ''}
{menu_btn}
  </header>
"""


def footer(lang):
    t = T[lang]
    note = t["footer"].get("langNote") or ""
    note_html = f'\n      <p class="small">{esc(note)}</p>' if note else ""
    return f"""  <footer class="footer">
    <div class="wrap">
      <strong>RiusHost</strong>
      <p>{esc(t['footer']['subtitle'])}</p>
      <nav class="legal-links" aria-label="Legal">
        <a href="/aviso-legal/">{esc(t['footer']['legal'])}</a>
        <a href="/privacidad/">{esc(t['footer']['privacy'])}</a>
        <a href="/cookies/">{esc(t['footer']['cookies'])}</a>
      </nav>{note_html}
      <p class="small">{esc(t['footer']['copyright'])}</p>
    </div>
  </footer>
"""


def cards(items, icons, cls="card"):
    return "\n".join(
        f"""          <article class="{cls}">
            <div class="icon" aria-hidden="true">{icons[i] if i < len(icons) else '•'}</div>
            <h3>{esc(it['title'])}</h3>
            <p>{esc(it['description'])}</p>
          </article>""" for i, it in enumerate(items))


def home_page(lang):
    t = T[lang]
    c = t["contact"]
    f = c["form"]
    home = path_for(lang)
    faq = "\n".join(
        f"""          <details>
            <summary>{esc(q['q'])}</summary>
            <p>{esc(q['a'])}</p>
          </details>""" for q in t["faq"]["items"])
    faq_ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in t["faq"]["items"]]
    }, ensure_ascii=False)
    org_id = S["domain"] + "/#empresa"
    biz_ld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ProfessionalService", "@id": org_id, "name": "RiusHost",
                "url": S["domain"] + "/", "email": S["email"], "telephone": S["phoneHref"],
                "logo": S["domain"] + "/assets/logo.png", "image": S["domain"] + "/assets/og-image.jpg",
                "description": t["about"]["text"],
                "slogan": t["hero"]["main"],
                "founder": {"@type": "Person", "name": S["titular"]},
                "address": {"@type": "PostalAddress", "addressLocality": "València", "postalCode": "46006",
                            "addressRegion": "Comunitat Valenciana", "addressCountry": "ES"},
                "areaServed": [{"@type": "City", "name": m if m != "Valencia" else "València"} for m in MUNICIPIOS],
                "availableLanguage": [T[l]["langName"] for l in LANGS],
                "knowsAbout": ["Viviendas de uso turístico", "Airbnb", "Booking.com", "Alquiler vacacional",
                               "Registro de Turismo de la Comunitat Valenciana"],
                "hasOfferCatalog": {
                    "@type": "OfferCatalog", "name": t["services"]["title"],
                    "itemListElement": [{"@type": "Offer", "itemOffered": {
                        "@type": "Service", "name": it["title"], "description": it["description"],
                        "areaServed": "València"}} for it in t["services"]["items"]]
                }
            },
            {
                "@type": "WebSite", "@id": S["domain"] + "/#web", "url": S["domain"] + "/", "name": "RiusHost",
                "publisher": {"@id": org_id}, "inLanguage": [HTML_LANG[l] for l in LANGS]
            },
            {
                "@type": "WebPage", "@id": S["domain"] + home + "#pagina", "url": S["domain"] + home,
                "name": t["meta"]["title"], "description": t["meta"]["description"],
                "inLanguage": HTML_LANG[lang], "isPartOf": {"@id": S["domain"] + "/#web"},
                "about": {"@id": org_id}, "dateModified": TODAY,
                "primaryImageOfPage": S["domain"] + "/assets/og-image.jpg"
            }
        ]
    }, ensure_ascii=False)
    steps = "\n".join(
        f"""          <li>
            <h3>{esc(st['title'])}</h3>
            <p>{esc(st['text'])}</p>
          </li>""" for st in t["how"]["steps"])
    prefix_default = DEFAULT_PREFIX.get(lang, "+34")
    prefixes = "".join(
        f'<option value="{v}"{" selected" if v == prefix_default else ""}>{esc(n)}</option>' for v, n in PREFIXES)
    munis = "".join(f'<option value="{esc(m)}">{esc(m)}</option>' for m in MUNICIPIOS)
    ptypes = "".join(f'<option value="{k}">{esc(v)}</option>' for k, v in f["propertyTypes"].items())
    consent = esc(f["consent"]).replace(
        "{privacy}", f'<a href="/privacidad/" target="_blank" rel="noopener">{esc(f["privacyLink"])}</a>')
    msgs = json.dumps({k: c[k] for k in c if k.startswith("toast")} | {"consentError": f["consentError"]},
                      ensure_ascii=False)

    return head(lang, t["meta"]["title"], t["meta"]["description"], home) + f"""  <script type="application/ld+json">{biz_ld}</script>
  <script type="application/ld+json">{faq_ld}</script>
  <link rel="preload" as="image" type="image/webp" imagesrcset="/assets/hero-800.webp 800w, /assets/hero-1280.webp 1280w, /assets/hero-1600.webp 1600w" imagesizes="100vw" fetchpriority="high" />
</head>
<body>
{topbar(lang, home)}
  <section class="hero">
    <picture>
      <source type="image/webp" srcset="/assets/hero-800.webp 800w, /assets/hero-1280.webp 1280w, /assets/hero-1600.webp 1600w" sizes="100vw" />
      <img class="hero-img" src="/assets/hero-1280.jpg" width="1600" height="1198" alt="{esc(t['heroAlt'])}" fetchpriority="high" decoding="async" onerror="this.remove()" />
    </picture>
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <h1>{esc(t['hero']['main'])}</h1>
      <p>{esc(t['hero']['sub'])}</p>
      <a class="btn" href="#contacto">{esc(t['hero']['button'])}</a>
    </div>
  </section>

  <main>
    <section class="section" id="servicios">
      <div class="wrap">
        <h2>{esc(t['services']['title'])}</h2>
        <p class="lead">{esc(t['services']['subtitle'])}</p>
        <div class="grid grid-3">
{cards(t['services']['items'], SERVICE_ICONS)}
        </div>
      </div>
    </section>

    <section class="section alt" id="como-funciona">
      <div class="wrap">
        <h2>{esc(t['how']['title'])}</h2>
        <p class="lead">{esc(t['how']['subtitle'])}</p>
        <ol class="steps">
{steps}
        </ol>
      </div>
    </section>

    <section class="section" id="beneficios">
      <div class="wrap">
        <h2>{esc(t['benefits']['title'])}</h2>
        <p class="lead">{esc(t['benefits']['subtitle'])}</p>
        <div class="grid grid-4">
{cards(t['benefits']['items'], BENEFIT_ICONS, 'card benefit')}
        </div>

        <div class="banner">
          <h3>{esc(t['benefits']['bannerTitle'])}</h3>
          <p>{esc(t['benefits']['bannerSubtitle'])}</p>
        </div>

        <h2 class="mt">{esc(t['benefits']['pricing']['title'])}</h2>
        <p class="lead">{esc(t['benefits']['pricing']['subtitle'])}</p>
        <div class="grid grid-2">
          <article class="card price">
            <h3>{esc(t['benefits']['pricing']['fixed']['title'])}</h3>
            <p>{esc(t['benefits']['pricing']['fixed']['description'])}</p>
          </article>
          <article class="card price">
            <h3>{esc(t['benefits']['pricing']['percentage']['title'])}</h3>
            <p>{esc(t['benefits']['pricing']['percentage']['description'])}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section alt" id="sobre-riushost">
      <div class="wrap narrow about">
        <h2>{esc(t['about']['title'])}</h2>
        <p>{esc(t['about']['text'])}</p>
      </div>
    </section>

    <section class="section" id="faq">
      <div class="wrap narrow">
        <h2>{esc(t['faq']['title'])}</h2>
        <p class="lead">{esc(t['faq']['subtitle'])}</p>
        <div class="faq">
{faq}
        </div>
      </div>
    </section>

    <section class="section alt" id="contacto">
      <div class="wrap">
        <h2>{esc(c['title'])}</h2>
        <p class="lead">{esc(c['subtitle'])}</p>
        <div class="contact">
          <aside class="card contact-card">
            <h3>{esc(c['cardTitle'])}</h3>
            <p>{esc(c['cardSubtitle'])}</p>
            <dl>
              <dt>{esc(c['email'])}</dt>
              <dd><a href="mailto:{S['email']}">{S['email']}</a></dd>
              <dt>{esc(c['phone'])}</dt>
              <dd><a href="tel:{S['phoneHref']}">{S['phone']}</a></dd>
            </dl>
            <p class="trust">{esc(c['trust'])}</p>
          </aside>

          <form class="card form" id="contactForm" novalidate>
            <label for="f-nombre"><span>{esc(f['name'])}</span></label>
            <input id="f-nombre" name="nombre" type="text" required autocomplete="name" placeholder="{esc(f['namePlaceholder'])}" />
            <label for="f-email"><span>{esc(f['email'])}</span></label>
            <input id="f-email" name="email" type="email" required autocomplete="email" placeholder="{esc(f['emailPlaceholder'])}" />
            <label for="f-tel"><span>{esc(f['phone'])}</span></label>
            <span class="row">
              <select id="f-prefix" name="phonePrefix" aria-label="{esc(f['phonePrefix'])}">{prefixes}</select>
              <input id="f-tel" name="phoneNumber" type="tel" required autocomplete="tel-national" placeholder="{esc(f['phonePlaceholder'])}" />
            </span>
            <label for="f-location"><span>{esc(f['location'])}</span></label>
            <select id="f-location" name="location" required><option value="" disabled selected>{esc(f['location'])}</option>{munis}</select>
            <span class="row two">
              <span class="field">
                <label for="f-ptype"><span>{esc(f['propertyType'])}</span></label>
                <select id="f-ptype" name="propertyType" required><option value="" disabled selected>{esc(f['propertyType'])}</option>{ptypes}</select>
              </span>
              <span class="field">
                <label for="f-rooms"><span>{esc(f['rooms'])}</span></label>
                <select id="f-rooms" name="rooms" required><option value="" disabled selected>—</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6+</option></select>
              </span>
            </span>
            <label for="f-msg"><span>{esc(f['message'])}</span></label>
            <textarea id="f-msg" name="mensaje" rows="4" placeholder="{esc(f['messagePlaceholder'])}"></textarea>
            <label class="consent" for="f-consent">
              <input id="f-consent" name="consent" type="checkbox" required />
              <span>{consent}</span>
            </label>
            <button class="btn" type="submit">{esc(f['button'])}</button>
            <p class="status" id="formStatus" role="status" aria-live="polite"></p>
          </form>
        </div>
      </div>
    </section>
  </main>

{footer(lang)}
  <script id="rh-msgs" type="application/json">{msgs}</script>
  <script src="/assets/vendor/emailjs-4.4.1.min.js" defer></script>
  <script src="/assets/main.js" defer></script>
</body>
</html>
"""


def md_to_html(text):
    """Mini-markdown: '## ' títulos, '- ' listas, párrafos. Sustituye {clave} por site.json."""
    for k, v in S.items():
        text = text.replace("{" + k + "}", esc(str(v)))
    out, in_list = [], False
    for block in text.strip().split("\n\n"):
        lines = block.strip().split("\n")
        if lines[0].startswith("## "):
            out.append(f"<h2>{lines[0][3:]}</h2>")
            lines = lines[1:]
            if not lines:
                continue
        if all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{l[2:]}</li>" for l in lines) + "</ul>")
        else:
            out.append("<p>" + "<br />".join(lines) + "</p>")
    return "\n        ".join(out)


def legal_page(slug, title):
    lang = LANGS[0]
    body = md_to_html(open(os.path.join(SRC, "legal", f"{slug}.md"), encoding="utf-8").read())
    return head(lang, f"{title} · RiusHost", f"{title} de RiusHost.", f"/{slug}/", alternates=False) + f"""</head>
<body class="legal-page">
{topbar(lang, '/', solid=True, nav=False)}
  <main class="section">
    <div class="wrap narrow legal">
      <p><a href="/">← RiusHost</a></p>
      <h1>{esc(title)}</h1>
      <p class="small">Última actualización: {esc(S['legalUpdated'])}</p>
        {body}
    </div>
  </main>
{footer(lang)}
</body>
</html>
"""


def sitemap():
    urls = [path_for(l) for l in LANGS] + ["/aviso-legal/", "/privacidad/", "/cookies/"]
    items = []
    for u in urls:
        alts = ""
        if u in [path_for(l) for l in LANGS]:
            alts = "".join(
                f'\n    <xhtml:link rel="alternate" hreflang="{HREFLANG[l]}" href="{S["domain"]}{path_for(l)}" />'
                for l in LANGS)
        items.append(f"  <url>\n    <loc>{S['domain']}{u}</loc>\n    <lastmod>{TODAY}</lastmod>{alts}\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(items) + "\n</urlset>\n")


def not_found_page():
    lang = LANGS[0]
    links = " · ".join(f'<a href="{path_for(l)}" lang="{HTML_LANG[l]}">{esc(T[l]["notFound"]["button"])}</a>'
                       for l in LANGS)
    t = T[lang]["notFound"]
    return head(lang, f"{t['title']} · RiusHost", t["text"], "/404.html", alternates=False, noindex=True) + f"""</head>
<body class="legal-page">
{topbar(lang, '/', solid=True, nav=False)}
  <main class="section">
    <div class="wrap narrow legal" style="text-align:center">
      <h1>{esc(t['title'])}</h1>
      <p>{esc(t['text'])}</p>
      <p><a class="btn" href="/">{esc(t['button'])}</a></p>
      <p class="small">{links}</p>
    </div>
  </main>
{footer(lang)}
</body>
</html>
"""


def llms_txt():
    es, en = T["es"], T["en"]
    lines = [
        "# RiusHost",
        "",
        f"> {en['about']['text']}",
        "",
        f"- Website: {S['domain']}/ (Spanish), with versions in "
        + ", ".join(f"{T[l]['langName']} ({S['domain']}{path_for(l)})" for l in LANGS[1:]),
        f"- Email: {S['email']}",
        f"- Phone: {S['phone']}",
        "- Location: València, Comunitat Valenciana, Spain (postal code 46006)",
        "- Service area: València city and its metropolitan area: " + ", ".join(m for m in MUNICIPIOS if m != "Valencia"),
        "- Billing: fixed monthly fee or a percentage of the rental income, chosen by the owner",
        "",
        "## Services",
        "",
    ]
    lines += [f"- {it['title']}: {it['description']}" for it in en["services"]["items"]]
    lines += ["", "## How it works", ""]
    lines += [f"{i}. {st['title']}: {st['text']}" for i, st in enumerate(en["how"]["steps"], 1)]
    lines += ["", "## FAQ", ""]
    lines += [f"- {q['q']} {q['a']}" for q in en["faq"]["items"]]
    lines += ["", "## Pages", ""]
    lines += [f"- [{T[l]['langName']}]({S['domain']}{path_for(l)}): {T[l]['meta']['description']}" for l in LANGS]
    lines += [f"- [Aviso legal]({S['domain']}/aviso-legal/)", f"- [Política de privacidad]({S['domain']}/privacidad/)"]
    lines += ["", "## Resumen en castellano", "", es["about"]["text"], ""]
    return "\n".join(lines)


def robots_txt():
    bots = ["Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
            "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended",
            "DuckAssistBot", "CCBot"]
    out = ["# Buscadores y asistentes de IA son bienvenidos.", ""]
    for b in bots:
        out += [f"User-agent: {b}", "Allow: /", ""]
    out += ["User-agent: *", "Allow: /", "", f"Sitemap: {S['domain']}/sitemap.xml", ""]
    return "\n".join(out)


def main():
    for lang in LANGS:
        rel = "index.html" if lang == LANGS[0] else f"{lang}/index.html"
        write(rel, home_page(lang))
    for slug, title in [("aviso-legal", "Aviso legal"), ("privacidad", "Política de privacidad"),
                        ("cookies", "Política de cookies")]:
        write(f"{slug}/index.html", legal_page(slug, title))
    write("sitemap.xml", sitemap())
    write("404.html", not_found_page())
    write("llms.txt", llms_txt())
    write("robots.txt", robots_txt())
    print("OK:", ", ".join(path_for(l) for l in LANGS), "+ legales, 404, sitemap.xml, llms.txt, robots.txt")


if __name__ == "__main__":
    main()
