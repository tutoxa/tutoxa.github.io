"""The light portfolio homepage uses the existing project and experience data."""
from html import escape as escape


def render_home(lang, projects, config, translations, experience, path, links, copy, preview=False):
    index = 0 if lang == 'en' else 1

    def text(value):
        return escape(value[index] if isinstance(value, list) else value)

    def resources():
        email = f'<a class="button" href="mailto:{escape(config["email"])}">{["Email", "E-Mail"][index]} <span aria-hidden="true">↗</span></a>'
        linkedin = (f'<a class="button" href="{escape(config["linkedin"])}" rel="me">LinkedIn ↗</a>'
                    if config.get('linkedin') else (f'<span class="button unavailable" aria-disabled="true">{text(copy["linkedin_pending"])}</span>' if preview else ''))
        cv = (f'<a class="button" href="{escape(config["cv_de"])}" download>CV ↓</a>'
              if config.get('cv_de') else (f'<span class="button unavailable" aria-disabled="true">{text(copy["cv_pending"])}</span>' if preview else ''))
        return f'<div class="contact-buttons">{email}{linkedin}{cv}</div>'

    def review_note(key, css="content-note"):
        return f'<p class="{css}">{text(copy[key])}</p>' if preview else ""

    def experience_rows(entries):
        rows = []
        for year, organization, role, location, description in entries:
            if index:
                organization = organization.replace('Leibniz Institute for the History and Culture of Eastern Europe (GWZO)', 'Leibniz-Institut für Geschichte und Kultur des östlichen Europa (GWZO)').replace('Leipzig University', 'Universität Leipzig').replace('German Russian House', 'Deutsch-Russisches Haus')
                location = location.replace('Germany', 'Deutschland').replace('Moscow, Russia', 'Moskau, Russland')
            rows.append(f'<article class="career-entry"><p class="career-year">{escape(year)}</p><div><h3>{text(role)} <span>· {escape(organization)}</span></h3><p>{text(description)}</p><small>{escape(location)}</small></div></article>')
        return ''.join(rows)

    cards = []
    for number, project in enumerate(projects[:3], 1):
        href = path(lang, project['slug'])
        tags = ''.join(f'<span>{escape(tag)}</span>' for tag in project['cats'][index].split(' · '))
        if project.get('cover'):
            srcset = f' srcset="{escape(project["cover_srcset"])}" sizes="(max-width: 700px) 90vw, 42vw"' if project.get('cover_srcset') else ''
            visual = f'<img src="{escape(project["cover"])}"{srcset} alt="{text(project["cover_alt"])}" width="{project["cover_width"]}" height="{project["cover_height"]}" loading="lazy" decoding="async">'
        else:
            visual = f'<div class="case-placeholder"><span>{text(project["title"])}</span><small>{text(copy["visual_pending"]) if preview else escape(project["org"])}</small></div>'
        cards.append(f'<article class="case-card case-card-{number}"><div class="case-card-copy"><p class="tags">{tags}</p><p class="case-organization">{escape(project["org"])} · {escape(project["year"])}</p><h3><a href="{href}">{text(project["title"])}</a></h3><p>{text(project["intro"])}</p><a class="button" href="{href}">{text(copy["case_link"])} <span aria-hidden="true">↗</span></a></div><a class="case-card-visual" href="{href}" aria-label="{text(project["title"])}">{visual}</a></article>')

    research = []
    for item in copy['research_items']:
        tags = ''.join(f'<span>{escape(tag)}</span>' for tag in item['tags'][index])
        research.append(f'<article class="research-card"><p class="tags">{tags}</p><p class="case-organization">{text(item["org"])} · {escape(item["year"])}</p><h3>{text(item["title"])}</h3><p>{text(item["text"])}</p></article>')

    education = ''.join(f'<article class="qualification"><span>{escape(item["year"])}</span><div><h3>{text(item["org"])}</h3><p>{text(item["degree"])}</p><small>{text(item["text"])}</small></div></article>' for item in copy['education'])
    faq = ''.join(f'<details><summary>{text(item["q"])}</summary><p>{text(item["a"])}</p></details>' for item in copy['faq_items'])
    portrait = (f'<img src="{escape(config["portrait"])}" width="220" height="220" alt="{["Anton Frolov", "Anton Frolov"][index]}">'
                if config.get('portrait') else f'<div class="portrait-placeholder"><span>AF</span><small>{text(copy["portrait"]) if preview else "Anton Frolov"}</small></div>')
    older_work = ''.join(f'<a class="text-link" href="{path(lang, project["slug"])}">{text(project["title"])} ↗</a>' for project in projects[3:])
    about = translations[lang]['bio']
    body = f"""
    <div class="light-home">
      <section class="intro" id="about" aria-labelledby="intro-title">
        <div class="intro-portrait">{portrait}</div>
        <p class="open-badge"><span aria-hidden="true"></span>{text(copy['available'])}</p>
        <h1 id="intro-title">Anton Frolov</h1>
        <p class="intro-copy">{text(copy['intro'])}</p>
        {resources()}
        {review_note('missing_assets', 'asset-note')}
      </section>
      <section id="experience" class="home-section"><h2>{text(copy['experience'])}</h2>{experience_rows(experience[:3])}</section>
      <section id="work" class="home-section"><div class="home-section-title"><h2>{text(copy['cases'])}</h2><p>{text(copy['cases_note'])}</p></div><div class="selected-cases">{''.join(cards)}</div></section>
      <section id="research" class="home-section"><div class="home-section-title"><h2>{text(copy['research'])}</h2><p>{text(copy['research_note'])}</p></div><div class="research-grid">{''.join(research)}</div>{review_note('research_missing')}</section>
      <section id="additional" class="home-section"><h2>{text(copy['additional'])}</h2>{experience_rows(experience[3:])}<div class="other-projects">{older_work}</div><details class="more-about"><summary>{["More about my practice","Mehr zu meinen Arbeitsfeldern"][index]}</summary><p>{about}</p><p>{translations[lang]['morecopy']}</p><p>WordPress · Meta Ads Manager · Adobe InDesign · Adobe Illustrator · CapCut</p></details></section>
      <section id="achievements" class="home-section"><h2>{text(copy['achievements'])}</h2><div class="qualification-grid">{education}</div><p class="languages">{["Russian — Native · German — C1 · English — Fluent","Russisch — Muttersprache · Deutsch — C1 · Englisch — fließend"][index]}</p>{review_note('awards_missing')}</section>
      <section id="contact" class="home-section faq-contact"><h2>{text(copy['faq'])}</h2><div class="faq-list">{faq}</div><div class="contact-panel"><h3>{["Let’s talk.","Lassen Sie uns sprechen."][index]}</h3><a class="email-link" href="mailto:{escape(config['email'])}">{escape(config['email'])}</a>{resources()}</div></section>
    </div>"""

    return '\n'.join(line.rstrip() for line in body.splitlines())
