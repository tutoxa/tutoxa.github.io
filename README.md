# Anton Frolov — portfolio

Static bilingual portfolio hosted by GitHub Pages from `main`, root. No npm packages or paid services. English: `/`. German: `/de.html`. Each project has an English and German HTML page, so direct loads and refresh work without a router. The existing `CNAME` must remain `antonfrolov.de`.

## Edit content

`content.json` is the central source of project text and media settings. Each translated text is an array: `[English, German]`. `settings.featured_project` selects the featured project by its slug. The other projects appear in array order. Reorder the array to reorder those projects and the next-project links. Keep the featured Klimatechniker project first for the current case sequence. `homepage` holds the editorial homepage text; each project holds its own `home_visual_title`, cover, case text and optional `featured` summary/detail photograph. `build.py` contains shared interface translations, experience and the general case template. `editorial_home.py` renders the homepage and contains education and practical tool/language labels. `style.css` is the original base; `editorial.css` controls the new shell/homepage; `site.js` controls the mobile menu.

After editing content or templates, run `python3 build.py` (Python 3, standard library only). Commit the regenerated HTML files together with the source changes. You can run this locally or in a GitHub Codespace. Do not edit only generated HTML: it will be overwritten by the next build.

## Photographs

Create folders under `media/`: `portrait`, `climatech-people`, `climatech-recruitment`, `climatech-website`, `ekoniva`, `events`. Use descriptive lowercase filenames. Export photos as WebP or JPEG, roughly 1600–2000 pixels wide, ideally below 300 KB. Only use media you are allowed to publish.

In `content.json`, set `settings.portrait` to `/media/portrait/anton.webp`. Set a project's `cover` to `/media/climatech-people/cover.webp` and add `cover_alt`: `[English description, German description]`. Add gallery entries to `images`:

```json
{"src":"/media/climatech-people/interview.webp","alt":["Accurate English description","Passende deutsche Beschreibung"],"caption":["English caption","Deutsche Bildunterschrift"]}
```

The neutral editorial covers are explicitly labelled placeholders. They are HTML/CSS, not real work or stock photos. A configured cover replaces the placeholder automatically. Gallery images lazy-load. Preserve meaningful alt text. Set `cover_width` and `cover_height` to the original image dimensions, and optionally `cover_srcset` to a normal HTML srcset string such as `/media/events/cover-800.webp 800w, /media/events/cover-1600.webp 1600w`. Both the homepage and general case cover use configured photos. If a cover is missing, the homepage uses the project’s bilingual `home_visual_title` and an explicit placeholder label.

## Video

Use the project `videos` array. Prefer compressed finished videos or official embed URLs; do not commit raw footage. Example hosted file:

```json
{"type":"file","url":"/media/climatech-people/interview.mp4","poster":"/media/climatech-people/interview.webp","title":["Employee interview","Mitarbeiterinterview"]}
```

Example embed: `{"type":"embed","url":"https://www.youtube-nocookie.com/embed/ACTUAL_ID","title":["Project film","Projektfilm"]}`. Use an actual published embed URL, not a watch URL. Embeds load lazily; adding an external embed may require an updated privacy notice. Provide captions for spoken videos. Video players have controls and no autoplay.

## CV and LinkedIn

Upload the actual German PDF to `/media/cv/anton-frolov-de.pdf`; set `settings.cv_de` to that path. Set `settings.linkedin` to the verified profile URL. Until configured, the website displays honest unavailable labels instead of broken links. An English CV can be added as another setting/template link later.

## Translation

Keep each English/German pair complete. Shared text lives in `T` in `build.py`; homepage and project copy are in `content.json`. A few short case interface labels live in `klimatechniker.py`, and education/tools/language labels live in `editorial_home.py`. Language links preserve the current project; all in-language navigation stays in that language. English is the default at the canonical homepage; no browser-language redirect is used.

## Deployment and checks

Run `python3 build.py`. Preview with `python3 -m http.server 8000`, then visit `http://localhost:8000`. Check both languages and every project page. Commit and push to the existing repository's `main`. GitHub Pages deploys the root automatically. Keep `CNAME`, `.nojekyll`, `sitemap.xml`, `robots.txt`, CSS, JS and the social preview image. Do not change Pages to another host.

Domain DNS: four apex A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `www` CNAME `tutoxa.github.io`. Verify with current GitHub documentation before changes. In GitHub Settings → Pages, keep custom domain `antonfrolov.de` and enable Enforce HTTPS when the certificate is ready. Consider account Settings → Pages domain verification and add only the exact TXT token GitHub generates; preserve all unrelated DNS.

## Files still needed

