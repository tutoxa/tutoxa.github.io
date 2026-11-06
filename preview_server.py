"""Loopback-only static preview with byte ranges for Safari/Chrome video seeking."""
import argparse, functools, http.server, os, re
class PreviewHandler(http.server.SimpleHTTPRequestHandler):
 def send_head(self):
  self._range=None
  requested=self.headers.get('Range')
  if not requested:return super().send_head()
  path=self.translate_path(self.path)
  if not os.path.isfile(path):return super().send_head()
  size=os.path.getsize(path);match=re.fullmatch(r'bytes=(\d*)-(\d*)',requested.strip())
  if not match:return self.send_error(416,'Unsupported range')
  a,b=match.groups()
  if not a and not b:return self.send_error(416,'Empty range')
  start=int(a) if a else max(0,size-int(b));end=min(int(b) if b and a else size-1,size-1)
  if start>=size or start>end:
   self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.end_headers();return None
  f=open(path,'rb');f.seek(start);self._range=(start,end)
  self.send_response(206);self.send_header('Content-Type',self.guess_type(path));self.send_header('Accept-Ranges','bytes');self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(end-start+1));self.end_headers();return f
 def end_headers(self):
  self.send_header('X-Robots-Tag','noindex, nofollow');super().end_headers()
 def copyfile(self,source,outputfile):
  if self._range is None:return super().copyfile(source,outputfile)
  remaining=self._range[1]-self._range[0]+1
  while remaining:
   chunk=source.read(min(64*1024,remaining))
   if not chunk:break
   try:outputfile.write(chunk)
   except (BrokenPipeError,ConnectionResetError):break
   remaining-=len(chunk)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--directory',default='.');p.add_argument('--port',type=int,default=8000);a=p.parse_args()
 handler=functools.partial(PreviewHandler,directory=a.directory)
 print(f'Local preview: http://127.0.0.1:{a.port}/',flush=True)
 http.server.ThreadingHTTPServer(('127.0.0.1',a.port),handler).serve_forever()
