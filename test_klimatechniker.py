"""Artifact and publication-safety checks; run with Python 3."""
import pathlib, subprocess, sys, tempfile, urllib.parse
from html.parser import HTMLParser
R=pathlib.Path(__file__).parent
class Page(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
def check_tree(root,preview):
 for f in root.glob('*.html'):
  page=Page();page.feed(f.read_text());assert sum(t=='h1' for t,a in page.tags)==1,f
  ids=[a['id'] for t,a in page.tags if 'id' in a];assert len(ids)==len(set(ids)),f
  for tag,a in page.tags:
   for key in ['src','href','poster']:
    u=a.get(key,'');p=urllib.parse.urlsplit(u)
    if u.startswith('/'):
     target=root/(p.path.lstrip('/') or 'index.html');assert target.exists(),(f.name,u)
   if tag=='a' and a.get('href','').startswith(('/', '#')):
    href=urllib.parse.urlsplit(a['href'])
    if href.fragment:
     target=root/(href.path.lstrip('/') or ('index.html' if href.path=='/' else f.name))
     destination=Page();destination.feed(target.read_text())
     assert any(v.get('id')==href.fragment for _,v in destination.tags),(f.name,a['href'])
   if a.get('srcset'):
    for value in a['srcset'].split(','):assert (root/value.strip().split()[0].lstrip('/')).exists(),value
   if tag=='img':assert a.get('alt') and a.get('width') and a.get('height'),(f,a)
  if 'people-behind' in f.name:
   sources=[a['src'] for t,a in page.tags if t=='source']
   expected = ['/media/klimatechniker/reel-1.mp4']
   if preview:
    expected = [f'/.preview-media/klimatechniker/{name}.mp4' for name in ('reel-1', 'reel-2', 'interview')]
   assert sources == expected, (f, sources)
   timeline_ids = [a['id'] for t,a in page.tags if 'kt-stage' in a.get('class','').split()]
   assert timeline_ids == ['opportunity', 'planning', 'production', 'films', 'publication'], (f, timeline_ids)
   assert all(a.get('preload')=='none' and 'autoplay' not in a and 'playsinline' in a for t,a in page.tags if t=='video')
   if preview:assert any(t=='meta' and a.get('name')=='robots' and 'noindex' in a.get('content','') for t,a in page.tags)
 assert (root/'CNAME').read_text().strip()=='antonfrolov.de'
check_tree(R,False)
with tempfile.TemporaryDirectory() as tmp:
 subprocess.run([sys.executable,str(R/'build.py'),'--preview','--output',tmp],check=True,capture_output=True)
 check_tree(pathlib.Path(tmp),True)
print('PASS: both build modes; local links/anchors/srcsets/posters; image accessibility and dimensions; no autoplay; only the silent Reel in the public build; preview noindex; CNAME retained.')
