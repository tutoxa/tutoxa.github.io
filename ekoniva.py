"""Local EkoNiva case study, using the existing verified project record."""
from html import escape
from urllib.parse import urlsplit


def render_ekoniva(project, collection, lang):
    index = 0 if lang == 'en' else 1

    def text(value):
        return escape(value[index] if isinstance(value, list) else value)

    def local_url(value):
        return value if value and value.startswith('/') and not value.startswith('//') else None

    def publication_url(value):
        return value if value and urlsplit(value).scheme == 'https' else None

    def media(item):
        src = local_url(item.get('src'))
        poster = local_url(item.get('poster'))
        title = text(item['title'])
        if src and item['type'] == 'image':
            responsive = (f' srcset="{escape(item["srcset"])}" sizes="{escape(item.get("sizes", "100vw"))}"' if item.get('srcset') else '')
            return (f'<img src="{escape(src)}" alt="{text(item["alt"])}" '
                    f'width="{item["width"]}" height="{item["height"]}" loading="lazy" decoding="async"{responsive}>')
        if src and poster and item['type'] == 'video':
            return (f'<video controls playsinline preload="none" poster="{escape(poster)}" '
                    f'width="{item["width"]}" height="{item["height"]}" aria-label="{title}" {"muted" if item.get("silent_preview") else ""}>'
                    f'<source src="{escape(src)}" type="video/mp4"><p>{["Video unavailable. Please try the publication link.", "Video nicht verfügbar. Bitte den Veröffentlichungslink nutzen."][index]}</p></video>')
        return f'<div class="ek-slot"><span>{text(collection["slot_label"])}</span><strong>{title}</strong><small>{text(collection["media_pending"])}</small></div>'

    panels, entries = [], []
    for number, item in enumerate(collection['items'], 1):
        panels.append(
            f'<li class="ek-panel" role="group" aria-roledescription="{["slide", "Folie"][index]}" '
            f'aria-label="{number} / {len(collection["items"])} — {text(item["title"])}">'
            f'{media(item)}<div class="ek-panel-caption">{text(item["format"])}</div></li>'
        )
        year = f' · {text(item["year"])}' if item.get('year') else ''
        link = publication_url(item.get('external_url'))
        external = (f'<a href="{escape(link)}" target="_blank" rel="noopener noreferrer">'
                    f'{["View publication", "Veröffentlichung ansehen"][index]} ↗</a>') if link else ''
        contribution = item.get('contribution') or collection['contribution_pending']
        entries.append(f'<article class="ek-work-row"><h3>{text(item["title"])}</h3><span>{text(item["format"])}{year}</span><p>{text(contribution)}</p>{external}</article>')

    behind = ''
    for number, item in enumerate(collection['behind'], 1):
        image = media(item)
        src = local_url(item.get('src'))
        if src:
            label = [f'Open production photograph {number}', f'Produktionsfoto {number} öffnen'][index]
            image = f'<a class="ek-gallery-link" href="{escape(src)}" target="_blank" rel="noopener noreferrer" aria-label="{label}">{image}</a>'
        caption = f'<figcaption>{text(item["caption"])}</figcaption>' if item.get('caption') else ''
        behind += f'<figure class="{"ek-production-featured" if item.get("featured") else ""}">{image}{caption}</figure>'
    source_note = ''
    sources = collection.get('production_sources')
    if sources:
        source_links = ''.join(
            f'<a href="{escape(sources[key])}" target="_blank" rel="noopener noreferrer">{label} ↗</a>'
            for key, label in [('article', 'EkoNiva'), ('article_credit', 'Milknews')]
            if publication_url(sources.get(key))
        )
        video_links = ''.join(
            f'<a href="{escape(video["url"])}" target="_blank" rel="noopener noreferrer">{text(video["title"])} ↗</a>'
            for video in sources.get('videos', []) if publication_url(video.get('url'))
        )
        source_note = f'<div class="ek-production-source"><p>{text(sources["note"])}</p><div class="ek-source-links">{source_links}</div><p>{text(sources["videos_label"])}</p><div class="ek-source-links">{video_links}</div></div>'
    base = '/' if index == 0 else '/de.html'
    roles = ''.join(f'<li>{escape(role)}</li>' for role in project['role'][index])
    headings = collection['headings']
    return f"""
<div class="ek-case">
 <section class="ek-intro" aria-labelledby="ek-title">
  <a class="text-link" href="{base}#work">← {["All work", "Alle Projekte"][index]}</a>
  <p class="ek-credit">{escape(project['org'])} · {escape(project['year'])}</p>
  <h1 id="ek-title">{text(collection['title'])}</h1>
  <p class="ek-introduction">{text(collection['intro'])}</p>
  <p class="ek-role">{text(collection['role'])}</p>
 </section>
 <section id="ek-showcase" class="ek-showcase" aria-label="{text(collection['showcase_label'])}" aria-roledescription="{["carousel", "Karussell"][index]}" tabindex="0"
          data-status="{["Media slot", "Medienplatz"][index]}">
  <p class="ek-preview-note">{text(collection['review_note'])}</p>
  <ol class="ek-panels">{''.join(panels)}</ol>
  <div class="ek-controls" hidden>
   <button type="button" data-direction="-1" aria-label="{["Previous media", "Vorheriges Medium"][index]}">←</button>
   <p class="ek-status" role="status" aria-live="polite" aria-atomic="true"></p>
   <button type="button" data-direction="1" aria-label="{["Next media", "Nächstes Medium"][index]}">→</button>
  </div>
 </section>
 <section class="ek-editorial" aria-labelledby="ek-context">
  <h2 id="ek-context">{text(headings[0])}</h2><p>{text(project['context'])}</p>
  <h2>{text(headings[1])}</h2><div><p>{text(collection['collaboration'])}</p><ul class="ek-responsibilities">{roles}</ul></div>
 </section>
 <section class="ek-work" aria-labelledby="ek-selected">
  <div class="ek-section-heading"><h2 id="ek-selected">{text(headings[2])}</h2><p>{text(collection['work_note'])}</p></div>
  {''.join(entries)}
 </section>
 <section id="commercial-production" class="ek-behind" aria-labelledby="ek-production">
  <div class="ek-section-heading"><h2 id="ek-production">{text(headings[3])}</h2><p>{text(collection['behind_note'])}</p></div>
  <div class="ek-behind-grid">{behind}</div>{source_note}
 </section>
 <section class="ek-editorial ek-contribution" aria-labelledby="ek-contribution">
  <h2 id="ek-contribution">{text(headings[4])}</h2><div><p>{text(project['process'])}</p><p>{text(collection['collaboration'])}</p></div>
 </section>
 <a class="text-link ek-back" href="{base}#work">{["Back to selected work", "Zurück zu den Projekten"][index]} ↗</a>
</div>"""
