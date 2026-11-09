"""Render the portfolio homepage using the shared project and career records."""
from html import escape


def button_icon(path):
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
        f'<path d="{path}"/></svg>'
    )


MAIL_ICON = button_icon('M3 5h18v14H3z M3 6l9 7 9-7')
CV_ICON = button_icon('M6 3h8l4 4v14H6z M14 3v5h4 M9 12h6 M9 16h6')
ARROW_ICON = button_icon('M6 18L18 6 M8 6h10v10')


def render_home(lang, projects, config, experience, path, copy):
    index = 0 if lang == 'en' else 1
    project_by_slug = {project['slug']: project for project in projects}
    project_by_slug.update(copy['draft_projects'])

    def text(value):
        return escape(value[index] if isinstance(value, list) else value)

    def resources():
        buttons = [
            f'<a class="button" href="mailto:{escape(config["email"])}">'
            f'{["Email", "E-Mail"][index]} {MAIL_ICON}</a>'
        ]
        if config.get('linkedin'):
            buttons.append(f'<a class="button" href="{escape(config["linkedin"])}" rel="me">LinkedIn {ARROW_ICON}</a>')
        if config.get('cv_de'):
            buttons.append(
                f'<a class="button" href="{escape(config["cv_de"])}" target="_blank" rel="noopener noreferrer">'
                f'{["View CV", "Lebenslauf ansehen"][index]} {CV_ICON}</a>'
            )
        return f'<div class="contact-buttons">{"".join(buttons)}</div>'

    def experience_rows(entries):
        rows = []
        for entry in entries:
            rows.append(
                f'<article class="career-entry"><p class="career-year">{text(entry["period"])}'
                f'<span class="career-duration">{text(entry["duration"])}</span></p>'
                f'<div><h3>{text(entry["role"])} <span>· {text(entry["organization"])}</span></h3>'
                f'<p>{text(entry["description"])}</p><small>{text(entry["location"])}</small></div></article>'
            )
        return ''.join(rows)

    def draft_row(project, number=None):
        label = f'{number:02} / ' if number is not None else ''
        date = f' · {escape(project["year"])}' if project.get('year') else ''
        return f"""
        <article class="project-draft">
          <div class="draft-meta">{label}{text(project['org'])}{date}</div>
          <div><h3>{text(project['title'])}</h3><p>{text(project['intro'])}</p>
            <p class="draft-status">{text(copy['draft_label'])}</p></div>
        </article>"""

    def published_card(project, number):
        href = path(lang, project['slug'])
        title = text(project['title'])
        summary = project.get('featured', {}).get('summary', project['intro'])
        tags = ''.join(f'<span>{escape(tag)}</span>' for tag in project['cats'][index].split(' · '))
        srcset = ''
        if project.get('cover_srcset'):
            srcset = f' srcset="{escape(project["cover_srcset"])}" sizes="(max-width: 700px) 90vw, 42vw"'
        label = text(copy['featured_label']) if project['slug'] == config.get('featured_project') else f'{number:02}'
        return f"""
        <article class="case-card case-card-{number}">
          <div class="case-card-copy"><p class="tags">{tags}</p>
            <p class="case-organization">{label} / {escape(project['org'])} · {escape(project['year'])}</p>
            <h3><a href="{href}">{title}</a></h3><p>{text(summary)}</p>
            <a class="button" href="{href}">{text(copy['case_link'])} {ARROW_ICON}</a>
          </div>
          <a class="case-card-visual" href="{href}" aria-label="{title}">
            <img src="{escape(project['cover'])}"{srcset} alt="{text(project['cover_alt'])}"
                 width="{project['cover_width']}" height="{project['cover_height']}" loading="lazy" decoding="async">
          </a>
        </article>"""

    selected_work = []
    for number, slug in enumerate(copy['selected_work'], 1):
        project = project_by_slug[slug]
        if project.get('status') == 'draft' or not project.get('cover'):
            selected_work.append(draft_row(project, number))
        else:
            selected_work.append(published_card(project, number))

    # Group existing employment records without changing their titles or dates.
    relevant = [experience[key] for key in ('climatech', 'ekoniva', 'german-russian-house')]
    additional = [experience[key] for key in ('gwzo', 'leipzig-university')]
    education = ''.join(
        f'<article class="qualification"><span>{escape(item["year"])}</span><div>'
        f'<h3>{text(item["org"])}</h3><p>{text(item["degree"])}</p>'
        f'<small>{text(item["text"])}</small></div></article>'
        for item in copy['education']
    )
    portrait = (
        f'<img src="{escape(config["portrait"])}" width="220" height="220" alt="Anton Frolov">'
        if config.get('portrait')
        else '<div class="portrait-placeholder" aria-hidden="true"><span>AF</span></div>'
    )
    research = draft_row(project_by_slug[copy['research_project']])
    body = f"""
    <div class="light-home">
      <section class="intro" id="about" aria-labelledby="intro-title">
        <div class="intro-dots" aria-hidden="true"><canvas></canvas></div>
        <div class="intro-portrait">{portrait}</div>
        <p class="open-badge"><span aria-hidden="true"></span>{text(copy['available'])}</p>
        <h1 id="intro-title">Anton Frolov</h1>
        <p class="intro-copy">{text(copy['intro'])}</p>
        {resources()}
      </section>
      <section id="work" class="home-section">
        <div class="home-section-title"><h2>{text(copy['cases'])}</h2><p>{text(copy['cases_note'])}</p></div>
        <div class="selected-cases">{''.join(selected_work)}</div>
      </section>
      <section id="experience" class="home-section">
        <h2>{text(copy['experience'])}</h2>{experience_rows(relevant)}
      </section>
      <section id="research" class="home-section">
        <span id="additional"></span><h2>{text(copy['additional'])}</h2>
        {experience_rows(additional)}
        {research}
      </section>
      <section id="achievements" class="home-section">
        <h2>{text(copy['achievements'])}</h2>
        <div class="qualification-grid">{education}</div>
        <p class="languages">{["Russian — Native · German — C1 · English — Fluent","Russisch — Muttersprache · Deutsch — C1 · Englisch — fließend"][index]}</p>
      </section>
      <section id="contact" class="home-section">
        <h2>{text(copy['contact'])}</h2>
        <div class="contact-panel">
          <h3>{["Let’s talk.","Lassen Sie uns sprechen."][index]}</h3>
          <a class="email-link" href="mailto:{escape(config['email'])}">{escape(config['email'])}</a>
          {resources()}
        </div>
      </section>
    </div>"""
    return '\n'.join(line.rstrip() for line in body.splitlines())
