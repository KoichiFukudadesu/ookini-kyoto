#!/usr/bin/env python3
"""Offline structural QA for an ookini Netlify Drop ZIP (no network or dependencies)."""
import sys, zipfile, posixpath, re
from pathlib import PurePosixPath
from urllib.parse import urlsplit, unquote

REQUIRED = {'index.html','404.html','verify.html','pages/home.html','pages/discover.html','pages/station.html','pages/pass.html','pages/help.html','assets/season-01.jpg','assets/season-02.jpg','assets/season-03.jpg','assets/season-04.jpg'}

def check(path):
    errors=[]
    with zipfile.ZipFile(path) as z:
        names=set(z.namelist())
        errors += [f'missing: {name}' for name in sorted(REQUIRED-names)]
        for bad in z.testzip() or []: errors.append(f'bad CRC: {bad}')
        for name in sorted(names):
            if name.startswith('/') or '..' in PurePosixPath(name).parts:
                errors.append(f'unsafe archive path: {name}')
            if not name.endswith('.html'): continue
            data=z.read(name).decode('utf-8',errors='replace')
            if not re.search(r'<title\\b[^>]*>.*?</title>',data,re.I|re.S):
                errors.append(f'no title: {name}')
            for ref in re.findall(r'(?:src|href)\\s*=\\s*[\"\\']([^\"\\']+)',data,re.I):
                if ref.startswith(('#','//')) or urlsplit(ref).scheme or ref.startswith(('tel:','mailto:')): continue
                dest=unquote(urlsplit(ref).path)
                if not dest or '{' in dest or dest.startswith('/'): continue
                target=posixpath.normpath(posixpath.join(posixpath.dirname(name),dest))
                if target not in names and not any(x.startswith(target.rstrip('/')+'/') for x in names):
                    errors.append(f'{name}: missing local link {ref} -> {target}')
    return errors

if __name__=='__main__':
    if len(sys.argv)!=2: sys.exit('Usage: python3 tools/check_preview_zip.py path/to/preview.zip')
    errors=check(sys.argv[1]); print('\\n'.join(errors) if errors else 'PASS: ZIP integrity and required paths')
    sys.exit(bool(errors))
