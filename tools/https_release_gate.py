#!/usr/bin/env python3
"""Read-only HTTPS release gate for ookini. Never purchases or modifies the site."""
import argparse, json, urllib.request, urllib.error, urllib.parse
from datetime import datetime, timezone

PATHS={
 '/':'text/html', '/pages/home.html':'text/html',
 '/pages/discover.html':'text/html','/pages/station.html':'text/html',
 '/pages/pass.html':'text/html','/pages/help.html':'text/html',
 '/verify.html':'text/html', '/assets/season-01.jpg':'image/jpeg',
 '/assets/season-02.jpg':'image/jpeg', '/assets/season-03.jpg':'image/jpeg',
 '/assets/season-04.jpg':'image/jpeg',
 '/media/baby.mp4':'video/mp4','/media/exit.mp4':'video/mp4',
}

def probe(url, expect):
 req=urllib.request.Request(url,headers={'User-Agent':'ookini-release-gate/1.0','Range':'bytes=0-1023'})
 try:
  with urllib.request.urlopen(req,timeout=5) as r:
   status=r.status
   ctype=r.headers.get('Content-Type','').split(';')[0].strip().lower()
   body=r.read(1024)
   ok=status in (200,206) and ctype==expect
   if expect=='text/html':
    ok=ok and (b'<html' in body.lower() or b'<!doctype' in body.lower())
   return {'status':status,'content_type':ctype,'ok':bool(ok),'sample_bytes':len(body)}
 except urllib.error.HTTPError as e:
  return {'status':e.code,'ok':False,'error':str(e)}
 except Exception as e:
  return {'ok':False,'error':str(e)}

def main():
 p=argparse.ArgumentParser()
 p.add_argument('base_url')
 p.add_argument('--output')
 args=p.parse_args()
 base=args.base_url.rstrip('/')
 if urllib.parse.urlsplit(base).scheme!='https':
  p.error('HTTPS URL required')
 checks={path:probe(base+path,typ) for path,typ in PATHS.items()}
 missing=probe(base+'/__ookini_release_gate_missing_9b4a.html','text/html')
 missing['ok']=missing.get('status')==404
 checks['/__missing_probe__']=missing
 report={'site':base,'checked_at_utc':datetime.now(timezone.utc).isoformat(),
         'read_only':True,'checks':checks,
         'passed':sum(bool(x['ok']) for x in checks.values()),
         'total':len(checks)}
 print(json.dumps(report,ensure_ascii=False,indent=2))
 if args.output:
  with open(args.output,'w',encoding='utf-8') as f:
   json.dump(report,f,ensure_ascii=False,indent=2)
 return 0 if report['passed']==report['total'] else 1

if __name__=='__main__':
 raise SystemExit(main())
