"""Editorial renderer for the first developed case; content stays in content.json."""
from html import escape as esc

def render_case(project,lang,assets,preview=False,next_project=None,path=None):
 i=0 if lang=='en' else 1;c=project['case_study'];base='/de.html' if i else '/'
 def tx(v):return esc(v[i])
 def image(key,alt,classes='',eager=False,sizes='(max-width: 650px) 88vw, 45vw'):
  a=assets[key];vs=a['variants'];v=vs[-1]
  srcset=', '.join(f'{x["path"]} {x["width"]}w' for x in vs)
  return f'<img class="{classes}" src="{v["path"]}" srcset="{srcset}" sizes="{sizes}" width="{a["width"]}" height="{a["height"]}" alt="{tx(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async" {"fetchpriority=high" if eager else ""}>'
 def label(n,title):return f'<p class="kt-kicker">{n} / {title}</p>'
 def figure(item,classes='',sizes='(max-width: 650px) 88vw, 45vw'):
  return f'<figure class="{classes}"><a href="{assets[item["asset"]]["variants"][-1]["path"]}" target="_blank" rel="noopener" aria-label="{tx(item["alt"])}">{image(item["asset"],item["alt"],sizes=sizes)}</a><figcaption>{tx(item["caption"])}</figcaption></figure>'
 profiles=''
 for p in c['profiles']:
  profiles+=f'<figure class="kt-profile"><div class="kt-profile-head"><span>{esc(p["handle"])}</span><strong>{tx(p["count"])}</strong></div><a class="kt-source-image" href="{assets[p["asset"]]["variants"][-1]["path"]}" target="_blank" rel="noopener" aria-label="{tx(p["alt"])} — {"open image" if i==0 else "Bild öffnen"}">{image(p["asset"],p["alt"],sizes="(max-width: 650px) 40vw, 180px")}</a><figcaption>{tx(p["caption"])}</figcaption></figure>'
 videos=''
 published_count = 0
 for v in c['videos']:
  a=assets[v['asset']]; playable=preview or c.get('publication_approved',False)
  # Public release requires explicit approval AND a separately configured licensed URL.
  url=a['preview_url'] if preview else v.get('public_url')
  playable=playable and bool(url)
  if playable:
   published_count += 1
  source=f'<source src="{esc(url)}" type="video/mp4">' if playable else ''
  fallback=['Playback pending audio clearance.','Wiedergabe nach Klärung der Tonrechte.'][i]
  player=(f'<video id="kt-{v["asset"]}" controls playsinline preload="none" width="{v["width"]}" height="{v["height"]}" poster="{a["poster"]}" aria-label="{tx(v["label"])}" aria-describedby="desc-{v["asset"]}">{source}<p>{fallback}</p></video>' if playable else f'<div class="kt-held"><img src="{a["poster"]}" width="{v["width"]}" height="{v["height"]}" alt="{tx(v["label"])}" loading="lazy"><p>{fallback}</p></div>')
  start=(f'<button class="kt-start" hidden type="button" data-video="kt-{v["asset"]}" style="background-image:url({a["poster"]})" aria-label="{'Play' if i==0 else 'Abspielen'}: {tx(v["label"])}"><span><b aria-hidden="true">▶</b>{'Play film' if i==0 else 'Video abspielen'}</span></button>' if playable else '')
  videos+=f'<article class="kt-video"><div class="kt-player" style="--video-ratio:{v["width"]}/{v["height"]}">{player}{start}</div><div class="kt-video-heading"><h3>{tx(v["label"])}</h3><span>{v["duration"]}</span></div><p id="desc-{v["asset"]}">{tx(v["text"])}</p></article>'
 carousel=''.join(f'<li>{image(p["asset"],p["alt"],sizes="(max-width: 650px) 75vw, 29vw")}<span class="kt-slide-number">{n+1:02} / 05</span></li>' for n,p in enumerate(c['carousel']))
 performance = next(item for item in c['evidence'] if item['asset'] == 'performance')
 evidence = ''.join(figure(item, sizes='(max-width: 650px) 38vw, 220px')
                    for item in c['evidence'] if item is not performance)
 planning_focus = ''.join(f'<li>{esc(item)}</li>' for item in c['timeline']['planning_focus'][i])
 production_stills = ''.join(figure(item, sizes='(max-width: 650px) 29vw, 24vw')
                             for item in c['photos'][1:])
 summary=''.join(f'<li><span>{n+1:02}</span>{esc(role)}</li>' for n,role in enumerate(c['contribution']['roles'][i]))
 notice=f'<aside class="kt-review" role="note"><strong>{"REVIEW PREVIEW" if i==0 else "VORSCHAU ZUR PRÜFUNG"}</strong><p>{tx(c["preview_notice"])}</p></aside>' if preview else ''
 title=tx(c['editorial_title']).replace('&lt;br&gt;','<br>').replace('&lt;em&gt;','<em>').replace('&lt;/em&gt;','</em>')
 timeline = c['timeline']
 stages = timeline['stages']
 stage_links = ''.join(
  f'<li><a href="#{slug}"><span class="kt-nav-number">{number:02}</span><span>{tx(name)}</span></a></li>'
  for number, (slug, name) in enumerate(stages.items(), 1)
 )
 def stage_header(slug, description):
  number = list(stages).index(slug) + 1
  return (
   f'<div class="kt-stage-heading"><span class="kt-stage-number">{number:02} / 05</span>'
   f'<h3 id="{slug}-title">{tx(stages[slug])}</h3><p>{tx(description)}</p></div>'
  )
 if published_count == len(c['videos']):
  player_note = ["Reel 1 is silent. The interview has German on-screen subtitles.",
                 "Reel 1 ist ohne Ton. Das Interview enthält eingeblendete deutsche Untertitel."][i]
 else:
  player_note = ["Reel 1 plays without sound. Reel 2 and the interview are shown as stills while their audio rights are being confirmed.",
                 "Reel 1 wird ohne Ton abgespielt. Reel 2 und das Interview sind bis zur Klärung der Tonrechte als Standbilder zu sehen."][i]
 next_link=path(lang,next_project['slug']) if next_project else base+'#work'
 next_title=next_project['title'][i] if next_project else c['back'][i]
 return f'''<div class="kt-case">
 <section class="kt-hero" aria-labelledby="case-title">
  <div class="kt-hero-top"><a class="text-link" href="{base}#work">← {"All work" if i==0 else "Alle Projekte"}</a><span>{esc(project['org'])} / {esc(project['year'])}</span></div>
  <div class="kt-hero-grid">
   <div class="kt-hero-copy">
    <p class="kt-kicker">BERLIN / 2026</p>
    <h1 id="case-title">{title}</h1>
    <p class="kt-subtitle">{tx(project['intro'])}</p>
    <p class="kt-categories">{tx(project['cats'])}</p>
    <dl class="kt-metadata">
     <div><dt>{"My role" if i==0 else "Meine Rolle"}</dt><dd>{tx(c['role'])}</dd></div>
     <div><dt>{"Final formats" if i==0 else "Fertige Formate"}</dt><dd>{"2 Reels + 1 employee interview" if i==0 else "2 Reels + 1 Mitarbeiterinterview"}</dd></div>
    </dl>
   </div>
   <div class="kt-hero-media">
    <div class="kt-lead">
     <figure class="kt-lead-wide">{image('rooftop',c['photos'][0]['alt'],eager=True,sizes='(max-width: 750px) 67vw, 42vw')}</figure>
     <figure class="kt-lead-person">{image('hero',c['hero_alt'],eager=True,sizes='(max-width: 750px) 24vw, 15vw')}</figure>
    </div>
    <p class="kt-lead-caption">{tx(c['hero_caption'])}</p>
   </div>
  </div>
 </section>{notice}
 <section class="kt-timeline" aria-labelledby="timeline-title">
  <div class="kt-index">
   <h2 id="timeline-title">{tx(timeline['label'])}</h2>
   <nav class="kt-stage-nav" aria-label="{tx(timeline['label'])}"><ol>{stage_links}</ol></nav>
  </div>
  <ol class="kt-stages">
   <li class="kt-stage" id="opportunity" aria-labelledby="opportunity-title">
    {stage_header('opportunity', c['opportunity']['text'])}
    <div class="kt-stage-content">
     <div class="kt-profile-pair">{profiles}</div>
     <p class="kt-source-note">{tx(c['snapshot_note'])}</p>
    </div>
   </li>
   <li class="kt-stage" id="planning" aria-labelledby="planning-title">
    {stage_header('planning', timeline['planning'])}
    <ol class="kt-plan-list" aria-label="{"Planning focus" if i==0 else "Schwerpunkte der Planung"}">{planning_focus}</ol>
   </li>
   <li class="kt-stage kt-production" id="production" aria-labelledby="production-title">
    {stage_header('production', c['production']['text'])}
    <div class="kt-photo-grid">{production_stills}</div>
   </li>
   <li class="kt-stage kt-formats" id="films" aria-labelledby="films-title">
    {stage_header('films', c['formats_intro'])}
    <div class="kt-stage-content">
     <p class="kt-output-hint">{"Swipe or use arrow keys to browse the three videos →" if i==0 else "Mit Wischen oder den Pfeiltasten durch die drei Videos blättern →"}</p>
     <div class="kt-video-grid" tabindex="0" role="region" aria-label="{"Three finished videos" if i==0 else "Drei fertige Videos"}">{videos}</div>
     <p class="kt-player-note">{player_note}</p>
     <details class="kt-evidence kt-carousel-details">
      <summary>{"Interview carousel · five slides" if i==0 else "Interview-Carousel · fünf Slides"}</summary>
     <div class="kt-carousel-intro"><h3>{tx(c['carousel_heading'])}</h3><p>{tx(c['carousel_note'])}</p><span class="kt-swipe">{"Scroll or use arrow keys to explore all five slides →" if i==0 else "Alle fünf Slides per Scrollen oder Pfeiltasten ansehen →"}</span></div><ul class="kt-carousel" tabindex="0" aria-label="{'Five original interview carousel slides' if i==0 else 'Fünf Original-Slides des Interview-Carousels'}">{carousel}</ul><details class="kt-transcript"><summary>{"Read the carousel text in English" if i==0 else "Carousel-Texte lesen"}</summary><ol>{''.join('<li>'+esc(s)+'</li>' for s in (["In conversation with Gregor — CLIMATECH Berlin.","The idea was to build a social media community, exchange ideas and share how I practise different tasks.","At CLIMATECH Berlin, we try to complete our tasks as well as possible and keep customers satisfied.","Of course there are colleagues who say: we do it this way, and this is where you made a mistake. It is not about making someone look bad; it is about learning from mistakes together.","We have good equipment at CLIMATECH and everything is flexible."] if i==0 else ["Im Gespräch mit Gregor — CLIMATECH Berlin.","Die Idee war eigentlich, auf Social Media eine Community aufzubauen, um mich auszutauschen – wie ich verschiedene Sachen am besten praktiziere.","Bei CLIMATECH Berlin versuchen wir, unsere Aufgaben so gut wie möglich umzusetzen und die Kunden zufriedenzustellen.","Natürlich gibt es hier Kollegen, die sagen: Wir machen das so und dort hast du einen Fehler gemacht. Aber das wird niemals genutzt, mich runterzumachen. Es geht darum, aus Fehlern zu lernen und jeden Tag besser zu werden.","Wir sind bei CLIMATECH gut ausgestattet. Top Equipment und alles ist flexibel."]))}</ol></details>
     </details>
    </div>
   </li>
   <li class="kt-stage kt-publication" id="publication" aria-labelledby="publication-title">
    {stage_header('publication', c['publication']['text'])}
    <div class="kt-stage-content">
     <div class="kt-results">
      <div class="kt-metric">
       <strong>{"4,066" if i==0 else "4.066"}</strong>
       <h4>{tx(c['metric_heading'])}</h4>
       <p>{tx(c['metric_note'])}</p>
      </div>
      {figure(performance, 'kt-performance', sizes='(max-width: 750px) 34vw, 190px')}
     </div>
     <details class="kt-evidence">
      <summary>{"Two publication screenshots" if i==0 else "Zwei Screenshots zur Veröffentlichung"}</summary>
      <div class="kt-evidence-grid">{evidence}</div>
     </details>
    </div>
   </li>
  </ol>
 </section>
 <section id="contribution" class="kt-contribution" aria-labelledby="contribution-title">
  <div>{label('06','What I took from it' if i==0 else 'Was ich daraus mitnehme')}<h2 id="contribution-title">{tx(c['contribution']['heading'])}</h2><p>{tx(c['contribution']['text'])}</p></div>
  <ul>{summary}</ul>
 </section>
 <div class="kt-next"><div class="kt-next-label"><span>{"Next project / 02" if i==0 else "Nächstes Projekt / 02"}</span><a href="{base}#work">{"All selected work ↗" if i==0 else "Alle Projekte ↗"}</a></div><a class="kt-next-title" href="{next_link}"><h2>{esc(next_title)}</h2><span aria-hidden="true">↗</span></a></div>
 </div>'''
