"""Presentation for the editorial homepage; editable copy lives in content.json."""
from html import escape as E


def render_home(lang, projects, config, translations, experience, path, links, copy):
    i = 0 if lang == 'en' else 1
    t = translations[lang]
    def tx(key): return E(copy[key][i])
    def rich(key): return E(copy[key][i]).replace('&lt;br&gt;', '<br>').replace('&lt;em&gt;', '<em>').replace('&lt;/em&gt;', '</em>')
    def image(src, alt, width, height, eager=False, srcset=None, sizes='90vw', extra=''):
        responsive = f' srcset="{E(srcset)}" sizes="{sizes}"' if srcset else ''
        return f'<img src="{src}" alt="{E(alt)}" width="{width}" height="{height}" loading="{"eager" if eager else "lazy"}" decoding="async"{responsive}{" fetchpriority=high" if eager else ""} {extra}>'
    p = next((p for p in projects if p['slug'] == config.get('featured_project')), projects[0])
    featured = p.get('featured', {})
    def project_image(project, eager=False, sizes='(max-width: 700px) 90vw, 45vw'):
        return image(E(project['cover']), project.get('cover_alt',project['title'])[i], project.get('cover_width',1600), project.get('cover_height',1100), eager, project.get('cover_srcset'), sizes)
    feature_image = project_image(p, True, '(max-width: 700px) 92vw, 62vw') if p.get('cover') else f'<div class="ed-feature-blank"><span>{E(p["title"][i])}</span><small>{tx("placeholder")}</small></div>'
    detail = featured.get('detail')
    people = image(E(detail['src']), detail['alt'][i], detail['width'], detail['height'], True, detail.get('srcset'), '(max-width: 700px) 34vw, 30vw') if detail else ''
    people_block = f'<div class="ed-people">{people}</div>' if detail else ''
    feature_summary = E(featured.get('summary',p['intro'])[i])
    feature_scope = featured.get('scope',[p['cats'][0].split(' · '),p['cats'][1].split(' · ')])[i]
    cards = []
    for n, project in enumerate((q for q in projects if q is not p), 2):
        title = E(project['title'][i]); href = path(lang, project['slug'])
        visual_title = E(project.get('home_visual_title',project['title'])[i]).replace('&lt;br&gt;', '<br>')
        if project.get('cover'):
            cover = f'<a class="ed-cover ed-cover-photo" href="{href}" aria-label="{title}">{project_image(project)}</a>'
        else:
            cover = f'<a class="ed-cover" href="{href}" aria-label="{title}"><span class="ed-cover-top"><span>{n:02}</span><span>{E(project["year"])}</span></span><span class="ed-cover-title">{visual_title}</span><span class="ed-cover-note">{tx("placeholder")}</span></a>'
        cards.append(f'''<article class="ed-project ed-project-{n}">
          {cover}
          <div class="ed-project-info"><p class="ed-meta">{E(project['org'])}</p><h3><a href="{href}">{title} <span aria-hidden="true">↗</span></a></h3><p class="ed-project-intro">{E(project['intro'][i])}</p><p class="ed-cats">{E(project['cats'][i])}</p><a class="ed-link" href="{href}">{tx('view_case')} <span aria-hidden="true">↗</span></a></div>
        </article>''')
    rows = []
    for year, org, roles, location, description in experience:
        location = location if not i else location.replace('Germany', 'Deutschland').replace('Moscow, Russia', 'Moskau, Russland')
        name = org if not i else org.replace('Leipzig University','Universität Leipzig').replace('German Russian House','Deutsch-Russisches Haus')
        rows.append(f'<details class="ed-timeline-row"><summary><span class="ed-year">{year}</span><h3>{E(name)}</h3><span class="ed-job">{E(roles[i])}</span><span class="ed-expand" aria-hidden="true">+</span></summary><div class="ed-job-detail"><p>{E(description[i])}</p><small>{E(location)}</small></div></details>')
    capabilities = ''.join(f'<article><span class="ed-counter">0{n}</span><h3>{E(c["title"][i])}</h3><p>{E(c["text"][i])}</p></article>' for n,c in enumerate(copy['capabilities'],1))
    education = [
        ('2022–2025', ['Leipzig University','Universität Leipzig'], ['Master’s Degree in European Studies','Masterabschluss in European Studies'], ['Political science, law, sociology and selected economics subjects, with a European and international focus.','Politikwissenschaft, Recht, Soziologie und ausgewählte wirtschaftswissenschaftliche Themen mit europäischem und internationalem Schwerpunkt.']),
        ('2014–2018', ['RANEPA','RANEPA'], ['Bachelor’s Degree in International Relations','Bachelorabschluss in Internationalen Beziehungen'], ['Russian Presidential Academy of National Economy and Public Administration','Russische Akademie für Volkswirtschaft und öffentliche Verwaltung beim Präsidenten der Russischen Föderation'])]
    education_html = ''.join(f'<article><span class="ed-meta">{year}</span><h3>{E(org[i])}</h3><p>{E(degree[i])}</p><small>{E(desc[i])}</small></article>' for year,org,degree,desc in education)
    portrait = (image(E(config['portrait']), ['Portrait of Anton Frolov','Porträt von Anton Frolov'][i], 600, 800) if config.get('portrait') else f'<span>{["Portrait<br>to follow","Porträt<br>folgt"][i]}</span>')
    return f'''<div class="ed-home">
      <section class="ed-intro" aria-labelledby="intro-title"><div class="ed-intro-top"><p>{tx('eyebrow')}</p><p class="ed-available">{tx('availability')}</p></div><div class="ed-intro-grid"><h1 id="intro-title">{rich('heading')}</h1><div class="ed-intro-note"><p>{tx('intro')}</p><span>{tx('location')}</span></div></div></section>
      <section class="ed-work" id="work" aria-labelledby="work-title"><div class="ed-section-head"><h2 id="work-title">{tx('work_heading')}</h2><p>{tx('work_note')}</p></div>
       <article class="ed-feature"><a class="ed-feature-media {'' if detail else 'ed-feature-single'}" href="{path(lang,p['slug'])}" aria-label="{E(p['title'][i])}"><div class="ed-rooftop">{feature_image}</div>{people_block}<span class="ed-feature-open" aria-hidden="true">↗</span></a><div class="ed-feature-caption"><div><p class="ed-meta">{tx('feature_kicker')} — {E(p['org'])} / {p['year']}</p><h3><a href="{path(lang,p['slug'])}">{E(p['title'][i])}</a></h3><p>{feature_summary}</p><a class="ed-link" href="{path(lang,p['slug'])}">{tx('view_case')} <span aria-hidden="true">↗</span></a></div><ul>{''.join('<li>'+E(s)+'</li>' for s in feature_scope)}</ul></div></article>
       <div class="ed-more-head"><h2>{tx('more_heading')}</h2><p>{tx('more_note')}</p></div><div class="ed-project-grid">{''.join(cards)}</div><details class="ed-other"><summary>{t['more']}</summary><p>{t['morecopy']}</p></details>
      </section>
      <section id="about" class="ed-about"><div><p class="ed-label">{t['nav'][1]}</p><h2>{rich('about_heading')}</h2><div class="ed-portrait">{portrait}</div></div><div class="ed-about-copy"><p>{tx('about_text')}</p><p class="ed-interest">{tx('about_interest')}</p><div class="resource-links">{links(lang,t)}</div></div></section>
      <section id="experience" class="ed-experience"><div class="ed-section-head"><h2>{tx('experience_heading')}</h2><p>{['Germany & Russia','Deutschland & Russland'][i]}</p></div><div class="ed-timeline">{''.join(rows)}</div><div class="ed-education"><h3>{tx('education_heading')}</h3>{education_html}</div></section>
      <section class="ed-capabilities"><div class="ed-section-head"><h2>{tx('capabilities_heading')}</h2><p>{['A practical range of skills.','Ein vielseitiges, praktisches Profil.'][i]}</p></div><div class="ed-capability-grid">{capabilities}</div><div class="ed-practical"><div><h3>Tools</h3><p>WordPress · Meta Ads Manager · Adobe InDesign · Adobe Illustrator · CapCut</p></div><div><h3>{['Languages','Sprachen'][i]}</h3><p>{['Russian — Native · German — C1 · English — Fluent','Russisch — Muttersprache · Deutsch — C1 · Englisch — fließend'][i]}</p></div></div></section>
      <section id="contact" class="ed-contact"><p class="ed-label">{t['nav'][3]}</p><div class="ed-contact-grid"><h2>{rich('contact_heading')}</h2><div><p>{tx('contact_text')}</p><a class="ed-email" href="mailto:{E(config['email'])}">{E(config['email'])} <span aria-hidden="true">↗</span></a><div class="resource-links">{links(lang,t)}</div></div></div></section>
    </div>'''