Portrait; approved covers/photos for the four other projects; approved public video URLs and captions; website/recruitment/product/event materials; German CV; LinkedIn URL. Klimatechniker now has actual supplied project photographs, graphics and local preview films. No performance results or sole authorship are implied for collaborative work. Project time ranges follow the supplied employment years and should be refined if exact project dates become available.

## Klimatechniker case — review branch

The first project now uses a dedicated editorial renderer, `klimatechniker.py`, with all bilingual copy, section data, media references and publication approval in `projects[0].case_study` in `content.json`. The existing English/German URLs are preserved. Other project templates are unchanged; their final next-project label updates automatically.

Optimized WebP images and video posters are in `media/klimatechniker/`. `manifest.json` records original filenames, dimensions, derivatives and sizes. Original source photos, MOV files and RAW material are not copied into the repository. The scoped layout is in `klimatechniker.css`; `klimatechniker.js` enables clear poster/play buttons and prevents simultaneous video playback. Native controls remain available without JavaScript.

### Local review with videos

The three optimized MP4s are stored in ignored `.preview-media/klimatechniker/`. They are local-only and are **not** included in Git. Generate an isolated preview outside the repository:

```sh
python3 build.py --preview --output ../klimatechniker-preview
python3 preview_server.py --directory ../klimatechniker-preview --port 8000
```

Visit `http://127.0.0.1:8000/people-behind-the-projects.html` or `http://127.0.0.1:8000/de-people-behind-the-projects.html`. The preview supports byte-range requests for playback/seek and is bound to loopback. Preview pages have `noindex,nofollow`. Keep the server running during review. A fresh clone will need the local MP4s restored from the original finished exports; no video download is automatic.

### Before a future release

The approved public build plays the silent Reel 1 from `media/klimatechniker/reel-1.mp4`. Reel 2 and the interview contain audio and are represented by poster stills pending rights clearance. All three finished videos are available in the local review build.

To release another video after clearance, set its `public_url` to an approved MP4 and regenerate the normal build with `python3 build.py`. The case requires both `publication_approved` and an explicit URL per video. Keep original footage and review copies outside the public build.

The profile follower counts are source-screenshot snapshots. No growth attribution or campaign performance total has been added. The mixed Reel-grid screenshot is presented as source evidence without extracting uncertain project-level metrics.

## Editorial redesign — local review only

Branch: `feature/portfolio-editorial-redesign`. This branch builds on the completed Klimatechniker case branch. It has not been pushed or deployed. The shared header changes on all pages; the four other case bodies, language routes and domain files are preserved.

The homepage is now a compact introduction, large photographic feature, varied project layouts, short About, expandable experience rows, education, capabilities and contact. The Klimatechniker page uses a two-photo lead, small profile excerpts, asymmetric production gallery, three poster-led players, a five-slide carousel and expandable source evidence. All full screenshots remain linked. No numeric campaign outcome is inferred from the mixed Reel grid.

### Editing the feature and media

- `settings.featured_project`: the slug of the featured case.
- `projects[].cover`, `cover_alt`, `cover_width`, `cover_height`, optional `cover_srcset`: the main project photograph. Add these to the four placeholder projects when approved images arrive.
- `projects[].home_visual_title`: bilingual text on a placeholder; stays attached to its project when the array is reordered.
- `projects[].featured.summary` and `featured.scope`: the compact feature caption and role list.
- `projects[].featured.detail`: optional second photograph (`src`, `alt: [EN,DE]`, `width`, `height`, optional `srcset`). Remove it to use a single-photo feature. A new featured project without custom feature text falls back to its normal introduction/categories.
- `homepage`: introduction, About, section headings, contact text and capabilities. Text is always `[English, German]`; the few styled headings accept `<br>` and `<em>` only.
- `projects[0].case_study`: Klimatechniker story, including `editorial_title`. The source `media/klimatechniker/manifest.json` maps the photo/screenshot/video keys to optimized files. To replace a case photo, export a new optimized file and update its manifest variants, dimensions and bilingual case alt/caption. To select a different existing photo, change the `asset` key in the relevant case entry.

### Review and future release

From this repository run:

```sh
python3 build.py
python3 test_klimatechniker.py
python3 build.py --preview --output ../klimatechniker-preview
python3 preview_server.py --directory ../klimatechniker-preview --port 8000
```

Open `http://127.0.0.1:8000/` and `http://127.0.0.1:8000/de.html`, then open the featured case. The server is private to this computer. These commands do not deploy. The preview directory and private preview archive contain review-only MP4s: do not upload them as a public site.

After visual approval and rights clearance, regenerate the normal build, review its diff, and only then merge/push through the existing GitHub Pages workflow. No DNS or Pages setting change is needed for this redesign. Keep the existing `CNAME` and root HTML routes.
