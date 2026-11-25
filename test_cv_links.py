"""Protect CV language selection, new-tab behavior and cache versioning."""
import hashlib,json,pathlib,urllib.parse
from html.parser import HTMLParser
from editorial_home import render_home
R=pathlib.Path(__file__).parent
class Links(HTMLParser):
 def __init__(self):super().__init__();self.pdf=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a' and '.pdf' in a.get('href',''):self.pdf.append(a)
def links(text):
 p=Links();p.feed(text);return p.pdf
for lang,name in [('en','index.html'),('de','de.html')]:
 anchors=links((R/name).read_text());assert len(anchors)==2,(lang,anchors)
 for a in anchors:
  url=urllib.parse.urlsplit(a['href']);assert url.path==f'/media/cv/anton-frolov-{lang}.pdf'
  assert a['target']=='_blank' and set(a['rel'].split())=={'noopener','noreferrer'} and 'download' not in a
  pdf=R/url.path.lstrip('/');assert pdf.read_bytes().startswith(b'%PDF-')
  assert urllib.parse.parse_qs(url.query)['v']==[hashlib.sha256(pdf.read_bytes()).hexdigest()[:12]]
d=json.loads((R/'content.json').read_text());config={**d['settings'],'cv_en':None}
def path(lang,slug=None):return ('/de-' if lang=='de' else '/')+slug+'.html' if slug else ('/de.html' if lang=='de' else '/')
assert not links(render_home('en',d['projects'],config,d['experience'],path,d['light_home']))
assert len(links(render_home('de',d['projects'],config,d['experience'],path,d['light_home'])))==2
print('PASS: both languages; hero/contact CV links; matching file hashes; new-tab controls; missing English CV never falls back to German.')

# Safari displayed the exporter-generated inverted soft mask instead of the portrait.
from pypdf import PdfReader
en_pdf=PdfReader(R/'media/cv/anton-frolov-en.pdf')
assert len(en_pdf.pages)==1
for image in en_pdf.pages[0]['/Resources']['/XObject'].values():
 assert '/SMask' not in image.get_object(), 'English portrait must not reintroduce the Safari transparency-mask bug'
print('PASS: one-page English PDF and Safari-compatible opaque portrait stream.')
