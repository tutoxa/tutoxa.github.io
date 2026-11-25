"""Editorial CLIMATECH cases; copy and replaceable media live in climatech-cases.json."""
from html import escape


def render_climatech_case(slug, collection, lang, preview=False):
    i = 0 if lang == 'en' else 1
    case = collection[slug]
    home = '/de.html' if i else '/'

    def text(value):
        return escape(value[i] if isinstance(value, list) else value)

    def photo(key, eager=False):
        asset = collection['media'][key]
        return (f'<figure class="ce-photo ce-photo-{key}"><img src="{escape(asset["src"])}" '
                f'srcset="{escape(asset["srcset"])}" sizes="(max-width: 650px) 92vw, 50vw" '
                f'width="{asset["width"]}" height="{asset["height"]}" alt="{text(asset["alt"])}" '
                f'loading="{"eager" if eager else "lazy"}" decoding="async">'
                f'<figcaption>{text(asset["alt"])}</figcaption></figure>')

    blocks = []
    for section in case['sections']:
        visuals = ''.join(photo(key) for key in section.get('photos', []))
        video = section.get('video')
        if video:
            if preview or video.get("public"):
                visuals += (f'<figure class="ce-video"><video controls muted playsinline preload="none" '
                           f'poster="{escape(video["poster"])}" aria-label="{text(section["title"])}">'
                           f'<source src="{escape(video["src"])}" type="video/mp4"></video>'
                           f'<figcaption>{text(video["caption"])}</figcaption></figure>')
            else:
                visuals += ('<figure class="ce-video"><img '
                           f'src="{escape(video["poster"])}" width="540" height="960" '
                           f'alt="{text(section["title"])}" loading="lazy">'
                           f'<figcaption>{text(video.get("fallback_caption", ["Production still. Final Instagram media link pending.", "Produktionsstill. Link zum finalen Instagram-Beitrag folgt."]))}</figcaption></figure>')
        if section.get('embed'):
            embed = section['embed']
            visuals += (f'<figure class="ce-instagram"><iframe src="{escape(embed["src"])}" '
                        f'title="{text(embed["title"])}" loading="lazy" width="470" height="720" '
                        f'allow="fullscreen; picture-in-picture" allowfullscreen '
                        f'referrerpolicy="strict-origin-when-cross-origin"></iframe>'
                        f'<figcaption><a class="text-link" href="{escape(embed["url"])}" '
                        f'target="_blank" rel="noopener noreferrer">{text(embed["label"])} ↗</a></figcaption></figure>')
        if section.get('reference_photo'):
            visuals += photo(section['reference_photo'])
        note = f'<p class="ce-note">{text(section["note"])}</p>' if section.get('note') else ''
        blocks.append(f'''<section class="ce-section" id="{section['id']}">
          <div class="ce-section-copy"><p class="eyebrow">{text(section['label'])}</p>
            <h2>{text(section['title'])}</h2><p>{text(section['body'])}</p>{note}</div>
          <div class="ce-gallery ce-gallery-{len(section.get('photos', []))}">{visuals}</div>
        </section>''')
    responsibility = ''
    if case.get('responsibilities'):
        role = case['responsibilities']
        responsibility = f'<section class="ce-responsibilities"><h2>{text(role["title"])}</h2><p>{text(role["body"])}</p></section>'
    return f'''<article class="ce-case{' ce-schau' if slug == 'technical-careers' else ''}">
      <header class="ce-intro"><a class="text-link" href="{home}#work">← {['All work','Alle Projekte'][i]}</a>
        <p class="eyebrow">CLIMATECH Montage GmbH · {text(case.get("year", "2025–2026"))}</p>
        <h1>{text(case['title'])}</h1>
        <div class="ce-intro-grid"><p class="ce-deck">{text(case['intro'])}</p>
          <p class="ce-role"><span>{['My role','Meine Rolle'][i]}</span>{text(case['role'])}</p></div>
      </header>
      <div class="ce-opening">{photo(case['hero'], True)}</div>
      <nav class="ce-index" aria-label="{['Case sections','Projektabschnitte'][i]}">
        {''.join(f'<a href="#{s["id"]}">{text(s["label"])}</a>' for s in case['sections'])}</nav>
      {''.join(blocks)}{responsibility}
      <a class="ce-back text-link" href="{home}#work">← {['Back to selected work','Zurück zu den Projekten'][i]}</a>
    </article>'''
