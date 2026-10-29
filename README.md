# Anton Frolov — portfolio

Static bilingual portfolio hosted by GitHub Pages from `main`, root. No npm packages or paid services. English: `/`. German: `/de.html`. Each project has an English and German HTML page, so direct loads and refresh work without a router. The existing `CNAME` must remain `antonfrolov.de`.

## Edit content

`content.json` is the central source of project text and media settings. Each translated text is an array: `[English, German]`. Projects appear in array order. Reorder the array to reorder the work grid and next-project links. `build.py` contains shared interface translations, biography, experience, education and page templates. `style.css` controls design; `site.js` controls the mobile menu.

After editing content or templates, run `python3 build.py` (Python 3, standard library only). Commit the regenerated HTML files together with the source changes. You can run this locally or in a GitHub Codespace. Do not edit only generated HTML: it will be overwritten by the next build.

## Photographs

Create folders under `media/`: `portrait`, `climatech-people`, `climatech-recruitment`, `climatech-website`, `ekoniva`, `events`. Use descriptive lowercase filenames. Export photos as WebP or JPEG, roughly 1600–2000 pixels wide, ideally below 300 KB. Only use media you are allowed to publish.

In `content.json`, set `settings.portrait` to `/media/portrait/anton.webp`. Set a project's `cover` to `/media/climatech-people/cover.webp` and add `cover_alt`: `[English description, German description]`. Add gallery entries to `images`:

```json
{"src":"/media/climatech-people/interview.webp","alt":["Accurate English description","Passende deutsche Beschreibung"],"caption":["English caption","Deutsche Bildunterschrift"]}
```

The neutral editorial covers are explicitly labelled placeholders. They are HTML/CSS, not real work or stock photos. A configured cover replaces the placeholder automatically. Gallery images lazy-load. Preserve meaningful alt text. For responsive source sets, extend `media()` in `build.py` when multiple image sizes are available.

## Video

Use the project `videos` array. Prefer compressed finished videos or official embed URLs; do not commit raw footage. Example hosted file:

```json
{"type":"file","url":"/media/climatech-people/interview.mp4","poster":"/media/climatech-people/interview.webp","title":["Employee interview","Mitarbeiterinterview"]}
```

Example embed: `{"type":"embed","url":"https://www.youtube-nocookie.com/embed/ACTUAL_ID","title":["Project film","Projektfilm"]}`. Use an actual published embed URL, not a watch URL. Embeds load lazily; adding an external embed may require an updated privacy notice. Provide captions for spoken videos. Video players have controls and no autoplay.

## CV and LinkedIn

Upload the actual German PDF to `/media/cv/anton-frolov-de.pdf`; set `settings.cv_de` to that path. Set `settings.linkedin` to the verified profile URL. Until configured, the website displays honest unavailable labels instead of broken links. An English CV can be added as another setting/template link later.

## Translation

Keep each English/German pair complete. Shared text lives in `T` in `build.py`; project copy is in `content.json`. Language links preserve the current project; all in-language navigation stays in that language. English is the default at the canonical homepage; no browser-language redirect is used.

## Deployment and checks

Run `python3 build.py`. Preview with `python3 -m http.server 8000`, then visit `http://localhost:8000`. Check both languages and every project page. Commit and push to the existing repository's `main`. GitHub Pages deploys the root automatically. Keep `CNAME`, `.nojekyll`, `sitemap.xml`, `robots.txt`, CSS, JS and the social preview image. Do not change Pages to another host.

Domain DNS: four apex A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `www` CNAME `tutoxa.github.io`. Verify with current GitHub documentation before changes. In GitHub Settings → Pages, keep custom domain `antonfrolov.de` and enable Enforce HTTPS when the certificate is ready. Consider account Settings → Pages domain verification and add only the exact TXT token GitHub generates; preserve all unrelated DNS.

## Files still needed

Portrait; original approved covers/photos for all five projects; finished video URLs and captions; website/recruitment/product/event materials; German CV; LinkedIn URL. No performance results or sole authorship are implied for collaborative work. Project time ranges follow the supplied employment years and should be refined if exact project dates become available.
